# -*- coding=utf-8
'''
Created on 2017年6月7日

@author: youjun
'''
from majiang2.flower_rule.flower_base import MFlowerRuleBase
from majiang2.tile.tile import MTile

class MFlowerRuleQueshou(MFlowerRuleBase):
    """
    花牌判断
    """
    
    def __init__(self):
        super(MFlowerRuleQueshou, self).__init__()

    def hasFlower(self, tiles):
        flowers =[]
        for tile in tiles:
            if self.isFlower(tile):
                flowers.append(tile)

        return flowers
    
    def isFlower(self,tile):
        return tile > 30

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
