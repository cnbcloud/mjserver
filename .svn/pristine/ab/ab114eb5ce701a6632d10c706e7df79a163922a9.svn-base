# -*- coding=utf-8
'''
Created on 2016年9月23日

@author: zhaol
'''
import copy

class MHand(object):
    # 握在手里的牌，未吃/碰/杠的牌
    TYPE_HAND = 0
    # 吃牌
    TYPE_CHI = 1
    # 碰牌
    TYPE_PENG = 2
    # 明杠牌
    TYPE_GANG = 3
    # 锚蛋牌
    TYPE_MAO = 4
    # 和牌
    TYPE_HU = 5
    # 最新的一手牌
    TYPE_CUR = 6
    # 亮出去的花牌
    TYPE_SHOW_FLOWERS = 7
    # 类别总数
    TYPE_COUNT = 8
    
    def __init__(self):
        super(MHand, self).__init__()
        
    @classmethod
    def copyAllTilesToList(cls, tiles):
        """
        拷贝所有的手牌到一个list内
        """
        newTiles = copy.deepcopy(tiles)
        
        re = []
        re.extend(newTiles[cls.TYPE_HAND])
        for chi in newTiles[cls.TYPE_CHI]:
            re.extend(chi)
            
        for peng in newTiles[cls.TYPE_PENG]:
            re.extend(peng)
         
        for gang in newTiles[cls.TYPE_GANG]:    
            re.extend(gang['pattern'])
          
        for mao in newTiles[cls.TYPE_MAO]:
            re.extend(mao['pattern'])
                
        re.extend(newTiles[cls.TYPE_HU])
        return re
    
    @classmethod
    def copyAllTilesToListButHu(cls, tiles):
        """
        拷贝所有的手牌到一个list内 除去胡
        """
        newTiles = copy.deepcopy(tiles)
        
        re = []
        re.extend(newTiles[cls.TYPE_HAND])
        for chi in newTiles[cls.TYPE_CHI]:
            re.extend(chi)
            
        for peng in newTiles[cls.TYPE_PENG]:
            re.extend(peng)
         
        for gang in newTiles[cls.TYPE_GANG]:    
            re.extend(gang['pattern'])
          
        for mao in newTiles[cls.TYPE_MAO]:
            re.extend(mao['pattern'])

        return re

    @classmethod
    def copyAllTilesToListButMao(cls, tiles):
        """
        拷贝所有的手牌到一个list内 除去锚
        """
        newTiles = copy.deepcopy(tiles)

        re = []
        re.extend(newTiles[cls.TYPE_HAND])
        for chi in newTiles[cls.TYPE_CHI]:
            re.extend(chi)

        for peng in newTiles[cls.TYPE_PENG]:
            re.extend(peng)

        for gang in newTiles[cls.TYPE_GANG]:
            re.extend(gang['pattern'])

        re.extend(newTiles[cls.TYPE_HU])

        return re