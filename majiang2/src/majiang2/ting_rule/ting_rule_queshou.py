# -*- coding=utf-8
'''
Created on 2017年6月6日
听牌规则
@author: youjun
'''
from majiang2.ai.ting import MTing
from majiang2.ting_rule.ting_rule import MTingRule
from majiang2.win_rule.win_rule_queshou import MWinRuleQueshou
from majiang2.tile.tile import MTile
from freetime.util import log as ftlog

class MTingQueshouRule(MTingRule):
    """胡牌规则
    """
    def __init__(self):
        super(MTingQueshouRule, self).__init__()
	self.__flower_rule = None   
 
    def canTing(self, tiles, leftTiles, tile, magicTiles = [], curSeatId = 0, winSeatId = 0, actionID = 0):
        isTing, tingResults = MTing.canTing(MTile.cloneTiles(tiles), leftTiles, self.winRuleMgr, tile, magicTiles, curSeatId, winSeatId, actionID,False,self.flowerRule)
        ftlog.debug( 'MTingQueshouRule.canTing using MTing isTing:', isTing, ' tingResults:', tingResults )
        
        return isTing, tingResults

    def canTingForQiangjin(self, tiles, leftTiles, tile, magicTiles = [], curSeatId = 0, winSeatId = 0, actionID = 0,tingForQiangjin = True):
        isTing, tingResults = MTing.canTing(MTile.cloneTiles(tiles), leftTiles, self.winRuleMgr, tile, magicTiles, curSeatId, winSeatId, actionID,tingForQiangjin,self.flowerRule)
        ftlog.debug( 'MTingQueshouRule.canTingForQiangjin using MTing isTing:', isTing, ' tingResults:', tingResults) 
	return isTing, tingResults

    def canTingForQiangjinBeforeAddTile(self, tiles, leftTiles, magicTiles = [], curSeatId = 0, winSeatId = 0, actionID = 0,tingForQiangjin = True):
        return MTing.canTingBeforeAddTile(tiles, leftTiles, self.winRuleMgr, magicTiles, curSeatId, winSeatId, actionID,tingForQiangjin,self.flowerRule)

    def setFlowerRule(self,flowerRule):
        self.__flower_rule = flowerRule

    @property
    def flowerRule(self):
        return self.__flower_rule

    def canTingAfterPeng(self, tiles):
        """"碰之后是否可以马上听牌"""
        return True

if __name__ == "__main__":
    tiles = [[11,11,13,13,15,15,18,18,19,19,22,22,24,29], [], [], [], [], []]
    rule = MTingQueshouRule()
    rule.setWinRuleMgr(MWinRuleQueshou())
    isTing, tingResults = rule.canTing(tiles, [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], 22, [])
    ftlog.debug(isTing, tingResults)
    assert True == isTing
    isTing, tingResults = rule.canTing(tiles, [0,0,0,0], 22, [])
    ftlog.debug(isTing, tingResults)
    assert False == isTing
