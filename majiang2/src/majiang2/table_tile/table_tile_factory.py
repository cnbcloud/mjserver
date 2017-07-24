# -*- coding=utf-8
'''
Created on 2016年9月23日
庄家规则
@author: zhaol
'''
from majiang2.ai.play_mode import MPlayMode
from majiang2.table.run_mode import MRunMode
from majiang2.tile.tile import MTile
from majiang2.table_tile.table_tile import MTableTile
from majiang2.table_tile.table_tile_luosihu import MTableTileLuosihu
from majiang2.table_tile.table_tile_queshou import MTableTileQueshou
class MTableTileFactory(object):
    def __init__(self):
        super(MTableTileFactory, self).__init__()
    
    @classmethod
    def getTableTileMgr(cls, playerCount, playMode, runMode):
        """牌桌手牌管理器获取工厂
        输入参数：
            playMode - 玩法      
        返回值：
            对应玩法手牌管理器
        """
        if MPlayMode().isSubPlayMode(playMode, MPlayMode.LUOSIHU):
            return MTableTileLuosihu(playerCount, playMode, runMode)
        elif MPlayMode().isSubPlayMode(playMode, MPlayMode.QUESHOU):
            return MTableTileQueshou(playerCount, playMode, runMode)
        return MTableTile(playerCount, playMode, runMode)

if __name__ == "__main__":
    tableTileMgr = MTableTileFactory.getTableTileMgr(4, MPlayMode.LUOSIHU, MRunMode.CONSOLE)
    tableTileMgr.tileTestMgr.setHandTiles([[5, 5, 5, 5], [6, 6, 6, 6], [7, 7, 7, 7], [8, 8, 8, 8]])
    tableTileMgr.tileTestMgr.setTiles([9, 9, 9, 9])
    tableTileMgr.shuffle(0, 13)
    tiles = tableTileMgr.tiles
    print tiles
    
    tileArr = MTile.changeTilesToValueArr(tiles)
    print tileArr
