# -*- coding=utf-8
'''
Created on 2016年9月23日

@author: zhaol
'''
from majiang2.table_state_processor.processor import MProcessor
from freetime.util import log as ftlog
from majiang2.table_state.state import MTableState
from majiang2.table.table_config_define import MTDefine

"""
在游戏开打之前听牌的处理器
对多个人
"""
class MTianTingProcessor(MProcessor):
    def __init__(self, count):
        super(MTianTingProcessor, self).__init__()
        self.__states = [MTableState.TABLE_STATE_NEXT for _ in range(count)]
        self.__seatIds = [-1 for _ in range(count)]
        self.__win_nodes = [[] for _ in range(count)]
        self.__count = count
        self.__tianting = False
        
    def reset(self):
        """重置数据"""
        self.__states = [MTableState.TABLE_STATE_NEXT for _ in range(self.__count)]
        self.__seatIds = [-1 for _ in range(self.__count)]
        self.__win_nodes = [[] for _ in range(self.__count)]
        self.__tianting = False

    @property
    def winNodes(self):
        """扩展信息"""
        return self.__win_nodes
    
    def setWinNodes(self, winNodes, seatId):
        self.__win_nodes[seatId] = winNodes

    @property
    def tianTing(self):
        """扩展信息"""
        return self.__tianting

    def setTianTing(self, tianting):
        self.__tianting = tianting
    
    @property
    def states(self):
        """获取本轮出牌状态"""
        return self.__states
    
    def setStates(self, state, seatId):
        ftlog.debug('[MTianTingProcessor]  setState:', state)
        self.__states[seatId] = state
        
    def getState(self):
        for state in self.states:
            if state != MTableState.TABLE_STATE_NEXT:
                ftlog.debug('[MTianTingProcessor] .getState return:', self.states)
                return state
        # 天听结束
        self.setTianTing(False)
        return MTableState.TABLE_STATE_NEXT
    
    @property
    def seatIds(self):
        """获取座位号
        """
        return self.__seatIds
    
    def setSeatIds(self, seatId):
        self.__seatIds[seatId] = seatId
        
    def getWinTiles(self, seatId):
        if self.states[seatId] == MTableState.TABLE_STATE_NEXT:
            return []
        # [{'winNodes': [{'winTile': 11, 'winTileCount': 1, 'pattern': [[1, 2, 3], [19, 19, 19], [11, 11], [22, 23, 24], [21, 21, 21]]}]}]
        wins = []
        winNodes = self.winNodes[seatId][0]['winNodes']
        ftlog.debug('[MTianTingProcessor] .getWinTiles winNodes:', winNodes)
        for winNode in winNodes:
            wins.append(winNode['winTile'])
        return wins
    
    def initProcessor(self, state, seatId, winNodes, timeOut = 9):
        """
        初始化处理器
        参数
            state - 状态集合，当前座位号可以做出的全部选择
        """
        ftlog.debug('[MTianTingProcessor] .initProcessor state:', state
                , ' seatId:', seatId
                , ' winNodes:', winNodes)
        self.setStates(state, seatId)
        self.setSeatIds(seatId)
        self.setWinNodes(winNodes, seatId)
        self.setTimeOut(timeOut)

        if state & MTableState.TABLE_STATE_TING:
            # 天听阶段
            self.setTianTing(True)

    def hasAutoDecideAction(self, curSeat, trustTeeSet):
        """是否有托管可以处理的行为"""
        if self.states[curSeat] == MTableState.TABLE_STATE_NEXT:
            return MTDefine.INVALID_SEAT

        ftlog.debug('[MTianTingProcessor] .hasAutoDecideAction userId:', self.players[curSeat].userId)
        if self.players[curSeat].userId < 10000:
            ftlog.debug('[MTianTingProcessor] .isUserAutoDecided robot:', self.players[curSeat].userId)
            return self.seatIds[curSeat]
            
        return MTDefine.INVALID_SEAT
    
    def updateProcessor(self, seatId):
        """
        用户做出了选择
        只有出牌一个解的时候，不能放弃，一定要出牌
        参数
            state - 最终做出的选择
        返回值：
            True - 动作有效
            False - 动作无效
        """
        ftlog.debug('[MTianTingProcessor] .updateProcessor seatId:', seatId
                    , ' seatIds:', self.seatIds
                    , ' states:', self.states)

        if seatId not in self.seatIds:
            return False

        if self.states[seatId] == MTableState.TABLE_STATE_NEXT:
            return False
        self.setStates(MTableState.TABLE_STATE_NEXT, seatId)
        return True

    def handlePlayerReconnect(self, userId, seatId, bankerId, actionID):
        """处理玩家的断线重连
        """
        ftlog.debug('[MTianTingProcessor] .handlePlayerReconnect userId:', userId, 'seatId:', seatId ,'bankerId:', bankerId)
        if not self.msgProcessor:
            return

        if self.msgProcessor.tianTing and not self.tianTing and seatId == bankerId:
            # 特殊情况 闲家天听状态已过 庄家点击了听或过之后 断线重连走这 这时需要重新更新庄家天听状态
            self.initProcessor(MTableState.TABLE_STATE_TING,
                                                 bankerId, [], 9)

        if self.tianTing and seatId != bankerId:
            # 闲家还没选天听，通知其选择
            ftlog.debug('[MTianTingProcessor] .handlePlayerReconnect state:', self.states)
            if self.states[seatId] & MTableState.TABLE_STATE_TING:
                winTiles = self.getWinTiles(seatId)
                ftlog.debug('[MTianTingProcessor] .handlePlayerReconnect winTiles:', winTiles)
                self.msgProcessor.table_call_ask_ting(seatId, actionID, winTiles, [], 9)