# -*- coding=utf-8
'''
Created on 2016年9月23日
牌型整理
@author: zhaol
'''
from majiang2.ai.play_mode import MPlayMode
from majiang2.tile_pattern_checker.tile_pattern_checker import MTilePatternChecker
from majiang2.tile_pattern_checker.tile_pattern_checker_luosihu import MTilePatternCheckerLuosihu
from majiang2.tile_pattern_checker.tile_pattern_checker_queshou import MTilePatternCheckerQueshou
class MTilePatternCheckerFactory(object):
    def __init__(self):
        super(MTilePatternCheckerFactory, self).__init__()
    
    @classmethod
    def getTilePatternChecker(cls, playMode):
        """判和规则获取工厂
        输入参数：
            playMode - 玩法
        
        返回值：
            对应玩法的判和规则
        """
        if MPlayMode().isSubPlayMode(playMode, MPlayMode.LUOSIHU):
            return MTilePatternCheckerLuosihu()
        elif MPlayMode().isSubPlayMode(playMode, MPlayMode.QUESHOU):
            return MTilePatternCheckerQueshou()
        return MTilePatternChecker()
