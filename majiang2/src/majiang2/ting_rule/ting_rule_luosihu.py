# -*- coding=utf-8
'''
Created on 2016年9月23日
听牌规则
@author: zhaol
'''
from majiang2.ai.ting import MTing
from majiang2.ting_rule.ting_rule import MTingRule
from majiang2.win_rule.win_rule_luosihu import MWinRuleLuosihu
from majiang2.tile.tile import MTile
from freetime.util import log as ftlog

class MTingLuosihuRule(MTingRule):
    """胡牌规则，此处听牌和亮牌一个含义
    """
    def __init__(self):
        super(MTingLuosihuRule, self).__init__()
    
    def canTing(self, tiles, leftTiles, tile, magicTiles = [], curSeatId = 0, winSeatId = 0, actionID = 0):
        #if self.tableTileMgr.playMode == 'luosihu-suizhou' or self.tableTileMgr.playMode == 'luosihu-luosihu':
            #小于12张可以显示听牌
            #if len(leftTiles) < 12:
                # 随州和孝感小于12张不能亮牌/听牌
            #    return False, []
        isTing, tingResults = MTing.canTing(MTile.cloneTiles(tiles), leftTiles, self.winRuleMgr, tile, magicTiles, curSeatId, winSeatId, actionID)
        ftlog.debug( 'MTingLuosihuRule.canTing using MTing isTing:', isTing, ' tingResults:', tingResults )
        
        #if not self.tableTileMgr:
        #    # 用于单元测试，正常情况下都有tableTileMgr
        return isTing, tingResults

        finalTingResults = []
        if isTing:
            # 听牌时，要丢弃的牌必须要过滤掉别人要胡的牌，如果都被滤掉了，就不能听牌
            for tingResult in tingResults:
                resultOk = True
                for player in self.tableTileMgr.players:
                    if player.curSeatId != winSeatId:
                        if player.tingLiangWinTiles:
                            if tingResult['dropTile'] and player.tingLiangWinTiles \
                                    and tingResult['dropTile'] in player.tingLiangWinTiles:
                                ftlog.debug( 'MTingLuosihuRule.canTing drop tile: ', tingResult['dropTile'], ' is forbidden by player: ', player.curSeatId)
                                resultOk = False
                                break
                if resultOk:
                    for wn in tingResult['winNodes']:
                        allWinTiles = []
                        for p in wn['pattern']:
                            allWinTiles.extend(p)
                        tileCountArr = MTile.changeTilesToValueArr(MTile.cloneTiles(allWinTiles))
                        #canKouTiles = []
                        #for p in wn['pattern']:
                        #    if len(p) == 2:
                        #        continue
                        #    if p[0] == p[1] and p[1] == p[2]:
                        #        if tileCountArr[p[0]] == 4 and p[0] != wn['winTile']:
                        #            # 手上已经有四张了（去掉winTile），不能扣牌
                        #            continue
                        #        if (p[0] != wn['winTile'] or (p[0] == wn['winTile'] and tileCountArr[p[0]] == 4)) and p[0] not in canKouTiles:
                        #            # 手上只有3张一样的牌，或者手上有4张一样的牌（包含winTile）
                        #            canKouTiles.append(p[0])
                        # 此处为引用，原有tingResults在每个winNode增加canKouTiles
                        #wn['canKouTiles'] = canKouTiles
                        #ftlog.debug( 'MTingLuosihuRule.canTing winNode: ', wn, ' ,current allWinTiles: ', allWinTiles)
                    finalTingResults.append(tingResult)

        ftlog.debug( 'MTingLuosihuRule.canTing using after liang filter tingResults:', finalTingResults )
        if len(finalTingResults) > 0:
            return True, finalTingResults
        else:
            return False, []

    def canTingAfterPeng(self, tiles):
        """"碰之后是否可以马上听牌"""
        # 和抢听是矛盾的，非抢听情况下，卡五星玩家正常碰牌后，应马上弹出听牌按钮
        return True

if __name__ == "__main__":
    tiles = [[11,11,13,13,15,15,18,18,19,19,22,22,24,29], [], [], [], [], []]
    rule = MTingLuosihuRule()
    rule.setWinRuleMgr(MWinRuleLuosihu())
    isTing, tingResults = rule.canTing(tiles, [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], 22, [])
    ftlog.debug(isTing, tingResults)
    assert True == isTing
    isTing, tingResults = rule.canTing(tiles, [0,0,0,0], 22, [])
    ftlog.debug(isTing, tingResults)
    assert False == isTing
