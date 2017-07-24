#! -*- coding:utf-8 -*-
# Author:   qianyong
# Created:  2017/3/9

from majiang2.ai.play_mode import MPlayMode
from majiang2.peng_rule.peng_rule import MPengRule
from majiang2.peng_rule.peng_rule_luosihu import MPengRuleLuoSiHu
class MPengRuleFactory(object):
    def __init__(self):
        super(MPengRuleFactory, self).__init__()

    @classmethod
    def getPengRule(cls, playMode):
        """判碰规则获取工厂
        输入参数：
            playMode - 玩法

        返回值：
            对应玩法的判和规则
        """
        if playMode == "luosihu-ctxuezhan":
            return MPengRuleLuoSiHu()
        return MPengRule()
