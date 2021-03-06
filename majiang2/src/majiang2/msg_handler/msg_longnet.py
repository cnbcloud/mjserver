# -*- coding=utf-8
'''
Created on 2016年9月23日

@author: zhaol
'''
from majiang2.msg_handler.msg import MMsg
from freetime.entity.msg import MsgPack
from poker.entity.dao import sessiondata
from poker.protocol import router
from poker.entity.game.tables.table_player import TYPlayer
from majiang2.table_state.state import MTableState
import poker.util.timestamp as pktimestamp
from freetime.util import log as ftlog
from majiang2.ai.play_mode import MPlayMode
import json
from majiang2.entity import uploader, majiang_conf
from freetime.core.tasklet import FTTasklet
import random
from majiang2.table.table_config_define import MTDefine
from majiang2.win_loose_result.one_result import MOneResult
from majiang2.tile.tile import MTile
import time

class MMsgLongNet(MMsg):
    
    def __init__(self):
        super(MMsgLongNet, self).__init__()
        
    def table_call_add_card(self, player, tile, state, seatId, timeOut, actionId, extendInfo, recordUserIds):
        """给玩家发牌，只给收到摸牌的玩家发这条消息
        参数说明：
        seatId - 发牌玩家的座位号
        {
            "cmd": "send_tile",
            "result": {
                "gameId": 7,
                "gang_tiles": [],
                "peng_tiles": [],
                "chi_tiles": [],
                "timeout": 9,
                "tile": 6,
                "remained_count": 53,
                "seatId": 0,
                "trustee": 0,
                "standup_tiles": [
                    2,
                    3,
                    4,
                    8,
                    12,
                    12,
                    14,
                    19,
                    19,
                    22,
                    23,
                    24,
                    35
                ],
                "action_id": 1
            }
        }
        
        "ting_action": [
            [
                8,
                [
                    [
                        12,
                        1,
                        1
                    ]
                ]
            ],
            [
                2,
                [
                    [
                        12,
                        1,
                        1
                    ]
                ]
            ],
            [
                12,
                [
                    [
                        2,
                        1,
                        3
                    ],
                    [
                        5,
                        1,
                        0
                    ],
                    [
                        8,
                        1,
                        1
                    ]
                ]
            ],
            [
                5,
                [
                    [
                        12,
                        1,
                        1
                    ]
                ]
            ]
        ]
        """
        message = self.createMsgPackResult('send_tile')
        message.setResult('gang_tiles', player.copyGangArray())
        message.setResult('peng_tiles', player.copyPengArray())
        message.setResult('chi_tiles', player.copyChiArray())
        message.setResult('zhan_tiles', player.zhanTiles)
        message.setResult('kou_tiles', player.kouTiles)
        message.setResult('flower_tiles', player.flowers)
        message.setResult('laizi_action',player.laizi)
        # AI运算需要，这时已经把牌加到手牌中了，消息中挪出新增的牌
        ftlog.debug("add_card tile = ", tile)
        handTiles = player.copyHandTiles()
        ftlog.debug("add_card handTiles = ", handTiles)
        if tile in handTiles:
            handTiles.remove(tile)
        else:
            ftlog.info('msg_long_net.table_call_add_card handTiles:', handTiles
                    , ' tile:', tile)
            
        zhanTiles = player.zhanTiles
        if zhanTiles and zhanTiles in handTiles:
            handTiles.remove(zhanTiles)
        kouTiles = player.kouTiles
        if kouTiles:
            for kouTilePattern in kouTiles:
                for kouTile in kouTilePattern:
                    if kouTile in handTiles:
                        handTiles.remove(kouTile)

	if MPlayMode().isSubPlayMode(self.playMode, MPlayMode.QUESHOU):
            if player.isTing():
                magicTile = self.tableTileMgr.getMagicTile()
		dropTiles = player.jinkanDrop
                for dropTile in dropTiles:
                    if dropTile != magicTile:
                        handTiles.remove(dropTile)

        message.setResult('standup_tiles', handTiles)
        ftlog.debug("add_card standup_tiles = ", handTiles)
        
        message.setResult('timeout', timeOut)
        message.setResult('tile', tile)
            
        message.setResult('remained_count', self.tableTileMgr.getTilesLeftCount())
        message.setResult('seatId', seatId)
        message.setResult('trustee', 1 if player.autoDecide else 0)
        message.setResult('action_id', actionId)

        # 定缺时，不能让用户做动作及胡牌。必须先选完缺哪一门 (庄家起手牌要定缺时)
        if not extendInfo.getIsInAbsence():
            gang = extendInfo.getChiPengGangResult(MTableState.TABLE_STATE_GANG)
            if gang:
                message.setResult('gang_action', gang)
                pigus = extendInfo.getPigus(MTableState.TABLE_STATE_FANPIGU)
                if pigus:
                    message.setResult('fanpigu_action', pigus)
                else:
                    ftlog.debug('table_call_add_card gang_action not find pigus')
            ting_action = extendInfo.getTingResult(self.tableTileMgr, seatId)
            if ting_action:
                tingliang_action = extendInfo.getTingLiangResult(self.tableTileMgr)
                if tingliang_action:
                    message.setResult('tingliang_action', tingliang_action)
                kou_ting_action = extendInfo.getCanKouTingResult(self.tableTileMgr, seatId)
                if kou_ting_action:
                    message.setResult('kou_ting_action', kou_ting_action)
                else:
		    ftlog.debug('table_call_add_card ting_action',ting_action)
                    message.setResult('ting_action',ting_action)
		    jinkanResult,jinkanDrop = self.getJinKanDrop(tile,handTiles,ting_action)
                    if jinkanResult:
                        message.setResult('jinkanDrop', jinkanDrop)
		    
            mao_action = extendInfo.getMaoResult(self.tableTileMgr, seatId)
            if mao_action:
                message.setResult('mao_action', mao_action)

            flower_action = extendInfo.getFlowerResult(self.tableTileMgr, seatId)
            if flower_action:
                message.setResult('flower_action', flower_action)
        
            # 自动胡的时候不下发胡的行为给前端
            if not self.autoWin:
                wins = extendInfo.getChiPengGangResult(MTableState.TABLE_STATE_HU)
		#血战血流玩家胡后不再提示胡
                if wins and len(wins) > 0 and not player.isWon():
                    ftlog.debug('table_call_add_card wins: ', wins)
                    message.setResult('win_tile', wins[0]['tile'])
                    message.setResult('win_degree', 1)
		    if MPlayMode().isSubPlayMode(self.playMode, MPlayMode.QUESHOU):
                        if wins[0]['sanjindao']:
                            message.setResult('sanjindao', 1)
			message.setResult('winMode', wins[0]['winMode']) 	

        # 定缺时不能继续打牌的
        if extendInfo.getIsInAbsence() or self.tianTing:
            message.setResult('can_not_play', 1)

        # 缓存消息    
        self.latestMsg[player.curSeatId] = message
	ftlog.debug('msg_long_net.table_call_add_card message=',message)
        send_msg(message, player.userId)
        self.addMsgRecord(message, recordUserIds)

    def table_call_ask_gang(self, player, tile, actionId, extendInfo):
        message = self.createMsgPackResult('ask_gang')
        if not extendInfo.getIsInAbsence():
            gang = extendInfo.getChiPengGangResult(MTableState.TABLE_STATE_GANG)
            if gang:
                message.setResult('gang_action', gang)
            # ting_action = extendInfo.getTingResult(self.tableTileMgr, player.curSeatId)
            # if ting_action:
            #     message.setResult('ting_action',ting_action)
        message.setResult('action_id', actionId)
        message.setResult('tile', tile)
        message.setResult('seatId', player.curSeatId)
        self.latestMsg[player.curSeatId] = message
        send_msg(message, player.userId)
        self.addMsgRecord(message, player.userId)

    def table_call_ask_ting(self, seatId, actionId, winNodes, tingAction, timeOut):
        message = self.createMsgPackResult('table_call', 'ask_ting')
        message.setResult('action_id', actionId)
        message.setResult('seatId', seatId)
        message.setResult('all_win_tiles', winNodes)
        message.setResult('timeout', timeOut)
        message.setResult('ting_result', tingAction)
        
        self.latestMsg[seatId] = message
        send_msg(message, self.players[seatId].userId)
        self.addMsgRecord(message, self.players[seatId].userId)

    def table_call_tian_ting_over(self, seatId, actionId):
        message = self.createMsgPackResult('table_call', 'tian_ting_over')
        message.setResult('action_id', actionId)
        message.setResult('seatId', seatId)
        #self.latestMsg[seatId] = message
        send_msg(message, self.players[seatId].userId)
        self.addMsgRecord(message, self.players[seatId].userId)

    def table_call_geo(self, gps, distances, userIds):
        message = self.createMsgPackResult('geo')
        message.setResult('gps', gps)
        message.setResult('distances', distances)
        send_msg(message, userIds)
        self.addMsgRecord(message, userIds)

    def table_call_fang_mao(self
                             , player
                             , mao
                             , maos
                             , state
                             , seatId
                             , timeOut
                             , actionID
                             , extendInfo):
        message = self.createMsgPackResult('fang_mao')
        message.setResult('gang_tiles', player.copyGangArray())
        message.setResult('peng_tiles', player.copyPengArray())
        message.setResult('chi_tiles', player.copyChiArray())
        message.setResult('zhan_tiles', player.zhanTiles)
        message.setResult('kou_tiles', player.kouTiles)
        
        # AI运算需要，这时已经把牌加到手牌中了，消息中挪出新增的牌
        handTiles = player.copyHandTiles()
        ftlog.debug("add_card handTiles = ", handTiles)
            
        zhanTiles = player.zhanTiles
        if zhanTiles and zhanTiles in handTiles:
            handTiles.remove(zhanTiles)
        kouTiles = player.kouTiles
        if kouTiles:
            for kouTilePattern in kouTiles:
                for kouTile in kouTilePattern:
                    if kouTile in handTiles:
                        handTiles.remove(kouTile)
        message.setResult('standup_tiles', handTiles)
        ftlog.debug("add_card standup_tiles = ", handTiles)
        
        message.setResult('timeout', timeOut)
        message.setResult('mao_tiles', player.copyMaoTile())
        message.setResult('mao', mao)
        message.setResult('remained_count', self.tableTileMgr.getTilesLeftCount())
        message.setResult('seatId', seatId)
        message.setResult('trustee', 1 if player.autoDecide else 0)
        message.setResult('action_id', actionID)
        
        gang = extendInfo.getChiPengGangResult(MTableState.TABLE_STATE_GANG)
        if gang:
            message.setResult('gang_action', gang)
            pigus = extendInfo.getPigus(MTableState.TABLE_STATE_FANPIGU)
            if pigus:
                message.setResult('fanpigu_action', pigus)
            else:
                ftlog.debug('table_call_add_card gang_action not find pigus')
        ting_action = extendInfo.getTingResult(self.tableTileMgr, seatId)
        if ting_action:
            tingliang_action = extendInfo.getTingLiangResult(self.tableTileMgr)
            if tingliang_action:
                message.setResult('tingliang_action', tingliang_action)
            kou_ting_action = extendInfo.getCanKouTingResult(self.tableTileMgr, seatId)
            if kou_ting_action:
                message.setResult('kou_ting_action', kou_ting_action)
            else:
                message.setResult('ting_action', ting_action)
                
        mao_action = extendInfo.getMaoResult(self.tableTileMgr, seatId)
        if mao_action:
            message.setResult('mao_action', mao_action)
            
        wins = extendInfo.getChiPengGangResult(MTableState.TABLE_STATE_HU)
        if wins and len(wins) > 0:
            ftlog.debug('table_call_add_card wins: ', wins)
            message.setResult('win_tile', wins[0]['tile'])
            message.setResult('win_degree', 1)
         
        # 缓存消息    
        self.latestMsg[player.curSeatId] = message
        send_msg(message, player.userId)
        self.addMsgRecord(message, player.userId)
    
    def table_call_add_card_broadcast(self, seatId, timeOut, actionId, userId, tile,showTile = False):
        """通知其他人给某个人发牌
        参数说明：
        seatId 发牌玩家的座位号
        {
            "cmd": "send_tile",
            "result": {
                "remained_count": 54,
                "seatId": 3,
                "gameId": 7,
                "timeout": 9
            }
        }
        """
        message = self.createMsgPackResult('send_tile')
        message.setResult('seatId', seatId)
        message.setResult('remained_count', self.tableTileMgr.getTilesLeftCount())
        message.setResult('timeout', timeOut)
        message.setResult('action_id', actionId)
        if self.tableTileMgr and self.tableTileMgr.players:
            message.setResult('flower_tiles', self.tableTileMgr.players[seatId].flowers)

        if self.players[seatId].isTingLiang() or showTile:
            # 亮牌时，输出当前用户抓到的牌，否则不要输出用户抓到的牌
            message.setResult('tile', tile)
        
        ftlog.debug('MMsgLongNet.table_call_add_card_broadcast broadcast add card msg to user:', userId, ' message:', message)
        
        send_msg(message, userId)
        
    def table_call_fang_mao_broadcast(self
                        , seatId
                        , timeOut
                        , actionID
                        , userId
                        , maos
                        , mao):
        message = self.createMsgPackResult('fang_maos')
        message.setResult('seatId', seatId)
        message.setResult('remained_count', self.tableTileMgr.getTilesLeftCount())
        message.setResult('timeout', timeOut)
        message.setResult('action_id', actionID)
        message.setResult('mao_tiles', maos)
        message.setResult('mao', mao)
        ftlog.debug('MMsgLongNet.table_call_fang_mao_broadcast broadcast add tiles after fangMao to user:', userId
                    , ' message:', message)
        send_msg(message, userId)
        
        
    def table_call_drop(self, seatId, player, tile, state, extendInfo, actionId, timeOut, winTiles=None):
        """通知玩家出牌
        参数：
            seatId - 出牌玩家的ID
            player - 针对出牌做出牌操作的玩家
            tile - 本次出牌
            state - 通知玩家可以做出的选择
            extendInfo - 扩展信息
            actionId - 当前的操作ID
            winTiles - 可能胡哪些牌，某些玩法没有听牌功能，但也要每次提示玩家可胡哪些牌
        eg:
        {'ting': {'chiTing': []}, 'chi': [[12, 13, 14]]}
        """
        ftlog.debug( 'table_call_drop longnet player drop tile = ', tile)
        message = self.createMsgPackResult('play')
        message.setResult('tile', tile)
        message.setResult('seatId', seatId)
        message.setResult('remained_count', self.tableTileMgr.getTilesLeftCount())
        hasAction = False
        if tile in player.laizi:
            message.setResult('laizi_gang', len(self.players[seatId].laiziGang))
        # 吃
        if state & MTableState.TABLE_STATE_CHI:
            hasAction = True
            patterns = extendInfo.getChiPengGangResult(MTableState.TABLE_STATE_CHI)
            message.setResult('chi_action', patterns)
        
        # 碰
        if state & MTableState.TABLE_STATE_PENG:
            hasAction = True
            patterns = extendInfo.getChiPengGangResult(MTableState.TABLE_STATE_PENG)
            message.setResult('peng_action', patterns)
            
        # exmao碰
        if state & MTableState.TABLE_STATE_QIANG_EXMAO:
            hasAction = True
            patterns = extendInfo.getChiPengGangResult(MTableState.TABLE_STATE_QIANG_EXMAO)
            message.setResult('peng_action', patterns)
        
        # 杠
        if state & MTableState.TABLE_STATE_GANG:
            hasAction = True
            pattern = extendInfo.getChiPengGangResult(MTableState.TABLE_STATE_GANG)
            message.setResult('gang_action', pattern)
            pigus = extendInfo.getPigus(MTableState.TABLE_STATE_FANPIGU)
            if pigus:
                message.setResult('fanpigu_action', pigus)
            else:
                ftlog.debug('table_call_drop gang_action not find pigus')
            
        # 听
        if state & MTableState.TABLE_STATE_GRABTING:
            #"grabTing_action":{"chi_action":[2],"peng_action":27}
            hasAction = True
            grabTingAction = {}
            ces = extendInfo.getChiPengGangTingResult(MTableState.TABLE_STATE_CHI)
            if ces:
                grabTingAction['chi_action'] = ces
                
            pes = extendInfo.getChiPengGangTingResult(MTableState.TABLE_STATE_PENG)
            if pes:
                grabTingAction['peng_action'] = pes
                
            ges = extendInfo.getChiPengGangTingResult(MTableState.TABLE_STATE_GANG)
            if ges:
                grabTingAction['gang_action'] = ges
            
            ges = extendInfo.getChiPengGangTingResult(MTableState.TABLE_STATE_ZHAN)
            if ges:
                grabTingAction['zhan_action'] = ges
            message.setResult('grabTing_action', grabTingAction)
        
        # 和
	# 血战胡后不提示胡(自动胡)
        if (state & MTableState.TABLE_STATE_HU) and (not self.autoWin) and (not player.isWon()):
            hasAction = True
            message.setResult('win_degree', 1)
            message.setResult('win_action', 1)
            if MPlayMode().isSubPlayMode(self.tableTileMgr.playMode,MPlayMode.QUESHOU):
	        winMode = extendInfo.getChiPengGangResult(MTableState.TABLE_STATE_HU)
                message.setResult('winMode', winMode[0]['winMode']) 
        if hasAction:
            message.setResult('player_seat_id', player.curSeatId)
            message.setResult('timeout', timeOut)
            message.setResult('action_id', actionId)

        if winTiles is not None:
            message.setResult('winTiles', winTiles)

        tingliang_action = {}
        if extendInfo and self.players[seatId].isTing():
            # 客户端听亮和听
            tingliang_action = extendInfo.getTingLiangResult(self.tableTileMgr)
            message.setResult('tingliang_action', tingliang_action)
        if self.players[seatId].isTing() and not tingliang_action:
            message.setResult('ting', 1)
            if extendInfo and MPlayMode().isSubPlayMode(self.playMode, MPlayMode.QUESHOU):
                ting_action=extendInfo.getTingResult(self.tableTileMgr,seatId)
		ftlog.debug('table_call_drop ting_action=',ting_action)


        # 保存最新的消息
        if hasAction:
            self.latestMsg[player.curSeatId] = message
            
        # send_msg(message, player.userId)
        self.addMsgRecord(message, player.userId)
        return message

    def table_call_Qiangjin(self, player, state, actionId, timeOut,isTianHu = False,isSanJinDao = False):
	ftlog.debug('table_call_Qiangjin player, state, actionId, timeOut=',player, state, actionId, timeOut)
        message = self.createMsgPackResult('qiangjin')
        message.setResult('remained_count', self.tableTileMgr.getTilesLeftCount())
        hasAction = False
        if state & MTableState.TABLE_STATE_QIANGJIN_B:
            hasAction = True
            message.setResult('win_degree', 1)
            message.setResult('qiangjin_action', state)

        if state & MTableState.TABLE_STATE_QIANGJIN:
            hasAction = True
            message.setResult('win_degree', 1)
            message.setResult('qiangjin_action', state)
            
        if state & MTableState.TABLE_STATE_TIANHU:
            hasAction = True
            message.setResult('win_degree', 1)
            message.setResult('qiangjin_action', state)

        if state & MTableState.TABLE_STATE_SANJINDAO:
            hasAction = True
            message.setResult('win_degree', 1)
            message.setResult('qiangjin_action', state)

        if hasAction:
            message.setResult('player_seat_id', player.curSeatId)
            message.setResult('timeout', timeOut)
            message.setResult('action_id', actionId)
	    message.setResult('isTianHu', isTianHu)
	    message.setResult('isSanJinDao',isSanJinDao)

        self.latestMsg[player.curSeatId] = message
        send_msg(message, player.userId)
        self.addMsgRecord(message, player.userId)
 
    def sendTableEvent(self, count, userId, seatId, broadcastTargets = []):
        """发送table_event消息，实时更新牌桌人数"""
        msg = self.createMsgPackResult('table_event')
        msg.setResult('count', count)
        msg.setResult('players', self.getPlayersInMsg(seatId, False))
        send_msg(msg, broadcastTargets)
        self.addMsgRecord(msg, userId)
    
    def broadcastUserSit(self, seatId, userId, is_reconnect,is_host = False, broadcastTargets = []):
        """广播用户坐下消息"""
        message = self.createMsgPackResult('sit')
        message.setResult('isTableHost', 1 if is_host else 0)
        message.setResult('seatId', seatId)
        message.setResult('userId', userId)
        message.setResult('ip', sessiondata.getClientIp(userId))
        message.setResult('name', self.players[seatId].name)
        message.setResult('pic', self.players[seatId].purl)
        message.setResult('sex', self.players[seatId].sex)
        message.setResult('state', self.players[seatId].state)
