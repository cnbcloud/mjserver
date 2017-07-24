#! -*- coding:utf-8 -*-
# Author:   yawen
# Created:  2017/3/25


from majiang2.table_state_processor.processor import MProcessor
from freetime.util import log as ftlog
from majiang2.table_state.state import MTableState
import random


class ZhisaiziProcessor(MProcessor):
    """掷塞子
    """

    def __init__(self, count, playMode):
        super(ZhisaiziProcessor, self).__init__()
        # 标记
        self.__state = MTableState.TABLE_STATE_NEXT

    def reset(self):
        self.setTimeOut(0)
        self.__state = MTableState.TABLE_STATE_NEXT
        
        
    @property
    def state(self):
        return self.__state
    
    def setState(self, state):
        self.__state = state
        
    def initProcessor(self, state, timeOut, bankerMgr, msgProcessor, uids):
        self.__state = state
        self.setTimeOut(timeOut)
        banker = bankerMgr.queryBanker()
        points = []
        points.append(random.randint(1, 6))
        points.append(random.randint(1, 6))
        msgProcessor.table_call_crapshoot(banker, points, uids)
        
    def updateProcessor(self, state):
        if self.state == MTableState.TABLE_STATE_NEXT:
            return False
        
        if self.timeOut > 0:
            return False

        self.__state = state
        return True



    def updateTimeOut(self, deta):
        self.setTimeOut(self.timeOut + deta )

    def getState(self):
        """获取状态 1 掷骰子 0 完毕
        """
        return self.state