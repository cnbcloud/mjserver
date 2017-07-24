# -*- coding=utf-8 -*-
'''
Created on 2015年9月28日

@author: zhaol
'''

from freetime.util import log as ftlog
from freetime.util.log import getMethodName
from poker.entity.game.quick_start import BaseQuickStart, \
    BaseQuickStartDispatcher
from poker.entity.game.rooms.room import TYRoom
from hall.entity.todotask import TodoTaskHelper
from freetime.entity.msg import MsgPack
from poker.protocol import router
from poker.entity.dao import onlinedata, userchip
from poker.entity.configure import gdata, pokerconf
from majiang2.servers.room.rpc import room_rpc
from majiang2.servers.table.rpc import table_rpc
from poker.entity.game.rooms.room_mixin import TYRoomMixin
from poker.util import strutil
from majiang2.table.friend_table_define import MFTDefine
from majiang2.table.table_config_define import MTDefine

class MajiangQuickStartDispatcher(BaseQuickStartDispatcher):
    '''
    按clientId分发快速开始请求
    '''
    @classmethod
    def dispatchQuickStart(cls, msg, userId, gameId, roomId, tableId, playMode, clientId):
        clientVersion = 4.0
        if clientVersion >= 4.0 :
            return MajiangQuickStartV4_0.onCmdQuickStart(msg, userId, gameId, roomId, tableId, playMode, clientId)
        ftlog.error(getMethodName(), "unsupported client:", clientVersion)
        