#         message.setResult('score', 0)
        if self.tableConf.get(MTDefine.OVER_BY_SCORE, 0) and self.players[seatId].curScore:
            score = self.players[seatId].getCurScoreByBaseCount(self.tableConf.get("curBaseCount", 0))
            message.setResult('score', score)

        send_msg(message, broadcastTargets)
        self.addMsgRecord(message, userId)
        
    def send_location_message(self, seatId, userId):
        '''
        通知用户的location
        {
            "cmd": "location",
            "result": {
                "gameId": 7,
                "maxSeatN": 4,
                "play_mode": "harbin",
                "players": [
                    {
                        "master_point_level_diff": [
                            26,
                            100
                        ],
                        "name": "MI 3C",
                        "pic": "http://ddz.image.tuyoo.com/avatar/head_coffee.png",
                        "userId": 10788,
                        "master_point": 126,
                        "sex": 0,
                        "week_master_point": 126,
                        "charm": 0,
                        "max_win_sequence_count": 12,
                        "win_sequence_count": 0,
                        "seatId": 0,
                        "coin": 0,
                        "master_point_level": 5,
                        "max_degree": 4,
                        "new_win_sequence_count": 0
                    }
                ],
                "tableId": 750410010200,
                "seatId": 0,
                "roomId": 75041001,
                "tableType": "create"
            }
        }
        
        TODO:
        补充master_point_level等信息
        '''
        message = self.createMsgPackResult('location')
        message.setResult('seatId', seatId)
        message.setResult('maxSeatN', self.playerCount)
        message.setResult('play_mode', self.playMode)
        message.setResult('tableType', self.tableType)

        players = self.getPlayersInMsg(seatId, False)
        message.setResult('players', players)
        send_msg(message, userId)
        # 录入牌局记录
        self.addMsgRecord(message, userId)
        
    def getPlayersInMsg(self, mySeatId, isReconnect = False):
        ftlog.debug('msg_longnet.getPlayersInMsg players:', self.players
                    , ' playerCount:', self.playerCount)
        
        players = []
        allWinTtiles = [[] for _ in range(self.playerCount)]
        for i in range(self.playerCount):
            if not self.players[i]:
                continue
            allWinTtiles[i] = self.players[i].tingLiangWinTiles
            
        for i in range(self.playerCount):
            if not self.players[i]:
                continue
            
            player  = {}
            player['ip'] = sessiondata.getClientIp(self.players[i].userId)
            player['userId'] = self.players[i].userId
            player['name'] = self.players[i].name
            player['pic'] = self.players[i].purl
            player['sex'] = self.players[i].sex
            player['coin'] = self.players[i].coin
            player['seatId'] = i
            player['state'] = self.players[i].state
            player['ting'] = self.players[i].isTing()

            if self.tableTileMgr.sendInfoNeedMoreInfo():
                player['pengFromSeat']=self.players[i].pengTilesFromSeat
                player['gangFromSeat']=self.players[i].gangTilesFromSeat
		player['chiWithTile'] = self.players[i].chiTilesWithTile

            if self.tableConf.get(MTDefine.OVER_BY_SCORE, 0) and self.players[i].curScore:
                player['score'] = self.players[i].getCurScoreByBaseCount(self.tableConf.get("curBaseCount", 0))
                player['jiaoScore'] = self.players[i].getCurJiaoScoreByBaseCount(self.tableConf.get("curBaseCount", 0))

            if isReconnect:
                player['trustee'] = self.players[i].autoDecide
                userHands = self.players[i].copyHandTiles()
                zhanTiles = self.players[i].zhanTiles
                if zhanTiles and zhanTiles in userHands:
                    userHands.remove(zhanTiles)

		ftlog.debug('msg_longnet.sendMsgTableInfo userHands=',userHands)
		if MPlayMode().isSubPlayMode(self.playMode, MPlayMode.QUESHOU):
                    if self.players[i].isTing():
                        magicTile = self.tableTileMgr.getMagicTile()
			dropTiles = self.players[i].jinkanDrop
	                player['jinkanDrop'] = self.players[i].jinkanDrop
                	for dropTile in dropTiles:
                    	    if dropTile != magicTile:
                        	userHands.remove(dropTile)
					

                player['standup_tiles'] = userHands
                if self.players[i].isTingLiang():
                    # 亮牌时，输出当前用户手牌
                    ftlog.debug('msg_longnet.sendMsgTableInfo seatId:', i
                                , ' isTingLiang')
                    player['tingLiang'] = True
                    player['all_win_tiles'] = allWinTtiles
                   
                # 整理handTile    
                if i != mySeatId:
                    if self.players[i].isTingLiang():
                        # 亮牌情况下，当前用户手牌发放
                        ftlog.debug('msg_longnet.sendMsgTableInfo seatId:', i
                                    , ' isTingLiang, broadcast handTiles to client...')
                        ftlog.debug('tingLiangTilesCurrent Tile', self.players[i].tingLiangTilesCurrent)
                        newHands = []
                        for _ in range(len(userHands) - len(self.players[i].tingLiangTilesCurrent)):
                            newHands.append(0)
                        newHands.extend(self.players[i].tingLiangTilesCurrent)    
                        player['standup_tiles'] = newHands
                        player['liang_tiles']   = self.players[i].tingLiangTilesCurrent
                        ftlog.debug('msg_longnet.sendMsgTableInfo seatId:', i
                                    , ' standup_tiles:', newHands)
                    else:
                        # 隐藏其他玩家手牌
                        ftlog.debug('msg_longnet.sendMsgTableInfo hide handTiles...')
                        player['standup_tiles'] = [0 for _ in range(len(userHands))]

		ftlog.debug('msg_longnet.sendMsgTableInfo userHands=xxx',userHands,player['standup_tiles'])                
 
                player['gang_tiles'] = self.players[i].copyGangArray()
                player['peng_tiles'] = self.players[i].copyPengArray()
                player['chi_tiles'] = self.players[i].copyChiArray()
                player['ting_tiles'] = self.players[i].copyTingArray()
                player['drop_tiles'] = self.tableTileMgr.menTiles[self.players[i].curSeatId]
                player['zhan_tiles'] = self.players[i].zhanTiles
                player['flower_tiles'] = self.players[i].flowers
                player['flower_scores'] = self.players[i].flowerScores
		player['hu_tiles'] = self.players[i].copyHuArray()
                player['winMode'] = self.players[i].copyHuModeArray()		
                player['huRank'] = self.players[i].xuezhanRank		

                gangTiles = [] 
                for gang in self.players[i].copyGangArray():          
                    for gangTile in gang['pattern']:
                        gangTiles.append(gangTile)
                kouTiles = []
                for kouPattern in self.players[i].kouTiles:
                    for kouTile in kouPattern:
                        if kouTile not in gangTiles:
                            kouTiles.append([kouTile,kouTile,kouTile])
                            break
                player['kou_tiles'] = kouTiles
                player['mao_tiles'] = self.players[i].copyMaoTile()
                player['laizi_tiles'] = {"tile":self.players[i].laizi,"factor":self.players[i].laiziPi}
                message = self.latestMsg[mySeatId]
                if message:
                    if i == mySeatId:
                        if (self.actionId == message.getResult('action_id', 0)) and \
                            (message.getCmd() == 'send_tile'):
                            # 发送快照中的手牌
                            ftlog.debug('msg_longnet.sendMsgTableInfo lastMsg:', self.latestMsg
                                        , ' actionId:', self.actionId
                                        , ' seatId:', i)
                            #modify by youjun 0629 补花阶段断线重连回来手牌会含有花牌这时候send_tile中
			    player['standup_tiles'] = message.getResult('standup_tiles', [])
                    
                    '''
                        mySeatId是断线的人，i是play的人
                    '''
                    if i != mySeatId:
                        if (self.actionId == message.getResult('action_id', 0)) and \
                            (message.getCmd() == 'play') and \
                            (message.getResult('seatId', 0) == i):
                            ftlog.debug('msg_longnet.sendMsgTableInfo lastMsg:', self.latestMsg
                                        , ' actionId:', self.actionId
                                        , ' reconnectSeatId:', mySeatId
                                        , ' seatId:', i, ' play, but I need tile to rebuild..')
                            player['standup_tiles'].append(message.getResult('tile', 0))
            	ftlog.debug('msg_longnet.sendMsgTableInfo userHands=YYY',userHands,player['standup_tiles'])    
            ftlog.debug('msg_longnet.sendMsgTableInfo pack player info:', player)        
            players.append(player)
        return players

    def sendMsgInitTils(self, tiles, banker, userId, seatId,second = False):
        """发牌
        {
            "cmd": "init_tiles",
            "result": {
                "tiles": [
                    22,
                    24,
                    29,
                    8,
                    14,
                    3,
                    12,
                    12,
                    4,
                    23,
                    2,
                    19,
                    35
                ],
                "gameId": 7,
                "header_seat_id": 0
            }
        }
        """
	ftlog.debug('sendMsgInitTiles log userId',userId)
        message = self.createMsgPackResult('init_tiles')
        message.setResult('tiles', tiles)
        message.setResult('seatId', seatId)
        message.setResult('init_second',second)
        message.setResult('header_seat_id', banker)
        send_msg(message, userId)
        self.addMsgRecord(message, userId)
	ftlog.debug('sendMsgInitTiles xxx')
    def createMsgPackRequest(self, cmd, action=None):
        """消息里面的公共信息"""
        mp = MsgPack()
        mp.setCmd(cmd)
        if action: 
            mp.setParam('action', action)
        mp.setParam('gameId', self.gameId)
        mp.setParam('roomId', self.roomId)
        mp.setParam('tableId', self.tableId)
        return mp
    
    def createMsgPackResult(self, cmd, action=None):
        """消息里面的公共信息"""
        mp = MsgPack()
        mp.setCmd(cmd)
        if action: 
            mp.setResult('action', action)
        mp.setResult('gameId', self.gameId)
        mp.setResult('roomId', self.roomId)
        mp.setResult('tableId', self.tableId)
        return mp
    
    def getMsgDispatchRobot(self, playerCount):
        """获取加机器人的上行消息"""
        message = self.createMsgPackRequest('table_call', 'dispatch_virtual_player')
        message.setParam('player_count', playerCount)
        return message
    
    def getMsgReadyTimeOut(self):
        """自建桌的准备超时"""
        message = self.createMsgPackRequest('table_call', 'friend_table_ready_time_out')
        return message
    
    def table_call_latest_msg(self, seatId):
        """补发最新的消息"""
        message = self.latestMsg[seatId]
        if not message:
            return
        
        if self.actionId == message.getResult('action_id', 0):
            message.setResult('reconnect', True)
            send_msg(message, self.players[seatId].userId)
        else:
            ftlog.debug('table_call_latest_msg actionId not match'
                        , ' actionId:', self.actionId
                        , ' actionIdInMsg:', message.getResult('action_id', 0)
                        , ' message:', message
                        , ' no need to send latest msg ......')
    
    def table_call_table_info(self, userId, banker, seatId, isReconnect, quanMenFeng, curSeat, tableState, cInfo = None, btInfo = None,bankerRemainCount = 0):
        """
        table_info消息
        参数
        1）userId - 发送table_info的用户
        2）banker - 庄家
        3）isReconnect - 是否断线重连
        例子：
        {
            "cmd": "table_info",
            "result": {
                "room_level": "master",
                "maxSeatN": 4,
                "room_coefficient": 6,
                "userId": 10788,
                "header_seat_id": 0,
                "table_product": [
                    {
                        "name": "36\\u4e07\\u91d1\\u5e01",
                        "price": "30",
                        "tip": "36\\u4e07\\u91d1\\u5e01",
                        "buy_type": "direct",
                        "needChip": 0,
                        "addchip": 360000,
                        "picurl": "http://111.203.187.150:8040/hall/pdt/imgs/goods_t300k_2.png",
                        "price_diamond": "300",
                        "type": 1,
                        "id": "TY9999D0030001",
                        "desc": "1\\u5143=12000\\u91d1\\u5e01"
                    }
                ],
                "table_raffle": 1,
                "base_chip": 1200,
                "reconnect": false,
                "seatId": 0,
                "roomId": 75041001,
                "quan_men_feng": 11,
                "tableType": "create",
                "gameId": 7,
                "gameRule": "classic",
                "interactive_expression_config": {
                    "0": {
                        "charm": 120,
                        "cost": 1200,
                        "chip_limit": 1320,
                        "ta_charm": -120
                    },
                    "1": {
                        "charm": 240,
                        "cost": 1200,
                        "chip_limit": 1320,
                        "ta_charm": 240
                    },
                    "2": {
                        "charm": 60,
                        "cost": 600,
                        "chip_limit": 1320,
                        "ta_charm": -60
                    },
                    "3": {
                        "charm": 120,
                        "cost": 600,
                        "chip_limit": 1320,
                        "ta_charm": 120
                    }
                },
                "play_mode": "harbin",
                "taskUnreward": true,
                "room_name": "\\u5927\\u5e08\\u573a",
                "current_player_seat_id": 0,
                "good_tile_chance": 1.5,
                "service_fee": 800,
                "min_coin": 10000,
                "play_timeout": 9,
                "max_coin": -1,
                "table_state": "play",
                "players": [
                    {
                        "ip": "111.203.187.129",
                        "pic": "http://ddz.image.tuyoo.com/avatar/head_coffee.png",
                        "userId": 10788,
                        "sex": 0,
                        "week_master_point": 126,
                        "max_win_sequence_count": 12,
                        "win_sequence_count": 0,
                        "seatId": 0,
                        "master_point_level": 5,
                        "vipInfo": {
                            "vipExp": 0,
                            "vipLevel": {
                                "level": 0
                            }
                        },
                        "ting": 0,
                        "new_win_sequence_count": 0,
                        "max_degree": 4,
                        "member": {
                            "flag": 0
                        },
                        "rank_name": "\\u5168\\u56fd\\u96c0\\u795e\\u699c",
                        "rank_index": 2,
                        "master_point_level_diff": [
                            26,
                            100
                        ],
                        "stat": "playing",
                        "charm": 0,
                        "coin": 21004366,
                        "name": "MI 3C",
                        "master_point": 126
                    },
                    {
                        "stat": "playing",
                        "name": "\\u6211\\u662f\\u738b",
                        "ip": "192.168.10.76",
                        "pic": "http://ddz.image.tuyoo.com/avatar/head_male_1.png",
                        "userId": 1057,
                        "sex": 1,
                        "ting": 0,
                        "seatId": 1,
                        "coin": 703440,
                        "vipInfo": {
                            "vipExp": 0,
                            "vipLevel": {
                                "level": 0
                            }
                        }
                    },
                    {
                        "stat": "playing",
                        "name": "\\u53c1\\u5343\\u5757\\u4e0a\\u4f60",
                        "ip": "192.168.10.76",
                        "pic": "http://ddz.image.tuyoo.com/avatar/head_lotus.png",
                        "userId": 1145,
                        "sex": 1,
                        "ting": 0,
                        "seatId": 2,
                        "coin": 811200,
                        "vipInfo": {
                            "vipExp": 0,
                            "vipLevel": {
                                "level": 0
                            }
                        }
                    },
                    {
                        "stat": "playing",
                        "name": "\\u5c0fEVA",
                        "ip": "192.168.10.76",
                        "pic": "http://ddz.image.tuyoo.com/avatar/head_feimao.png",
                        "userId": 1107,
                        "sex": 0,
                        "ting": 0,
                        "seatId": 3,
                        "coin": 637250,
                        "vipInfo": {
                            "vipExp": 0,
                            "vipLevel": {
                                "level": 0
                            }
                        }
                    }
                ],
                "tableId": 750410010200,
                "big_degree_fee": [
                    30,
                    0.1,
                    200
                ]
            }
        }
        """
        ftlog.debug('MMsgLongNet.table_call_table_info actionId:', self.actionId)
        message = self.createMsgPackResult('table_info')
        message.setResult('action_id', self.actionId)
        message.setResult('maxSeatN', self.playerCount)
	message.setResult('header_seat_id', banker)
        message.setResult('bankerRemainCount', bankerRemainCount)
        message.setResult('room_level', self.roomConf.get('level', ''))
        message.setResult('room_coefficient', self.tableConf.get('room_coefficient', 1))
        message.setResult('no_drop_card_count', self.tableTileMgr.getTilesNoDropCount())
        message.setResult('base_chip', self.tableConf.get('base_chip', 0))
        message.setResult('reconnect', isReconnect)
        message.setResult('seatId', seatId)
        message.setResult('quan_men_feng', quanMenFeng)
        message.setResult('tableType', self.tableType)
        message.setResult('gameRule', self.roomConf.get('gameRule', ''))
        message.setResult('play_mode', self.playMode)
        message.setResult('room_name', self.roomConf.get('name', ''))
        message.setResult('current_player_seat_id', curSeat)
        message.setResult('min_coin', self.roomConf.get('minCoin', 0))
        message.setResult('play_timeout', -1)
        message.setResult('max_coin', self.roomConf.get("maxCoin", 0))
        message.setResult('table_state', tableState)
        message.setResult('big_degree_fee', self.tableConf.get('big_degree_fee', []))
        message.setResult('remained_count', len(self.tableTileMgr.tiles))
        message.setResult('magic_tiles', self.tableTileMgr.getMagicTile()) 
        message.setResult('laizi_tiles',{"tile":self.players[seatId].laizi,"factor":self.players[seatId].laiziPi})
        pigus = self.tableTileMgr.getPigus()
        if pigus:
            message.setResult('pigus', pigus)
            
        if cInfo:
            message.setResult('create_table_extend_info', cInfo)
        
        players = self.getPlayersInMsg(seatId, isReconnect)
        message.setResult('players', players)
        ftlog.debug('MMsgLongNet.table_call_table_info: ', message)
        
        if TYPlayer.isHuman(userId):
            message.setResult('userId', userId)
            send_msg(message, userId)
            self.addMsgRecord(message, userId)
        else:
            return
        
    def table_call_after_chi(self, lastSeatId, seatId, tile, pattern, timeOut, actionId, player, actionInfo = None,exInfo = None):
        """吃/碰后的广播
        1）吃
        {
            "cmd": "chi",
            "result": {
                "tile": 22,
                "pattern": [22, 23, 24],
                "seatId": 1,
                "player_seat_id": 0,
                "timeout": 12,
                "action_id": 17,
                "gameId": 7,
		"limitTiles":[22,25]
            }
        }
        
         {'ting_action_not_grab': [[1, [[1, 1, 2]]], [26, [[26, 1, 3], [29, 1, 4]]], [27, [[27, 1, 3]]], [28, [[25, 1, 3], [28, 1, 2]]]]}
         
        """
        ftlog.debug('MsgLongnet.table_call_after_chi playerChi:', seatId
                    , ' playerChied:', lastSeatId
                    , ' nowPlayerUserId:', player.curSeatId
                    , ' actionInfo:', actionInfo)
        
        message = self.createMsgPackResult('chi')
        message.setResult('tile', tile)
        message.setResult('pattern', pattern)
        message.setResult('seatId', seatId)
        message.setResult('player_seat_id', lastSeatId)
        message.setResult('timeout', timeOut)
        message.setResult('action_id', actionId)
        if player.curSeatId == seatId:
            message.setResult('limitTiles', player.limitTiles)
        hasAction = False
        if (player.curSeatId == seatId):
            if actionInfo.has_key('ting_action'):
                ting_action = actionInfo.get('ting_action', None)
                if ting_action:
                    message.setResult('grabTing', ting_action)
                    hasAction = True
            if actionInfo.has_key('gang_action'):
                gang_action = actionInfo.get('gang_action', None)
                if gang_action:
                    message.setResult('gang_action', gang_action)
                    hasAction = True

                fanpigu_action = actionInfo.get('fanpigu_action', None)
                if fanpigu_action:
                    message.setResult('fanpigu_action', fanpigu_action)
                    hasAction = True

            if actionInfo.has_key('tingliang_action'):
                tingliang_action = actionInfo.get('tingliang_action', None)
                if tingliang_action:
                    message.setResult('tingliang_action', tingliang_action)
                    hasAction = True

            if actionInfo.has_key('ting_action_not_grab'):
                # 和抢听不会并存
                ting_action = actionInfo.get('ting_action_not_grab', None)
                if ting_action:
		    handTiles = player.copyHandTiles()
		    jinkanResult,jinkanDrop = self.getJinKanDrop(tile,handTiles,ting_action)
                    if jinkanResult:
                        message.setResult('jinkanDrop', jinkanDrop)
                    kou_ting_action = actionInfo.get('kou_ting_action', None)
                    if kou_ting_action:
                        message.setResult('kou_ting_action', kou_ting_action)
                    else:
                        message.setResult('ting_action', ting_action)
                    hasAction = True

            # 吃牌后可以放锚
            mao_action = exInfo.getMaoResult(self.tableTileMgr, seatId)
            if mao_action:
                message.setResult('mao_action', mao_action)
                hasAction = True

        ftlog.debug('table_call_after_chi message:', message)
        send_msg(message, player.userId)
        self.addMsgRecord(message, player.userId)
        if hasAction:
            self.latestMsg[player.curSeatId] = message

    def table_call_after_peng(self, lastSeatId, seatId, tile, timeOut, actionId, player, pattern, actionInfo = None, exInfo = None):
        """吃/碰后的广播
        1）碰
        {
            "cmd": "peng",
            "result": {
                "tile": 19,
                "seatId": 1,
                "player_seat_id": 0,
                "timeout": 12,
                "action_id": 12,
                "gameId": 7,
		"limitTiles":[19]
            }
        }
        """
        ftlog.debug('MsgLongnet.table_call_after_peng')
        message = self.createMsgPackResult('peng')
        message.setResult('tile', tile)
        message.setResult('seatId', seatId)
        message.setResult('player_seat_id', lastSeatId)
        message.setResult('timeout', timeOut)
        message.setResult('action_id', actionId)
        if player.curSeatId == seatId:
            message.setResult('limitTiles', player.limitTiles) 
        if pattern is None:
            pattern = [tile, tile, tile]
        message.setResult('pattern', pattern)

        hasAction = False
        if (player.curSeatId == seatId):
            if actionInfo.has_key('ting_action'):
                ting_action = actionInfo.get('ting_action', None)
                if ting_action:
                    message.setResult('grabTing', ting_action)
                    hasAction = True
            if actionInfo.has_key('gang_action'):
                gang_action = actionInfo.get('gang_action', None)
                if gang_action:
                    message.setResult('gang_action', gang_action)
                    hasAction = True

                fanpigu_action = actionInfo.get('fanpigu_action', None)
                if fanpigu_action:
                    message.setResult('fanpigu_action', fanpigu_action)
                    hasAction = True

            if actionInfo.has_key('tingliang_action'):
                tingliang_action = actionInfo.get('tingliang_action', None)
                if tingliang_action:
                    message.setResult('tingliang_action', tingliang_action)
                    hasAction = True

            if actionInfo.has_key('ting_action_not_grab'):
                # 和抢听不会并存
                ting_action = actionInfo.get('ting_action_not_grab', None)
                if ting_action:
		    handTiles = player.copyHandTiles()
		    jinkanResult,jinkanDrop = self.getJinKanDrop(tile,handTiles,ting_action)
                    if jinkanResult:
                        message.setResult('jinkanDrop', jinkanDrop)
                    kou_ting_action = actionInfo.get('kou_ting_action', None)
                    if kou_ting_action:
                        message.setResult('kou_ting_action', kou_ting_action)
                    else:
                        message.setResult('ting_action', ting_action)
                    hasAction = True
        #群发消息 花分显示更新
        if actionInfo.has_key('flower_score'):
            # 更新花分
            flower_score = actionInfo.get('flower_score', None)
            message.setResult('flower_score', flower_score)

            # 碰牌后可以放锚
            mao_action = exInfo.getMaoResult(self.tableTileMgr, seatId)
            if mao_action:
                message.setResult('mao_action', mao_action)
                hasAction = True

        send_msg(message, player.userId)
        self.addMsgRecord(message, player.userId)
        if hasAction:
            self.latestMsg[player.curSeatId] = message

    def getJinKanDrop(self,tile,handTiles,ting_action):
        if MPlayMode().isSubPlayMode(self.tableTileMgr.playMode,MPlayMode.QUESHOU):
            jinkanDrop = []
            magicTile = self.tableTileMgr.getMagicTile()
            magicCount = MTile.getTileCount(magicTile,handTiles)
            if magicCount > 0:
                return False,[]
            if magicTile and (not magicTile in handTiles) and magicTile % 10 != 1 and magicTile % 10 != 9:
                for tingSolution in ting_action:
                    winNodes = tingSolution[1]
                    for winNode in winNodes:
                        if winNode[0] == magicTile:
                            patterns = winNode[3]
                            for pattern in patterns:
                                if magicTile in pattern:
                                    if len(pattern) == 3:
                                        if (pattern[0] == magicTile - 1) and (pattern[2] == magicTile + 1):
                                            jinkanDrop.append(tingSolution)
                                            break
                                        if magicTile % 10 == 3:
                                            if (pattern[0] == magicTile - 2) and (pattern[1] == magicTile - 1):
                                                jinkanDrop.append(tingSolution)
                                                break
                                        if magicTile % 10 == 7:
                                            if (pattern[2] == magicTile + 2) and (pattern[1] == magicTile + 1):
                                                jinkanDrop.append(tingSolution)
                                                break
                if len(jinkanDrop) > 0:
                    return True,jinkanDrop

        return False,[] 


    def table_call_after_gang(self, lastSeatId, seatId, tile, loser_seat_ids,loser_coins,real_win_coin,actionId, player, gang, exInfo = None,exInfo1=None):
        """杠牌广播消息
        {
            "cmd": "gang",
            "result": {
                "tile": 21,
                "pattern": [21, 21, 21, 21]
                "seatId": 3,
                "player_seat_id": 0,
                "loser_seat_ids": [
                    0
                ],
                "loser_coins":[
                    1
                ],
                "real_win_coin":1,
                "gameId": 7
            }
        }
        """
        message = self.createMsgPackResult('gang')
        message.setResult('tile', tile)
        message.setResult('gang', gang)
        message.setResult('seatId', seatId)
        message.setResult('player_seat_id', lastSeatId)
        message.setResult('action_id', actionId)
        message.setResult('loser_seat_ids', loser_seat_ids)

        message.setResult('loser_coins', loser_coins)
        message.setResult('real_win_coin', real_win_coin)

        if exInfo:
            choose = exInfo.getChoosedInfo(MTableState.TABLE_STATE_QIANGGANG)
            if choose:
                message.setResult("win_tile", choose['tile'])
                message.setResult('win_degree', 1)
            # 杠牌后可以放锚
            mao_action = exInfo.getMaoResult(self.tableTileMgr, seatId)
            if mao_action:
                message.setResult('mao_action', mao_action)


        #潜江晃晃朝天笑后可以听可以继续杠
        if exInfo1:
            gang_action=exInfo1.getChiPengGangResult(MTableState.TABLE_STATE_GANG)
            if gang_action:
                message.setResult("gang_action",gang_action)
            ting_action=exInfo1.getTingResult(self.tableTileMgr,seatId)
            if ting_action:
                message.setResult("ting_action",ting_action)
        send_msg(message, player.userId)
        if exInfo:
            # 抢杠和消息缓存
            self.latestMsg[player.curSeatId] = message
        self.addMsgRecord(message, player.userId)
        
    def table_call_after_extend_mao(self, lastSeatId, seatId, mao, actionId, player):
        message = self.createMsgPackResult('extend_mao')
        message.setResult('mao', mao)
        message.setResult('seatId', seatId)
        message.setResult('player_seat_id', lastSeatId)
        message.setResult('action_id', actionId)
        send_msg(message, player.userId)
        self.addMsgRecord(message, player.userId)
        
            
    def table_call_after_zhan(self, lastSeatId, seatId, tile, timeOut, actionId, player, pattern, actionInfo = None):
        """粘牌广播消息
        {
            "cmd": "zhan",
            "result": {
                "tile": 21,
                "pattern": [21, 21]
                "seatId": 3,
                "player_seat_id": 0,
                "gameId": 7
            }
        }
        """
        ftlog.debug('MsgLongnet.table_call_after_peng')
        message = self.createMsgPackResult('zhan')
        message.setResult('tile', tile)
        message.setResult('seatId', seatId)
        message.setResult('player_seat_id', lastSeatId)
        message.setResult('timeout', timeOut)
        message.setResult('action_id', actionId)
        if pattern is None:
            pattern = [tile, tile]
        message.setResult('pattern', pattern)
        if (player.curSeatId == seatId):
            if actionInfo.has_key('ting_action'):
                ting_action = actionInfo.get('ting_action', None)
                if ting_action:
                    message.setResult('grabTing', ting_action)
        send_msg(message, player.userId)
        self.addMsgRecord(message, player.userId)

    def table_call_after_ting(self, player, actionId, userId, allWinTiles, tingResult,jinkanDrop = []):
        """听牌消息"""
        isCurrentUser = False
        for userSeatId in range(self.playerCount):
            if self.players[userSeatId].userId == userId:
                if player.curSeatId == userSeatId:
                    isCurrentUser = True
                break
            
        message = self.createMsgPackResult('ting')
        message.setResult('gang_tiles', player.copyGangArray())
        message.setResult('peng_tiles', player.copyPengArray())
        message.setResult('chi_tiles', player.copyChiArray())
        message.setResult('kou_tiles', player.kouTiles)
        
        handTiles = player.copyHandTiles()
        if MPlayMode().isSubPlayMode(self.tableTileMgr.playMode,MPlayMode.LUOSIHU):
            if self.tableTileMgr.getTingLiangMode()==self.tableTileMgr.MODE_LIANG_TING:
                message.setResult('standup_tiles', player.tingLiangTilesCurrent)
            elif self.tableTileMgr.getTingLiangMode()==self.tableTileMgr.MODE_LIANG_HAND:
                message.setResult('standup_tiles', handTiles)
        else:
            if isCurrentUser:
                message.setResult('standup_tiles', handTiles)
            else:
                newHands = []
                for _ in range(len(handTiles) - len(player.tingLiangTilesCurrent)):
                    newHands.append(0)
                newHands.extend(player.tingLiangTilesCurrent)
                message.setResult('standup_tiles', newHands)
	if MPlayMode().isSubPlayMode(self.tableTileMgr.playMode,MPlayMode.QUESHOU):
	    message.setResult('jinkanDrop', jinkanDrop)         
        message.setResult('mao_tiles', player.copyMaoTile())
        message.setResult('all_win_tiles', allWinTiles)
        message.setResult('ting_result', tingResult)
        message.setResult('seatId', player.curSeatId)
        send_msg(message, userId)
        self.addMsgRecord(message, userId)

    def table_call_game_win_loose(self
            , uids
            , wins
            , looses
            , observers
            , winMode
            , tile
            , scores
            , scoreBase
            , fanPattern
            , customInfo = None
            , piaoPoints = None
            , flowerScores = None
            , displayExtends = None
    	    ,lastSeatId = -1
	    ,winFinal = 0
            ):
        """
        结算
        -1 点炮
        -2 不输不赢
        
        score - 当前积分
        total_score - 目前为止总的输赢积分
        delta_score - 当前局的输赢积分
        customInfo 包含之前的ctInfo btInfo lstInfo
        """
        totalScore = scores.get('totalScore')
        if not totalScore:
            totalScore = [0 for _ in range(self.playerCount)]
        deltaScore = scores.get('deltaScore')
        if not deltaScore:
            deltaScore = [0 for _ in range(self.playerCount)]
        deltaGangScore = scores.get('deltaGangScore')
        if not deltaGangScore:
            deltaGangScore = [0 for _ in range(self.playerCount)]
        deltaWinScore = scores.get('deltaWinScore')
        if not deltaWinScore:
            deltaWinScore = [0 for _ in range(self.playerCount)]

        if customInfo:
            ftlog.debug('msg_longnet.table_call_game_win_loose customInfo:', customInfo
                        , ' wins:', wins
                        , ' looses:', looses
                        , ' observers:', observers
                        , ' winMode:', winMode
                        , ' totalScore:', totalScore
                        , ' deltaGangScore:', deltaGangScore
                        , ' deltaWinScore:', deltaWinScore
                        )
        
        gameFlow = 0
        if len(wins) == 0:
            gameFlow = 1

        if winFinal :
            if self.playMode == 'luosihu-xuezhan' or self.playMode == 'luosihu-luosihu' or self.playMode =='luosihu-ctxuezhan':
                for player in self.players:
                    if player.curSeatId not in wins and player.isWon():
                        wins.append(player.curSeatId)

        if self.getWinPlayerCount() > 0:
            gameFlow = 0 	
	messageCount = 0
        messageEnd = False
	ftlog.debug('msg_longnet.table_call_game_win_loose gameflow 2',gameFlow,len(wins),len(looses), self.getWinPlayerCount())
        for winPlayer in wins:
            huCount = len(self.players[winPlayer].huTiles)
            if huCount > 0:
                tile = self.players[winPlayer].huTiles[huCount - 1]	
	    messageCount += 1
	    if messageCount >= self.playerCount:
                 messageEnd = True
            self.table_call_game_win(self.players[winPlayer]
                    , winMode[winPlayer]
                    , tile
                    , uids
                    , totalScore[winPlayer]
                    , deltaScore[winPlayer]
                    , deltaGangScore[winPlayer]
                    , deltaWinScore[winPlayer]
                    , scoreBase
                    , fanPattern[winPlayer]
                    , gameFlow
                    , customInfo
                    , piaoPoints
                    ,flowerScores
                    , displayExtends[winPlayer] if displayExtends else None
		    ,lastSeatId
		    ,messageEnd
		    ,self.players[winPlayer].xuezhanRank)
