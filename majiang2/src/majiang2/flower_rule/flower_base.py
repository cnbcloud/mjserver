# -*- coding=utf-8
'''
Created on 2017年6月7日

@author: youjun
'''

from majiang2.tile.tile import MTile

class MFlowerRuleBase(object):
    """
    花牌判断
    """
    
    def __init__(self):
        super(MFlowerRuleBase, self).__init__()

    def hasFlower(self, tiles):
        flowers =[]
        for tile in tiles:
            if self.isFlower(tile):
                flowers.append(tile)

        return flowers
    
    def isFlower(self,tile):
        flowers = [MTile.TILE_FLOWER_CHUN, MTile.TILE_FLOWER_XIA, MTile.TILE_FLOWER_QIU,MTile.TILE_FLOWER_DONG,MTile.TILE_FLOWER_MEI,MTile.TILE_FLOWER_LAN,MTile.TILE_FLOWER_ZHU,MTile.TILE_FLOWER_JU,]
        return tile in flowers

    def getAllFlowers(self, players):
        flowers = [None for _ in range(len(players))]
        for player in players:
            flowers[player.curSeatId] = self.hasFlower(player.copyHandTiles())
        return flowers

    def getFlowerCount(self, flowers):
        count = 0
        for f in flowers:
            count += len(f)
        return count
