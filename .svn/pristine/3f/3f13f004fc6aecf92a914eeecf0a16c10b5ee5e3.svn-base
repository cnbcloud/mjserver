# -*- coding=utf-8
'''
Created on 2016年9月23日

@author: zhaol
'''
from majiang2.tile.tile import MTile
from freetime.util import log as ftlog

class MPeng(object):
    """是否可以碰
    """
    
    def __init__(self):
        super(MPeng, self).__init__()
        
    @classmethod
    def hasPeng(cls, tiles, tile):
        """是否可以碰
        判断之前tile已经加到tiles中
        tiles - 手牌
        tile - 待碰的牌
        """
        tileArr = MTile.changeTilesToValueArr(tiles)
        if tileArr[tile] >= 3:
            return True
        return False
    
if __name__ == "__main__":
    tiles = [1, 2, 3, 2, 3, 4, 3, 4, 5, 4, 5, 6, 5, 5]
    ftlog.debug( MPeng.hasPeng(tiles, 5) )