#modified by robin

        for loosePlayer in looses:
	    messageCount += 1
            if messageCount >= self.playerCount:
                 messageEnd = True 
            self.table_call_game_loose(self.players[loosePlayer]
                    , winMode[loosePlayer]
                    , uids
                    , totalScore[loosePlayer]
                    , deltaScore[loosePlayer]
                    , deltaGangScore[loosePlayer]
                    , deltaWinScore[loosePlayer]
                    , scoreBase
                    , fanPattern[loosePlayer]
                    , gameFlow
                    , customInfo
                    , piaoPoints
                    ,flowerScores
                    , displayExtends[loosePlayer] if displayExtends else None
	            ,lastSeatId
		    ,messageEnd)
        for ob in observers:
	    messageCount += 1
            if messageCount >= self.playerCount:
                 messageEnd = True 
            self.table_call_game_loose(self.players[ob]
                    , winMode[ob]
                    , uids
                    , totalScore[ob]
                    , deltaScore[ob]
                    , deltaGangScore[ob]
                    , deltaWinScore[ob]
                    , scoreBase
                    , fanPattern[ob]
                    , gameFlow
                    , customInfo
                    , piaoPoints
                    ,flowerScores
                    , displayExtends[ob] if displayExtends else None
		    ,lastSeatId
		    ,messageEnd)

    def table_call_game_win(self
                            , winPlayer
                            , winMode
                            , tile
                            , uids
                            , totalScore
                            , deltaScore
                            , gangScore
                            , winScore
                            , scoreBase
                            , fanPatternInfo
                            , gameFlow
                            , customInfo
                            , piaoPoints
                            , flowerScores
                            , displayExtend=None
			    ,lastSeatId = -1
			    ,messageEnd = False
			    ,huRank = 0):
        """
        注：给赢家发送和牌消息
        
        params：
        1）winType：0是自摸和，1是放炮和
        
        例子：
        {
        "cmd": "win",
        "result": {
            "gameId": 710,
            "roomId": 7105021001,
            "tableId": 71050210010199,
            "seatId": 2,
            "userId": 9597,
            "timestamp": 1479255694,
     
            //分数相关， 总分，这把的分变化，目前为止的分数变化
            "score": 4,
            "delta_score": 5,
            "total_delta_score": 5,
     
            //当前座位的玩家，宝牌信息[牌花，牌数]
            "baopai":[{
                "tile":1
            }],
            //结算界面不需要看，遗弃过的宝牌
             
            //胡牌的模式，cmd>=0 为自己胡
            "winMode": 1,
     
            //当前这把，是否是流局
            "gameFlow": 0,
            //番型 是个 二维数组 [番型名称，番数]
            "patternInfo": [],
            //自建桌信息 是个 对象
            create_table_extend_info : {
                //房间号
                "create_table_no":123456,
                //游戏时长
                "time":123123,
                //是否最后一把
                "create_final":0,
                //当前剩余房卡
                "create_now_cardcount":2,
                //起始时，使用房卡
                "create_total_cardcount":5
            },
            
            //牌面信息
            "tilesInfo": {
                "tiles": [
                    5,
                    5,
                    6,
                    6,
                    6,
                    22,
                    23,
                    18
                ],
                "chi": [
                    [
                        24,
                        25,
                        26
                    ]
                ],
                "peng": [],
                "gang": [
                    {
                        "pattern": [
                            5,
                            5,
                            5,
                            5
                        ],
                        "style": 0
                    }
                ],
                "tile": 18
            }
        }

        """
        message = self.createMsgPackResult('win')
        message.setResult('score', scoreBase + totalScore)
        ftlog.debug('msg_longnet.table_call_game_win scoreBase:', scoreBase,' totalScore:',totalScore)

        message.setResult('total_delta_score', totalScore)
        message.setResult('seatId', winPlayer.curSeatId)# 赢家座位号
        message.setResult('userId', winPlayer.userId)# 赢家userId
	message.setResult('player_seat_id', lastSeatId) #胡牌提供玩家
        isBanker = 1
        if customInfo:
            ftlog.debug('msg_longnet.table_call_game_win customInfo:', customInfo)
            if 'winNode' in customInfo:
                winNode = customInfo['winNode']
                ftlog.debug('msg_longnet.table_call_game_win winNode:', winNode)
                isBanker = winNode.get('isBanker', 1)
        ftlog.debug('msg_longnet.table_call_game_win isBanker:', isBanker)
        if isBanker:
            message.setResult('tile', tile)#和牌的牌
            
        message.setResult('timestamp', pktimestamp.getCurrentTimestamp())# 和牌时间戳
        #message.setResult('balance', 20000) #赢家金币总额
        #message.setResult('totalCharges', 1000) #该局赢家总钱数(赢了也可能输钱哦)
        message.setResult('gameFlow', gameFlow) #是否流局(1 流局, 0 不流局)
        #message.setResult('score',  4) #番数, 输了不需要番数
        message.setResult('winMode', winMode)  # 该局赢的类型，0是自摸，1是放炮 -1输了
	message.setResult('messageEnd', messageEnd)
        message.setResult('huRank', huRank)
        if self.tableConf.get(MTDefine.WINLOSE_WINMODE_DESC, 0):
            message.setResult('winModeDesc', self._getWinModeDesc(winMode))
        if customInfo.has_key('lianzhuangCount'):
            lianzhuangCount = customInfo.get('lianzhuangCount', None)
            message.setResult('lianzhuangCount', lianzhuangCount)  
	if customInfo.has_key('ctInfo'):
            ctInfo = customInfo.get('ctInfo', None)
            if ctInfo:
                message.setResult('create_table_extend_info', ctInfo)
	#modify by youjun 04.25
        if customInfo.has_key('loseFinal'):
            loseFinal = customInfo.get('loseFinal', None)
            ftlog.debug('loseFinal',loseFinal)
	    if loseFinal:
                message.setResult('loseFinal', loseFinal)
        if customInfo.has_key('winFinal'):
            winFinal = customInfo.get('winFinal', None)
	    ftlog.debug('winFinal:',winFinal)
            if winFinal:
              message.setResult('winFinal', winFinal)
        if customInfo.has_key('btInfo'):
            btInfo = customInfo.get('btInfo', None)
            if btInfo:
                message.setResult('baopai', btInfo)
        if customInfo.has_key('lstInfo'):
            lstInfo = customInfo.get('lstInfo', None)
            if lstInfo:
                message.setResult('lastSpeicalTilesInfo', lstInfo)
        if customInfo.has_key('awardInfo'):
            awardInfo = customInfo.get('awardInfo', None)
            if awardInfo:
                message.setResult('awardInfo', awardInfo)
        if piaoPoints:
            message.setResult('piaoPoints', piaoPoints['points'][winPlayer.curSeatId])
        if flowerScores:
            message.setResult('flowerScore', flowerScores['scores'][winPlayer.curSeatId])
        if customInfo.has_key('moziScores'):
            moziScores = customInfo.get('moziScores', None)
            if moziScores:
                message.setResult('moziScore', moziScores[winPlayer.curSeatId])

        #鸡西兑奖分数
        showDeltaScore = deltaScore
        awordTileScore = None
        if customInfo.has_key('awardScores'):
            awordTileScores = customInfo.get('awardScores', None)
            if awordTileScores:
                awordTileScore = awordTileScores[winPlayer.curSeatId]
                showDeltaScore -= awordTileScore
                    
        ftlog.debug('MsgLongnet.table_call_game_win deltaScore:',deltaScore,'showDeltaScore:',showDeltaScore, 'awordTileScore:',awordTileScore)
            
            
        #结算分数发在detail里面
        detailData = {
            "delta_score":showDeltaScore,
            "deltaGangScore":gangScore,
            "deltaWinScore": winScore,
            "total_delta_score":totalScore,
            "score":scoreBase + totalScore,
            "patterns":fanPatternInfo
        }
        if self.tableConf.get(MTDefine.WINLOSE_DISPLAY_EXTEND, 0):
            titlesConf = self.tableConf.get(MTDefine.DISPLAY_EXTEND_TITLES, [])
            if displayExtend is None:
                displayExtend = [0] * len(titlesConf)
            detailData['display_extend'] = {'titles': self.tableConf.get(MTDefine.DISPLAY_EXTEND_TITLES, []), 'details': displayExtend}

        if awordTileScore:
            detailData["awordTileScore"] = awordTileScore
            message.setResult('awordTileScore',awordTileScore)
            
        message.setResult('detail',detailData)
        message.setResult('delta_score', showDeltaScore)
        
        # 如果是曲靖的十风或者十三幺等特殊牌型,胡牌牌面显示打出的牌
        winHandTiles = winPlayer.copyHandTiles()
        if customInfo.has_key('dropTiles'):
            dropTiles = customInfo.get('dropTiles',None)
            if dropTiles:
                winHandTiles = dropTiles
        
        if isBanker and (len(winHandTiles) == 14) and (tile in winHandTiles):
            winHandTiles.remove(tile)
        # 手牌信息
	huTile = None
	if len(winPlayer.huTiles) > 0:
	    huTile = winPlayer.copyHuArray()[-1]
        tilesInfo = {
            "tiles": winHandTiles, #[1,2,3,4,5]
            "gang": winPlayer.copyGangArray(), #[[1,1,1,1],[9,9,9,9]] 明1&暗杠0, 花色
            "chi": winPlayer.copyChiArray(), #[[2,3,4]]代表吃(1,2,3),(5,6,7)
            "peng": winPlayer.copyPengArray(),#[1,2]代表吃(1,1,1),(2,2,2)
            "zhan": winPlayer.zhanTiles,
            "mao": winPlayer.copyMaoTile(),
            "tile": huTile
        }
        ftlog.debug('msg_longnet.table_call_game_win tilesInfo:', tilesInfo)
	#         
        #if isBanker:
        #    tilesInfo['tile'] = tile
	
        message.setResult('tilesInfo', tilesInfo)
        #番数信息 patternInfo = [ ["连六", "1番"], ["连六", "1番"] ]
        #message.setResult('patternInfo', fanPatternInfo) #流局没有番型数据, 输了不需要番型数据
        send_msg(message, uids)
        ftlog.debug('win message by youjun :',message)
	self.addMsgRecord(message, uids)

    def table_call_game_loose(self
                              , loosePlayer
                              , winMode
                              , uids
                              , totalScore
                              , deltaScore
                              , gangScore
                              , winScore
                              , scoreBase
                              , fanPattern
                              , gameFlow
                              , customInfo
                              , piaoPoints
                              , flowerScores
                              , displayExtend=None
			      ,lastSeatId = -1
			      ,messageEnd = False):
        '''
	失败消息
        {
            "cmd": "lose",
            "result": {
                "userId": 1008,
                "seatId": 1,
                "timestamp": 1473782986.013167,
                "gameFlow": true,
                "balance": 937780,
                "totalCharges": -27000,
                "continuous": 0,
                "score": 0,
                "masterPoint": 0,
                "basePoint": 0,
                "roomPoint": 0,
                "memberPoint": 0,
                "winMode": -1,
                "final": true,
                "tilesInfo": {
                    "tiles": [
                        5,
                        5,
                        22,
                        22,
                        22,
                        26,
                        26,
                        27,
                        28,
                        28
                    ],
                    "kong": [],
                    "chow": [
                        15
                    ],
                    "pong": [],
                    "tile": null
                },
                "patternInfo": [],
                "loserInfo": [],
                "gameId": 7,
                "moziScore": 100,  # 摸子分(和县)
            }
        }
	'''        
        message = self.createMsgPackResult('lose')
        message.setResult('score', scoreBase + totalScore)
        ftlog.debug('msg_longnet.table_call_game_loose scoreBase:', scoreBase,' totalScore:',totalScore)

        message.setResult('total_delta_score', totalScore)
        message.setResult('userId', loosePlayer.userId)
        message.setResult('seatId', loosePlayer.curSeatId)
	message.setResult('player_seat_id', lastSeatId) #胡牌提供玩家
        message.setResult('timestamp', pktimestamp.getCurrentTimestamp())
        message.setResult('gameFlow', gameFlow) #是否流局(1 流局, 0 不流局)
	message.setResult('messageEnd', messageEnd)
        message.setResult('winMode', winMode)
        if self.tableConf.get(MTDefine.WINLOSE_WINMODE_DESC, 0):
            message.setResult('winModeDesc', self._getWinModeDesc(winMode))
	if customInfo.has_key('lianzhuangCount'):
	    lianzhuangCount = customInfo.get('lianzhuangCount', None)
	    message.setResult('lianzhuangCount', lianzhuangCount)
        #鸡西兑奖分数
        showDeltaScore = deltaScore
        awordTileScore = None
        if customInfo.has_key('awardScores'):
            awordTileScores = customInfo.get('awardScores', None)
            if awordTileScores:
                awordTileScore = awordTileScores[loosePlayer.curSeatId]
                showDeltaScore -= awordTileScore
        ftlog.debug('MsgLongnet.table_call_game_loose deltaScore:',deltaScore,'showDeltaScore:',showDeltaScore, 'awordTileScore:',awordTileScore)
        
        detailData = {
            "delta_score":showDeltaScore,
            "deltaGangScore":gangScore,
            "deltaWinScore": winScore,
            "total_delta_score":totalScore,
            "score":scoreBase + totalScore,
            "patterns":fanPattern
        }
        if self.tableConf.get(MTDefine.WINLOSE_DISPLAY_EXTEND, 0):
            titlesConf = self.tableConf.get(MTDefine.DISPLAY_EXTEND_TITLES, [])
            if displayExtend is None:
                displayExtend = [0] * len(titlesConf)
            detailData['display_extend'] = {'titles': self.tableConf.get(MTDefine.DISPLAY_EXTEND_TITLES, []), 'details': displayExtend}
        if awordTileScore:
            detailData["awordTileScore"] = awordTileScore
            message.setResult('awordTileScore',awordTileScore)
        message.setResult('detail',detailData)
        message.setResult('delta_score', showDeltaScore)
        looseHandTiles = loosePlayer.copyHandTiles()
        if gameFlow and loosePlayer.curTile:
            looseHandTiles.remove(loosePlayer.curTile)
        isQiangjin = False
        if MPlayMode().isSubPlayMode(self.playMode, MPlayMode.QUESHOU) and not gameFlow and len(looseHandTiles) > 16:
            looseHandTiles.remove(loosePlayer.curTile)
            isQiangjin = True

        tilesInfo = {
                "tiles": looseHandTiles,
                "gang": loosePlayer.copyGangArray(), 
                "chi": loosePlayer.copyChiArray(), 
                "peng": loosePlayer.copyPengArray(), 
                "zhan": loosePlayer.zhanTiles, 
                "mao": loosePlayer.copyMaoTile()
                }
	ftlog.debug('MsgLongnet.table_call_game_loose looseHandTiles xxx')

        if len(loosePlayer.copyHuArray()) > 0:
            tilesInfo['tile'] = loosePlayer.copyHuArray()[-1]

        if MPlayMode().isSubPlayMode(self.playMode, MPlayMode.QUESHOU) and isQiangjin:
            tilesInfo['tile'] = loosePlayer.curTile

        if gameFlow and MPlayMode().isSubPlayMode(self.playMode, MPlayMode.QUESHOU):
            tilesInfo['tile'] = loosePlayer.curTile
	
        message.setResult('tilesInfo', tilesInfo)

        #message.setResult('patternInfo', fanPattern)

        if customInfo.has_key('ctInfo'):
            ctInfo = customInfo.get('ctInfo', None)
            if ctInfo:
                message.setResult('create_table_extend_info', ctInfo)
        if customInfo.has_key('loseFinal'):
            loseFinal = customInfo.get('loseFinal', None)
            if loseFinal:
                message.setResult('loseFinal', loseFinal)
        if customInfo.has_key('winFinal'):
            winFinal = customInfo.get('winFinal', None)
            if winFinal:
              message.setResult('winFinal', winFinal)
        if customInfo.has_key('btInfo'):
            btInfo = customInfo.get('btInfo', None)
            if btInfo:
                message.setResult('baopai', btInfo)
        if customInfo.has_key('lstInfo'):
            lstInfo = customInfo.get('lstInfo', None)
            if lstInfo:
                message.setResult('lastSpeicalTilesInfo', lstInfo)
        if customInfo.has_key('awardInfo'):
            awardInfo = customInfo.get('awardInfo', None)
            if awardInfo:
                message.setResult('awardInfo', awardInfo)
        if piaoPoints:
            message.setResult('piaoPoints', piaoPoints['points'][loosePlayer.curSeatId])
        if flowerScores:
            message.setResult('flowerScore', flowerScores['scores'][loosePlayer.curSeatId])
        if customInfo.has_key('moziScores'):
            moziScores = customInfo.get('moziScores', None)
            if moziScores:
                message.setResult('moziScore', moziScores[loosePlayer.curSeatId])

        uids = []
        for player in self.players:
            uids.append(player.userId)
        
        send_msg(message, uids)
	ftlog.debug('lose message by youjun :',message) 
        self.addMsgRecord(message, uids)
        
    def table_call_game_all_stat(self, terminate, extendBudgets, ctInfo):
        """
        {
        "cmd":"gaming_leave_display_budget",
        "result":
        {
            "create_table_extend_info":
            {
                "create_final":1,
                "create_table_no":"000936",
                "create_now_cardcount":1,
                "create_total_cardcount":2,
                "time":1478278335
            },
            "roomId":78131001,
            "terminate":0 
            "detail":
            [
                {
                    "sid":1,
                    "total_delta_score":-2,
                    "statistics":[
                        {"desc":"自摸","value":0},
                        {"desc":"点炮","value":1},
                        {"desc":"明杠","value":0},
                        {"desc":"暗杠","value":0}
                        {"desc":"最大番数","value":2}
                    ],
                    "head_mark":"dianpao_most"
                },
                {
                    "sid":0,
                    "total_delta_score":2,
                    "statistics":[
                        {"desc":"自摸","value":0},
                        {"desc":"点炮","value":0},
                        {"desc":"明杠","value":0},
                        {"desc":"暗杠","value":0},
                        {"desc":"最大番数","value":2}
                    ],"head_mark":""
                }
            ],
            "gameId":7
            "calcTime":2017-03-14 09:28
        }
        }
            
        """
        calcTime = time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time()))
        message = self.createMsgPackResult('gaming_leave_display_budget')
        message.setResult('create_table_extend_info', ctInfo)
        message.setResult('terminate', terminate)
        message.setResult('detail', extendBudgets)
        message.setResult('calcTime', calcTime)

        uids = []
        for player in self.players:
            uids.append(player.userId)
        ftlog.debug(message)
        send_msg(message, uids)
        self.addMsgRecord(message, uids)

    def getWinPlayerCount(self):
        count = 0
        for player in self.players:
            if player.isWon():
                count += 1
        return count    
    
    def table_leave(self, userId, seatId, uids):
        message = self.createMsgPackResult('leave')
        message.setResult('seatId', seatId)
        message.setResult('userId', userId)
        send_msg(message, uids)
        self.addMsgRecord(message, uids)
     
    def table_call_baopai(self, player, baopai, abandones):
        """通知宝牌
        
        实例：
        {
            "cmd": "baopai",
            "result": {
                "gameId": 7,
                "userId": 10788,
                "tableId": 750410010200,
                "seatId": 0,
                "roomId": 75041001,
                "baopai": [
                    [
                        9,    花色
                        2,    倍数
                        3     剩余张数
                    ]
                ]
            }
        }
        """
        message = self.createMsgPackResult('baopai')
        message.setResult('userId', player.userId)
        message.setResult('seatId', player.curSeatId)
        if baopai:
            message.setResult('baopai', baopai)
        if abandones:
            message.setResult('abandoned', abandones)
        
        ftlog.debug(message)
        send_msg(message, player.userId) 
        self.addMsgRecord(message, player.userId)

    def table_call_alarm(self, alarmId, player, isAlarm):
        """通知报警
        实例：
        {
            "cmd": "alarm_result",
            "result": {
                "gameId": 7,
                "userId": 10788,
                "tableId": 750410010200,
                "seatId": 0,
                "roomId": 75041001,
                "alarmId":1
                "isAlarm": 1
            }
        }
        """
        message = self.createMsgPackResult('alarm_result')
        message.setResult('userId', player.userId)
        message.setResult('seatId', player.curSeatId)
        message.setResult('alarmId', alarmId)
        if isAlarm:
            message.setResult('isAlarm', isAlarm)

        ftlog.debug(message)
        send_msg(message, player.userId)
        self.addMsgRecord(message, player.userId)

    def table_chat_broadcast(self, uid, gameId, voiceIdx, msg, users):
        """广播聊天"""
        mo = self.createMsgPackResult('table_chat')
        mo.setResult('userId', uid)
        mo.setResult('gameId', gameId)
        mo.setResult('isFace', 0)
        if voiceIdx != -1:
            mo.setResult('voiceIdx', voiceIdx)
        mo.setResult('msg', msg)
        router.sendToUsers(mo, users)
        
    def table_chat_to_face(self, uid, gameId, voiceIdx, msg, player):
        """定向发消息"""
        mo = self.createMsgPackResult('table_chat')
        mo.setResult('userId', uid)
        mo.setResult('gameId', gameId)
        mo.setResult('isFace', 1)
        if voiceIdx != -1:
            mo.setResult('voiceIdx', voiceIdx)
        mo.setResult('msg', msg)
        mo.setResult('userName', player.name)
        router.sendToUser(mo, player.userId)
        
    def create_table_succ_response(self, userId, seatId, action, tableHost, uids):
        """
        {
            "cmd": "create_table",
            "result": {
                "isTableHost": 1,
                "action": "ready",
                "seatId": 0,
                "gameId": 7
            }
        }
        """
        message = self.createMsgPackResult('create_table', action)
        message.setResult('isTableHost', tableHost)
        message.setResult('seatId', seatId)
        message.setResult('userId', userId)
        send_msg(message, uids)
        self.addMsgRecord(message, uids)
        
    def create_table_dissolve(self, userId, seatId, state, uids):
        """
        {
            "cmd": "create_table",
            "result": {
                "action": "leave",
                "seatId": 0,
                "state": "win",
                "gameId": 7
            }
        }
        """
        message = self.createMsgPackResult('create_table', 'leave')
        message.setResult('seatId', seatId)
        message.setResult('state', state)
        send_msg(message, uids)
        self.addMsgRecord(message, uids)
        
    def create_table_dissolve_vote(self, userId, seatId, seatNum, vote_info, vote_detail, vote_name, vote_timeOut, uids):
        message = self.createMsgPackResult('create_table_dissolution')
        message.setResult('seatId', seatId)
        message.setResult('userId', userId)
        message.setResult('seatNum', seatNum)
        message.setResult('vote_info', vote_info)
        message.setResult('vote_info_detail', vote_detail)
        message.setResult('name', vote_name)
        message.setResult('vote_cd', vote_timeOut)
        send_msg(message, uids)
        self.addMsgRecord(message, uids)
        
    # 兼容客户端投票窗口关闭的协议，之后要优化合并 add by taoxc  添加是否需要弹出大结算界面
    def create_table_dissolve_close_vote(self, userId, seatId, isShowBuget=False):
        message = self.createMsgPackResult('user_leave_vote')
        message.setResult('seatId', seatId)
        message.setResult('userId', userId)
        message.setResult('vote_info_detail', [])
        message.setResult('close_vote_cd', 2)
        message.setResult('close_vote', 1)
        message.setResult('show_budget', isShowBuget)
        send_msg(message, userId)
        self.addMsgRecord(message, userId)
        
    def table_call_fanpigu(self, pigus, uids):
        """发送翻屁股消息"""
        message = self.createMsgPackResult('fanpigu')
        message.setResult('pigus', pigus)
        send_msg(message, uids)
        self.addMsgRecord(message, uids)

    def table_call_buflower(self, tile, uids):
        """发送摸花牌消息"""
        message = self.createMsgPackResult('buflower')
        message.setResult('flower', tile)
        send_msg(message, uids)
        self.addMsgRecord(message, uids)

    def table_call_crapshoot(self,seatId, points, uids):
        """掷骰子通知"""
        message = self.createMsgPackResult('table_call', 'crapshoot')
        message.setResult('seatId', seatId) #谁掷骰子
        message.setResult('points', points) #点数
        send_msg(message, uids)
        self.addMsgRecord(message, uids)

    def table_call_score(self, uids, score, delta, jiaoScore=None):
        """牌桌积分变化"""
        message = self.createMsgPackResult('score')
        message.setResult('score', score)
        message.setResult('delta', delta)
        if jiaoScore:
            message.setResult('jiaoScore', jiaoScore)

        send_msg(message, uids)
        self.addMsgRecord(message, uids)
    
    def table_call_laizi(self, uids, magicTiles = [], magicFactors = []):
        """向所有人发送赖子"""    
        message = self.createMsgPackResult('show_laizi_tiles')
        message.setResult('dice_points', [])
        if magicTiles:
            message.setResult('table_laizi_tiles', magicTiles)
        if magicFactors:
            message.setResult('table_laizi_factors', magicFactors)
        send_msg(message, uids)
        self.addMsgRecord(message, uids)
        
    def quick_start_err(self, userId):
        messsage = self.createMsgPackResult('quick_start')
        messsage.setError(1, '对不起,该房间已满员')
        send_msg(messsage, userId)
        
    def removeTrustee(self, userId):
        """取消托管"""
        message = self.createMsgPackResult('remove_trustee')
        send_msg(message, userId)

    def table_call_ask_absence(self, userId, seatId):
        """通知前端开始定缺"""
	ftlog.debug('Mmsg table_call_ask_absence')
        message = self.createMsgPackResult('ask_absence')
        message.setResult('seatId', seatId)
	message.setResult('action','ask_absence')
        self.latestMsg[seatId] = message
        send_msg(message, userId)
        self.addMsgRecord(message, userId)

    def table_call_player_absence_end(self,userId,seatId):
        """单个玩家定缺结束"""
        message = self.createMsgPackResult('one_absence_end')
	message.setResult('action','one_absence_end')
        message.setResult('seatId', seatId)
        send_msg(message, userId)
        self.addMsgRecord(message, userId)

    def table_call_absence_end(self, userId, seatId, absenceInfo):
        """所有人定缺完毕"""
        message = self.createMsgPackResult('absence_end')
        #message.setResult('seatId', seatId)
	message.setResult('action','absence_end')
        message.setResult('seatId', seatId)
	message.setResult('info',absenceInfo)
        send_msg(message, userId)
        self.addMsgRecord(message, userId)

    def table_call_player_change3tiles_end(self,userId,seatId):
        """单个玩家换三张选定"""
        message = self.createMsgPackResult('table_call','one_change_3_tiles')
        message.setResult('seatId', seatId)
        self.latestMsg[seatId] = message
        send_msg(message, userId)
        self.addMsgRecord(message, userId)

    def table_call_tableInfo_broadcast(self, userIds,curCount,totalCount):
        """连庄后刷新局数"""
        currentProgress = '%s/%s局' % (curCount,totalCount)
        message = self.createMsgPackResult('currentProgress')
        message.setResult('currentProgress',currentProgress)
        message.setResult("create_now_cardcount",curCount)
        message.setResult("create_total_cardcount",totalCount)
        send_msg(message, userIds)
        self.addMsgRecord(message, userIds)

    def table_call_kaijin_broadcast(self,tile, userIds,tobanker = False,bankerSeatId = 0):
        ftlog.debug('table_call_kaijin_broadcast called')
        message = self.createMsgPackResult('kaijin')
	message.setResult('action','kaijin')
        message.setResult('tile', tile)
	message.setResult('banker', bankerSeatId)
	message.setResult('tobanker',tobanker)
        send_msg(message, userIds)
        self.addMsgRecord(message, userIds)

    def table_call_last_round_broadcast(self, userIds):
        """最后一次提示
        lastRount:
        {
            "cmd":"lastRount",
            "result":
            {
                "gameId":791,
                "roomId":7918011001,
                "tableId":79180110010200,
            }
        }
        """
        message = self.createMsgPackResult('lastRount')
        message.setResult('action','lastRount') 
	send_msg(message, userIds)
        self.addMsgRecord(message, userIds)

    def table_call_last_eight_broadcast(self, userIds):
        """最后8提示
        lastEight:
        {
            "cmd":"lastEight",
            "result":
            {
                "gameId":791,
                "roomId":7918011001,
                "tableId":79180110010200,
            }
        }
        """
        message = self.createMsgPackResult('lastEight')
	message.setResult('action','lastEight')
        send_msg(message, userIds)
        self.addMsgRecord(message, userIds) 

    def table_call_ask_change3tiles(self,userId,seatId):
        """提示前端换三张"""
        message = self.createMsgPackResult('table_call','change_3_tiles')
        message.setResult('seatId', seatId)
        self.latestMsg[seatId] = message
        send_msg(message, userId)
        self.addMsgRecord(message, userId)

    def table_call_send_3tiles(self,userId,seatId,threeTiles,standup_tiles,direction = 0):
        """下发换三张"""
        #cmds = {"cmd":"send_3tiles","result":{"gameId":7,"threeTiles":[26,25,28],"standup_tiles":[1,1,31,1,22,23,25,2,34,5,25,26,28],"absence":1,"action_id":1}};
        message = self.createMsgPackResult('table_call')
	message.setResult('action','send_3tiles')
        message.setResult('threeTiles',threeTiles)
        message.setResult('standup_tiles',standup_tiles)
        message.setResult('direction',direction)
        self.latestMsg[seatId] = message
        send_msg(message, userId)
        self.addMsgRecord(message, userId)

    def table_call_player_buFlower_start(self,userIds):
        """开始补花"""
        message = self.createMsgPackResult('buFlower_start')
        message.setResult('action','buFlower_start')
        send_msg(message, userIds)
        self.addMsgRecord(message, userIds)
	ftlog.debug('sendMsgInitTiles YYY')

    def table_call_lock_qiangjin(self,userId):
	message = self.createMsgPackResult('lock_qiangjin')
        message.setResult('action','lock_qiangjin')
        send_msg(message, userId)
        self.addMsgRecord(message, userId)  

    def table_call_unlock_qiangjin(self,userId):  
        message = self.createMsgPackResult('unlock_qiangjin')
        message.setResult('action','unlock_qiangjin')
        send_msg(message, userId)
        self.addMsgRecord(message, userId) 
 
    def table_call_player_buFlower_end(self,userIds):
        """结束补花"""
        message = self.createMsgPackResult('buFlower_end')
        message.setResult('action','buFlower_end')
        send_msg(message, userIds)
        self.addMsgRecord(message, userIds)


    def table_call_refresh_handtiles(self,userId,seatId,standup_tiles,tile):
        """玩家被抢杠胡后，移除被抢杠胡tile(刷新)，不然会多一张牌"""
        message = self.createMsgPackResult('table_call')
        message.setResult('action','refresh_handtiles')
        message.setResult('tile',tile)
        message.setResult('standup_tiles',standup_tiles)
        self.latestMsg[seatId] = message
        send_msg(message, userId)
        self.addMsgRecord(message, userId)

    def table_call_ask_piao(self, userId, seatId, piaoSolution, piaoTimeOut):
        message = self.createMsgPackResult('table_call', 'ask_piao')
        message.setResult('setting', piaoSolution)
        message.setResult('timeOut', piaoTimeOut)
        message.setResult('seatId', seatId)
        self.latestMsg[seatId] = message
        send_msg(message, userId)
        
    def table_call_accept_piao(self, userId, seatId, piaoSolution, piaoTimeOut):
        message = self.createMsgPackResult('table_call', 'accept_piao')
        message.setResult('solution', piaoSolution)
        message.setResult('timeOut', piaoTimeOut)
        message.setResult('seatId', seatId)
        self.latestMsg[seatId] = message
        send_msg(message, userId)
        
    def table_call_accepted_piao(self, userId, seatId, piaoSolution):
        message = self.createMsgPackResult('table_call', 'accepted_piao')
        message.setResult('solution', piaoSolution)
        message.setResult('seatId', seatId)
        self.latestMsg[seatId] = message
        send_msg(message, userId)
        
    def table_call_piao(self, userId, seatId, piao):
        message = self.createMsgPackResult('table_call', 'piao')
        message.setResult('piao', piao)
        message.setResult('seatId', seatId)
        send_msg(message, userId)
        
    def table_call_double_ask(self, uids, actionId, timeOut, doublePoints):
        message = self.createMsgPackResult('table_call', 'ask_double')
        message.setResult('timeOut', timeOut)
        message.setResult('action_id', actionId)
        message.setResult('double', doublePoints)
        send_msg(message, uids)
        
    def table_call_double_broadcast(self, uids, seatId, doubles):
        message = self.createMsgPackResult('table_call', 'double')
        message.setResult('seatId', seatId)
        message.setResult('double', doubles)
        send_msg(message, uids)

    def table_call_player_leave(self, userIds , online_info_list):
        '''
        长连接掉线了
        '''
        message = self.createMsgPackResult('user_online_info')
        message.setResult('online_info', online_info_list)
        send_msg(message, userIds)
        
    def table_call_ping(self, userIds , net_state, time):
        message = self.createMsgPackResult('table_call')
        message.setResult('action', 'ping')
        message.setResult('net_state', net_state)
        message.setResult('time', time)
        send_msg(message, userIds)

    def table_call_first_bu_flower_broadcast(self, seatId, flower_action, flowerTiles,flowerScore, userId,flower_round = 1,isSelf = False):
        message = self.createMsgPackResult('reissue_flowers')
        message.setResult('seatId', seatId)
        message.setResult('change_tiles', flower_action)
        message.setResult('flower_tiles', flowerTiles)
	message.setResult('flower_round',flower_round)
	message.setResult('flower_self',isSelf)
	message.setResult('flower_score', flowerScore)
	message.setResult('remained_count', self.tableTileMgr.getTilesLeftCount())
	self.latestMsg[seatId] = message
        send_msg(message, userId)
        self.addMsgRecord(message, userId)


    def table_call_bu_flower_broadcast(self, seatId, tile, flowerTiles,flowerScore, userIds):
        message = self.createMsgPackResult('bu_flower')
        message.setResult('seatId', seatId)
        message.setResult('tile', tile)
        message.setResult('flower_tiles', flowerTiles)
        message.setResult('flower_score', flowerScore)
        send_msg(message, userIds)
        self.addMsgRecord(message, userIds)

    def table_call_seen_tiles_broadcast(self,userIds):
        """
            {
                "cmd":"seen_tiles",
                "result":{
                    "detail":[
                        {"userId":10007,"seatId":0,"tiles":[1,3,3,6,9,11,17,18,21,23,25,26,36]},
                        {"userId":10002,"seatId":1,"tiles":[2,5,8,13,13,14,24,25,27,28,28,29,35]},
                        {"userId":10029,"seatId":2,"tiles":[37,37,29,25,23,21,16,11,9,9,8,7,6]},
                        {"userId":10004,"seatId":3,"tiles":[1,4,4,11,14,15,18,27,28,35,36,36,37]}
                    ],
                    "record_uid_list":[10007,10002,10029,10004],
                    "gameId":790
                }
            }

        """
        message = self.createMsgPackResult('seen_tiles')
        detail = []
        for player in self.players:
            tilesInfo = {}
            tilesInfo['userId'] = player.userId
            tilesInfo['seatId'] = player.curSeatId
            tilesInfo['tiles'] = player.copyHandTiles()
            detail.append(tilesInfo)
        message.setResult('detail', detail)
        send_msg(message, userIds)
        self.addMsgRecord(message, userIds)

    def saveRecord(self, recordName):
        """保存牌局记录"""
        trConfig = majiang_conf.getTableRecordConfig()
        uploadKey = trConfig.get('trUploadKey', '')
        uploadUrls = trConfig.get('trUploadUrls', [])
        if len(uploadUrls) == 0:
            return

        uploadUrl = random.choice(uploadUrls)
        uploadPath = trConfig.get('trFilePath', 'cdn37/majiang2/difang/')
        recordString = json.dumps(self.msgRecords)
        cdn = trConfig.get('trDownloadPath', 'http://ddz.dl.tuyoo.com/')
        cdn = cdn + uploadPath + recordName
        self.reset()
	ftlog.info('Mmsg_longnet saveRecord cdn', cdn, recordName)    	
   	ftlog.info('runupload uploadUrl=', uploadUrl, ' uploadKey=', uploadKey,' recordName',recordName,' recordString',recordString) 
        def runUpload():
            #ftlog.debug('runupload uploadUrl=', uploadUrl, ' uploadKey=', uploadKey,' recordName',recordName,' recordString',recordString)
            ec, info = uploader.uploadVideo(uploadUrl, uploadKey, uploadPath + recordName, recordString)
            #ftlog.debug('runupload ec=', ec, 'info=', info)
            #if ec == 0:
            #    ftlog.info('Majiang2.saveRecord ok, recordName:', recordName, ' CDNPath:', cdn)
            #else:
            #    ftlog.error('Majiang2.saveRecord error, code:', ec, ' info:', info)
                
        argd = {'handler':runUpload}
        FTTasklet.create([], argd)
        return cdn
    
    def send_message(self, message, uidList):
        """发送消息"""
        if not message:
            return
        send_msg(message, uidList)

    def _getWinModeDesc(self, winMode):
        """根据winMode获取winMode描述"""
        if winMode == MOneResult.WIN_MODE_DIANPAO_BAOZHUANG:
            return "点炮包庄"
        elif winMode == MOneResult.WIN_MODE_LOSS:  # 输
            return ""
        elif winMode == MOneResult.WIN_MODE_DIANPAO:  # 点炮输
            return "点炮"
        elif winMode == MOneResult.WIN_MODE_ZIMO:  # 自摸胡
            return '自摸'
        elif winMode == MOneResult.WIN_MODE_PINGHU:  # 点炮胡
            return '胡'
        elif winMode == MOneResult.WIN_MODE_GANGKAI:
            return '杠开'
        elif winMode == MOneResult.WIN_MODE_QIANGGANGHU:
            return '抢杠'
        return ''

def send_msg(msg, uidList):
    '''向客户端发消息'''
    if not isinstance(uidList, list):
        uidList = [uidList]
        
    newList = []
    for uid in uidList:
        if TYPlayer.isHuman(uid):
            newList.append(uid)
            
    router.sendToUsers(msg, uidList)