class MajiangCreateTable(object):
    '''创建牌桌
            1.找到符合需求的房间
            2.找到该房间所有的桌子
            3.排除已经创建的牌桌，从剩余的桌子选择合适的进入(quick_start)并且坐下
    '''
    @classmethod
    def createTableQuickStart(cls, msg, itemParams, userId, roomId, tableId, playMode, clientId):
        '''UT server中处理来自客户端的create_table请求  
        Args:
            msg
                cmd : create_table
                if roomId == 0:
                    表示玩家创建房间，服务器为玩家选择房间，然后将请求转给GR
                    
                if roomId > 0 and tableId == 0 : 
                    表示玩家选择了房间，将请求转给GR
                    
                if roomId > 0 and tableId == roomId * 10000 :
                    表示玩家在队列里断线重连，将请求转给GR
                    
                if roomId > 0 and tableId > 0:
                    if onlineSeatId > 0: 
                        表示玩家在牌桌里断线重连，将请求转给GT
                    else:
                        表示玩家选择了桌子，将请求转给GR
        '''
        assert isinstance(userId, int) and userId > 0
        assert isinstance(roomId, int) and roomId >= 0
        assert isinstance(tableId, int) and tableId >= 0
        ftlog.debug("<< |clientId:", clientId,
                   "|userId, roomId, tableId:", userId, roomId, tableId,
                   "|gameId, playMode:", playMode, caller=cls)
        
        isReconnect = False
        gameId = msg.getResult('gameId')

        # 单开, 无论何时quick_start进入都检查loc
        if not pokerconf.isOpenMoreTable(clientId) :
            loc = onlinedata.checkUserLoc(userId, gameId)
            ftlog.debug('old client, checkUserLoc->', loc, caller=cls)
            if isinstance(loc, basestring) :
                lgameId, lroomId, ltableId, lseatId = loc.split('.') 
                lgameId, lroomId, ltableId, lseatId = strutil.parseInts(lgameId, lroomId, ltableId, lseatId)
                if lgameId == gameId and lroomId > 0 :
                    roomId = lroomId
                    tableId = ltableId
                    isReconnect = True
                    ftlog.debug('old client, reset roomId, tableId->', roomId, tableId, caller=cls)
                    
        if (not isReconnect) and roomId > 0 and tableId > 0:
            reason = cls._canQuickEnterCreateRoom(userId, gameId, roomId)
            if reason != TYRoom.ENTER_ROOM_REASON_OK:
                cls._onEnterCreateRoomFailed(reason, userId, gameId, clientId, roomId)
                return
        tempShadowRoomId = 0
        if roomId == 0 :  # 第一个玩家创建房间牌桌
            chosenRoomId, checkResult = cls._chooseCreateRoom(userId, gameId, playMode)
            ftlog.info("after choose room", "|userId, chosenRoomId, checkResult:", userId, chosenRoomId, checkResult, caller=cls)
            if checkResult == TYRoom.ENTER_ROOM_REASON_OK :
                #得到房间ID,找合适的tableId
                roomDef = gdata.roomIdDefineMap()[chosenRoomId]
                shadowRoomIds = roomDef.shadowRoomIds
                if shadowRoomIds:
                    for shadowRoomId in shadowRoomIds:
                        tableId = table_rpc.getTableByRoomId(shadowRoomId)
                        if isinstance(tableId, int) and tableId > 0:
                            tempShadowRoomId = shadowRoomId
                            break
                        
                shadowRoomId = tableId / 10000
                if shadowRoomId == tempShadowRoomId:# 验证
                    ctrRoomId = gdata.roomIdDefineMap()[shadowRoomId].parentId
                    TYRoomMixin.queryRoomQuickStartReq(msg, ctrRoomId, tableId, shadowRoomId=shadowRoomId)  # 请求转给GR
                    return
                else:
                    cls._onEnterCreateRoomFailed(checkResult, userId, gameId, clientId, roomId)
                    return   
            else:
                cls._onEnterCreateRoomFailed(checkResult, userId, gameId, clientId, roomId)
                return   
        else:
            onlineSeat = onlinedata.getOnlineLocSeatId(userId, gameId, roomId, tableId)
            if onlineSeat:
                extParam = {}
                extParam['seatId'] = onlineSeat
                moParams = msg.getKey('params')
                for k, v in moParams.items() :
                    if not k in extParam :
                        extParam[k] = v
                ftlog.debug('extParam=', extParam)
                TYRoomMixin.querySitReq(userId, roomId, tableId, clientId, extParam)  # 玩家断线重连，请求转给GT
                return
        if tableId == roomId * 10000:  # 玩家在队列里断线重连
            TYRoomMixin.queryRoomQuickStartReq(msg, roomId, tableId)  # 请求转给GR
            return
        # 玩家选择了桌子,进桌
        shadowRoomId = tableId / 10000
        ctrRoomId = gdata.roomIdDefineMap()[shadowRoomId].parentId
        TYRoomMixin.queryRoomQuickStartReq(msg, ctrRoomId, tableId, shadowRoomId=shadowRoomId)  # 请求转给GR
            
        
            
    @classmethod
    def _canQuickEnterCreateRoom(cls, userId, gameId, roomId):
        try :
            ftlog.debug(gdata.roomIdDefineMap()[roomId].configure)
            roomConfig = gdata.roomIdDefineMap()[roomId].configure
            ismatch = roomConfig.get('ismatch')
            isBigMatch = False
            if roomConfig.get('typeName','') == 'majiang_bigmatch':
                isBigMatch = True
            if ismatch and not isBigMatch:
                return TYRoom.ENTER_ROOM_REASON_ROOM_ID_ERROR
            return TYRoom.ENTER_ROOM_REASON_OK
        except Exception as e:
            ftlog.error(e)
            return TYRoom.ENTER_ROOM_REASON_INNER_ERROR
    
    @classmethod
    def _canQuickEnterCreateTable(cls):
        pass

    @classmethod
    def _chooseCreateRoom(cls, userId, gameId, playMode, playerCount = 4, hasRobot = 0, itemId = None):
        '''服务端为玩家选择要创建的房间'''
        candidateRoomIds = MajiangQuickStartV4_0._getCandidateRoomIds(gameId, playMode)
        ftlog.debug("MajiangCreateTable._chooseCreateRoom:", candidateRoomIds
                    , ' playMode=', playMode
                    , ' playerCount=', playerCount
                    , ' hasRobot=', hasRobot)
        
        for roomId in candidateRoomIds :
            roomConfig = gdata.roomIdDefineMap()[roomId].configure
            tableConf = roomConfig.get('tableConf', {})
            ftlog.debug('_chooseCreateRoom tableConf:', tableConf)
            if roomConfig.get(MFTDefine.IS_CREATE,0) \
                and (tableConf.get(MTDefine.MAXSEATN, 4) == playerCount) \
                and (roomConfig.get(MTDefine.HAS_ROBOT, 0) == hasRobot):
                roomItemId = roomConfig.get(MFTDefine.CREATE_ITEM, 0)
                if not hasRobot and itemId and (itemId != roomItemId):
                    ftlog.debug('MajiangCreateTable.check playMode ok, hasRobot ok, but fangKa item no ok, curRoomConsume:', roomItemId
                                , ' findRoomConsume:', itemId)
                    continue
                
                ret = cls._canQuickEnterCreateRoom(userId, gameId, roomId)
                ftlog.debug("MajiangCreateTable.check roomId, ret:", roomId, ret, caller=cls)
                if ret == TYRoom.ENTER_ROOM_REASON_OK:
                    return roomId, TYRoom.ENTER_ROOM_REASON_OK
        return 0, TYRoom.ENTER_ROOM_REASON_LESS_MIN
    
    @classmethod
    def _onEnterCreateRoomFailed(cls, checkResult, userId, gameId, clientId, roomId=0):
        '''进入创建房间失败回调函数'''
        ftlog.warn("|userId, reason, roomId:", userId, checkResult, roomId, caller=cls)
        mo = MsgPack()
        mo.setCmd('quick_start') 
        mo.setResult('gameId', gameId)
        mo.setResult('userId', userId)        
        mo.setResult('reason', checkResult) 
        router.sendToUser(mo, userId)
    
