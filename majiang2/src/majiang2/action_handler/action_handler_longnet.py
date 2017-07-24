# -*- coding=utf-8
'''
Created on 2016年9月23日
上行行为处理

@author: zhaol
'''
from majiang2.action_handler.action_handler import ActionHandler
from majiang2.table_state.state import MTableState
from freetime.util import log as ftlog
from majiang2.player.player import MPlayerTileGang
from majiang2.table.table_config_define import MTDefine
from majiang2.ai.play_mode import MPlayMode

class ActionHandlerLongNet(ActionHandler):
    def __init__(self):
        super(ActionHandlerLongNet, self).__init__()
        
    def processAction(self, cmd):
        """处理玩家行为
        在本例里为上行的长连接消息
        """
        pass
    
    def getActionIdFromMessage(self, message):
        """从消息中获取action_id"""
        return message.getParam('action_id')
    
    def handleTableCallTing(self, userId, seatId, message):
        ftlog.debug('handleTableCallTing message:', message)
        actionId = self.getActionIdFromMessage(message)
        if actionId == self.table.actionID:
            seatId = message.getParam('seatId')
            self.table.tingBeforeAddCard(seatId, actionId)
        else:
            ftlog.info('handleTableCallGrabTing message:', message
                       , ' but actionID is wrong, actionIDInTable:', self.table.actionID
                        , ' actionIDInMsg:', actionId)

    def handleTableCallTianTing(self, userId, seatId, message):
        ftlog.debug('handleTableCallTianTing message:', message)
        actionId = self.getActionIdFromMessage(message)
        if actionId == self.table.actionID:
            seatId = message.getParam('seatId')
            self.table.tianTing(seatId, actionId)
        else:
            ftlog.debug('handleTableCallTianTing message:', message
                        , ' but actionID is wrong, actionIDInTable:', self.table.actionID
                        , ' actionIDInMsg:', actionId)
    
    def handleTableCallGrabTing(self, userId, seatId, message):
        """处理抢听消息
        
        1）抢听 吃
        {
            "cmd": "table_call",
            "params": {
                "gameId": 7,
                "clientId": "Android_3.90_360.360,yisdkpay.0-hall6.360.win",
                "userId": 10788,
                "roomId": 75041001,
                "tableId": 750410010199,
                "seatId": 0,
                "action": "grabTing",
                "action_id": 1,
                "chi": 17,
                "pattern": [16, 17, 18]
            }
        }
        
        2）抢听 碰
        {
            "cmd": "table_call",
            "params": {
                "gameId": 7,
                "clientId": "Android_3.90_360.360,yisdkpay.0-hall6.360.win",
                "userId": 10788,
                "roomId": 75041001,
                "tableId": 750410010200,
                "seatId": 0,
                "action": "grabTing",
                "action_id": 11,
                "peng": 4,
                "pattern": [4, 4, 4]
            }
        }
        
        3）抢听 杠
        {
            "cmd": "table_call",
            "params": {
                "gameId": 7,
                "clientId": "Android_3.90_360.360,yisdkpay.0-hall6.360.win",
                "userId": 10788,
                "roomId": 75041001,
                "tableId": 750410010200,
                "seatId": 0,
                "action": "grabTing",
                "action_id": 11,
                "gang": 4,
                "pattern": [4, 4, 4, 4],
                "special_tile": 23
            }
        }
        
        4）抢听 粘
        {
            "cmd": "table_call",
            "params": {
                "gameId": 7,
                "clientId": "Android_3.90_360.360,yisdkpay.0-hall6.360.win",
                "userId": 10788,
                "roomId": 75041001,
                "tableId": 750410010200,
                "seatId": 0,
                "action": "grabTing",
                "action_id": 11,
                "zhan": 4,
                "pattern": [4, 4],
                "special_tile": 23
            }
        }
        
        """
        ftlog.debug('handleTableCallGrabTing message:', message)
        actionId = self.getActionIdFromMessage(message)
        if actionId == self.table.actionID:
            tile = message.getParam('tile', None)
            
            chi = message.getParam('chi', None)
            if chi:
                self.table.chiTile(seatId
                    , tile
                    , chi
                    , MTableState.TABLE_STATE_CHI | MTableState.TABLE_STATE_GRABTING)
                
            peng = message.getParam('peng', None)
            if peng:
                self.table.pengTile(seatId
                    , tile
                    , peng
                    , MTableState.TABLE_STATE_PENG | MTableState.TABLE_STATE_GRABTING)
                
            gang = message.getParam('gang', None)
            if gang:
                gangPattern = gang.get('pattern')
                gangPattern.sort()
                style = gang.get('style')
                tile = gang.get('tile')
                special_tile = gang.get('special_tile', None)
                self.table.gangTile(seatId
                    , tile
                    , gangPattern
                    , style
                    , MTableState.TABLE_STATE_GANG | MTableState.TABLE_STATE_GRABTING
                    , special_tile)
                
            zhan = message.getParam('zhan', None)
            if zhan:
                zhanPattern = zhan.get('pattern')
                tile = zhan.get('tile')
                special_tile = zhan.get('special_tile', None)
                self.table.zhanTile(seatId
                    , tile
                    , zhanPattern
                    , MTableState.TABLE_STATE_ZHAN | MTableState.TABLE_STATE_GRABTING
                    ,special_tile)
        else:
            ftlog.info('handleTableCallGrabTing message:', message
                       , ' but actionID is wrong, actionIDInTable:', self.table.actionID
                        , ' actionIDInMsg:', actionId)
            
    def handleTableCallGrabHuGang(self, userId, seatId, message):
        """处理抢杠胡"""
        actionId = self.getActionIdFromMessage(message)
        if actionId == self.table.actionID:
            winTile = message.getParam('tile', None)
            if winTile:
                self.table.grabHuGang(seatId, winTile)
            else:
                ftlog.error("handleTableCallGrabHuGang winTile is None")
        else:
            ftlog.info('handleTableCallGrabHuGang message:', message
                       , ' but actionID is wrong, actionIDInTable:', self.table.actionID
                        , ' actionIDInMsg:', actionId)
            
    def handleTableCallpass(self, userId, seatId, message):
        """处理过消息
        {
            "clientId": "Android_3.90_360.360,yisdkpay.0-hall6.360.win",
            "cmd": "       table_call",
            "params": {
                "gameId": 7,
                "clientId": "Android_3.90_360.360,yisdkpay.0-hall6.360.win",
                "userId": 10788,
                "roomId": 75041001,
                "tableId": 750410010200,
                "seatId": 0,
                "action": "pass",
                "action_id": 15
            }
        }
        """
        actionId = self.getActionIdFromMessage(message)
        if actionId == self.table.actionID:
            self.table.playerCancel(seatId)
        else:
            ftlog.info('handleTableCallpass message:', message
                       , ' but actionID is wrong, actionIDInTable:', self.table.actionID
                        , ' actionIDInMsg:', actionId)
                        
    def handleTableCallChi(self, userId, seatId, message):
        """处理吃消息
        {
            "clientId": "Android_3.90_360.360,yisdkpay.0-hall6.360.win",
            "cmd": "table_call",
            "params": {
                "gameId": 7,
                "clientId": "Android_3.90_360.360,yisdkpay.0-hall6.360.win",
                "userId": 10788,
                "roomId": 75041001,
                "tableId": 750410010200,
                "seatId": 0,
                "action": "chi",
                "action_id": 34,
                "tile": 19,
                "pattern": [17, 18, 19]
            }
        }
        """
        actionId = self.getActionIdFromMessage(message)
        ftlog.info('action_handler_longnet.handleTableCallChi acitonId:', actionId
                   , ' message:', message)
        
        if actionId == self.table.actionID:
            chi = message.getParam('tile')
            chiResult = message.getParam('pattern', None)
            if not chiResult:
                ftlog.error('handleTableCallChi pattern is None')
            if chi not in chiResult:
                ftlog.error('handleTableCallChi chiTile:', chi
                            , ' chiPattern:', chiResult
                            , ' chiTile not in chiPattern...')
            self.table.chiTile(seatId, chi, chiResult, MTableState.TABLE_STATE_CHI)
        else:
            ftlog.info('handleTableCallChi message:', message
                       , ' but actionID is wrong, actionIDInTable:', self.table.actionID
                        , ' actionIDInMsg:', actionId)
                    
    def handleTableCallPeng(self, userId, seatId, message):
        """处理碰牌消息
        {
            "cmd": "table_call",
            "params": {
                "gameId": 7,
                "clientId": "Android_3.90_360.360,yisdkpay.0-hall6.360.win",
                "userId": 10788,
                "roomId": 75041001,
                "tableId": 750410010200,
                "seatId": 0,
                "action": "peng",
                "action_id": 0,
                "tile": 7,
                "pattern": [7, 7, 7]
            }
        }
        """
        actionId = self.getActionIdFromMessage(message)
        if actionId == self.table.actionID:
            tile = message.getParam('tile')
            pattern = message.getParam('pattern', None)
            self.table.pengTile(seatId, tile, pattern, MTableState.TABLE_STATE_PENG)
        else:
            ftlog.info('handleTableCallPeng message:', message
                       , ' but actionID is wrong, actionIDInTable:', self.table.actionID
                        , ' actionIDInMsg:', actionId)
    
    def handleTableCallGang(self, userId, seatId, message):
        """处理杠牌消息
        {
            "cmd": "table_call",
            "params": {
                "gameId": 7,
                "clientId": "Android_3.776_weixin,tyGuest.alipay.0-hall7.youle.scmj",
                "userId": 10003,
                "roomId": 78051001,
                "tableId": 780510010200,
                "seatId": 0,
                "action": "gang",
                "action_id": 0,
                "gang": {
                    "tile": 1,
                    "pattern": [1, 1, 1, 1],
                    "style": 1
                }
            }
        }
        """
        actionId = self.getActionIdFromMessage(message)
        if actionId == self.table.actionID:
            _tile = message.getParam('tile', None)
            gang = message.getParam('gang', None)
            if not gang:
                ftlog.error('wrong message gang...')
                return
            
            tile = gang.get('tile', _tile)
            gangPattern = gang.get('pattern')
            gangPattern.sort()
            style = gang.get('style')
            
            if style == MPlayerTileGang.MING_GANG and not tile:
                ftlog.error('handleTableCallGang error tile:', tile, ' gang:', gang)
                return
            
            special_tile = gang.get('special_tile', None)
            ftlog.debug('handleTableCallGang tile:', tile, ' gang:', gang,' message:', message)
            self.table.gangTile(seatId, tile, gangPattern, style, MTableState.TABLE_STATE_GANG, special_tile)
        else:
            ftlog.info('handleTableCallGang message:', message
                       , ' but actionID is wrong, actionIDInTable:', self.table.actionID
                        , ' actionIDInMsg:', actionId)
            
    def handleTableCallWin(self, userId, seatId, message):
        """处理和牌消息
        {
            "cmd": "table_call",
            "params": {
                "gameId": 7,
                "clientId": "Android_3.90_360.360,yisdkpay.0-hall6.360.win",
                "userId": 10788,
                "roomId": 75041001,
                "tableId": 750410010200,
                "seatId": 0,
                "action": "win",
                "action_id": 14,
                "tile": 2
            }
        }
        """
        actionId = self.getActionIdFromMessage(message)
        if actionId == self.table.actionID:
            tile = message.getParam('tile')
            ftlog.debug('handleTableCallWin actionId =',actionId,'tile', tile,'seatId',seatId)
            self.table.gameWin(seatId, tile)
        else:
            ftlog.info('handleTableCallWin message:', message
                       , ' but actionID is wrong, actionIDInTable:', self.table.actionID
                        , ' actionIDInMsg:', actionId)
    
    def handleTableCallPlay(self, userId, seatId, message):
        """处理出牌消息
        {
            "cmd": "table_call",
            "params": {
                "gameId": 7,
                "clientId": "Android_3.90_360.360,yisdkpay.0-hall6.360.win",
                "userId": 10788,
                "roomId": 75041001,
                "tableId": 750410010200,
                "seatId": 0,
                "action": "play",
                "action_id": 11,
                "tile": 12,
                "ting": 1
            }
        }
        """
        # 定缺阶段禁止打牌
        if self.table.absenceProcessor.getState() != 0:
            return

        actionId = self.getActionIdFromMessage(message)
        if actionId == self.table.actionID:
            tile = message.getParam('tile')
            if not tile:
                ftlog.error('handleTableCallPlay message error, no valid tile...')
                return
            
            isTing = message.getParam('ting', 0)
            # 自己摸牌，状态是听
            if (isTing == 1) and (self.table.addCardProcessor.getState() & MTableState.TABLE_STATE_TING):
                kouTiles = message.getParam('kou', [])
                exInfo = self.table.addCardProcessor.extendInfo
                ftlog.debug('handleTableCallPlay kouTiles:', kouTiles,' exInfo.extend:', exInfo.extend)
                self.table.tingAfterDropCard(seatId, tile, kouTiles, exInfo)
            elif self.table.addCardProcessor.mustTing:
                exInfo = self.table.addCardProcessor.extendInfo
                dropTiles = exInfo.getAllDropTilesInGrabTing()
                if tile not in dropTiles:
                    tile = dropTiles[0]
                self.table.tingAfterDropCard(seatId, tile, [], exInfo)
            else:
                self.table.playerCancel(seatId)
                self.table.dropTile(seatId, tile)
        else:
            ftlog.info('handleTableCallPlay message:', message
                       , ' but actionID is wrong, actionIDInTable:', self.table.actionID
                        , ' actionIDInMsg:', actionId)

    def handleTableCallPing(self, userId, seatId, message):
        """处理过消息
        {
            "cmd":"table_call",
            "result":{
                "action":"ping",
                "tableId":71280310010200,
                "time":1486807436
                "ping":15
                }
        }
        """
        ping = message.getParam('ping', 0)
        time = message.getParam('time', 0)
        ftlog.debug('handleTableCallPing userId=',userId, ping, time)
        self.table.sendUserNetState(userId, seatId, ping, time)
 
    def handleTableCallAskPiao(self, userId, seatId, message):
        """
        客户端定飘
        
        {
            "cmd": "table_call",
            "params": {
                "action": "ask_piao", // 定飘的action
                "gameId": 730,
                "roomId": 7309011001,
                "tableId": 73090110010200,
                "piaoPoint": 3, // 定飘的数值
                "seatId": 0 // 玩家当前的座位号
            }
        }
        """
        piaoPoint = message.getParam('piaoPoint', 0)
        self.table.piao(seatId, piaoPoint)

    def handleTableCallAcceptPiao(self, userId, seatId, message):
        """
        客户端定飘
        
        {
            "cmd": "table_call",
            "params": {
                "action": "accept_piao",
                "gameId": 730,
                "roomId": 7309011001,
                "tableId": 73090110010200,
                "solution": [ // list，多个飘得邀请
                    {
                        "piaoSeatId": 1,  // 飘得人座位ID
         
                        "piaoPoint": 3      // 牌的数值，大于0表示接受，0表示不接受
         
                    }
         
                ],
                "timeOut": 5,
                "seatId": 0 // 我的座位ID
            }
        }
        """
        piaos = message.getParam('solution', 0)
        for piao in piaos:
            piaoSeatId = piao['piaoSeatId']
            piaoPoint = piao['piaoPoint']
            self.table.acceptPiao(seatId, piaoSeatId, piaoPoint)

    def handleTableCallFangMao(self, userId, seatId, message):
        actionId = self.getActionIdFromMessage(message)
        ftlog.debug('action_handler_longnet.handleTableCallFangMao actionIdInMsg:', actionId
                    , ' actionIdInTable:', self.table.actionID)
        
        if actionId == self.table.actionID:
            mao = message.getParam('mao', None)
            if not mao:
                ftlog.info('action_handler_longnet.handleTableCallFangMao wrong message:', message)
                return
            self.table.fangMao(seatId, mao)
        else:
            ftlog.info('handleTableCallFangMao message:', message
                       , ' but actionID is wrong, actionIDInTable:', self.table.actionID
                        , ' actionIDInMsg:', actionId)
            
    def handleTableCallExtendMao(self, userId, seatId, message):
        actionId = self.getActionIdFromMessage(message)
        ftlog.debug('action_handler_longnet.handleTableCallExtendMao actionIdInMsg:', actionId
            , ' actionIdInTable:', self.table.actionID)
                
        if actionId == self.table.actionID:
            mao = message.getParam('mao', None)
            if not mao:
                return
            
            extend = mao['tile']
            maoType = mao['type']
            if not extend or type == MTDefine.MAO_DAN_NO:
                ftlog.info('action_handler_longnet.handleTableCallExtendMao wrong message:', message)
                return
            self.table.extendMao(seatId, extend, maoType)
        else:
            ftlog.info('handleTableCallExtendMao message:', message
                       , ' but actionID is wrong, actionIDInTable:', self.table.actionID
                        , ' actionIDInMsg:', actionId)
            
    def handleTableCallDouble(self, userId, seatId, message):
        actionId = self.getActionIdFromMessage(message)
        ftlog.debug('action_handler_longnet.handleTableCallDouble actionIdInMsg:', actionId
                    , ' actionIdInTable:', self.table.actionID
                    , ' userId:', userId, ' seatId:', seatId)
        
        if actionId == self.table.actionID:
            self.table.double(seatId)
        else:
            ftlog.info('handleTableCallDouble message:', message
                       , ' but actionID is wrong, actionIDInTable:', self.table.actionID
                        , ' actionIDInMsg:', actionId)
            
    def handleTableCallNoDouble(self, userId, seatId, message):
        actionId = self.getActionIdFromMessage(message)
        ftlog.debug('action_handler_longnet.handleTableCallNoDouble actionIdInMsg:', actionId
                    , ' actionIdInTable:', self.table.actionID
                    , ' userId:', userId, ' seatId:', seatId)
        
        if actionId == self.table.actionID:
            self.table.noDouble(seatId)
        else:
            ftlog.info('handleTableCallNoDouble message:', message
                       , ' but actionID is wrong, actionIDInTable:', self.table.actionID
                        , ' actionIDInMsg:', actionId)
            
    def handleTableCallQiangJin(self, userId, seatId, message):
        """
        处理抢金请求消息
            {
                cmd: table_call,
                params: {
                    "action": "qiangjin",
                    action_id: 1,
                    state: 1,
                    seatId: 0,
                    roomId: xxxx,
                    tableId: xxxx,
                    gameId: 7002,
                    userId: 10250
                }
            }
        """
        actionId = self.getActionIdFromMessage(message)
        ftlog.debug('handleTableCallQiangJin actionId=',actionId,self.table.actionID)
        if actionId == self.table.actionID:
            state = message.getParam('state', None)
            self.table.actionQiangjin(userId,seatId,state)

    def handleTableCallBuFlower(self, userId, seatId, message):
        """处理补花请求消息, 怀宁需要玩家主动请求补花
            {
                cmd: table_call,
                params: {
                    "action": "bu_hua",
                    action_id: 1,
                    tile: 31,
                    seatId: 0,
                    roomId: xxxx,
                    tableId: xxxx,
                    gameId: 7002,
                    userId: 10250
                }
            }
        """
        actionId = self.getActionIdFromMessage(message)
        if actionId == self.table.actionID:
            tile = message.getParam('tile', None)
            if not tile:
                return
            self.table.buFlower(seatId, tile)

    def handleTableCallCrapShoot(self, userId, seatId, message):
        """
        掷骰子

        {
            "cmd": "table_call",
            "params": {
                "action": "crapshoot", // 掷骰子
                "gameId": 730,
                "roomId": 7309011001,
                "tableId": 73090110010200,
                "seatId": 0 // 玩家当前的座位号
            }
        }
        """
        self.table.crapshoot(seatId)

    def handleTableCallDingAbsence(self, userId, seatId, message):
        """定缺

        cmd: table_call
        params: {
            action: ding_absence,
            gameId: 7006,
            roomId: xxxx,
            tableId: xxxx,
            userId: xxxx,
            seatId: x,
            color: 0,  # 有效值0,1,2，分别对应万筒条
        }
        """
        color = message.getParam('color', None)
        if color is None:
            return
        self.table.dingAbsence(userId, seatId, color)

    def handleTableCallChange3Tiles(self, userId, seatId, message):

        """
        "cmd": "table_call",
            "params": {
                "action":"change_3tiles",
                "action_id":_model.getActionId(),
                "threeTiles":_tiles,
                "roomId":_roomId,
                "tableId":_tableId,
                "seatId":_seatId
            }
        """
        threeTiles = message.getParam('threeTiles', None)
        if threeTiles is None:
            return
        self.table.chooseChange3tiles(userId, seatId, threeTiles)


