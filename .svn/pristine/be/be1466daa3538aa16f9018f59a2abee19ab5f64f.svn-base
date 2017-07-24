# -*- coding=utf-8
'''
Created on 2017年6月6日

一条和牌结果

@author: youjun
'''
from majiang2.player.player import MPlayerTileGang
from majiang2.win_loose_result.one_result import MOneResult
from majiang2.tile.tile import MTile
from majiang2.table.table_config_define import MTDefine
from majiang2.player.hand.hand import MHand
from majiang2.table_tile.table_tile_factory import MTableTileFactory
from majiang2.win_rule.win_rule_factory import MWinRuleFactory
from majiang2.tile_pattern_checker.tile_pattern_checker_factory import MTilePatternCheckerFactory
from majiang2.ai.play_mode import MPlayMode
from freetime.util import log as ftlog
from majiang2.table_state.state import MTableState
import copy
class MQueshouOneResult(MOneResult):

    HUNYISE='HUNYISE'
    QINGYISE='QINGYISE'
    PINGHU='PINGHU'
    JINKAN = 'JINKAN'
    JINQUE = 'JINQUE'
    SANJINDAO = 'SANJINDAO'
    QIANGJIN = 'QIANGJIN'
    TIANHU = 'TIANHU'
    PINGHUYIHUA = 'PINGHUYIHUA'
    def __init__(self):
        super(MQueshouOneResult, self).__init__()
        self.__fan_xing = {
            self.QINGYISE: {"name": "清一色", "value": 200,"index":11},
            self.HUNYISE: {"name": "混一色", "value": 100,"index":12},
            self.JINKAN:{"name":"金坎","value":100,"index":13},
            self.JINQUE: {"name":"金雀", "value":60,"index":14},
            self.SANJINDAO: {"name":"三金倒","value":40,"index":15},
            self.TIANHU: {"name":"天胡","value":30,"index":16},
            self.QIANGJIN: {"name":"抢金","value":30,"index":17},
            self.PINGHU:{"name":"平胡","value":30,"index":18},
            self.PINGHUYIHUA:{"name":"平胡(一张花)","value":15,"index":19}
        }
 
    @property
    def fanXing(self):
        return self.__fan_xing
    
    def setFanXing(self, fanXing):
        self.__fan_xing = fanXing

    def calcScore(self,winState = 0):
        """计算输赢数值"""

        # 序列化，以备后续的查找核实
        self.serialize()
        if self.resultType == self.RESULT_GANG:
            self.calcGang() 
        elif self.resultType == self.RESULT_WIN:
            playersAllTiles = [[] for _ in range(self.playerCount)]
            for player in self.tableTileMgr.players:
                playersAllTiles[player.curSeatId] = player.copyTiles()
            self.__win_rule_mgr = MWinRuleFactory.getWinRule(MPlayMode.QUESHOU)
            self.__win_pattern = []
            self.__tile_pattern_checker = MTilePatternCheckerFactory.getTilePatternChecker(MPlayMode.QUESHOU)
            self.__tile_pattern_checker.initChecker(playersAllTiles, self.winTile, self.tableTileMgr, False, self.lastSeatId, self.winSeatId, self.actionID)
            tiles = {MHand.TYPE_HAND: self.__tile_pattern_checker.playerHandTilesWithHu[self.winSeatId]}
            ftlog.info('MQueshouOneResult.calcScore tiles=',tiles) 
            winResult, winPattern = self.__win_rule_mgr.getHuPattern(tiles)
            self.__win_pattern = winPattern
            self.calcWin(winState)
        elif self.resultType == self.RESULT_FLOW:

            self.results[self.KEY_TYPE] = ''
            self.results[self.KEY_NAME] = '流局'
            score = [0 for _ in range(self.playerCount)]
            self.results[self.KEY_SCORE] = score
            winMode = [MOneResult.WIN_MODE_LOSS for _ in range(self.playerCount)]
            self.results[self.KEY_WIN_MODE] = winMode
            resultStat = [[] for _ in range(self.playerCount)]
            self.results[self.KEY_STAT] = resultStat

    def calcWin(self,winState = 0):
        self.clearWinFanPattern()
        # 在和牌时统计自摸，点炮状态
        resultStat = [[] for _ in range(self.playerCount)]
        winMode = [MOneResult.WIN_MODE_LOSS for _ in range(self.playerCount)]
        fanPattern = [[] for _ in range(self.playerCount)]
        fanXing = self.fanXing[self.PINGHU]
        resultStat[self.winSeatId].append({MOneResult.STAT_WIN:1})
        isZiMo = (self.lastSeatId == self.winSeatId)
        if isZiMo:
            resultStat[self.lastSeatId].append({MOneResult.STAT_ZIMO:1})
            winMode[self.lastSeatId] = MOneResult.WIN_MODE_ZIMO
        else:
	    if not winState:
                resultStat[self.lastSeatId].append({MOneResult.STAT_DIANPAO: 1})
                winMode[self.lastSeatId] = MOneResult.WIN_MODE_DIANPAO
                winMode[self.winSeatId] = MOneResult.WIN_MODE_PINGHU
            if self.qiangGang:
                winMode[self.winSeatId] = MOneResult.WIN_MODE_QIANGGANGHU

        score = [0 for _ in range(self.playerCount)]
        # 底分 配置项的底分
	baseScore = 1
	winScore = 0
	# 连庄
	bankerRemainCount = 0
	if self.winSeatId == self.bankerSeatId:
            bankerRemainCount = self.tableTileMgr.tableConfig.get(MTDefine.WIN_BASE,1) - 1

	winScore = winScore + bankerRemainCount
        ### 算杠分
        minggangScore = 0
        angangScore = 0        
	gangscore = 0  # 杠牌得分
        gangList = self.playerGangTiles[self.winSeatId]
        for gang in gangList:
            #if MTile.getColor(gang['pattern'][0]) == 3:
            #    gangscore += 1
	    #	minggangScore += 1
            if gang['style'] == 0:  # 暗杠
                gangscore += 2
		angangScore += 2
            else:
                gangscore += 1
		minggangScore += 1

        #winScore = winScore + angangScore + minggangScore

        ##算花分
        huaScore = len(self.tableTileMgr.flowerTiles(self.winSeatId))
        #winScore = winScore + huaScore

        ###算金分
        magicTile = self.tableTileMgr.getMagicTile()
        handTiles = self.playerAllTiles[self.winSeatId][MHand.TYPE_HAND]
        magicScore = MTile.getTileCount(magicTile,handTiles)
	huTiles = self.tableTileMgr.players[self.winSeatId].huTiles
	if len(huTiles) > 0 and huTiles[0] == magicTile and not winState == MTableState.TABLE_STATE_SANJINDAO:
            magicScore = magicScore + 1
	ftlog.debug('calcWin handTiles=',handTiles,huTiles,magicScore)
        winScore = winScore + magicScore

        winnerResults = []
        if winState:
            if winState == MTableState.TABLE_STATE_TIANHU:
                winnerResults.append(self.processFanXingResult(self.TIANHU))
            elif winState == MTableState.TABLE_STATE_QIANGJIN:
                winnerResults.append(self.processFanXingResult(self.QIANGJIN))
	    elif winState == MTableState.TABLE_STATE_QIANGJIN_B: 
		winnerResults.append(self.processFanXingResult(self.QIANGJIN))
            elif winState == MTableState.TABLE_STATE_SANJINDAO: 
	        winnerResults.append(self.processFanXingResult(self.SANJINDAO))

        #if not isZiMo:
        if not huaScore and not len(gangList):
            winnerResults.append(self.processFanXingResult(self.PINGHU))
        if huaScore + gangscore == 1:
            winnerResults.append(self.processFanXingResult(self.PINGHUYIHUA))
 
        if winState and winState == MTableState.TABLE_STATE_TIANHU:
            if self.isSanJinDao():
                winnerResults.append(self.processFanXingResult(self.SANJINDAO))
	    if self.tableConfig.get(MTDefine.QINGHUNYISE, 0):
                if self.isQingyise():   #清一色
                    winnerResults.append(self.processFanXingResult(self.QINGYISE))
                elif self.isHunyise():  # 混一色
                    winnerResults.append(self.processFanXingResult(self.HUNYISE))
            if self.tableTileMgr.players[self.winSeatId].jinkanState:
                winnerResults.append(self.processFanXingResult(self.JINKAN))
            if self.isJinQue(isZiMo):
                winnerResults.append(self.processFanXingResult(self.JINQUE))
        if not winState:
            if self.isSanJinDao():
                winnerResults.append(self.processFanXingResult(self.SANJINDAO))
	    if self.tableConfig.get(MTDefine.QINGHUNYISE, 0):
                if self.isQingyise():   #清一色
                    winnerResults.append(self.processFanXingResult(self.QINGYISE))
                elif self.isHunyise():  # 混一色
                    winnerResults.append(self.processFanXingResult(self.HUNYISE))
            if self.tableTileMgr.players[self.winSeatId].jinkanState:
                winnerResults.append(self.processFanXingResult(self.JINKAN))
            if self.isJinQue(isZiMo):
                winnerResults.append(self.processFanXingResult(self.JINQUE))

        if not len(winnerResults):
            winScore = winScore + baseScore

        ###自摸 或者特殊番型*2
        #if isZiMo or len(winnerResults) > 0:
        #    winScore = winScore * 2 

        bestWinnerResult = None
        maxScore = 0
        for result in winnerResults:
            tempScore = self.getScoreByResults(result)
            if tempScore > maxScore:
                maxScore = tempScore
                bestWinnerResult = result

        if bestWinnerResult and bestWinnerResult['index'] == 19:
            huaScore = 0 
	else:
	    winScore = winScore + angangScore + minggangScore
	    winScore = winScore + huaScore
        ###自摸 或者特殊番型*2
        if isZiMo or len(winnerResults) > 0:
            winScore = winScore * 2 

	winScore = winScore + maxScore

        #### 胡法判断
        if isZiMo: #自摸
            score = [-winScore for _ in range(self.playerCount)]
            score[self.winSeatId] = (self.playerCount-1) * winScore
        else: #点炮
            # if self.qiangGang: #抢杠包三家
            #     score = [0 for _ in range(self.playerCount)]
            #     score[self.winSeatId] = (self.playerCount - 1) * winScore
            #     score[self.lastSeatId] = -(self.playerCount - 1) * winScore
            # else:

            if winState: #抢金
                score = [-winScore for _ in range(self.playerCount)]
                score[self.winSeatId] = (self.playerCount-1) * winScore
            else:
                if self.getFangHuConfig() == 1:
                    score = [-winScore for _ in range(self.playerCount)]
                    score[self.winSeatId] = (self.playerCount-1) * winScore
                elif self.getFangHuConfig() == 2:
                    score[self.lastSeatId] = -winScore
                    score[self.winSeatId] = winScore

        if bestWinnerResult:
            winMode[self.winSeatId] = bestWinnerResult['index']

        flowerScores = {}
        flowerScores['scores'] = [self.tableTileMgr.flowerScores(seat) for seat in range(self.playerCount)]  # 给前端显示花分

        # 最大番统计(改成单局最佳)
        resultStat[self.winSeatId].append({MOneResult.STAT_ZUIDAFAN: score[self.winSeatId]})

        self.results[self.KEY_TYPE] = '和牌'
        self.results[self.KEY_NAME] = fanXing['name']
        self.results[self.KEY_SCORE] = score
        self.results[self.KEY_WIN_MODE] = winMode
        self.results[self.KEY_STAT] = resultStat
        fanPattern[self.winSeatId] = bestWinnerResult
        #self.results[self.KEY_FAN_PATTERN] = fanPattern
	'''	
	winInfo = []
        jinResult = []
        huaResult = []
        baseResult = []
	winPatt = []
        if len(winnerResults) > 0 or isZiMo:
            #self.results['double'] = 2
            jinResult.append("金牌:" + str(magicScore) + "花" + "*2")
            huaResult.append("花牌:" + str(huaScore) + "花" + "*2")
            baseResult.append("底分:" + str(baseScore) + "花" + "*2")
	    if bestWinnerResult:
		winPatt.append(bestWinnerResult['name'] + ":" + str(bestWinnerResult['value'])+ "花")
        else:
            jinResult.append("金牌:" + str(magicScore) + "花")
            huaResult.append("花牌:" + str(huaScore) + "花")
	    baseResult.append("底分:" + str(baseScore) + "花")
	winInfo.append(baseResult)
	if magicScore:
            winInfo.append(jinResult)
	if huaScore:
            winInfo.append(huaResult)
	if len(winPatt) > 0:
            winInfo.append(winPatt)
	'''

        winInfo = []
        jinResult = "金牌" + str(magicScore)
        huaResult = "花牌" + str(huaScore)
        baseResult = "底分" + str(baseScore)
        remainResult = "连庄" + str(bankerRemainCount)
        winPatt = None
        if bestWinnerResult:
            winPatt = bestWinnerResult['name'] + str(bestWinnerResult['value'])
        minggangResult = "明杠" + str(minggangScore)
        angangResult = "暗杠" + str(angangScore)


        winResult = "("
        if not len(winnerResults):
            winResult = winResult + " " + baseResult
        if huaScore:
            winResult = winResult + " " + huaResult
        if magicScore:
            winResult = winResult + " " + jinResult
        if minggangScore:
            winResult = winResult + " " + minggangResult
        if angangScore:
            winResult = winResult + " " + angangResult
        if bankerRemainCount:
            winResult = winResult + " " + remainResult

	if len(winnerResults) > 0 or isZiMo:
	    if bestWinnerResult:
                winPatt = bestWinnerResult['name'] + str(bestWinnerResult['value'])
		if huaScore or magicScore or minggangScore or angangScore or bankerRemainCount:
	            winResult = winResult + " )" + " *2 + " + winPatt + " = " + str(winScore)
		else:
		    winResult = winPatt + " = " + str(winScore)
            else:
                winResult = winResult + " )" + " *2" + " = " + str(winScore)
        else:
            winResult = winResult + " )" + " *1" + " = " + str(winScore)
	winInfo.append([winResult])
	
        fanPattern[self.winSeatId] = winInfo
        self.results[self.KEY_FAN_PATTERN] = fanPattern
        self.results[self.KEY_FLOWER_SCORES] = flowerScores
	self.results[self.KEY_LIANZHUANG] = bankerRemainCount

    def processFanXingResult(self, fanSymbol, scoreTimes = 0 ,indexTimes = 1):
        res = {"name":'', "value":0, "index":0, 'fanSymbol':''}
        if self.fanXing[fanSymbol]:
            if self.fanXing[fanSymbol]["name"]:
                res['name'] = self.fanXing[fanSymbol]["name"]
            if self.fanXing[fanSymbol].has_key("value"):
                res['value'] = self.fanXing[fanSymbol]["value"] * indexTimes
            if self.fanXing[fanSymbol].has_key("index"):
                res['index'] = self.fanXing[fanSymbol]["index"]
            res['fanSymbol'] = fanSymbol
        return res

    def getScoreByResults(self, results, maxFan=0):
        score = 0
	ftlog.debug('getScoreByResults.results=',results)
        score += results['value']
        return score

    def getFangHuConfig(self):
        """获取赔付配置"""
        fanghu_config = self.tableConfig.get(MTDefine.FANGHU,0)
        ftlog.debug('getFangHuConfig info:', fanghu_config)
        return fanghu_config  

    def calcGang(self):
        """计算杠的输赢"""
        #明杠暗杠统计
        resultStat = [[] for _ in range(self.playerCount)]
	self.results[self.KEY_TYPE] = MOneResult.KEY_TYPE_NAME_GANG        
        
        base = self.tableConfig.get(MTDefine.GANG_BASE, 0)
        if self.style == MPlayerTileGang.AN_GANG:
            self.results[self.KEY_NAME] = "暗杠"
            base *= 2
            resultStat[self.winSeatId].append({MOneResult.STAT_ANGANG:1})
        else:
            self.results[self.KEY_NAME] = "明杠"
            resultStat[self.winSeatId].append({MOneResult.STAT_MINGGANG:1})
        resultStat[self.winSeatId].append({MOneResult.STAT_GANG:1})
        
        scores = [0 for _ in range(self.playerCount)] 
        # if self.lastSeatId != self.winSeatId: #放杠
        #     scores = [0 for _ in range(self.playerCount)]
        #     scores[self.lastSeatId] = -base
        #     scores[self.winSeatId] = base
        # else:
        #     scores = [-base for _ in range(self.playerCount)]
        #     scores[self.winSeatId] = (self.playerCount - 1) * base
        
        self.results[self.KEY_SCORE] = scores
        #self.results[self.KEY_STAT] = resultStat


    def isQingyise(self):
        """
        清一色：只有一色牌（如全是万），有无金牌皆可，但金牌必须与其他牌同色
        """
        colorArr = [0, 0, 0, 0]
        handTile = MHand.copyAllTilesToList(self.playerAllTiles[self.winSeatId])  # 手牌区+吃+碰+杠+锚+胡区

        for tile in handTile:
            color = MTile.getColor(tile)
            colorArr[color] = 1

        colorCount = 0
        for eachColor in colorArr:
            if eachColor:
                colorCount += 1
        if colorCount == 1:
            return True
        return False

    def isHunyise(self):
        """
        混一色：只有一色牌（如全是万），有金牌，但金牌不同色
        """
	'''
        colorArr = [0, 0, 0, 0]
        handTile = MHand.copyAllTilesToList(self.playerAllTiles[self.winSeatId])  # 手牌区+吃+碰+杠+锚+胡区
        for tile in handTile:
            color = MTile.getColor(tile)
            colorArr[color] = 1
        
        magicTile = self.tableTileMgr.getMagicTile()
        magicTileColor = MTile.getColor(magicTile)
	
	handTile = MHand.copyAllTilesToList(self.playerAllTiles[self.winSeatId])
        tilesArr = MTile.changeTilesToValueArr(handTile)
        count = MTile.getTileCountByColor(tilesArr, magicTileColor)

        magicCount = MTile.getTileCount(magicTile,handTile[MHand.TYPE_HAND])
	
        if count!=magicCount:
            return False
	
        colorCount = 0
        for eachColor in colorArr:
            if eachColor:
                colorCount += 1
        if colorCount == 2 and colorArr[magicTileColor] == 1:
            return True
        return False
	'''
	magicTile = self.tableTileMgr.getMagicTile()
	magicCount = 0
	allTiles = MHand.copyAllTilesToList(self.playerAllTiles[self.winSeatId])
        #allTiles = MHand.copyAllTilesToListButHu(handTile)
        allTileArr = MTile.changeTilesToValueArr(allTiles)
        allColors = MTile.getColorCount(allTileArr)
        for tile in allTiles:
            if magicTile and tile == magicTile:
		magicCount = magicCount + 1

        for i in range(magicCount):
            allTiles.remove(magicTile)

        tileArr = MTile.changeTilesToValueArr(allTiles)
        colors = MTile.getColorCount(tileArr)

        if allColors == 2 and colors == 1:
            return True
        return False 


    def isSanJinDao(self):
        """
        三金倒
        """
        magicTile = self.tableTileMgr.getMagicTile()
        handTiles = self.playerAllTiles[self.winSeatId][MHand.TYPE_HAND]
        magicCount = MTile.getTileCount(magicTile,handTiles)
	huTiles = self.tableTileMgr.players[self.winSeatId].huTiles
	ftlog.debug('isSanJinDao. self.winSeatId,huTiles=',self.winSeatId,huTiles)
	if len(huTiles) and huTiles[0] == magicTile:
	    magicCount = magicCount + 1
	ftlog.debug('isSanJinDao.magicCount=',magicCount,handTiles,magicTile)
        if magicCount == 3:
            return True
        return False

    def isJinQue(self,isZiMo = False):
        """
        金雀：金做将对
        
	if not isZiMo:
	    return False
	"""
	magicTile = self.tableTileMgr.getMagicTile()
	handTiles = self.playerAllTiles[self.winSeatId][MHand.TYPE_HAND]
	magicCount = MTile.getTileCount(magicTile,handTiles)
        huTiles = self.tableTileMgr.players[self.winSeatId].huTiles
        if len(huTiles) and huTiles[0] == magicTile:
            magicCount = magicCount + 1 
	if magicCount != 2:
	    return False
        for p in self.__win_pattern:
            if len(p) == 2:
                if p[0] == p[1] and p[0] == magicTile:
                    return True
        return False


if __name__ == "__main__":
    result = MQueshouOneResult()
    tilePatternChecker = MTilePatternCheckerFactory.getTilePatternChecker(MPlayMode.QUESHOU)
    tableTileMgr = MTableTileFactory.getTableTileMgr(3, 'queshou', 1)

