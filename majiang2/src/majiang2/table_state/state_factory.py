# -*- coding=utf-8
'''
Created on 2016年9月23日

@author: zhaol
'''
from majiang2.ai.play_mode import MPlayMode
from majiang2.table_state.state_luosihu import MTableStateLuosihu
from majiang2.table_state.state_queshou import MTableStateQueshou
from freetime.util import log as ftlog
class TableStateFactory(object):
    
    def __init__(self):
        super(TableStateFactory, self).__init__()
    
    @classmethod
    def getTableStates(cls, playMode):
        """发牌器获取工厂
        输入参数：
            playMode - 玩法
        
        返回值：
            对应玩法的牌桌状态
        """
        if MPlayMode().isSubPlayMode(playMode, MPlayMode.LUOSIHU):
            return MTableStateLuosihu()
        elif MPlayMode().isSubPlayMode(playMode,MPlayMode.QUESHOU):
            return MTableStateQueshou()

        ftlog.error('TableStateFactory.getTableStates error, playMode:', playMode)
        return None
