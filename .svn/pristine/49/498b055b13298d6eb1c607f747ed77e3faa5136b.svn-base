# -*- coding=utf-8
'''
Created on 2016年9月23日

@author: zhaol
'''
from majiang2.tile.tile import MTile
from freetime.util import log as ftlog

class MChi(object):
    """是否可以杠
    
    例子：
    [[2, 3, 4], [3, 4, 5], [4, 5, 6]]
    """
    
    def __init__(self):
        super(MChi, self).__init__()
        
    @classmethod
    def hasChi(cls, tiles, tile):
        """是否可以吃
        吃牌的判断中，tile已经在tiles中
        参数：
            tiles - 手牌
            tile - 待吃的牌
        返回值：吃牌选择
            最多三种解
            
        例子：
            [[2, 3, 4], [3, 4, 5], [4, 5, 6
        """
        tileArr = MTile.changeTilesToValueArr(tiles)
        result = []
	
        # 第一种情况 001
        if (tile % 10) >= 3:
            if tileArr[tile - 2] > 0 and tileArr[tile - 1] > 0 and tileArr[tile] > 0:
                solution = [tile - 2, tile - 1, tile]
                result.append(solution)
        '''
        # 第三种情况 100
        if (tile % 10) < 8:
            if tileArr[tile] > 0 and tileArr[tile + 1] > 0 and tileArr[tile + 2] > 0:
                solution = [tile, tile + 1, tile + 2]
                result.append(solution)
	'''
        # 第二种情况 010
        if (tile % 10) >= 2 and (tile % 10) < 9:
            if tileArr[tile - 1] > 0 and tileArr[tile] > 0 and tileArr[tile + 1] > 0:
                solution = [tile - 1, tile, tile + 1]
                result.append(solution)
	        
        # 第三种情况 100
        if (tile % 10) < 8:
            if tileArr[tile] > 0 and tileArr[tile + 1] > 0 and tileArr[tile + 2] > 0:
                solution = [tile, tile + 1, tile + 2]
                result.append(solution)
   	'''     
        # 第一种情况 001
        if (tile % 10) >= 3:
            if tileArr[tile - 2] > 0 and tileArr[tile - 1] > 0 and tileArr[tile] > 0:
                solution = [tile - 2, tile - 1, tile]
                result.append(solution) 
        '''
        return result
    
if __name__ == "__main__":
    tiles = [1, 2, 3, 2, 3, 4, 3, 4, 5, 4, 5, 6, 5]
    result = MChi.hasChi(tiles, 4)
    ftlog.debug( result )
