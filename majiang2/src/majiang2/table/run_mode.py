# -*- coding=utf-8
'''
Created on 2016年9月23日

@author: zhaol
'''

class MRunMode(object):
    # 命令行模式
    CONSOLE = 1
    # 联网模式
    LONGNET = 2
    
    def __init__(self):
        super(MRunMode, self).__init__()