# -*- coding=utf-8 -*-
'''
Created on 2015年9月28日

@author: liaoxx
'''

import freetime.util.log as ftlog
from hall.servers.common.base_checker import BaseMsgPackChecker
from poker.protocol import runcmd, router
from majiang2.entity.quick_start import MajiangQuickStartDispatcher,\
    MajiangCreateTable
from majiang2.entity import majiang_conf
from freetime.entity.msg import MsgPack
from poker.entity.configure import gdata
from majiang2.entity.create_table import CreateTableData
from majiang2.entity.create_table_record import MJCreateTableRecord
from majiang2.entity.util import sendPopTipMsg, Util
from poker.entity.dao import onlinedata, gamedata
from poker.util import strutil
from hall.entity.todotask import TodoTaskEnterGameNew, TodoTaskHelper
import poker.util.timestamp as pktimestamp
from majiang2.table.friend_table_define import MFTDefine
from hall.entity import hall_fangka

class GameTcpHandler(BaseMsgPackChecker):

    def __init__(self):
        pass

    def _check_param_sessionIndex(self, msg, key, params):
        sessionIndex = msg.getParam(key)
        if isinstance(sessionIndex, int) and sessionIndex >= 0:
            return None, sessionIndex
        return None, -1
    
    def _check_param_match_id(self, msg, key, params):
        match_id = msg.getParam("match_id")
        if match_id and  isinstance(match_id, (str, unicode)) :
            return None, match_id
        return 'ERROR of match_id !' + str(match_id), None
    
    def _check_param_hasRobot(self, msg, key, params):
        hasRobot = msg.getParam("hasRobot")
        if isinstance(hasRobot, int) :
            return None, hasRobot
        return None, 0

    def doGameQuickStart(self, userId, gameId, clientId, roomId0, tableId0, playMode, sessionIndex):
        '''
        TCP 发送的至UTIL服务的quick_start暂时不能用lock userid的方式, 
        因为,消息流 CO->UT->GR->GT->UT会死锁
        '''
        msg = runcmd.getMsgPack()
        ftlog.debug('doGameQuickStart', userId, gameId, clientId, roomId0, tableId0, playMode, sessionIndex, caller=self)
        if not playMode and roomId0 <= 0 and tableId0 <= 0 :
            try:
                # 前端对于sessionIndex是写死的, 不会更具hall_info中的顺序改变而改变
                if sessionIndex == 0 :
                    playMode = majiang_conf.PLAYMODE_GUOBIAO
                elif sessionIndex == 1 :
                    playMode = majiang_conf.PLAYMODE_SICHUAN
                elif sessionIndex == 2 :
                    playMode = majiang_conf.PLAYMODE_GUOBIAO_EREN
                elif sessionIndex == 3 :
                    playMode = majiang_conf.PLAYMODE_HARBIN
                elif sessionIndex == 4 :
                    playMode = majiang_conf.PLAYMODE_SICHUAN_DQ
                elif sessionIndex == 5 :
                    playMode = majiang_conf.PLAYMODE_SICHUAN_XLCH
                elif sessionIndex == 6 :
                    playMode = majiang_conf.PLAYMODE_GUOBIAO_VIP
                else:
                    playMode = majiang_conf.PLAYMODE_GUOBIAO
                msg.setParam('playMode', playMode) # 透传playMode, 以便发送高倍房引导弹窗
            except:
                ftlog.error('doGameQuickStart', msg)
            ftlog.debug('doGameQuickStart sessionIndex=', sessionIndex, 'playMode=', playMode)
            
        if roomId0 < 1000:
            roomIdx = roomId0
            roomId0 = 0
            ftlog.info("quickstart roomID error, from %d change to %d" % (roomIdx, roomId0))
            
        MajiangQuickStartDispatcher.dispatchQuickStart(msg, userId, gameId, roomId0, tableId0, playMode, clientId)
        if router.isQuery() :
            mo = runcmd.newOkMsgPack(1)
            router.responseQurery(mo, '', str(userId))

    def doAwardCertificate(self, userId, gameId, match_id, clientId):
        '''
        TCP 发送的至UTIL服务的quick_start暂时不能用lock userid的方式, 
        因为,消息流 CO->UT->GR->GT->UT会死锁
        '''
        msg = runcmd.getMsgPack()
        roomId = msg.getParam("roomId")
        ftlog.debug('doAwardCertificate', userId, gameId, roomId, match_id, caller=self)
        if len(str(roomId)) != 4 and len(str(roomId)) != 8 and len(str(roomId)) != 0:
            roomIdx = roomId
            roomId = roomId * 100
            ftlog.info("doAwardCertificate roomID error, from %d change to %d" % (roomIdx, roomId))

        allrooms = gdata.roomIdDefineMap()
        ctrlRoomId = roomId
        if roomId in allrooms :
            roomDef = allrooms[roomId]
            if roomDef.parentId > 0: # this roomId is shadowRoomId
                ctrlRoomId = roomDef.parentId
        else:
            ftlog.warn("doAwardCertificate, error roomId", roomId)
            return
                
        ftlog.debug("ctrlRoomId:", ctrlRoomId)
                
        msg1 = MsgPack()
        msg1.setCmd('room')
        msg1.setParam('gameId', gameId)
        msg1.setParam('userId', userId) 
        msg1.setParam('roomId', ctrlRoomId)       
        msg1.setParam('action', "match_award_certificate")
        msg1.setParam('match_id', match_id)
        msg1.setParam('clientId', clientId)
        router.sendRoomServer(msg1, roomId)
        if router.isQuery() :
            mo = runcmd.newOkMsgPack(1)
            router.responseQurery(mo, '', str(userId))
    
    def doGetCreatTableInfo(self, userId, gameId, clientId, hasRobot):
        """获取创建牌桌配置信息
        """
        msg = runcmd.getMsgPack()
        playModes = msg.getParam('playModes')  # 用来过滤playMode,避免返回这个gameId下所有玩法的配置信息,造成无用的一堆冗余数据
        ftlog.debug('GameTcpHandler.doGetCreatTableInfo userId:', userId
                    , ' gameId:', gameId
                    , ' clientId:' ,clientId
                    , ' hasRobot:', hasRobot
                    , ' playModes:', playModes)
        configList = []
        config = majiang_conf.getCreateTableTotalConfig(gameId)
        for playMode in config:
            if playModes is not None and playMode not in playModes:
                continue
            pConfig = config.get(playMode)
            pConfig['playMode'] = playMode
            if hasRobot > 0:
                pConfig['hasRobot'] = 1
                cardCounts = pConfig.get('cardCount', [])
                newCardCounts = []
                for card in cardCounts:
                    ftlog.debug('game_handler.doGetCreatTableInfo card in cardCount:', card)
                    if 'hasRobot' in card:
                        newCardCounts.append(card.get('hasRobot', {}))
                pConfig['cardCount'] = newCardCounts
                    
                cardCounts4 = pConfig.get('cardCount4', [])
                newCardCount4 = []
                for card in cardCounts4:
                    ftlog.debug('game_handler.doGetCreatTableInfo card in cardCount4:', card)
                    if 'hasRobot' in card:
                        newCardCount4.append(card.get('hasRobot', {}))
                    else:
                        newCardCount4.append(card)
                pConfig['cardCount4'] = newCardCount4
                if newCardCount4[0]['type'] == MFTDefine.CARD_COUNT_ROUND:
                    pConfig['paramType']['cardCount4'] = '选择局数'
                    
                cardCounts3 = pConfig.get('cardCount3', [])
                newCardCount3 = []
                for card in cardCounts3:
                    ftlog.debug('game_handler.doGetCreatTableInfo card in cardCount3:', card)
                    if 'hasRobot' in card:
                        newCardCount3.append(card.get('hasRobot', {}))
                    else:
                        newCardCount3.append(card)
                pConfig['cardCount3'] = newCardCount3
                    
                cardCounts2 = pConfig.get('cardCount2', [])
                newCardCounts2 = []
                for card in cardCounts2:
                    ftlog.debug('game_handler.doGetCreatTableInfo card in cardCount2:', card)
                    if 'hasRobot' in card:
                        newCardCounts2.append(card.get('hasRobot', {}))
                    else:
                        newCardCounts2.append(card)
                pConfig['cardCount2'] = newCardCounts2
                
            paramType = pConfig.get('paramType', {})
            ftlog.debug('doGetCreatTableInfo paramType:', paramType)
            showOrder = pConfig.get('showOrder', [])
            ftlog.debug('doGetCreatTableInfo showOrder:', showOrder)
            
            if isinstance(paramType, dict):
                pConfig['paramType'] = Util.dict_sort(paramType, showOrder)
                
            configList.append(pConfig)
        ftlog.debug('doGetCreatTableInfo configList:', configList)
            
        mo = MsgPack()
        mo.setCmd("create_table")
        mo.setResult('action', 'info')
        mo.setResult('gameId', gameId)
        mo.setResult('userId', userId)
        mo.setResult('list', configList)
        router.sendToUser(mo, userId)
        
    def _canEnterGame(self, userId, gameId):
        """是否可进入游戏"""
        gameTime = gamedata.getGameAttrInt(userId, gameId, 'createTableTime')
        nowTime = pktimestamp.getCurrentTimestamp()
        ftlog.debug('Majiang2 game_handler _canEnterGame gameTile:', gameTime
            , ' nowTime:', nowTime)
        return (nowTime - gameTime) >= 5
            
    def doCreateTable(self, userId, gameId, clientId, roomId0, tableId0, playMode, hasRobot = 0):
        
        #临时硬编码，解决91晃晃提审问题
        if gameId==791 and playMode=="queshou-lianjiang" and clientId=="IOS_3.901_weixin.appStore,weixinPay.0-hall791.queshou.iostsljmj":
            hasRobot=1
	if gameId == 790 and playMode == 'luosihu-luosihuts' and clientId=="IOS_3.901_weixin.appStore,weixinPay.0-hall790.laodao.iostsxjmj":
	    hasRobot=1
        """房主创建牌桌"""
        if not playMode:
            ftlog.error('game_handler, cat not create table without playMode...')
        
        loc = onlinedata.checkUserLoc(userId, clientId, gameId)
        lgameId, lroomId, ltableId, lseatId = loc.split('.')
        lgameId, lroomId, ltableId, lseatId = strutil.parseInts(lgameId, lroomId, ltableId, lseatId)
        if lgameId > 0 and lroomId > 0 and ltableId > 0 and lseatId >=0:
            ftlog.warn('create_table error, user in table',lgameId, lroomId, ltableId, lseatId)
            sendPopTipMsg(userId, "请稍候,正在进桌...")
            config = {
                      "type":"quickstart",
                      "pluginParams": {
                          "roomId": lroomId,
                          "tableId": ltableId,
                          "seatId": lseatId
                          }
                      }
            todotask = TodoTaskEnterGameNew(lgameId, config)
            mo = MsgPack()
            mo.setCmd('todo_tasks')
            mo.setResult('gameId', gameId)
            mo.setResult('pluginId', lgameId)
            mo.setResult('userId', userId)
            mo.setResult('tasks', TodoTaskHelper.encodeTodoTasks(todotask))
            router.sendToUser(mo, userId)
        elif self._canEnterGame(userId, gameId):
            # 保存建桌时间戳
            gamedata.setGameAttr(userId, gameId, 'createTableTime', pktimestamp.getCurrentTimestamp())
            
            msg = runcmd.getMsgPack()
            itemParams = msg.getParam("itemParams")
            
            playerCount = 4
            playerTypeId = itemParams.get(MFTDefine.PLAYER_TYPE, 1)
            playerTypeConfig = majiang_conf.getCreateTableConfig(gameId, playMode, MFTDefine.PLAYER_TYPE, playerTypeId)
            if not playerTypeConfig:
                sendPopTipMsg(userId, '人数配置有误，请稍后重试')
                return
            
            playerCount = playerTypeConfig.get('count', 4)
            ftlog.debug('MajiangCreateTable.create_table playerCount:', playerCount)
            cardCountKey = playerTypeConfig.get(MFTDefine.CARD_COUNT, MFTDefine.CARD_COUNT)

            cardCountId = itemParams.get(cardCountKey, 0)
            cardCountConfig = majiang_conf.getCreateTableConfig(gameId, playMode, cardCountKey, cardCountId)
            if not cardCountConfig:
                sendPopTipMsg(userId, '房卡配置有误，请稍后重试')
                return
            
            if hasRobot == 1 and 'hasRobot' in cardCountConfig:
                cardCountConfig = cardCountConfig.get('hasRobot', {})
                ftlog.debug('MajiangCreateTable.create_table hasRobot == 1:')
            fangka_count = cardCountConfig.get('fangka_count', 1)
            ftlog.debug('MajiangCreateTable.create_table fangka_count:', fangka_count
                        , ' cardCountConfig:', cardCountConfig)
            
            msg.setParam('isCreateTable', 1) #标记创建的桌子是 自建桌
            from poker.entity.game.rooms.room import TYRoom
            '''
            根据五个因素筛选合适的房间
            1）gameId         游戏ID
            2）playMode       游戏玩法
            3）playerCount    玩家个数
            4）hasRobot       是否有机器人
            5）itemId         房卡道具
            '''
            itemId = hall_fangka.queryFangKaItem(gameId, userId, clientId)
            if itemId:
                ftlog.debug('MajiangCreateTable._chooseCreateRoom fangKa itemId:', itemId)
            roomId, checkResult = MajiangCreateTable._chooseCreateRoom(userId, gameId, playMode, playerCount, hasRobot, itemId)
            ftlog.debug('MajiangCreateTable._chooseCreateRoom roomId:', roomId, ' checkResult:', checkResult)

            if checkResult==TYRoom.ENTER_ROOM_REASON_OK:
                msg = runcmd.getMsgPack()
                msg.setCmdAction("room", "create_table")
                msg.setParam("roomId", roomId)
                msg.setParam("itemParams", itemParams)
                msg.setParam('needFangka', fangka_count)
                ftlog.debug('MajiangCreateTable._chooseCreateRoom send message to room:', msg)

                router.sendRoomServer(msg, roomId)
            else:
                sendPopTipMsg(userId, "暂时无法创建请稍后重试")
                
            if router.isQuery() :
                mo = runcmd.newOkMsgPack(1)
                router.responseQurery(mo, '', str(userId))
        else:
            ftlog.info('majiang2 game_handler, ignore enter game request...')
    
    def doJoinCreateTable(self, userId, gameId, clientId, roomId0, tableId0, playMode):
        """用户加入自建牌桌
        """
        loc = onlinedata.checkUserLoc(userId, clientId, gameId)
        lgameId, lroomId, ltableId, lseatId = loc.split('.')
        lgameId, lroomId, ltableId, lseatId = strutil.parseInts(lgameId, lroomId, ltableId, lseatId)
        if lgameId > 0 and lroomId > 0 and ltableId > 0 and lseatId >=0:
            ftlog.warn('create_table error, user in table')
            sendPopTipMsg(userId, "请稍候,正在进桌...")
            config = {
                      "type":"quickstart",
                      "pluginParams": {
                          "roomId": lroomId,
                          "tableId": ltableId,
                          "seatId": lseatId
                          }
                      }
            todotask = TodoTaskEnterGameNew(lgameId, config)
            mo = MsgPack()
            mo.setCmd('todo_tasks')
            mo.setResult('gameId', gameId)
            mo.setResult('pluginId', lgameId)
            mo.setResult('userId', userId)
            mo.setResult('tasks', TodoTaskHelper.encodeTodoTasks(todotask))
            router.sendToUser(mo, userId)
        else:
            msg = runcmd.getMsgPack()
            createTableNo = msg.getParam('createTableNo', 0)
            if not createTableNo:
                return
            tableId0, roomId0 = CreateTableData.getTableIdByCreateTableNo(createTableNo)
            if not tableId0 or not roomId0:
                sendPopTipMsg(userId, "找不到您输入的房间号")
                return
            msg = runcmd.getMsgPack()
            msg.setParam("shadowRoomId", roomId0)
            msg.setParam("roomId", roomId0)
            msg.setParam("tableId", tableId0)
            msg.setCmdAction("room", "join_create_table")
            router.sendRoomServer(msg, roomId0)
            
            if router.isQuery() :
                mo = runcmd.newOkMsgPack(1)
                router.responseQurery(mo, '', str(userId))
    
    def doGetCreateTableRecord(self, userId, gameId, clientId):
        """全量请求牌桌记录
        """
        msg = runcmd.getMsgPack()
        startRecordIndex = msg.getParam('startRecordIndex', None)
        if not startRecordIndex:
            startRecordIndex = 0
        endRecordIndex = msg.getParam('endRecordIndex', None)
        if not endRecordIndex:
            endRecordIndex = 19
            
        MJCreateTableRecord.sendAllRecordToUser(userId, gameId, startRecordIndex, endRecordIndex)
        if router.isQuery() :
            mo = runcmd.newOkMsgPack(1)
            router.responseQurery(mo, '', str(userId))

    def doGetCreateTableRecordForCustomer(self, userId, gameId, clientId):
        """全量请求他人的牌桌记录
        """
        msg = runcmd.getMsgPack()
        targetUserId = msg.getParam('targetUserId', None)
        targetTableNo = msg.getParam('targetTableNo', None)
        playMode = msg.getParam('playMode', None)

        startRecordIndex = msg.getParam('startRecordIndex', None)
        if not startRecordIndex:
            startRecordIndex = 0
        endRecordIndex = msg.getParam('endRecordIndex', None)
        if not endRecordIndex:
            endRecordIndex = 19

        MJCreateTableRecord.sendAllRecordToUserForCustomer(userId, gameId, playMode, targetUserId, targetTableNo, startRecordIndex, endRecordIndex)
        if router.isQuery():
            mo = runcmd.newOkMsgPack(1)
            router.responseQurery(mo, '', str(userId))
