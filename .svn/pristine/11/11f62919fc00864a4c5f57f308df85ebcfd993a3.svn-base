# -*- coding=utf-8
'''
Created on 2016年9月23日

@author: zhaol
'''
from majiang2.table.run_mode import MRunMode
from majiang2.table_statistic.statistic_console import MTableStatisticConsole
from majiang2.table_statistic.statistic_longnet import MTableStatisticLongNet

class TableStatisticFactory(object):
    
    def __init__(self):
        super(TableStatisticFactory, self).__init__()
    
    @classmethod
    def getTableStatistic(cls, runMode):
        """
        牌桌事件统计
        输入参数：
            runMode - 运行模式
        """
        if runMode == MRunMode.LONGNET:
            return MTableStatisticLongNet()
        else:
            return MTableStatisticConsole()
