# -*- coding=utf-8
'''
Created on 2016年9月23日
庄家规则
@author: zhaol
'''
from majiang2.ai.play_mode import MPlayMode
from majiang2.win_rule.win_rule_simple import MWinRuleSimple
from majiang2.win_rule.win_rule_luosihu import MWinRuleLuosihu
from majiang2.win_rule.win_rule_queshou import MWinRuleQueshou
from freetime.util import log as ftlog
class MWinRuleFactory(object):
    def __init__(self):
        super(MWinRuleFactory, self).__init__()
    
    @classmethod
    def getWinRule(cls, playMode):
        """判和规则获取工厂
        输入参数：
            playMode - 玩法
        
        返回值：
            对应玩法的判和规则
        """
	ftlog.debug('MWinRuleFactory.playMode=',playMode)	
        if MPlayMode().isSubPlayMode(playMode, MPlayMode.LUOSIHU):
            return MWinRuleLuosihu()
	elif MPlayMode().isSubPlayMode(playMode, MPlayMode.QUESHOU):
            return MWinRuleQueshou() 
        else:
            return MWinRuleSimple()
        return None
