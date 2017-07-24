# -*- coding=utf-8
'''
Created on 2016年9月23日
庄家规则
@author: zhaol
'''
from majiang2.ai.play_mode import MPlayMode
from majiang2.ting_rule.ting_rule_luosihu import MTingLuosihuRule
from majiang2.ting_rule.ting_rule_queshou import MTingQueshouRule
from freetime.util import log as ftlog
from majiang2.win_rule.win_rule_factory import MWinRuleFactory
class MTingRuleFactory(object):
    def __init__(self):
        super(MTingRuleFactory, self).__init__()
    
    @classmethod
    def getTingRule(cls, playMode):
        """判和规则获取工厂
        输入参数：
            playMode - 玩法
        
        返回值：
            对应玩法的判和规则
        """
        if MPlayMode().isSubPlayMode(playMode, MPlayMode.LUOSIHU):
            return MTingLuosihuRule()
        elif MPlayMode().isSubPlayMode(playMode, MPlayMode.QUESHOU):
            return MTingQueshouRule() 
        else:
            return MTingSimpleRule()
        return None
    
def tingHaerbin():
    tingRule = MTingRuleFactory.getTingRule(MPlayMode.LUOSIHU)
    winRule = MWinRuleFactory.getWinRule(MPlayMode.LUOSIHU)
    tingRule.setWinRuleMgr(winRule)
    tiles = [[4, 4, 4, 5 ,13, 14, 15, 29], [[23, 24, 25]], [[27, 27, 27]], [], [], []]
    leftTiles = [3, 4, 4, 4, 7, 8, 8, 9, 14, 14, 16, 17, 18, 19, 21, 21, 22, 23, 24, 24, 25, 27, 28, 29]
    result, resultDetail = tingRule.canTing(tiles, leftTiles, 7, [])
    ftlog.debug( result )
    if result:
        ftlog.debug(resultDetail)

if __name__ == "__main__":
    tingHaerbin()
