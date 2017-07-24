# -*- coding=utf-8
'''
Created on 2016年9月23日

@author: zhaol
'''

class MPlayMode(object):
    # 最简单的麻将玩法
    SIMPLE = 'simple'
    # 1) 新疆玩法
    LUOSIHU = 'luosihu'
    # 2) 福州玩法
    QUESHOU = "queshou"
    def __init__(self):
        super(MPlayMode, self).__init__()
        
    def isSubPlayMode(self, curPlayMode, defPlayMode):
        if curPlayMode.find('-') >= 0:
            # 为支持各种玩法自类型，例如，随州卡五星定义为luosihu-suizhou
            return curPlayMode.split('-')[0] == defPlayMode
        else:
            return curPlayMode == defPlayMode
