# -*- coding=utf-8
'''
Created on 2016年9月23日

@author: zhaol
'''
from majiang2.table.run_mode import MRunMode

class MsgFactory(object):
    
    def __init__(self):
        super(MsgFactory, self).__init__()
    
    @classmethod
    def getMsgProcessor(cls, runMode):
        """发牌器获取工厂
        输入参数：
            playMode - 玩法
        
        返回值：
            对应玩法的发牌算法
        """
        if runMode == MRunMode.CONSOLE:
            from majiang2.msg_handler.msg_console import MMsgConsole
            return MMsgConsole()
        elif runMode == MRunMode.LONGNET:
            from majiang2.msg_handler.msg_longnet import MMsgLongNet
            return MMsgLongNet()