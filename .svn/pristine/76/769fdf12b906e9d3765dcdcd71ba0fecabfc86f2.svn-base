# -*- coding=utf-8
'''
Created on 2016年9月23日
庄家规则
@author: zhaol
'''
from majiang2.win_rule.win_rule import MWinRule
from majiang2.ai.win import MWin
from majiang2.player.hand.hand import MHand

class MWinRuleSimple(MWinRule):
    """开局随机庄家，之后连庄的规则
    庄家赢，连庄
    闲家赢，闲家坐庄
    """
    def __init__(self):
        super(MWinRuleSimple, self).__init__()
    
    def isHu(self, tiles, tile, isTing, getTileType, magicTiles = [], tingNodes = [], curSeatId = 0, winSeatId = 0, actionID = 0, isGangKai = False):
        result, pattern = MWin.isHu(tiles[MHand.TYPE_HAND], magicTiles)
        return result, pattern