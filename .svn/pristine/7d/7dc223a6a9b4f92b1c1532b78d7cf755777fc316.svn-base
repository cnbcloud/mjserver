# -*- coding=utf-8
'''
Created on 2016年9月23日
庄家规则
@author: zhaol
'''
from majiang2.ai.play_mode import MPlayMode
from majiang2.win_loose_result.luosihu_one_result import MLuosihuOneResult
from majiang2.win_loose_result.one_result import MOneResult
from majiang2.win_loose_result.queshou_one_result import MQueshouOneResult
class MOneResultFactory(object):
    def __init__(self):
        super(MOneResultFactory, self).__init__()
    
    @classmethod
    def getOneResult(cls, playMode):
        """判和规则获取工厂
        输入参数：
            playMode - 玩法
        
        返回值：
            对应玩法的判和规则
        """
        if MPlayMode().isSubPlayMode(playMode, MPlayMode.LUOSIHU):
	    oneResultObj =  MLuosihuOneResult()
            oneResultObj.setPlayMode(playMode)
            return oneResultObj
        elif MPlayMode().isSubPlayMode(playMode, MPlayMode.QUESHOU):
            return MQueshouOneResult() 
        return MOneResult()
