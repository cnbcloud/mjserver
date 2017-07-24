# -*- coding=utf-8
'''
Created on 2016年9月23日
庄家规则
@author: zhaol
'''
from majiang2.ai.play_mode import MPlayMode
from majiang2.mao_rule.mao_base import MMaoRuleBase

class MMaoRuleFactory(object):
    def __init__(self):
        super(MMaoRuleFactory, self).__init__()
    
    @classmethod
    def getMaoRule(cls, playMode):
        """判和规则获取工厂
        输入参数：
            playMode - 玩法
        
        返回值：
            对应玩法的判和规则
        """
        return MMaoRuleBase()
