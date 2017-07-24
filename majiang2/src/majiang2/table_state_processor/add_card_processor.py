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
加牌的操作处理，最对一个人
分析
1）摸牌，会有杠/胡两种情况
2）吃/碰一张牌，之后主动出一张牌
3）杠牌后，发一张牌，之后主动出一张牌
"""
class MAddCardProcessor(MProcessor):
    def __init__(self):
        super(MAddCardProcessor, self).__init__()
        self.__tile = 0
        self.__state = MTableState.TABLE_STATE_NEXT
        self.__seatId = 0
        self.__extend_info = None
        self.__must_ting = False
        
    @property
    def extendInfo(self):
        """扩展信息"""
        return self.__extend_info
    
    @property
    def state(self):
        """获取本轮出牌状态"""
        return self.__state
    
    def getState(self):
        return self.__state
    
    def getTile(self):
        """获取手牌
        """
        return self.__tile
    
    @property
    def seatId(self):
        """获取座位号
        """
        return self.__seatId
    
    def getSeatId(self):
        return self.__seatId
    
    def getPlayer(self):
        """获取玩家"""
        return self.players[self.__seatId]
    
    @property
    def mustTing(self):
        return self.__must_ting
    
    def setMustTing(self, mustTing):
        self.__must_ting = mustTing
        
    def reset(self):
        """重置数据"""
        self.__tile = 0
        self.__state = MTableState.TABLE_STATE_NEXT
        self.__seatId = 0
        self.__extend_info = None
        self.__must_ting = False
        
    def initProcessor(self, actionID, state, seatId, tile, extendInfo, timeOut = 9):
        """
        初始化处理器
        参数
            state - 状态集合，当前座位号可以做出的全部选择
        """
        ftlog.debug('MAddCardProcessor.initProcessor actionID', actionID
                , ' state:', state
                , 'seatId:', seatId
                , ' tile:', tile
                , ' extendInfo:', extendInfo)
        self.setActionID(actionID)
        self.__state = state
        self.__seatId = seatId
        self.__tile = tile
        self.__extend_info = extendInfo
        self.setTimeOut(timeOut)
        
    def hasAutoDecideAction(self, curSeat, trustTeeSet):
        """是否有托管可以处理的行为"""
        if self.__state == MTableState.TABLE_STATE_NEXT:
            return MTDefine.INVALID_SEAT
        
        if self.isUserAutoDecided(self.seatId, trustTeeSet, self.state):
            return self.__seatId
            
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
        if actionID != self.actionID:
            ftlog.debug('MAddCardProcessor.updateProcessor actionId error...')
            return False
        
        if seatId != self.__seatId:
            return False
        
        if self.players[seatId].isTing() and (self.__state & MTableState.TABLE_STATE_HU):
            # 听牌状态，过胡，充值processor，后台自动替玩家打出当前的牌
            self.reset()
            return True

        if not (state & self.__state):
            ftlog.debug('MAddCardProcessor.updateProcessor state not match... processorState:', self.state
                , ' updateState:', state)
            return False
        
        self.reset()
        return True
            
