# -*- coding=utf-8
'''
Created on 2016年9月23日

@author: zhaol
'''
from majiang2.tile.tile import MTile
from freetime.util import log as ftlog

class MGang(object):
    """是否可以杠
    """
    
    def __init__(self):
        super(MGang, self).__init__()
        
    @classmethod
    def hasAnGang(cls, tiles, tile):
        """自摸是否可以暗杠
        判断杠牌时，tile已经加入tiles中
        tiles - 手牌
        tile - 待杠的牌
        """
        tileArr = MTile.changeTilesToValueArr(tiles)
        if tileArr[tile] == 4:
            return True
        return False
        
if __name__ == "__main__":
    tiles = [1, 2, 3, 2, 3, 4, 3, 4, 5, 4, 5, 6, 5, 5]
    ftlog.debug( MGang.hasGang(tiles, 4) )