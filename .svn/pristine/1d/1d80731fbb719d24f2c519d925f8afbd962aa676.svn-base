# -*- coding=utf-8
'''
Created on 2016年9月23日

@author: zhaol
'''
from majiang2.tile.tile import MTile
from majiang2.player.hand.hand import MHand
from freetime.util import log as ftlog

class MTileValue(object):
    """计算麻将牌的价值
    """
    
    def __init__(self):
        super(MTileValue, self).__init__()
        
    @classmethod
    def getBestChiPattern(cls, tiles, tiles_left, chiPatterns):
        """选择最佳的吃牌方案
        
        特殊说明：加上吃牌再比较
        """
        bestValue = 0
        chiChoise = []
        for chiSolution in chiPatterns:
            for tile in chiSolution:
                tiles[MHand.TYPE_HAND].remove(tile)
            left_tiles_value_arr, _ = cls.getHandTilesValue(tiles, tiles_left)
            leftValue = 0
            for itemValue in left_tiles_value_arr:
                leftValue += itemValue
            if bestValue < leftValue:
                bestValue = leftValue
                chiChoise = chiSolution
            for tile in chiSolution:
                tiles[MHand.TYPE_HAND].append(tile)
                
        ftlog.debug('best chiChoice:', chiChoise, ' value:', bestValue)
        return chiChoise, bestValue
        
    @classmethod
    def getHandTilesValue(cls, tiles_player_hand, tiles_left):
        """计算手牌价值
        
        返回值：
        1）每张牌的价值
        2）手牌花色个数的数组
        """
        tiles_player_Arr = MTile.changeTilesToValueArr(tiles_player_hand[MHand.TYPE_HAND])
        tiles_left_Arr = MTile.changeTilesToValueArr(tiles_left)
                
        # 权值初始化    
        tiles_value_Arr = [0 for _ in range(40)]
        for index in range(MTile.TILE_MAX_VALUE):
            if tiles_player_Arr[index] == 0:
                continue
            tiles_value_Arr[index] = tiles_player_Arr[index] * 4 + tiles_left_Arr[index]
            if index < 30:
                if index % 10 < 9:
                    tiles_value_Arr[index] += tiles_player_Arr[index + 1] * 3
                if index % 10 < 8:
                    tiles_value_Arr[index] += tiles_player_Arr[index + 2] * 2
                if index % 10 > 1:
                    tiles_value_Arr[index] += tiles_player_Arr[index - 1] * 3
                if index % 10 > 2:
                    tiles_value_Arr[index] += tiles_player_Arr[index - 2] * 2
                    
        return tiles_value_Arr, tiles_player_Arr
        
    @classmethod
    def getBestDropTile(cls, tiles_player_hand, tiles_left, playMode, tile, isTing, magicTiles, tingRule=None,isWin=False):
        """
        手牌的价值，根据玩家自己的手牌和已经出的牌，计算手牌价值
        参数：
            tiles_player_hand - 用户的手牌
            tiles_droped - 牌桌上已经打出的牌和玩家手里已经成型的牌，这部分牌不再参与计算牌的可能性
        计算方法：
        1）没有的手牌，权值为0
        2）有的手牌，初始权值为4 * count + 1 * left
        3）左右相邻的手牌，增加权重 3 * count
        4）左右隔一张的手牌，增加权重 2 * count
        """
        ftlog.debug( 'MTileValue.getBestDropTile tiles_player_hand:', tiles_player_hand )
        ftlog.debug( 'MTileValue.getBestDropTile tiles_left:', tiles_left )
        ftlog.debug( 'MTileValue.getBestDropTile playMode:', playMode )
        ftlog.debug( 'MTileValue.getBestDropTile tile:', tile )
        ftlog.debug( 'MTileValue.getBestDropTile isTing:', isTing )
        ftlog.debug( 'MTileValue.getBestDropTile magicTiles:', magicTiles )
        ftlog.debug( 'MTileValue.getBestDropTile tingRule:', tingRule )
	ftlog.debug( 'MTileValue.getBestDropTile isWin:', isWin )  
        # modify by youjun 05.04 
        if isTing:
            # 听牌后，直接打出摸到的牌
            return tile, 0
        if isWin:
            return tile, 0
        
        tiles_value_Arr, tiles_player_Arr = cls.getHandTilesValue(tiles_player_hand, tiles_left)
        for mTile in magicTiles:
            tiles_value_Arr[mTile] = tiles_value_Arr[mTile] * 100
                    
        # [{'dropTile': 11, 'winNodes': [{'winTile': 1, 'winTileCount': 3, 'pattern': [[6, 6], [5, 6, 7], [4, 5, 6], [1, 2, 3]]}, {'winTile': 2, 'winTileCount': 2, 'pattern': [[6, 6, 6], [5, 6, 7], [3, 4, 5], [2, 2]]}, {'winTile': 4, 'winTileCount': 3, 'pattern': [[6, 6], [5, 6, 7], [4, 5, 6], [2, 3, 4]]}, {'winTile': 5, 'winTileCount': 2, 'pattern': [[6, 6, 6], [5, 6, 7], [5, 5], [2, 3, 4]]}, {'winTile': 7, 'winTileCount': 1, 'pattern': [[6, 6], [5, 6, 7], [5, 6, 7], [2, 3, 4]]}, {'winTile': 8, 'winTileCount': 1, 'pattern': [[6, 7, 8], [6, 6, 6], [5, 5], [2, 3, 4]]}]}]
        if tingRule:
            canTing, tingResults = tingRule.canTing(tiles_player_hand, tiles_left, tile, magicTiles)
            ftlog.debug( canTing )
            ftlog.debug( tingResults )
            
            if canTing:
                for tingResult in tingResults:
                    dropTile = tingResult['dropTile']
                    winNodes = tingResult['winNodes']
                    outs = 0
                    for winNode in winNodes:
                        outs += winNode['winTileCount']
                    tiles_value_Arr[dropTile] = (0 - outs)
         
        minTile = 0
        minValue = 0  
        for index in range(MTile.TILE_MAX_VALUE):
            if tiles_player_Arr[index] > 0:
                if minTile == 0:
                    minTile = index
                    minValue = tiles_value_Arr[index]
                    continue
                
                if minValue > tiles_value_Arr[index]:
                    minValue = tiles_value_Arr[index]
                    minTile = index
                
        return minTile, tiles_value_Arr[minTile]
    
if __name__ == "__main__":
    #tiles = [1, 2, 3, 2, 3, 4, 3, 4, 5, 4, 5, 6, 5]
    #result = MTileValue.hasChi(tiles, 4)
    #ftlog.debug( result )
    tiles = [[3, 5, 6, 7, 11, 12, 14, 14, 34, 34, 21], [], [], [], [], []]
    tileLeft = [19, 15, 21, 14, 18, 9, 26, 22, 13, 23, 16, 5, 12, 35, 5, 5, 27, 24, 25, 29, 9, 12, 8, 9, 24, 7, 28, 24, 13, 7, 14, 25, 11]
    playMode = 'yunnan'
    tile = 21
    print MTileValue.getBestDropTile(tiles, tileLeft, playMode, tile, False, [21])
    
