# -*- coding=utf-8
'''
Created on 2016年9月23日
听牌规则
@author: zhaol
'''
from majiang2.player.hand.hand import MHand
from majiang2.tile.tile import MTile
from majiang2.table_state.state import MTableState
from majiang2.ai.peng import MPeng
from majiang2.table_tile.table_tile_factory import MTableTileFactory
from majiang2.ai.play_mode import MPlayMode
from freetime.util import log as ftlog
import copy

class MPengRule(object):
    """碰牌判断"""
    
    def __init__(self):
        super(MPengRule, self).__init__()
        self.__table_tile_mgr = None
        
    @property
    def tableTileMgr(self):
        return self.__table_tile_mgr
    
    def setTableTileMgr(self, tableTileMgr):
        self.__table_tile_mgr = tableTileMgr
        
    def hasPeng(self, tiles, tile, seatId=-1):
        """是否有碰牌解
        
        参数说明；
        tiles - 玩家的所有牌，包括手牌，吃牌，碰牌，杠牌，胡牌
        tile - 待碰的牌
        """
        
        #是否允许会牌参与,如果不允许，删除会牌
        tilesForPeng = copy.deepcopy(tiles[MHand.TYPE_HAND])
        if not self.tableTileMgr.allowMagicChiPengGang():
            magicTile = self.tableTileMgr.getMagicTile()
            while magicTile in tilesForPeng:
                tilesForPeng.remove(magicTile)
                
                
        pengSolutions = []
        normalPeng = MPeng.hasPeng(tilesForPeng, tile)
        if normalPeng:
            pengSolutions.append([tile, tile, tile])
            
        magics = self.tableTileMgr.getMagicTiles(False)
        tileArr = MTile.changeTilesToValueArr(tiles[MHand.TYPE_HAND])
        tileArr, magicTiles = self.tableTileMgr.exculeMagicTiles(tileArr, magics)
        magicCount = len(magicTiles)
        if magicCount == 0:
            return pengSolutions
        
        if not self.tableTileMgr.canUseMagicTile(MTableState.TABLE_STATE_PENG):
            return pengSolutions
        
        ftlog.debug('MPengRule.hasPeng tile:', tile
                    , ' tileCount:', tileArr[tile]
                    , ' magicCount:', magicCount)
        
        if (magicCount == 0) or (tileArr[tile] == 0):
            return pengSolutions
        
        if magicCount >= 1 and tileArr[tile] >= 2:
            # 使用一个癞子
            pengSolutions.append([tile, tile, magicTiles[0]])
            
        if magicCount >= 2 and tileArr[tile] >= 1:
            # 使用两个癞子
            pengSolutions.append([tile, magicTiles[0], magicTiles[1]])
            
        return pengSolutions
    
if __name__ == "__main__":
    tiles = [[4, 4, 7, 8, 11, 12, 21, 21], [29, 29, 29], [28, 28, 28, 28], [], []]
    tileMgr = MTableTileFactory.getTableTileMgr(4, MPlayMode.LUOSIHU)
    pengRuler = MPengRule()
    pengRuler.setTableTileMgr(tileMgr)
    
    result = pengRuler.hasPeng(tiles, 21)
    ftlog.debug( result )
