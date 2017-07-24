# -*- coding=utf-8
'''
Created on 2016年9月23日

@author: zhaol
'''
from majiang2.table_state_processor.processor import MProcessor
from freetime.util import log as ftlog
from majiang2.ai.play_mode import MPlayMode
from majiang2.table.table_config_define import MTDefine

class MPiaoProcessor(MProcessor):
    '''
    飘是1vs1的，所有的人都可以飘，也都可以选择飘
    飘的行为是两段式的
    第一阶段，大家决定是否飘
    第二阶段，大家决定是否接受别人的飘
    在超时时间的前5秒的时间内，所有人决定自己是否飘
    之后的时间内决定自己是否接受别人的飘
    '''
    # 第一阶段，是否飘
    SCHEDULE_PIAO_ORNOT = 1
    # 第二阶段，是否接受飘
    SCHEDULE_ACCEPT_PIAO_ORNOT = 2
    # 所有人都做了飘得决定后，自动进入第二阶段
    # 第三阶段 展示玩家的漂分
    SCHEDULE_SHOW_PIAO_SCORE = 3


    
    '''
    第一阶段的状态
    '''
    STATE_PIAO_INIT = -1     # 初始状态
    STATE_PIAO_NO = 0   # 不飘
    STATE_PIAO_YES = 1  # 飘
    
    '''
    第二阶段的状态
    '''
    ACCEPT_INIT = -1    # 初始状态
    ACCEPT_NO = 0       # 不接受
    ACCEPT_YES = 1      # 接受

    SHOW_PIAO_TIMEOUT = 2
    
    def __init__(self, count, playMode):
        super(MPiaoProcessor, self).__init__()
        # 玩家数量
        self.__player_count = count
        # 玩法
        self.__player_mode = playMode
        # 当前阶段
        self.__schedule = self.SCHEDULE_PIAO_ORNOT
        # 是否飘的超时
        self.__piao_timeOut = 5
        # 是否接受飘的超时
        self.__accept_piao_timeOut = 5
        # 展示所有玩家漂分的时间
        self.__show_piao_timeOut = self.SHOW_PIAO_TIMEOUT
        # 是否飘的状态集合
        self.__piao_states = [self.STATE_PIAO_INIT for _ in range(self.playerCount)]
        # 是否接受飘的状态集合
        self.__accept_piao_states = []
        for seatId in range(self.playerCount):
            states = [self.ACCEPT_INIT for _ in range(self.playerCount)]
            states[seatId] = self.ACCEPT_NO
            self.__accept_piao_states.append(states)
            
        self.__piao_points = [0 for _ in range(self.playerCount)]
        self.__is_piao = False
        self.__bi_piao_point = 0
        
        # 所有玩家一轮游戏票次数的总和
        self.__piao_count = [0 for _ in xrange(self.playerCount)]
        
    
    def reset(self):
        self.__schedule = self.SCHEDULE_PIAO_ORNOT
        self.__piao_states = [self.STATE_PIAO_INIT for _ in range(self.playerCount)]
        self.__accept_piao_states = []
        for seatId in range(self.playerCount):
            states = [self.ACCEPT_INIT for _ in range(self.playerCount)]
            states[seatId] = self.ACCEPT_NO
            self.__accept_piao_states.append(states)
            
        self.__piao_points = [0 for _ in range(self.playerCount)]
        self.__is_piao = False
        ftlog.debug('[MPiaoProcessor]  schedule:', self.schedule
                    , ' piaoStates:', self.piaoStates
                    , ' acceptPiaoStates:', self.acceptPiaoStates
                    , ' piaoPoints:', self.piaoPoints)
        self.__bi_piao_point = 0
        self.setShowPiaoTimeOut(self.SHOW_PIAO_TIMEOUT)

    @property
    def biPiaoPoint(self):
        return self.__bi_piao_point
    
    def setBiPiaoPoint(self, biPiaoPoint):
        self.__bi_piao_point = biPiaoPoint
        
    @property
    def isPiao(self):
        return self.__is_piao
    
    def setPiao(self, isPiao):
        self.__is_piao = isPiao
        
    @property
    def piaoPoints(self):
        return self.__piao_points
    
    def setPiaoPoints(self, piaoPoints):
        self.__piao_points = piaoPoints
            
    @property
    def piaoStates(self):
        return self.__piao_states
    
    def setPiaoStates(self, piaoState):
        self.__piao_states = piaoState
        
    @property
    def acceptPiaoStates(self):
        return self.__accept_piao_states
    
    def setAcceptPiaoStates(self, states):
        self.__accept_piao_states = states
        
    @property
    def acceptPiaoTimeOut(self):
        return self.__accept_piao_timeOut
    
    def setAcceptPiaoTimeOut(self, timeOut):
        self.__accept_piao_timeOut = timeOut

    @property
    def showPiaoTimeOut(self):
        return self.__show_piao_timeOut

    def setShowPiaoTimeOut(self, timeOut):
        self.__show_piao_timeOut = timeOut

    @property
    def piaoTimeOut(self):
        return self.__piao_timeOut
    
    def setPiaoTimeOut(self, timeOut):
        self.__piao_timeOut = timeOut
        
    @property
    def schedule(self):
        return self.__schedule
    
    def setSchedule(self, schedule):
        self.__schedule = schedule


    @property
    def piaoCount(self):
        """房间大结算时不同玩家飘的次数"""
        return self.__piao_count
    
    def resetPiaoCount(self):
        self.__piao_count=[0 for _ in xrange(self.playerCount)]
    
    
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

    def updateTimeOut(self, deta):
        #如果飘永远等待，就不更新时间
        if not self.tableTileMgr.tableConfig.get(MTDefine.PIAO_WAIT_FOREVER,0): 
            if self.schedule == self.SCHEDULE_PIAO_ORNOT:
                self.__piao_timeOut += deta
            elif self.schedule == self.SCHEDULE_ACCEPT_PIAO_ORNOT:
                self.__accept_piao_timeOut += deta
            elif self.schedule == self.SCHEDULE_SHOW_PIAO_SCORE:
                self.__show_piao_timeOut += deta

            ftlog.debug('[MPiaoProcessor]  schedule:', self.schedule
                    , ' piaoTimeOut:', self.piaoTimeOut
                    , ' acceptPiaoTimeOut:', self.acceptPiaoTimeOut,'showPiaoTimeOut:',self.showPiaoTimeOut)
        
    def getAutoDecideSeatsBySchedule(self):
        """根据座位号，获取托管的座位号列表"""
        seats = []
        if not self.isPiao:
            return seats
        
        if self.schedule == self.SCHEDULE_PIAO_ORNOT:
            for index in range(self.playerCount):
                if self.piaoStates[index] != self.STATE_PIAO_INIT:
                    continue
                
                if self.players[index].isRobot():
                    seats.append(index)
                    continue
                
                if self.piaoTimeOut <= 0:
                    seats.append(index)
                    continue
                
        if self.schedule == self.SCHEDULE_ACCEPT_PIAO_ORNOT:
            for accepter in range(self.playerCount):
                for piaoSir in range(self.playerCount):
                    if accepter == piaoSir:
                        continue
                    
                    if self.acceptPiaoStates[piaoSir][accepter] != self.ACCEPT_INIT:
                        continue
                    
                    if self.players[accepter].isRobot() and (accepter not in seats):
                        seats.append(accepter)
                        continue
                    
                    if self.acceptPiaoTimeOut <= 0 and (accepter not in seats):
                        seats.append(accepter)
                        continue        
        if self.schedule == self.SCHEDULE_SHOW_PIAO_SCORE:
           if  not (self.getState() == 0):
              for accepter in range(self.playerCount):
                    seats.append(accepter)

        if len(seats) > 0:
            ftlog.debug('[MPiaoProcessor]  schedule:', self.schedule
                    , ' piaoStates:', self.piaoStates
                    , ' piaoPoints:', self.piaoPoints
                    , ' acceptPiaoStates:', self.acceptPiaoStates
                    , ' acceptPiaoTimeOut:', self.acceptPiaoTimeOut
                    , ' seats:', seats)
                    
        return seats
    
    def isAllPiao(self):
        if self.schedule != self.SCHEDULE_PIAO_ORNOT:
            return True

        for seatId in range(self.playerCount):
            if self.piaoStates[seatId] == self.STATE_PIAO_INIT:
                return False
            
        return True
    
    def isAllAcceptPiao(self):
        if self.schedule != self.SCHEDULE_ACCEPT_PIAO_ORNOT:
            return False
        
        for accepter in range(self.playerCount):
            for piaoSir in range(self.playerCount):
                if accepter == piaoSir:
                    continue
                
                if self.acceptPiaoStates[piaoSir][accepter] == self.ACCEPT_INIT:
                    ftlog.debug('[MPiaoProcessor]  acceptPiaoStates:', self.acceptPiaoStates)
                    return False
        
        return True


    def getState(self):
        """获取本轮出牌状态
        """
        if not self.isPiao:
            return 0
        
        state = self.schedule

        if self.schedule == self.SCHEDULE_ACCEPT_PIAO_ORNOT:
            if self.isAllAcceptPiao():
                state = 0
        if self.schedule == self.SCHEDULE_SHOW_PIAO_SCORE:
            if self.showPiaoTimeOut == 0:
                state = 0

        return state

    def updateShowPiao(self):
        if self.showPiaoTimeOut < 0:
            self.setShowPiaoTimeOut(0)
            return True
        return False



    
    def piao(self, seatId, piaoPoint, msgProcessor):
        """飘"""
        if self.piaoStates[seatId] != self.STATE_PIAO_INIT:
            return
        if self.schedule != self.SCHEDULE_PIAO_ORNOT:
            return
        if self.getState() == 0:
            return
        if piaoPoint == 0:
            self.piaoStates[seatId] = self.STATE_PIAO_NO
            self.acceptPiaoStates[seatId] = [self.ACCEPT_NO for _ in range(self.playerCount)]
        else:
            self.piaoPoints[seatId] = piaoPoint
            self.piaoStates[seatId] = self.STATE_PIAO_YES
            self.piaoCount[seatId]+=1
        if self.isAllPiao(): #是否都飘了
            self.setPiaoTimeOut(0)
            self.setSchedule(self.SCHEDULE_ACCEPT_PIAO_ORNOT) #进入第二阶段
            if MPlayMode().isSubPlayMode(self.__player_mode, MPlayMode.LUOSIHU):
                for seatId in range(self.playerCount): #每个玩家自动接受飘
                    self.autoAccept(seatId)
            else:
                self.beginAcceptPiao(msgProcessor) #开始接受飘
            
    def acceptPiao(self, seatId, piaoSirId, piaoOrNot, msgProcessor):
        ftlog.debug('[MPiaoProcessor]  seatId:', seatId
                    , ' piaoSirId:', piaoSirId
                    , ' piaoOrNot:', piaoOrNot
                    , ' schedule:', self.schedule
                    , ' piaoStates:', self.piaoStates
                    , ' piaoPoints:', self.piaoPoints)
        if seatId == piaoSirId:
            return
        if self.schedule != self.SCHEDULE_ACCEPT_PIAO_ORNOT:
            return
        if self.getState() == 0:
            return
        if self.piaoStates[piaoSirId] != self.STATE_PIAO_YES:
            return
        if self.piaoPoints[piaoSirId] == 0:
            return
        
        if piaoOrNot:
            self.acceptPiaoStates[piaoSirId][seatId] = self.ACCEPT_YES
            piaoNode = {}
            piaoNode['piaoSeatId'] = piaoSirId
            piaoNode['piaoPoint'] = self.piaoPoints[piaoSirId]
            piaoNode['acceptedSeatId'] = seatId
            # 发给接受飘的人
            msgProcessor.table_call_accepted_piao(self.players[seatId].userId
                    , seatId
                    , [piaoNode])
            # 发给飘的人应答，有人接受
            msgProcessor.table_call_accepted_piao(self.players[piaoSirId].userId
                    , piaoSirId
                    , [piaoNode])
        else:
            self.acceptPiaoStates[piaoSirId][seatId] = self.ACCEPT_NO
            
    def autoDecide(self, seatId, msgProcessor):
        """自动操作"""
        ftlog.debug('[MPiaoProcessor] schedule:', self.schedule)
        if self.schedule == self.SCHEDULE_ACCEPT_PIAO_ORNOT:
            ftlog.debug('[MPiaoProcessor] acceptPiao before:', self.acceptPiaoStates)
            # 自己的漂，超时的变为不接收
            for index in range(self.playerCount):
                if index == seatId:
                    continue
                if self.acceptPiaoStates[seatId][index] == self.ACCEPT_INIT:
                    self.acceptPiaoStates[seatId][index] = self.ACCEPT_NO
                if self.piaoStates[index] > 0 and self.acceptPiaoStates[index][seatId] == self.ACCEPT_INIT:
                    self.acceptPiaoStates[index][seatId] = self.ACCEPT_NO
            ftlog.debug('[MPiaoProcessor] acceptPiao after:', self.acceptPiaoStates)
            
        if self.schedule == self.SCHEDULE_PIAO_ORNOT:
            ftlog.debug('[MPiaoProcessor] piao before:', self.piaoStates)
            self.piao(seatId, 0, msgProcessor)
            ftlog.debug('[MPiaoProcessor] piao after:', self.piaoStates)

    def autoAccept(self, seatId):
        """自动操作"""
        ftlog.debug('[MPiaoProcessor]  schedule:', self.schedule)
        if self.schedule == self.SCHEDULE_ACCEPT_PIAO_ORNOT:
            ftlog.debug('[MPiaoProcessor]  acceptPiao before:', self.acceptPiaoStates)
            # 自己的漂，超时的变为不接收
            for index in range(self.playerCount):
                if index == seatId:
                    continue
                if self.acceptPiaoStates[seatId][index] == self.ACCEPT_INIT:
                    self.acceptPiaoStates[seatId][index] = self.ACCEPT_YES
                if self.piaoStates[index] > 0 and self.acceptPiaoStates[index][seatId] == self.ACCEPT_INIT:
                    self.acceptPiaoStates[index][seatId] = self.ACCEPT_YES
            ftlog.debug('[MPiaoProcessor] acceptPiao after:', self.acceptPiaoStates)
            
    def beginPiao(self, msgProcessor, setting):
        if self.schedule != self.SCHEDULE_PIAO_ORNOT:
            return
        self.__is_piao = True
        for seatId in range(self.playerCount):
            msgProcessor.table_call_ask_piao(self.players[seatId].userId
                    , seatId
                    , setting
                    , self.piaoTimeOut)
    
    def beginAcceptPiao(self, msgProcessor):
        if self.schedule != self.SCHEDULE_ACCEPT_PIAO_ORNOT:
            return
        
        ftlog.debug('[MPiaoProcessor]  acceptPiaoStates:', self.acceptPiaoStates)
        for seatId in range(self.playerCount):
            solution = []
            for piaoSir in range(self.playerCount):
                if seatId == piaoSir:
                    continue
                
                if self.piaoStates[piaoSir] != self.STATE_PIAO_YES:
                    continue
                
                piaoNode = {}
                piaoNode['piaoSeatId'] = piaoSir
                piaoNode['piaoPoint'] = self.piaoPoints[piaoSir]
                solution.append(piaoNode)
            
            msgProcessor.table_call_accept_piao(self.players[seatId].userId
                    , seatId
                    , solution
                    , self.acceptPiaoTimeOut)
            
    def broadCastPiao(self, msgProcessor):
        for seatId in range(self.playerCount):
            # 向该seatId发送飘的结果
            ftlog.debug('[MPiaoProcessor]  seatId:', seatId
                        , ' piaoState:', self.piaoStates[seatId]
                        , ' acceptPiaoState:', self.acceptPiaoStates[seatId])
            # 卡五星只显示每个人自己选择漂数
            if MPlayMode().isSubPlayMode(self.__player_mode, MPlayMode.LUOSIHU):
                if self.players[seatId]:
                    msgProcessor.table_call_piao(self.players[seatId].userId
                        , seatId
                        , self.piaoPoints)
            if 0: 
                if self.players[seatId]:
                    piaoBiPiao = [p + self.biPiaoPoint for p in self.piaoPoints]
                    msgProcessor.table_call_piao(self.players[seatId].userId
                        , seatId
                        , piaoBiPiao)
            else:
                bSend = False
                piao = [0 for _ in range(self.playerCount)]
                for target in range(self.playerCount):
                    if target == seatId:
                        continue
                    
                    ftlog.debug('[MPiaoProcessor]  target:', target
                                , ' piaoState:', self.piaoStates[target]
                                , ' acceptPiaoState:', self.acceptPiaoStates[target])
                    # seatId是否飘了，target是否接受
                    if (self.piaoStates[seatId] == self.STATE_PIAO_YES) and (self.acceptPiaoStates[seatId][target] == self.ACCEPT_YES):
                        piao[target] += self.piaoPoints[seatId]
                        bSend = True
                        
                    # target是否飘了，seatId是否接受
                    if (self.piaoStates[target] == self.STATE_PIAO_YES) and (self.acceptPiaoStates[target][seatId] == self.ACCEPT_YES):
                        piao[target] += self.piaoPoints[target]
                        bSend = True
                
                if bSend:
                    msgProcessor.table_call_piao(self.players[seatId].userId
                        , seatId
                        , piao)
    def getPiaoPointsBySeats(self, seat1, seat2):
        """获取两个人之间的漂分"""
        piao = 0
        if self.acceptPiaoStates[seat1][seat2] == self.ACCEPT_YES:
            piao += self.piaoPoints[seat1]
            ftlog.debug('[MPiaoProcessor]  piao=====', piao)


        if self.acceptPiaoStates[seat2][seat1] == self.ACCEPT_YES:
            piao += self.piaoPoints[seat2]
            ftlog.debug('[MPiaoProcessor]  piao=====', piao)
        return piao + self.biPiaoPoint * 2
                
    def initProcessor(self, actionID, seatId, state, extendInfo = None, timeOut = 9):
        pass
    
    def updateProcessor(self, actionID, seatId, state, tile, pattern = None):
        pass
    
if __name__ == "__main__":
    dp = MPiaoProcessor(4)
