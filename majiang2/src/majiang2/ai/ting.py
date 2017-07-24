# -*- coding=utf-8
'''
Created on 2016年9月23日

@author: zhaol
'''
from majiang2.tile.tile import MTile
from majiang2.ai.play_mode import MPlayMode
from majiang2.win_rule.win_rule_factory import MWinRuleFactory
from majiang2.player.hand.hand import MHand
from freetime.util import log as ftlog
from majiang2.win_rule.win_rule import MWinRule
import datetime
"""
结果样例：
[{'dropTile': 11, 'winNodes': [{'winTile': 1, 'winTileCount': 3, 'pattern': [[6, 6], [5, 6, 7], [4, 5, 6], [1, 2, 3]]}, {'winTile': 2, 'winTileCount': 2, 'pattern': [[6, 6, 6], [5, 6, 7], [3, 4, 5], [2, 2]]}, {'winTile': 4, 'winTileCount': 3, 'pattern': [[6, 6], [5, 6, 7], [4, 5, 6], [2, 3, 4]]}, {'winTile': 5, 'winTileCount': 2, 'pattern': [[6, 6, 6], [5, 6, 7], [5, 5], [2, 3, 4]]}, {'winTile': 7, 'winTileCount': 1, 'pattern': [[6, 6], [5, 6, 7], [5, 6, 7], [2, 3, 4]]}, {'winTile': 8, 'winTileCount': 1, 'pattern': [[6, 7, 8], [6, 6, 6], [5, 5], [2, 3, 4]]}]}]
"""
class MTing(object):
    """是否可以听牌
    如果可以听牌，可以和哪些牌
    判断流程：
    去掉一张手牌，加入一张牌，是否可以和
    如果可以和，去掉改手牌，进入听牌状态，和可以和的牌。可以和的牌会有多个
    
    对可以和的牌，提示剩余牌的张数
    """
    
    def __init__(self):
        super(MTing, self).__init__()
        
    @classmethod    
    def chooseBestTingSolution(cls, tingReArr):
        """选择最好的听牌方案"""
        chooseTile = 0
        maxCount = 0
        chooseWinNodes = []
        for tingSolution in tingReArr:
            dropTile = tingSolution['dropTile']
            winNodes = tingSolution['winNodes']
            count = 0
            for node in winNodes:
                winTileCount = node['winTileCount']
                count += winTileCount
            if count > maxCount:
                maxCount = count
                chooseTile = dropTile
                chooseWinNodes = winNodes
                
        return chooseTile, chooseWinNodes
    
    @classmethod
    def canTingBeforeAddTile(cls, tiles, leftTiles, winRule, magicTiles = [], curSeatId = 0, winSeatId = 0, actionID = 0,tingForQiangjin = False,flowerRule = None):
        """判断在摸牌之前是否可以听
        """
        #ftlog.debug('MTile.changeTilesToValueArr', tiles[MHand.TYPE_HAND])
        leftTileArr = MTile.changeTilesToValueArr(leftTiles)
        leftTileCount = len(leftTileArr)
        '''
	ftlog.debug('MTing.canTingBeforeAddTile leftTiles:', leftTiles
                     , ' leftTileArr:', leftTileArr
                     , ' leftTileCount:', leftTileCount)
        '''
        result = []
        resultNode = cls.canWinAddOneTile(leftTileArr, leftTileCount, tiles, winRule, magicTiles, curSeatId, winSeatId, actionID,tingForQiangjin,flowerRule)
        if len(resultNode) > 0:
            winNode = {}
            winNode['winNodes'] = resultNode
            result.append(winNode)
            if tingForQiangjin:
                return len(result) > 0, result    
        return len(result) > 0, result
    
    @classmethod
    def canTing(cls, tiles, leftTiles, winRule, tile, magicTiles = [], curSeatId = 0, winSeatId = 0, actionID = 0,tingForQiangjin = False,flowerRule = None):
        """
        判断是否可以听牌
        参数：
        1）tiles 手牌
        2）leftTiles 剩余未发的牌
        3) tingForQiangjin 是否是抢金,当是判断抢金时，有可听的结果就返回  modify by youjun
        返回值：
        
        """
        handTileArr = MTile.changeTilesToValueArr(tiles[MHand.TYPE_HAND])
        
        leftTileArr = MTile.changeTilesToValueArr(leftTiles)
        leftTileCount = len(leftTileArr)
        '''
	ftlog.debug('MTing.canTing leftTiles:', leftTiles
                     , ' leftTileArr:', leftTileArr
                     , ' leftTileCount:', leftTileCount)
        '''
        result = []
        for tile in range(MTile.TILE_MAX_VALUE):
            if handTileArr[tile] > 0:
                newTiles = MTile.cloneTiles(tiles)
                newTiles[MHand.TYPE_HAND].remove(tile)
                resultNode = cls.canWinAddOneTile(leftTileArr, leftTileCount, newTiles, winRule, magicTiles, curSeatId, winSeatId, actionID,tingForQiangjin,flowerRule)
                if len(resultNode) > 0:
                    winNode = {}
                    winNode['dropTile'] = tile
                    winNode['winNodes'] = resultNode
		    result.append(winNode)
        	    if tingForQiangjin:
                        return len(result) > 0, result 
        return len(result) > 0, result
    
    @classmethod
    def canWinAddOneTile(cls, leftTileArr, leftTileCount, tiles, winRule, magicTiles = [], curSeatId = 0, winSeatId = 0, actionID = 0,tingForQiangjin = False,flowerRule = None):
        """
        tingForQiangjin 是否是抢金,当是判断抢金时，有可听的结果就返回  modify by youjun
        """ 
        result = []
        if len(magicTiles):
            testTile = MTile.cloneTiles(tiles)
            testTile[MHand.TYPE_HAND].append(magicTiles[0])
            testResult,testPattern,_ = winRule.isHu(testTile, magicTiles[0], True, MWinRule.WIN_BY_MYSELF, magicTiles, [], curSeatId, winSeatId, actionID,False,False)
            if not testResult:
                return result	

        for tile in range(leftTileCount):
	    if flowerRule and flowerRule.isFlower(tile):
                break
	    if tile % 10 == 0:
		continue
            newTile = MTile.cloneTiles(tiles)
            newTile[MHand.TYPE_HAND].append(tile)
            # 测试停牌时，默认听牌状态	modify youjun 06.23 默认未听牌状态
            winResult, winPattern,indexFan = winRule.isHu(newTile, tile, True, MWinRule.WIN_BY_MYSELF, magicTiles, [], curSeatId, winSeatId, actionID,False,False)
            if winResult:
                winNode = {}
                winNode['winTile'] = tile
                winNode['winTileCount'] = leftTileArr[tile]
		'''	
                ftlog.debug('MTing.canWinAddOneTile winTile:', tile
                            , ' winTileCount:', winNode['winTileCount']
                            , ' winPattern:', winPattern
			    , ' result:',indexFan)
		'''
                winNode['pattern'] = winPattern
		winNode['result'] = indexFan
		result.append(winNode)
       		if tingForQiangjin:
                    return result  
        return result
    
    @classmethod
    def calcTingResult(cls, winNodes, tableTileMgr, seatId):
        tings = []
        for winNode in winNodes:
            ting = []
            ting.append(winNode['winTile'])
            ting.append(1)
            dropCount = tableTileMgr.getVisibleTilesCount(ting[0], True, seatId)
            ting.append(dropCount)
            tings.append(ting)
        return tings

def test1():
    tiles = [[1,2,3,4,5,6,7,8,9,1,2,3,4,5,6,7,8], [], [], [], [], []]
    leftTiles = [1, 1, 7, 2, 2, 4, 14, 4, 5, 5, 7, 8, 9]
    winRule = MWinRuleFactory.getWinRule(MPlayMode.QUESHOU)
    magicTiles = []
    tile = 8
    ftlog.debug('test1 canting:xxx')
    begin = datetime.datetime.now()
    isTing, tingResults = MTing.canTing(tiles, leftTiles, winRule, tile, magicTiles, 0, 0,False)
    ftlog.debug('test1 canting:',isTing, tingResults)
    end = datetime.datetime.now()
    runTime = end-begin
    rstr = "运行时间:" + str(runTime) + " <callTime:"
    print rstr 
    
if __name__ == "__main__":
    test1()
