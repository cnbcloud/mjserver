# -*- coding=utf-8
'''
Created on 2016年9月23日
下行消息通知

@author: zhaol
'''
import json
from freetime.util import log as ftlog

class MMsg(object):
    
    def __init__(self):
        super(MMsg, self).__init__()
        self.__tableId = 0
        self.__roomId = 0
        self.__players = []
        self.__playMode = ''
        self.__tableTye = ''
        self.__gameId = 0
        self.__playerCount = 0
        self.__roomConf = {}
        self.__tableConf = {}
        self.__table_tile_mgr = None
        self.__latest_msgs = None
        self.__action_id = 0
        self.__msg_records = []
        self.__auto_win = False
        self.__tian_ting = False

    @property
    def autoWin(self):
        return self.__auto_win

    def setAutoWin(self, autoWin):
        self.__auto_win = autoWin

    @property
    def tianTing(self):
        return self.__tian_ting

    def setTianTing(self, tianTing):
        self.__tian_ting = tianTing

    def saveRecord(self, recordName):
        pass
        
    def reset(self):
        """重置消息模块"""
        self.__action_id = 0
        self.__latest_msgs = [None for _ in range(self.playerCount)]
        self.__msg_records = []
        self.__tian_ting = False
    	ftlog.info('MMsg.resetActionId now:', self.__action_id)     
    @property
    def actionId(self):
        return self.__action_id
    
    def setActionId(self, actionId):
        ftlog.info('MMsg.setActionId now:', self.__action_id
                   , ' actionId:', actionId)
        self.__action_id = actionId
        
    @property
    def msgRecords(self):
        return self.__msg_records
    
    def addMsgRecord(self, message, uidList):
        ftlog.info('addMsgRecord message:', message, 'toUidList:', uidList)
        mStr = message.pack()
        mObj = json.loads(mStr)
        if not isinstance(uidList, list):
            uidList = [uidList]
        mObj['record_uid_list'] = uidList
        mObj['isTableRecord'] = True
        self.__msg_records.append(mObj)
        
    @property
    def latestMsg(self):
        """玩家最新的消息"""
        return self.__latest_msgs
    
    def table_call_latest_msg(self, seatId):
        """补发最新的消息"""
        pass
        
    @property
    def tableTileMgr(self):
        return self.__table_tile_mgr
    
    def setTableTileMgr(self, tableTileMgr):
        """设置牌桌手牌管理器"""
        self.__table_tile_mgr = tableTileMgr
        
    @property
    def roomConf(self):
        """房间配置"""
        return self.__roomConf
    
    @property
    def tableConf(self):
        """牌桌配置"""
        return self.__tableConf
        
    @property
    def playerCount(self):
        return self.__playerCount
    
    @property
    def playMode(self):
        return self.__playMode
    
    @property
    def tableType(self):
        return self.__tableTye    
    
    @property
    def tableId(self):
        return self.__tableId
    
    @property
    def roomId(self):
        return self.__roomId
    
    @property
    def gameId(self):
        return self.__gameId
    
    @property
    def players(self):
        return self.__players
    
    def setPlayers(self, players):
        """设置玩家"""
        ftlog.debug('msg.setPlayers:', self.players)
        self.__players = players
        
    def setInfo(self, gameId, roomId, tableId, playMode, tableType, playerCount):
        """设置三个公共信息"""
        ftlog.debug('[msg] gameId:', gameId
                    , ' roomId:', roomId
                    , ' tableId:', tableId
                    , ' playMode:', playMode
                    , ' tableType:', tableType
                    , ' playerCount:', playerCount)
        
        self.__gameId = gameId
        self.__roomId = roomId
        self.__tableId = tableId
        self.__playMode = playMode
        self.__tableTye = tableType
        self.__playerCount = playerCount
        self.__latest_msgs = [None for _ in range(playerCount)]
        
    def setRoomInfo(self, roomConf, tableConf):
        """设置房间配置"""
        self.__roomConf = roomConf
        self.__tableConf = tableConf
        
    def setTableId(self, tableId):
        """设置tableId
        """
        self.__tableId = tableId
        
    def setRoomId(self, roomId):
        """设置roomId
        """
        self.__roomId = roomId
        
    def table_call_add_card(self, player, tile, state, seatId, timeOut, actionId, extendInfo, recordUserIds):
        """通知庄家游戏开始
        """
        pass
    
    def table_call_ask_ting(self, seatId, actionId, winNodes, tingAction, timeOut):
        """询问玩家是否听牌
        """
        pass

    def table_call_tian_ting_over(self, seatId, actionId):
        """通知庄家可以出牌
        """
        pass

    def table_call_add_card_broadcast(self, seatId, timeOut, actionId, userId, tile,showTile = False):
        """通知其他人游戏开始
        """
        pass
    
    def table_call_fang_mao(self
                             , player
                             , mao
                             , maos
                             , state
                             , seatId
                             , timeOut
                             , actionID
                             , extend):
        pass
    
    def table_call_fang_mao_broadcast(self
                        , seatId
                        , timeOut
                        , actionID
                        , userId
                        , maos
                        , mao):
        pass
        
    def table_call_drop(self, seatId, player, tile, state, extendInfo, actionId, timeOut, winTiles=None):
        """通知玩家出牌
        参数：
            player - 做出牌操作的玩家
            winTiles - 可能胡哪些牌，某些玩法没有听牌功能，但也要每次提示玩家可胡哪些牌
        """
        return None
    
    def table_call_after_chi(self, lastSeatId, seatId, tile, pattern, timeOut, actionId, player, actionInfo = None , exInfo = None):
        """吃牌广播"""
        pass
    
    def table_call_after_peng(self, lastSeatId, seatId, tile, timeOut, actionId, player, pengPattern, actionInfo = None, exInfo = None):
        """碰牌广播"""
        pass
    
    def table_call_after_gang(self, lastSeatId, seatId, tile, loser_seat_ids, actionId, player, gang, exInfo = None):
        """杠牌广播"""
        pass
    
    def table_call_after_extend_mao(self, lastSeatId, seatId, mao, actionId, player):
        """补锚/补蛋广播"""
        pass
    
    def table_call_after_zhan(self, lastSeatId, seatId, tile, timeOut, actionId, player, pattern, actionInfo = None):
        """粘牌广播"""
        pass
    
    def sendMsgInitTils(self, tiles, banker, userId, seatId,second = False):
        """发牌"""
        pass
    
    def table_call_table_info(self
                , userId
                , banker
                , seatId
                , isReconnect
                , quanMenFeng
                , curSeat
                , tableState
                , cInfo = None
                , btInfo = None
		,bankerRemainCount = 0):
        """发送table_info"""
        pass
    
    def table_call_after_ting(self, player, actionId, userId, allWinTiles, tingResult):
        """听牌消息"""
        pass
    
    def table_call_grab_ting(self):
        pass
    
    def table_call_baopai(self, player, baopai, abandones):
        """宝牌通知"""
        pass
    
    def table_call_fanpigu(self, pigus, uids):
        """翻屁股通知"""
        pass

    def table_call_addflower(self, tile, uids):
        """摸到花牌通知"""
        pass

    def table_call_crapshoot(self,seatId, points, uids):
        """掷骰子通知"""
        pass

    def table_call_score(self, players, score, delta, jiaoScore=None):
        """牌桌积分变化"""
        pass
    
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
            , piaoPoints=None
            ,flowerScores = None
            , displayExtends=None):
        """结算"""
        pass
    
    def table_call_game_all_stat(self, terminate, extendBudgets, ctInfo):
        """牌桌结束大结算"""
        pass
    
    def table_call_laizi(self, uids, magicTiles = [], magicFactors = []):
        """下发赖子"""
        pass
    
    def table_call_ask_piao(self, userId, seatId, piaoSolution, piaoTimeOut):
        pass
    
    def table_call_accept_piao(self, userId, seatId, piaoSolution, piaoTimeOut):
        pass
    
    def table_call_accepted_piao(self, userId, seatId, piaoSolution):
        pass
    
    def table_call_piao(self, userId, seatId, piao):
        pass

    def table_call_seen_tiles_broadcast(self,userIds):
	pass

    def table_call_ask_absence(self, userId, seatId):
        """提示前端定缺"""
        pass

    def table_call_player_absence_end(self,userId,seatId):
        pass

    def table_call_absence_end(self, userId, seatId, absenceInfo):
        """所有人定缺完毕"""
        pass

    def table_call_ask_change3tiles(self,userId,seatId):
        """提示前端换三张"""
        pass

    def table_call_player_change3tiles_end(self,userId,seatId):
        pass

    def table_call_Qiangjin(self, player, state, actionId, timeOut,isTianHu = False,isSanJinDao = False):
	pass

    def table_call_player_buFlower_start(self,userIds):
	pass

    def table_call_player_buFlower_end(self,userIds):
        pass 

    def table_call_send_3tiles(self,userId,seatId,threeTiles,standup_tiles,direction = 0):
        """换三张结束"""
        pass

    def table_call_double_broadcast(self, uids, seatid, doubles):
        pass
    
    def table_call_double_ask(self, uids, actionId, timeOut, doublePoints=[]):
        pass

    def send_message(self, message, uidList):
        """发送消息"""
        pass