class MajiangQuickStartV4_0(BaseQuickStart):
    
    @classmethod
    def onCmdQuickStart(cls, msg, userId, gameId, roomId, tableId, playMode, clientId):
        '''UT server中处理来自客户端的quick_start请求  
        Args:
            msg
                cmd : quick_start
                if roomId == 0:
                    表示快速开始，服务器为玩家选择房间，然后将请求转给GR
                    
                if roomId > 0 and tableId == 0 : 
                    表示玩家选择了房间，将请求转给GR
                    
                if roomId > 0 and tableId == roomId * 10000 :
                    表示玩家在队列里断线重连，将请求转给GR
                    
                if roomId > 0 and tableId > 0:
                    if onlineSeatId > 0: 
                        表示玩家在牌桌里断线重连，将请求转给GT
                    else:
                        表示玩家选择了桌子，将请求转给GR
        '''
        assert isinstance(userId, int) and userId > 0
        assert isinstance(roomId, int) and roomId >= 0
        assert isinstance(tableId, int) and tableId >= 0
        ftlog.debug("MajiangQuickStartV4_0.onCmdQuickStart clientId:", clientId
                   , " userId:", userId
                   , " roomId:", roomId
                   , " tableId:", tableId
                   , " gameId:", gameId
                   , " playMode:", playMode)
        
        isCreate = False
        if roomId > 0:
            isCreate = cls.isFriendRoom(roomId)
        
        isReconnect = False
        # 单开, 无论何时quick_start进入都检查loc
        if not pokerconf.isOpenMoreTable(clientId) :
            loc = onlinedata.checkUserLoc(userId, clientId, gameId)
            ftlog.debug('MajiangQuickStartV4_0.onCmdQuickStart checkUserLoc:', loc, caller=cls)
            if isinstance(loc, basestring) :
                lgameId, lroomId, ltableId, lseatId = loc.split('.') 
                lgameId, lroomId, ltableId, lseatId = strutil.parseInts(lgameId, lroomId, ltableId, lseatId)
                if isCreate and (lroomId == 0) and (ltableId == 0):
                    # 好友桌的快速开始必须有loc，没有loc则进桌失败
                    ftlog.debug('MajiangQuickStartV4_0.onCmdQuickStart room is friendTable, loc is 0, means, table is dissolved...')
                    cls._onEnterRoomFailed(msg, TYRoom.ENTER_ROOM_REASON_FRIEND_DISSOLVE, userId, clientId, roomId)
                    return
                    
                if lgameId == gameId and lroomId > 0 :
                    roomId = lroomId
                    tableId = ltableId
                    isReconnect = True
                    ftlog.debug('MajiangQuickStartV4_0.onCmdQuickStart old client roomId:', roomId
                                , ' tableId:', tableId
                                , caller=cls)
                    
        if (not isReconnect) and roomId > 0 and tableId > 0:
            reason = cls._canQuickEnterRoom(userId, gameId, roomId, 1)
            if reason != TYRoom.ENTER_ROOM_REASON_OK:
                cls._onEnterRoomFailed(msg, reason, userId, gameId, clientId, roomId)
                return

        if roomId == 0 :  # 玩家点击快速开始
            chosenRoomId, checkResult = cls._chooseRoom(userId, gameId, playMode)
            ftlog.info("MajiangQuickStartV4_0.onCmdQuickStart after choose room userId:", userId
                       , " chosenRoomId:", chosenRoomId
                       , " checkResult:", checkResult
                       , caller=cls)
            if checkResult == TYRoom.ENTER_ROOM_REASON_OK :
                #找到合适的房间 根据roomId找到合适的table
                TYRoomMixin.queryRoomQuickStartReq(msg, chosenRoomId, 0)  # 请求转给GR
            else:
                candidateRoomIds = cls._getCandidateRoomIds(gameId, playMode)
                if candidateRoomIds :
                    rid = candidateRoomIds[0]
                    msg.setParam('candidateRoomId', rid)
                cls._onEnterRoomFailed(msg, checkResult, userId, clientId, roomId)
            return         
        
        if tableId == 0:  # 玩家只选择了房间
            bigRoomId = gdata.getBigRoomId(roomId)
            if bigRoomId == 0 :
                cls._onEnterRoomFailed(msg, TYRoom.ENTER_ROOM_REASON_ROOM_ID_ERROR, userId, gameId, clientId, roomId)
                return
            ctrRoomIds = gdata.bigRoomidsMap()[bigRoomId]
            ctrlRoomId = ctrRoomIds[userId % len(ctrRoomIds)]
            
            reason = cls._canQuickEnterRoom(userId, gameId, ctrlRoomId, 1)
            if reason == TYRoom.ENTER_ROOM_REASON_OK:
                TYRoomMixin.queryRoomQuickStartReq(msg, ctrlRoomId, 0)  # 请求转给GR或GT
            else:
                cls._onEnterRoomFailed(msg, reason, userId, gameId, clientId, roomId)
            return

        if tableId == roomId * 10000:  # 玩家在队列里断线重连
            TYRoomMixin.queryRoomQuickStartReq(msg, roomId, tableId)  # 请求转给GR
            return
        
        onlineSeat = onlinedata.getOnlineLocSeatId(userId, roomId, tableId)
        
        if onlineSeat:
            extParam = {}
            extParam['seatId'] = onlineSeat
            moParams = msg.getKey('params')
            for k, v in moParams.items() :
                if not k in extParam :
                    extParam[k] = v
            ftlog.debug('extParam=', extParam)
            TYRoomMixin.querySitReq(userId, roomId, tableId, clientId, extParam)  # 玩家断线重连，请求转给GT
        else:  # 玩家选择了桌子, 
            shadowRoomId = tableId / 10000
            ctrRoomId = gdata.roomIdDefineMap()[shadowRoomId].parentId
            TYRoomMixin.queryRoomQuickStartReq(msg, ctrRoomId, tableId, shadowRoomId=shadowRoomId)  # 请求转给GR
            
    @classmethod
    def isFriendRoom(cls, roomId):
        roomType = gdata.roomIdDefineMap()[roomId].configure
        ftlog.debug(roomType, caller=cls)
        tableType = roomType.get('tableType', 'normal')
        return tableType == 'create'
    
    @classmethod
    def _chooseRoom(cls, userId, gameId, playMode):
        return super(MajiangQuickStartV4_0, cls)._chooseRoom(userId, gameId, playMode)
       
    @classmethod
    def _getCandidateRoomIds(cls, gameId, playMode):
        return super(MajiangQuickStartV4_0, cls)._getCandidateRoomIds(gameId, playMode)

    @classmethod
    def _onEnterRoomFailed(cls, msg, checkResult, userId, gameId, clientId, roomId=0):
        '''进入房间失败回调函数'''
        ftlog.warn("|userId, reason, roomId:", userId, checkResult, roomId, caller=cls)  # 调用最小房间金币不够充值提醒的todotask
        if not roomId:
            roomId = msg.getParam('candidateRoomId', 0)
        if checkResult == TYRoom.ENTER_ROOM_REASON_LESS_MIN or checkResult == 104:
            from hall.entity import hallproductselector
            product, _ = hallproductselector.selectLessbuyProduct(gameId, userId, clientId, roomId)
            if product:    
                from hall.entity.todotask import TodoTaskOrderShow   
                todotask = TodoTaskOrderShow.makeByProduct("金币不够啦，买一个超值礼包吧！", "", product) 
                if todotask:
                    TodoTaskHelper.sendTodoTask(gameId, userId, todotask)
                    
        mo = MsgPack()
        mo.setCmd('quick_start') 
        mo.setResult('gameId', gameId) 
        mo.setResult('userId', userId) 
        mo.setError(checkResult, '进入房间失败，请稍后重试')       
        router.sendToUser(mo, userId)
        
    @classmethod
    def _canQuickEnterRoom(cls, userId, gameId, roomId, isOnly):
        try :
            chip = userchip.getChip(userId)
            ftlog.debug(gdata.roomIdDefineMap()[roomId].configure, caller=cls)
            roomConfig = gdata.roomIdDefineMap()[roomId].configure
            ismatch = roomConfig.get('ismatch')
            isBigMatch = False
            if roomConfig.get('typeName','') == 'majiang_bigmatch':
                isBigMatch = True
            if ismatch and not isBigMatch:
                return cls._canQuickEnterMatch(userId, gameId, roomId, chip)
            
            if isOnly :
                minCoinQs = roomConfig['minCoin']
                maxCoinQs = roomConfig['maxCoin']
            else:
                minCoinQs = roomConfig['minCoinQS']
                maxCoinQs = roomConfig['maxCoinQS']
            
            ftlog.debug('MajiangQuickStartV4_0 roomId:', roomId
                        , 'minCoinQs:', minCoinQs
                        , 'maxCoinQs:', maxCoinQs
                        , 'chip:', chip
                        , caller=cls)

            if chip < minCoinQs and (minCoinQs != -1):
                return TYRoom.ENTER_ROOM_REASON_LESS_MIN
            
            if maxCoinQs > 0 and chip >= maxCoinQs:
                return TYRoom.ENTER_ROOM_REASON_GREATER_MAX

            return TYRoom.ENTER_ROOM_REASON_OK

        except Exception as e:
            ftlog.error(e)
            return TYRoom.ENTER_ROOM_REASON_INNER_ERROR

    @classmethod
    def _canQuickEnterMatch(cls, userId, gameId, roomId, userChip):
        ret = room_rpc.checkCanEnter(roomId, userId, userChip)
        return ret
