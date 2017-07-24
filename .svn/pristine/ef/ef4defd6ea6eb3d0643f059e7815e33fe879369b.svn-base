# -*- coding=utf-8
'''
Created on 2016年9月23日

@author: zhaol
'''
from majiang2.ai.mao import MMao

class MMaoRuleBase(object):
    """是否可以杠
    
    例子：
    [[2, 3, 4], [3, 4, 5], [4, 5, 6]]
    """
    
    def __init__(self):
        super(MMaoRuleBase, self).__init__()
        
    def checkMao(self, pattern, maoType, maoDanSetting):
        return MMao.checkMao(pattern, maoType, maoDanSetting)
        
    def hasMao(self, tiles, maoDanSetting, alreadyHave = 0,isFirstAddtile=False,hasPengMao={}):
        mao = MMao.hasMao(tiles, maoDanSetting, alreadyHave)
        # todo 根据自己的玩法过滤结果
        return mao
    
    def hasExtendMao(self, tiles, alreadyHave = 0):
        exMao = MMao.hasExtendMao(tiles, alreadyHave)
        return exMao

    def checkPengMao(self, tile, maoDanSetting, maoTiles):
        return MMao.checkPengMao(tile, maoDanSetting, maoTiles)
