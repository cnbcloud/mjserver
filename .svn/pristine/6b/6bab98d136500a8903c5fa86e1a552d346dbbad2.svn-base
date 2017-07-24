# -*- coding=utf-8
'''
Created on 2016年9月23日
牌桌统计
@author: zhaol
'''
from majiang2.table_statistic.statistic import MTableStatistic
from poker.entity.biz import bireport
from freetime.util import log as ftlog

class MTableStatisticLongNet(MTableStatistic):
    
    def __init__(self):
        super(MTableStatisticLongNet, self).__init__()

    def reportEvent(self, event, players, gameId, roomId, tableId, roundId):
        ftlog.info('MTableStatisticLongNet.reportEvent event:', event
                , ' players:', players
                , ' gameId:', gameId
                , ' roomId:', roomId
                , ' tableId:', tableId
                , ' roundId:', roundId
        )
        
        uids = []
        for player in players:
            if player.isRobot():
                continue
            
            uids.append(player.userId)
            bireport.reportGameEvent(event
                    , player.userId
                    , gameId
                    , roomId
                    , tableId
                    , roundId
                    , 0, 0, 0, []
                    , player.clientId)
        
        if event == MTableStatistic.TABLE_START:  
            bireport.tableStart(gameId, roomId, tableId, roundId, uids)
        elif event == MTableStatistic.TABLE_WIN:
            bireport.tableWinLose(gameId, roomId, tableId, roundId, uids)
