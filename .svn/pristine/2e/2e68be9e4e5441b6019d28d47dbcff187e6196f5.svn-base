# -*- coding=utf-8
'''
Created on 2016年9月23日

@author: zhaol
'''
from majiang2.table_state_processor.processor import MProcessor
from freetime.util import log as ftlog

class MDoubleProcessor(MProcessor):
    '''
    每个人都可以选择是否输赢加倍
        1）可以加倍
        2）也可以不加倍
    '''
    NORMAL_WIN_LOOSE = 1
    DOUBLE_WIN_LOOSE = 2
    NO_RESPONSE = 0
    ALREADY_RESPONSED = 1
    RESPONSE_INIT = 2
    
    def __init__(self, count, playMode):
        super(MDoubleProcessor, self).__init__()
        # 玩家数量
        self.__player_count = count
        # 玩法
        self.__player_mode = playMode
        # 是否飘的状态集合
        self.__double_points = [self.NORMAL_WIN_LOOSE for _ in range(self.playerCount)]
        # 是否应答
        self.__double_states = [self.RESPONSE_INIT for _ in range(self.playerCount)]

    def reset(self):
        self.__double_points = [self.NORMAL_WIN_LOOSE for _ in range(self.playerCount)]
        self.__double_states = [self.RESPONSE_INIT for _ in range(self.playerCount)]
        self.__action_id = 0
        
    def resetButPoints(self):#盘锦每局不重置加钢
        self.__double_states = [self.RESPONSE_INIT for _ in range(self.playerCount)]
        self.__action_id = 0
        
    @property
    def doubleStates(self):
        return self.__double_states
    
    def setDoubleStates(self, doubleStates):
        self.__double_states = doubleStates
        
    @property
    def doublePoints(self):
        return self.__double_points
    
    def setDoublePoints(self, doublePoints):
        self.__double_points = doublePoints

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
        
    def getAutoDecideSeatsBySchedule(self):
        if self.getState() == 0:
            return []
        
        autos = []
        for seatId in range(self.playerCount):
            if self.doubleStates[seatId] != self.NO_RESPONSE:
                continue
            
            if self.players[seatId].userId < 10000:
                autos.append(seatId)
            elif self.timeOut <= 0:
                autos.append(seatId)
        return autos
        
    def getState(self):
        """获取本轮出牌状态
        """
        for response in self.__double_states:
            if response == self.NO_RESPONSE:
                return 1
        return 0
    
    def double(self, seatId):
        self.doublePoints[seatId] = self.DOUBLE_WIN_LOOSE
        self.doubleStates[seatId] = self.ALREADY_RESPONSED
        self.broadCastDoule(seatId)
        
    def noDouble(self, seatId):
        self.doublePoints[seatId] = self.NORMAL_WIN_LOOSE
        self.doubleStates[seatId] = self.ALREADY_RESPONSED
        self.broadCastDoule(seatId)
        
    def keepNoChange(self, seatId):
        self.doubleStates[seatId] = self.ALREADY_RESPONSED
        self.broadCastDoule(seatId)
    
    def beginDouble(self, actionId, timeOut):
        self.setTimeOut(timeOut)
        self.setActionID(actionId)
        self.__double_states = [self.NO_RESPONSE for _ in range(self.playerCount)]
        self.askDouble()
        
    def getUids(self):
        uids = []
        for player in self.players:
            if not player:
                continue
            uids.append(player.userId)
        return uids
    
    def askDouble(self):
        uids = self.getUids()
        if not self.msgProcessor:
            return
        self.msgProcessor.table_call_double_ask(uids, self.actionID, self.timeOut, self.doublePoints)
    
    def broadCastDoule(self,seatId=-1):
        uids = self.getUids()
        if not self.msgProcessor:
            return
        self.msgProcessor.table_call_double_broadcast(uids
                , seatId, self.doublePoints)
                
    def initProcessor(self, actionID, seatId, state, extendInfo = None, timeOut = 9):
        pass
    
    def updateProcessor(self, actionID, seatId, state, tile, pattern = None):
        pass
    
if __name__ == "__main__":
    dp = MDoubleProcessor(4)
