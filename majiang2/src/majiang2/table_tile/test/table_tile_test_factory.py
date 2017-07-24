# -*- coding=utf-8
'''
Created on 2016年9月23日
庄家规则
@author: zhaol
'''
from majiang2.table.run_mode import MRunMode

class MTableTileTestFactory(object):
    def __init__(self):
        super(MTableTileTestFactory, self).__init__()
    
    @classmethod
    def getTableTileTestMgr(cls, playerCount, playMode, runMode):
        """牌桌手牌管理器获取工厂
        输入参数：
            playerCount - 玩家数量
            playMode - 玩法
            runMode - 运行模式    
        返回值：
            对应玩法手牌测试管理器
        """
        if runMode == MRunMode.LONGNET:
            from majiang2.table_tile.test.table_tile_test_longnet import MTableTileTestLongNet
            return MTableTileTestLongNet(playerCount, playMode)
        
        from majiang2.table_tile.test.table_tile_test_console import MTableTileTestConsole
        return MTableTileTestConsole(playerCount, playMode)
