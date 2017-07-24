# -*- coding=utf-8 -*-
'''
Created on 2015年9月30日
麻将好友桌的牌桌，负责好友桌号的管理和好友桌赛制的调度。
@author: 赵良
'''
from majiang2.table_statistic.statistic_factory import TableStatisticFactory
from majiang2.table.run_mode import MRunMode

class MajiangTableObserver(object):
    def __init__(self, gameId, roomId, tableId):
        self.__gameId = gameId
        self.__roomId = roomId
        self.__tableId = tableId
        self.__table_statistic = TableStatisticFactory.getTableStatistic(MRunMode.LONGNET)

    @property
    def tableStatistic(self):
        return self.__table_statistic
    
    @property
    def gameId(self):
        return self.__gameId
    
    @property
    def roomId(self):
        return self.__roomId
    
    @property
    def tableId(self):
        return self.__tableId
        
    def onBeginGame(self, players, banker):
        """游戏开始"""
        pass
    
    def onWinLoose(self):
        """结果"""
        pass
    
    def onGameEvent(self, event, players, roundId):
        """上报BI事件"""
        pass