#! -*- coding:utf-8 -*-
# Author:   qianyong
# Created:  2017/3/10

from majiang2.ai.play_mode import MPlayMode
from majiang2.chi_rule.chi_rule import MChiRule

class MChiRuleFactory(object):
    def __init__(self):
        super(MChiRuleFactory, self).__init__()

    @classmethod
    def getChiRule(cls, playMode):
        """判吃规则获取工厂
        输入参数：
            playMode - 玩法

        返回值：
            对应玩法的判和规则
        """
        return MChiRule()
