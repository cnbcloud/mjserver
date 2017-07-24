# -*- coding=utf-8
'''
Created on 2016年9月23日

@author: zhaol
'''
from majiang2.table_state_processor.processor import MProcessor
from freetime.util import log as ftlog
from majiang2.table_state.state import MTableState
from majiang2.table.table_config_define import MTDefine
from majiang2.ai.ting import MTing

"""
在摸牌之前听牌的处理器
对一个人
"""
class MTingBeforeAddCardProcessor(MProcessor):
    def __init__(self):
        super(MTingBeforeAddCardProcessor, self).__init__()
        self.__state = MTableState.TABLE_STATE_NEXT
        self.__seatId = 0
        self.__win_nodes = None
        
    def reset(self):
        """重置数据"""
        self.__state = MTableState.TABLE_STATE_NEXT
        self.__seatId = 0
        self.__win_nodes = None

    @property
    def winNodes(self):
        """扩展信息"""
        return self.__win_nodes
    
    def setWinNodes(self, winNodes):
        self.__win_nodes = winNodes
    
    @property
    def state(self):
        """获取本轮出牌状态"""
        return self.__state
    
    def setState(self, state):
        ftlog.debug('MTingBeforeAddCardProcessor setState:', state)
        self.__state = state
        
    def getState(self):
        if self.state != MTableState.TABLE_STATE_NEXT:
            ftlog.debug('MTingBeforeAddCardProcessor.getState return:', self.state)
        return self.__state
    
    @property
    def seatId(self):
        """获取座位号
        """
        return self.__seatId
    
    def setSeatId(self, seatId):
        self.__seatId = seatId
        
    def getWinTiles(self):
        if self.state == MTableState.TABLE_STATE_NEXT:
            return []
        # [{'winNodes': [{'winTile': 11, 'winTileCount': 1, 'pattern': [[1, 2, 3], [19, 19, 19], [11, 11], [22, 23, 24], [21, 21, 21]]}]}]
        wins = []
        winNodes = self.winNodes[0]['winNodes']
        ftlog.debug('MTingBeforeAddCardProcessor.getWinTiles winNodes:', winNodes)
        for winNode in winNodes:
            wins.append(winNode['winTile'])
        return wins
    
    def initProcessor(self, actionID, state, seatId, winNodes, timeOut = 9):
        """
        初始化处理器
        参数
            state - 状态集合，当前座位号可以做出的全部选择
        """
        ftlog.debug('MTingBeforeAddCardProcessor.initProcessor actionID', actionID
                , ' state:', state
                , ' seatId:', seatId
                , ' winNodes:', winNodes)
        self.setActionID(actionID)
        self.setState(state)
        self.setSeatId(seatId)
        self.setWinNodes(winNodes)
        self.setTimeOut(timeOut)
        
    def hasAutoDecideAction(self, curSeat, trustTeeSet):
        """是否有托管可以处理的行为"""
        if self.state == MTableState.TABLE_STATE_NEXT:
            return MTDefine.INVALID_SEAT
        
        ftlog.debug('MTingBeforeAddCardProcessor.hasAutoDecideAction userId:', self.players[self.seatId].userId)
        if self.players[self.seatId].userId < 10000:
            ftlog.debug('MTingBeforeAddCardProcessor.isUserAutoDecided robot:', self.players[self.seatId].userId)
            return self.seatId
            
        return MTDefine.INVALID_SEAT
    
    def updateProcessor(self, actionID, state, seatId):
        """
        用户做出了选择
        只有出牌一个解的时候，不能放弃，一定要出牌
        参数
            state - 最终做出的选择
        返回值：
            True - 动作有效
            False - 动作无效
        """
        ftlog.debug('actionID self.actionID =====',actionID ,self.actionID)
        if actionID != self.actionID:
            ftlog.debug('MAddCardProcessor.updateProcessor actionId error...')
            return False
        
        if seatId != self.__seatId:
            return False
        
        ftlog.debug('MTingBeforeAddCardProcessor.updateProcessor actionId:', actionID
                    , ' state:', state
                    , ' seatId:', seatId)
        self.setState(MTableState.TABLE_STATE_NEXT)
        return True
            