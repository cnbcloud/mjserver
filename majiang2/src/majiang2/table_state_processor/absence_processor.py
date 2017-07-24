#! -*- coding:utf-8 -*-
# Author:   qianyong
# Created:  2017/3/25

from freetime.util import log as ftlog

from majiang2.table_state_processor.processor import MProcessor
from majiang2.ai.play_mode import MPlayMode
from majiang2.tile.tile import MTile


class MAbsenceProcessor(MProcessor):
    """定缺处理
       在庄家14张牌，闲家13张牌时，庄家不打牌，进入定缺阶段，在所有玩家都定好缺之后，庄家才能继续打牌
    """

    SCHEDULE_ABSENCE_NONE = 0   # 默认处于非定缺阶段
    SCHEDULE_ABSENCE_BEGIN = 1  # 开始进入定缺阶段
    SCHEDULE_ABSENCE_DING = 2   # 询问玩家选择缺哪门

    COLOR_ABSENCE_INIT = -1  # 初始缺哪门状态

    def __init__(self, count, playMode):
        super(MAbsenceProcessor, self).__init__()
        # 玩家数量
        self.__player_count = count
        # 玩法
        self.__player_mode = playMode
        # 调度情况
        self.__schedule = self.SCHEDULE_ABSENCE_NONE
        # 缺门情况
        self.__absenceColor = [self.COLOR_ABSENCE_INIT] * self.playerCount

    def reset(self):
        self.__schedule = self.SCHEDULE_ABSENCE_NONE
        self.__absenceColor = [self.COLOR_ABSENCE_INIT] * self.playerCount

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
    def schedule(self):
        return self.__schedule

    def setSchedule(self, schedule):
        self.__schedule = schedule

    @property
    def absenceColor(self):
        return self.__absenceColor

    def setAbsenceColor(self, value):
        self.__absenceColor = value

    def getState(self):
        return 0 if self.schedule == self.SCHEDULE_ABSENCE_NONE else 1

    def beginAbsence(self):
        """开始定缺，前端收到这个消息之后提示让玩家选择缺哪门
        """
        self.setSchedule(self.SCHEDULE_ABSENCE_BEGIN)

    def onBankerAddedFirstTile(self):
        """庄家摸完了牌，开始询问玩家进行定缺
        """
        ftlog.debug('MAbsenceProcessor onBankerAddedFirstTile')
        self.setSchedule(self.SCHEDULE_ABSENCE_DING)
        for seatId in range(self.playerCount):
            self.msgProcessor.table_call_ask_absence(self.players[seatId].userId, seatId)

    def dingAbsence(self, seatId, color):
        """玩家定缺某个花色
        """
        # 玩家已经选择过了，不能再次选择
        if self.absenceColor[seatId] != self.COLOR_ABSENCE_INIT:
            return

        # 只能缺万筒条中的一个颜色
        if color not in (MTile.TILE_WAN, MTile.TILE_TONG, MTile.TILE_TIAO):
            return
        ftlog.debug('dingAbsence seatId:', seatId, ' color:', color)

        self.absenceColor[seatId] = color

        if self.isAllSelected():
            # 所有人都已选择定缺，结束定缺状态
            self.setSchedule(self.SCHEDULE_ABSENCE_NONE)
        else:
            for i in range(self.playerCount):
                self.msgProcessor.table_call_player_absence_end(self.players[i].userId, seatId) 
        #     uids = [p.userId for p in self.players]
        #     self.msgProcessor.table_call_ding_absence(uids, self.absenceColor)
        # else:
        #     # 发送回应, 重新组建一个临时的absenceColor发送，不能提前透露别人的选缺情况
        #     tmp = [self.COLOR_ABSENCE_INIT] * self.playerCount
        #     tmp[seatId] = color
        #     self.msgProcessor.table_call_ding_absence(self.players[seatId].userId, tmp)

    def isAllSelected(self):
        """是否所有人都已定缺
        """
        for color in self.absenceColor:
            if color == self.COLOR_ABSENCE_INIT:
                return False
        return True

    def handlePlayerReconnect(self, userId, seatId):
        """处理玩家的断线重连
        """
	ftlog.debug('MAbsenceProcessor.handlePlayerReconnect ')
        if not self.msgProcessor:
            return
	
        if self.schedule == self.SCHEDULE_ABSENCE_DING:  # 正在定缺的阶段
            # 玩家还没选缺，通知其选缺
            if self.absenceColor[seatId] == self.COLOR_ABSENCE_INIT:
                self.msgProcessor.table_call_ask_absence(userId, seatId)
        else:  # 否则，补发所有玩家的定缺情况
            if self.__absenceColor == [self.COLOR_ABSENCE_INIT] * self.playerCount:
                return
            else:
                absenceInfo = []
                for i in xrange(self.playerCount):
                    absenceInfo.append([self.players[i].userId,self.absenceColor[self.players[i].curSeatId]])
                #self.msgProcessor.table_call_absence_end(userId, seatId,absenceInfo)
                for i in xrange(self.playerCount):
                    self.msgProcessor.table_call_absence_end(self.players[i].userId, i, absenceInfo)

