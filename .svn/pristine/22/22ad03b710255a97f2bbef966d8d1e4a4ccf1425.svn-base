#! -*- coding:utf-8 -*-
# Author:   youjun
# Created:  2017/5/16

from majiang2.peng_rule.peng_rule import MPengRule
from majiang2.ai.peng import MPeng
from majiang2.player.hand.hand import MHand


class MPengRuleLuoSiHu(MPengRule):
    """怀宁麻将碰规则
    """

    def __init__(self):
        super(MPengRuleLuoSiHu, self).__init__()

    def hasPeng(self, tiles, tile, seatId=-1):
        """是否有碰牌解

        参数说明；
        tiles - 玩家的所有牌，包括手牌，吃牌，碰牌，杠牌，胡牌
        tile - 待碰的牌
        """
        pengSolutions = []

        # 过碰状态，还碰这张牌不让碰
        p = self.tableTileMgr.players[seatId]
        if tile in p.guoPengTiles:
            return pengSolutions

        # 手牌里加上这张牌>=3张，可以碰
        normalPeng = MPeng.hasPeng(tiles[MHand.TYPE_HAND], tile)
        if normalPeng:
            pengSolutions.append([tile, tile, tile])
        return pengSolutions
