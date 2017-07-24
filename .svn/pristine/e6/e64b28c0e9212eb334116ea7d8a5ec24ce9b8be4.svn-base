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
漏胡是穷胡的一种玩法
上听后或者换宝后，查看宝牌是不是自己的胡牌，如果是，自动胡牌

特点：
1）宝牌胡牌
2）直接胡牌

"""
class MLouHuProcessor(MProcessor):
    def __init__(self):
        super(MLouHuProcessor, self).__init__()
        self.__state = MTableState.TABLE_STATE_NEXT
        self.__seatId = 0
        self.__extend_info = None
        self.__tile = 0
        
    def reset(self):
        """重置数据"""
        self.__state = MTableState.TABLE_STATE_NEXT
        self.__seatId = 0
        self.__extend_info = None
        self.__tile = 0
        
    @property
    def tile(self):
        return self.__tile
    
    def setTile(self, tile):
        self.__tile = tile

    @property
    def extendInfo(self):
        """扩展信息"""
        return self.__extend_info
    
    def setExtendInfo(self, exInfo):
        self.__extend_info = exInfo
    
    @property
    def state(self):
        """获取本轮出牌状态"""
        return self.__state
    
    def setState(self, state):
        ftlog.debug('MLouHuProcessor setState:', state)
        self.__state = state
        
    def getState(self):
        if self.state != MTableState.TABLE_STATE_NEXT:
            ftlog.debug('MLouHuProcessor.getState return:', self.state)
        return self.__state
    
    @property
    def seatId(self):
        """获取座位号
        """
        return self.__seatId
    
    def setSeatId(self, seatId):
        self.__seatId = seatId
        
    def initProcessor(self, actionID, seatId, state, tile, extendInfo, timeOut = 9):
        """
        初始化处理器
        参数
            state - 状态集合，当前座位号可以做出的全部选择
        """
        ftlog.debug('MLouHuProcessor.initProcessor actionID', actionID
                , ' state:', state
                , ' seatId:', seatId
                , ' extendInfo:', extendInfo)
        self.setActionID(actionID)
        self.setState(state)
        self.setSeatId(seatId)
        self.setExtendInfo(extendInfo)
        self.setTile(tile)
        self.setTimeOut(timeOut)
        
    def hasAutoDecideAction(self, curSeat, trustTeeSet):
        """是否有托管可以处理的行为"""
        if self.state == MTableState.TABLE_STATE_NEXT:
            return MTDefine.INVALID_SEAT
        return self.seatId
    
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
        
        ftlog.debug('MLouHuProcessor.updateProcessor actionId:', actionID
                    , ' state:', state
                    , ' seatId:', seatId)
        self.setState(MTableState.TABLE_STATE_NEXT)
        return True
            