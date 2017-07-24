#! -*- coding:utf-8 -*-
# Author:   qianyong
# Created:  2017/3/25

from freetime.util import log as ftlog

from majiang2.table_state_processor.processor import MProcessor
from majiang2.ai.play_mode import MPlayMode
from majiang2.tile.tile import MTile
from majiang2.table_state.state import MTableState


class MQiangjinProcessor(MProcessor):
    """抢金处理
       在所有玩家都抢金，庄家才能继续打牌
    """

    def __init__(self, count, playMode):
        super(MQiangjinProcessor, self).__init__()
        # 玩家数量
        self.__player_count = count
        # 玩法
        self.__player_mode = playMode
        # 抢金情况
	self.__state = MTableState.TABLE_STATE_NEXT
        # 抢金情况
        self.__qiangjinState = [-1 for _ in range(self.playerCount)]
	
        self.__qiangjinOpt = []

    def reset(self):
        self.__qiangjinOpt = []
        self.__state = MTableState.TABLE_STATE_NEXT
        self.__qiangjinState = [-1 for _ in range(self.playerCount)]

    @property
    def playerCount(self):
        return self.__player_count

    def setPlayerCount(self, pCount):
        self.__player_count = pCount

    @property
    def playMode(self):
        """获取本局玩法"""
        return self.__player_mode

    def setPlayMode(self, playMode):
        self.__player_mode = playMode

    @property
    def state(self):
        return self.__state
    
    def setState(self, state):
        self.__state = state

    @property
    def qiangjinOpt(self):
        return self.__qiangjinOpt

    @property
    def qiangjinState(self):
        return self.__qiangjinState

    def getState(self):
        return self.state

    def beginQiangjin(self, states, actionId, timeOut):
        """开始抢金，前端收到这个消息之后提示让玩家选择抢金
        """
	self.reset()
	self.setState(MTableState.TABLE_STATE_QIANGJIN)
        self.__qiangjinOpt = states
        self.__action_id = actionId
        for seatId in range(self.playerCount):
            if not states[seatId]:
                self.setQiangjinState(seatId, states[seatId])
        for seatId in range(self.playerCount):
	    if states[seatId]:
		isTianHu = False
		isSanJinDao = False
		if states[seatId] == MTableState.TABLE_STATE_TIANHU:
		    isTianHu = True
	        if states[seatId] == MTableState.TABLE_STATE_SANJINDAO:
	            isSanJinDao = True
		ftlog.debug('MQiangjinProcessor.beginQiangjin isTianHu',isTianHu,states[seatId],MTableState.TABLE_STATE_TIANHU)
	        self.msgProcessor.table_call_Qiangjin(self.players[seatId], states[seatId], actionId, timeOut,isTianHu,isSanJinDao)

    def setQiangjinState(self, seatId, state):
        """
        """
        # 玩家已经选择过了，不能再次选择
        if self.qiangjinState[seatId] != -1:
            return False,0,0
        self.qiangjinState[seatId] = state
	ftlog.debug('MQiangjinProcessor.setQiangjinState=',self.qiangjinState[seatId],state,seatId,self.qiangjinState)	
        if self.isAllSelected():
	    self.setState(MTableState.TABLE_STATE_NEXT)
	    maxSeatId,maxState = self.calcMaxState()    
            if self.qiangjinOpt[maxSeatId] == maxState:    
                return True,maxSeatId,maxState
            else:
                return True,0,0   
        return False,0,0


    def calcMaxState(self):
        maxSeatId = 0
        maxState = 0
        maxState = max(self.qiangjinState)
        for seatId in range(self.playerCount):
            if maxState == self.qiangjinState[seatId]:
                maxSeatId = seatId
                
        return maxSeatId,maxState

    def isAllSelected(self):
        """是否所有人都已定缺
        """
        if -1 in self.qiangjinState:
            return False
        return True

    def handlePlayerReconnect(self, userId, seatId):
        """处理玩家的断线重连
        """
	ftlog.debug('MQiangjinProcessor.handlePlayerReconnect ')
        if not self.msgProcessor:
            return
        if self.state == MTableState.TABLE_STATE_QIANGJIN:  
            if self.absenceColor[seatId] == -1:
                self.msgProcessor.table_call_Qiangjin(self.players[seatId], self.__qiangjinOpt[seatId], self.__action_id)


