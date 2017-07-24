# -*- coding=utf-8 -*-
'''
Created on 2015年9月30日
麻将好友桌的牌桌，负责好友桌号的管理和好友桌赛制的调度。
@author: 赵良
'''
from majiang2.table.majiang_table_observer import MajiangTableObserver
from queshou.servers.util.rpc import table_events_remote

class QueshouTableObserver(MajiangTableObserver):
    def __init__(self, gameId, roomId, tableId):
        super(QueshouTableObserver, self).__init__(gameId, roomId, tableId)
        
    def onBeginGame(self, players, banker):
        """游戏开始"""
        for userId in players:
            table_events_remote.gamePlay(userId, self.gameId, self.roomId, self.tableId, banker)
    
    def onWinLoose(self):
        """结果"""
        pass
    
    def onGameEvent(self, event, players, roundId):
        # 统计
        self.tableStatistic.reportEvent(event
                , players
                , self.gameId
                , self.roomId
                , self.tableId
                , roundId)