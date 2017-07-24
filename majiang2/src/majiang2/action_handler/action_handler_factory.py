# -*- coding=utf-8
'''
Created on 2016年9月23日

@author: zhaol
'''
from majiang2.action_handler.action_handler_console import ActionHandlerConsole
from majiang2.action_handler.action_handler_longnet import ActionHandlerLongNet
from majiang2.table.run_mode import MRunMode

class ActionHandlerFactory(object):
    
    def __init__(self):
        super(ActionHandlerFactory, self).__init__()
    
    @classmethod
    def getActionHandler(cls, runMode):
        """发牌器获取工厂
        输入参数：
            playMode - 玩法
        
        返回值：
            对应玩法的发牌算法
        """
        if runMode == MRunMode.CONSOLE:
            return ActionHandlerConsole()
        elif runMode == MRunMode.LONGNET:
            return ActionHandlerLongNet()