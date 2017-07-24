#! -*- coding:utf-8 -*-
# Author:   youjun
# Created:  2017/6/7

from majiang2.ai.play_mode import MPlayMode
from majiang2.flower_rule.flower_base import MFlowerRuleBase
from majiang2.flower_rule.flower_queshou import MFlowerRuleQueshou


class MFlowerRuleFactory(object):
    def __init__(self):
        super(MFlowerRuleFactory, self).__init__()

    @classmethod
    def getFlowerRule(cls, playMode):
        """花规则获取工厂
        输入参数：
            playMode - 玩法

        返回值：
            对应玩法的判和规则
        """
        if MPlayMode().isSubPlayMode(playMode, MPlayMode.QUESHOU):
            return MFlowerRuleQueshou()

        return MFlowerRuleBase()
