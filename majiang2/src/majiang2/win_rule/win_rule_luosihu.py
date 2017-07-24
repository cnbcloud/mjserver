# -*- coding=utf-8
'''
Created on 2016年12月11日
庄家规则
@author: dongwei
'''
from majiang2.win_rule.win_rule import MWinRule
from majiang2.ai.win import MWin
from majiang2.player.hand.hand import MHand
from majiang2.player.player import MPlayerTileGang
from majiang2.table.table_config_define import MTDefine
from majiang2.tile.tile import MTile
from majiang2.ai.play_mode import MPlayMode
from majiang2.tile_pattern_checker.tile_pattern_checker_factory import MTilePatternCheckerFactory
from freetime.util import log as ftlog
import copy

class MWinRuleLuosihu(MWinRule):
    """卡五星胡牌
    多支持七对胡
    """
    QINGYISE = 'qingyise'
    QINGYISENOGANG = 'qingyisenogang'
    YIPAOSHUANGXIANG = 'yipaoshuangxiang'
    QIDUI = 'qidui'
    QIDUIHAO = 'qiduihao'
    PENGPENGHU = 'pengpenghu'
    GANGKAI = 'gangkai'
    QIANGGANG = 'qiangGang'
    GANGSHANGPAO = 'gangshangpao'
    TIANHU = 'TIANHU'
    DIHU = 'DIHU'
    JINGOUDIAO = 'JINGOUDIAO'
    JIANGDUI = 'JIANGDUI'
    SHISANYAO = 'shisanyao'
    YAOJIU = 'yaojiu'
    DUANYAOJIU = 'duanyaojiu'
    GEN = 'gen'
    LIANGGANGMANFAN = 'lianggangmanfan'
    ZIMOJIAFAN = 'zimojiafan'
    MENQING = 'menqing'
    HAIDILAO = 'haidilao'
    QINGYISEPENGPENGHU = 'qingyisepengpenghu'
    QINGQIDUI = 'qingqidui'
    QINGQIDUIHAO = 'qingqiduihao'
    JIANGQIDUI = 'jiangqidui'
    JINGOUHU = 'jingouhu'
    HAIDIPAO = 'haidipao'

    def __init__(self):
        super(MWinRuleLuosihu, self).__init__()
        self.__fan_xing = {
            # 赢的番型
            self.QINGYISE: {"name":"清一色", "index": 2},
            self.QINGYISENOGANG:{"name":"清一色无杠", "index": 1},
            self.QIDUI: {"name":"七对", "index": 2},
            self.QIDUIHAO: {"name":"豪华七对", "index": 3},
            self.PENGPENGHU: {"name":"碰碰胡", "index": 1},
            self.TIANHU: {"name": "天胡", "index": 5},
            self.DIHU: {"name": "地胡", "index": 5},
            self.JINGOUDIAO:{"name":"金钩钓","index":1},
            self.JINGOUHU:{"name":"金钩胡","index":1},
            self.JIANGDUI:{"name":"将对","index":2},
            self.YAOJIU:{"name":"幺九","index":2},
            self.DUANYAOJIU:{"name":"断幺九","index":1},
            self.GANGKAI: {"name":"杠上开花", "index": 1},
            self.QIANGGANG: {"name":"抢杠胡", "index": 1},
            self.SHISANYAO:{"name":"十三幺", "index":4},
            self.GEN:{"name":"根", "index":1},
            self.MENQING:{"name":"门清","index":1},
            self.LIANGGANGMANFAN:{"name":"两杠满番","index":1},
            self.HAIDIPAO: {"name":"海底炮", "index": 1},
            self.ZIMOJIAFAN:{"name":"自摸加番","index":1},
            self.GANGSHANGPAO: {"name":"杠上炮", "index": 1},
            self.YIPAOSHUANGXIANG: {"name":"一炮双响", "index": 1},
            self.HAIDILAO: {"name":"海底捞", "index": 1},
            self.QINGYISEPENGPENGHU:{"name":"清一色碰碰胡","index":3},
            self.QINGQIDUI:{"name":"清七对","index":3},
            self.JIANGQIDUI:{"name":"将七对","index":4},
            self.QINGQIDUIHAO:{"name":"清龙七对","index":4} 
        }
    @property
    def fanXing(self):
        return self.__fan_xing   
 
    def isHu(self, tiles, tile, isTing, getTileType, magicTiles = [], tingNodes = [], curSeatId = 0, winSeatId = 0, actionID = 0, isGangKai = False,isForHu = True):

	if self.tableTileMgr.playMode == "luosihu-luosihu" and isForHu:
	    if not isTing:
	        if not self.tableTileMgr.players[winSeatId].isWon():
		    return False,[],0

        allTiles = MHand.copyAllTilesToListButHu(tiles)
        tilesArr = MTile.changeTilesToValueArr(allTiles)	
        # 需要缺一门： 定缺的时候约定的那门
        if self.absenceColor:
            if MTile.getTileCountByColor(tilesArr, self.absenceColor[winSeatId]) > 0:
                return False, [],0
        result, pattern = self.isQidui(tiles)
        if result:
            if self.tableTileMgr.playMode == "luosihu-luosihu":
                self.fanXing[self.QIDUI]["index"] = 1 
            return True, pattern,self.fanXing[self.QIDUI]["index"]

        result, pattern = MWin.isHu(tiles[MHand.TYPE_HAND], magicTiles)

        if result:
            ftlog.debug('MWinRuleLuosihu.isHu result=',result,' getTileType=',getTileType,' pattern=',pattern)
            player = self.tableTileMgr.players[winSeatId]
            self.winSeatId = winSeatId
            self.__tile_pattern_checker = MTilePatternCheckerFactory.getTilePatternChecker(MPlayMode.LUOSIHU)
            playersAllTiles = [[] for _ in range(self.tableTileMgr.playCount)]
            self.__win_patterns = [[] for _ in range(self.tableTileMgr.playCount)]
            self.__win_patterns[winSeatId] = [pattern]
            for seatId in range(self.tableTileMgr.playCount):
                if seatId == winSeatId:
                    playersAllTiles[seatId] = copy.deepcopy(tiles)
                else:
                    playersAllTiles[seatId] = self.tableTileMgr.players[seatId].copyTiles()
            self.setAllPlayerTiles(playersAllTiles)
            # 判断和牌的时候
            self.__tile_pattern_checker.initChecker(playersAllTiles, tile, self.tableTileMgr, True, curSeatId, winSeatId, actionID)
            winnerResult = []
            if self.tableTileMgr.playMode == "luosihu-ctxuezhan":
                winnerResult = self.getWinnerResultsForXueZhanDaoDi(winSeatId)
            elif self.tableTileMgr.playMode == "luosihu-xuezhan":
                winnerResult = self.getWinnerResultsForLuoSiHuXueZhan(winSeatId)
            elif self.tableTileMgr.playMode == "luosihu-luosihu":
                winnerResult = self.getWinnerResultsForLuoSiHu(winSeatId)
            finalResult = []
            finalResult.extend(winnerResult)
            maxFan = self.tableConfig.get(MTDefine.MAX_FAN, 0)
            winScore,indexFan = self.getScoreByResults(finalResult, maxFan)
            ftlog.debug('MWinRuleLuosihu.isHu player.guoHuPoint :',winScore,' finalResult=',finalResult,' indexFan')
            # 过胡判断
            if getTileType == MWinRule.WIN_BY_MYSELF:
                return True,pattern,indexFan
            if player.guoHuPoint >= winScore and self.tableTileMgr.playMode == "luosihu-ctxuezhan":
                return False, [],0
            player.totalWinPoint = winScore
            return True,pattern,indexFan

	return False, [],0

    def getWinnerResultsForLuoSiHu(self,winSeatId, isFlow=False):
        winnerResults = []
        # 不需要根据和牌牌型计算的番型，先计算
        maxFan = self.tableConfig.get(MTDefine.MAX_FAN, 0)
        """清一色"""
        if self.__tile_pattern_checker.isQingyise():
            self.fanXing[self.QINGYISE]["index"] = 1
            winnerResults.append(self.processFanXingResult(self.QINGYISE))
        """碰碰胡"""
        for pattern in self.__win_patterns[winSeatId]:
            if self.__tile_pattern_checker.isPengpenghu(pattern):
                if self.isJinGouDiao():
                    winnerResults.append(self.processFanXingResult(self.JINGOUDIAO,0,2))
                else:
                    winnerResults.append(self.processFanXingResult(self.PENGPENGHU)) 

        # 个别番型和和牌牌型有关，算分时选取分数最大的情况
        #winnerResultsByPattern = []
        maxPatternScore = 0
        bestWinnerResultsByPattern = []

        ftlog.info('MLuosihuOneResult.getWinnerResults winSeatId', self.__win_patterns[winSeatId])
        for pattern in self.__win_patterns[winSeatId]:
            ftlog.info('MLuosihuOneResult.getWinnerResults win_pattern=', pattern)

            # pattern内，全部是手牌(包含最后一张牌)
            eachWinnerResultsByPattern = []
            """七对"""
            if self.__tile_pattern_checker.isQidui(pattern):
                self.fanXing[self.QIDUI]["index"] = 1
                eachWinnerResultsByPattern.append(self.processFanXingResult(self.QIDUI))
            """豪华七对"""
            hu_tiles = self.tableTileMgr.players[winSeatId].copyHuArray()
            tempcount = 0
            if len(hu_tiles) > 0:
                tiles = self.allPlayerTiles[self.winSeatId] # self.tableTileMgr.players[self.winSeatId].copyTiles()
                handTiles = tiles[MHand.TYPE_HAND]
                tempcount = MTile.getTileCount(hu_tiles[-1],handTiles)
            ftlog.debug('MLuosihuOneResult.getWinnerResults hu_tiles=',hu_tiles,tempcount)
            if self.__tile_pattern_checker.isQiduiHao(pattern) and tempcount >= 3:
                self.fanXing[self.QIDUIHAO]["index"] = 2
                eachWinnerResultsByPattern.append(self.processFanXingResult(self.QIDUIHAO))
            ftlog.info('MLuosihuOneResult.getWinnerResults eachWinnerResultsByPattern=', eachWinnerResultsByPattern) 
		
            bestWinnerResult = []
            maxScore = 0
            for result in eachWinnerResultsByPattern:
                tempResult = []
                tempResult.append(result)
                calctempResult = []
                calctempResult.extend(tempResult)
                tempScore,_ = self.getScoreByResults(calctempResult)
                if tempScore > maxScore:
                    maxScore = tempScore
                    bestWinnerResult = tempResult 

            # 计算当前牌型的赢牌奖励分数，选取最大值的牌型
            calceachWinnerResultsByPattern = []
            #calceachWinnerResultsByPattern.extend(winnerResults)
            calceachWinnerResultsByPattern.extend(bestWinnerResult)
            tempScore,_ = self.getScoreByResults(calceachWinnerResultsByPattern)
            if tempScore > maxPatternScore:
                # 分数相同就不管了
                maxPatternScore = tempScore
                bestWinnerResultsByPattern = calceachWinnerResultsByPattern

        winnerResults.extend(bestWinnerResultsByPattern)
        ftlog.info('MLuosihuOneResult.getWinnerResults luosihu winnerResults=', winnerResults)
        return winnerResults

    def getWinnerResultsForLuoSiHuXueZhan(self,winSeatId, isFlow=False):
        """和牌时，计算胜者的牌对整个牌桌的分数影响"""
        winnerResults = []
        # 不需要根据和牌牌型计算的番型，先计算
	maxFan = self.tableConfig.get(MTDefine.MAX_FAN, 0)
        """清一色 2番"""
        if self.__tile_pattern_checker.isQingyise():
            """清一色无杠 满番"""
            if self.getGangCount() == 0 :
                self.fanXing[self.QINGYISENOGANG]["index"] = maxFan
                winnerResults.append(self.processFanXingResult(self.QINGYISENOGANG))
            else:
                winnerResults.append(self.processFanXingResult(self.QINGYISE))
        for pattern in self.__win_patterns[winSeatId]:
            """碰碰胡"""
            if self.__tile_pattern_checker.isPengpenghu(pattern):
                if self.isJinGouDiao():
                    if self.getGangCount():
                        self.fanXing[self.JINGOUDIAO]["index"] = maxFan
                        winnerResults.append(self.processFanXingResult(self.JINGOUDIAO))
                    else:
                        winnerResults.append(self.processFanXingResult(self.JINGOUDIAO))
                if self.getGangCount():
                    self.fanXing[self.PENGPENGHU]["index"] = maxFan
                    winnerResults.append(self.processFanXingResult(self.PENGPENGHU))
        """两杠 满番"""
        if self.getGangCount() >= 2 and self.tableConfig.get(MTDefine.LIANGGANGMANFAN, 0):
            self.fanXing[self.LIANGGANGMANFAN]["index"] = maxFan
            winnerResults.append(self.processFanXingResult(self.LIANGGANGMANFAN)) 

        # 个别番型和和牌牌型有关，算分时选取分数最大的情况
        #winnerResultsByPattern = []
        maxPatternScore = 0
        bestWinnerResultsByPattern = []

        for pattern in self.__win_patterns[winSeatId]:
            # pattern内，全部是手牌(包含最后一张牌)
            eachWinnerResultsByPattern = []
            """七对 2番"""
            if self.__tile_pattern_checker.isQidui(pattern):
                eachWinnerResultsByPattern.append(self.processFanXingResult(self.QIDUI))
            """碰碰胡 1番"""
            if self.__tile_pattern_checker.isPengpenghu(pattern):
                eachWinnerResultsByPattern.append(self.processFanXingResult(self.PENGPENGHU)) 
            bestWinnerResult = []
            maxScore = 0
            for result in eachWinnerResultsByPattern:
                tempResult = []
                tempResult.append(result)
                calctempResult = []
                calctempResult.extend(tempResult)
                tempScore,_ = self.getScoreByResults(calctempResult)
                if tempScore > maxScore:
                    maxScore = tempScore
                    bestWinnerResult = tempResult

            # 计算当前牌型的赢牌奖励分数，选取最大值的牌型
            calceachWinnerResultsByPattern = []
            #calceachWinnerResultsByPattern.extend(winnerResults)
            calceachWinnerResultsByPattern.extend(bestWinnerResult)
            tempScore,_ = self.getScoreByResults(calceachWinnerResultsByPattern)
            if tempScore > maxPatternScore:
                # 分数相同就不管了
                maxPatternScore = tempScore
                bestWinnerResultsByPattern = calceachWinnerResultsByPattern
        winnerResults.extend(bestWinnerResultsByPattern)
        return winnerResults

    def getWinnerResultsForXueZhanDaoDi(self,winSeatId, isFlow=False):
        """血战到底"""
        """和牌时，计算胜者的牌对整个牌桌的分数影响"""
        winnerResults = []
        # 不需要根据和牌牌型计算的番型，先计算
	maxFan = self.tableConfig.get(MTDefine.MAX_FAN, 0)
        if self.__tile_pattern_checker.isGangshangpao():
            winnerResults.append(self.processFanXingResult(self.GANGSHANGPAO))
        """金钩胡 1番 不和对对胡一起算"""
        for pattern in self.__win_patterns[winSeatId]:
            if self.checkDaDiaoChe() and not self.__tile_pattern_checker.isPengpenghu(pattern):
                winnerResults.append(self.processFanXingResult(self.JINGOUHU))
            """根的番计算 龙七对,清龙七对 根要减1"""
            hasGen, winnerGen = self.getWinnerGen()
            if hasGen:
                if self.__tile_pattern_checker.isQiduiHao(pattern):
                    winnerGen -= 1
                winnerResults.append(self.processFanXingResult(self.GEN,0,winnerGen))
        # 个别番型和和牌牌型有关，算分时选取分数最大的情况
        maxPatternScore = 0
        bestWinnerResultsByPattern = []

        ftlog.info('MLuosihuOneResult.getWinnerResults winSeatId', self.__win_patterns[winSeatId])
        for pattern in self.__win_patterns[winSeatId]:
            ftlog.info('MLuosihuOneResult.getWinnerResults win_pattern=', pattern)

            # pattern内，全部是手牌(包含最后一张牌)
            eachWinnerResultsByPattern = []

            """碰碰胡 2番"""
            if self.__tile_pattern_checker.isPengpenghu(pattern):
                self.fanXing[self.PENGPENGHU]["index"] = 2
                eachWinnerResultsByPattern.append(self.processFanXingResult(self.PENGPENGHU))
            """清一色 2番"""
            if self.__tile_pattern_checker.isQingyise():
                eachWinnerResultsByPattern.append(self.processFanXingResult(self.QINGYISE))
            """清一色碰碰胡 3番"""
            if self.__tile_pattern_checker.isPengpenghu(pattern) and self.__tile_pattern_checker.isQingyise():
                eachWinnerResultsByPattern.append(self.processFanXingResult(self.QINGYISEPENGPENGHU))
            """七对 2番"""
            if self.__tile_pattern_checker.isQidui(pattern):
		eachWinnerResultsByPattern.append(self.processFanXingResult(self.QIDUI))
            """清七对 3番"""
            if self.__tile_pattern_checker.isQingyise() and self.__tile_pattern_checker.isQidui(pattern):
                eachWinnerResultsByPattern.append(self.processFanXingResult(self.QINGQIDUI))
            """龙七对 3番"""
            if self.__tile_pattern_checker.isQiduiHao(pattern):
                eachWinnerResultsByPattern.append(self.processFanXingResult(self.QIDUIHAO))
            """清龙七对 4番"""
            if self.__tile_pattern_checker.isQiduiHao(pattern) and self.__tile_pattern_checker.isQingyise():
                eachWinnerResultsByPattern.append(self.processFanXingResult(self.QINGQIDUIHAO))
	    if self.tableConfig.get(MTDefine.JIANGDUI,0):
                """全幺九 3番"""
                if self.isYaoJiu(pattern):
                    self.fanXing[self.YAOJIU]["index"] = 3
                    eachWinnerResultsByPattern.append(self.processFanXingResult(self.YAOJIU))
                """将对 3番"""
                if self.__tile_pattern_checker.isPengpenghu(pattern) and self.isJiangDui():
                    self.fanXing[self.JIANGDUI]["index"] = 3
                    eachWinnerResultsByPattern.append(self.processFanXingResult(self.JIANGDUI))
            """将七对 4番"""
            if self.__tile_pattern_checker.isQiduiHao(pattern) and self.isJiangDui():
                eachWinnerResultsByPattern.append(self.processFanXingResult(self.JIANGQIDUI))

            ftlog.debug('MLuosihuOneResult.getWinnerResults eachWinnerResultsByPattern= ', eachWinnerResultsByPattern,len(eachWinnerResultsByPattern))

            # 计算当前牌型的赢牌奖励分数，选取最大值的牌型

            bestWinnerResult = []
            maxScore = 0
            for result in eachWinnerResultsByPattern:
                tempResult = []
                tempResult.append(result)
                calctempResult = []
                calctempResult.extend(tempResult)
                tempScore,_ = self.getScoreByResults(calctempResult)
                if tempScore > maxScore:
                    maxScore = tempScore
                    bestWinnerResult = tempResult

            calceachWinnerResultsByPattern = []
            calceachWinnerResultsByPattern.extend(winnerResults)
            calceachWinnerResultsByPattern.extend(bestWinnerResult)
            tempScore,_ = self.getScoreByResults(calceachWinnerResultsByPattern)
            if tempScore > maxPatternScore:
                # 分数相同就不管了
                maxPatternScore = tempScore
                bestWinnerResultsByPattern = calceachWinnerResultsByPattern

        winnerResults.extend(bestWinnerResultsByPattern)
        ftlog.info('MLuosihuOneResult.getWinnerResults xuezhandaodi winnerResults=', winnerResults)

        return winnerResults

    def getScoreByResults(self, results, maxFan=0):
        index = 0
        score = 0
        for result in results:
            index += result['index']
            score += result['score']
        scoreIndex = self.tableConfig.get(MTDefine.FAN_LIST, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        ftlog.info('MLuosihuOneResult.getScoreByResults scoreIndex:', scoreIndex)
        if len(scoreIndex) <= index:
            # 如果超出最大番型的定义，按照len-1计算，防止超出边界
            ftlog.info('MLuosihuOneResult.getScoreByResults exceed fan_list in MTDefine, index=', index)
            index = len(scoreIndex) - 1
        fan = scoreIndex[index]
        if maxFan:
            # maxFan不为0时，限制最大番数。算最大番型时，不要传递此参数，要么就算不出来了
            if fan > maxFan:
                fan = maxFan
        finalScore = fan + score
        ftlog.info('MLuosihuOneResult.getScoreByResults score=', finalScore,' fan=',fan,' index=',index,' result=',results)
        return finalScore,index

    def processFanXingResult(self, fanSymbol, scoreTimes = 0 ,indexTimes = 1):
        res = {"name":'', "index":0, "score":0, 'fanSymbol':''}
        if self.fanXing[fanSymbol]:
            if self.fanXing[fanSymbol]["name"]:
                res['name'] = self.fanXing[fanSymbol]["name"]
            if self.fanXing[fanSymbol].has_key("index"):
                res['index'] = self.fanXing[fanSymbol]["index"] * indexTimes
            if self.fanXing[fanSymbol].has_key("addScore"):
                res['score'] += self.fanXing[fanSymbol]["addScore"]
            if self.fanXing[fanSymbol].has_key("multiplyScore"):
                res['score'] += self.fanXing[fanSymbol]["multiplyScore"] * scoreTimes
            res['fanSymbol'] = fanSymbol
        return res

    def checkDaDiaoChe(self):
        """检查大吊车：只剩一张牌单吊
        """
        tiles = self.allPlayerTiles[self.winSeatId] # self.tableTileMgr.players[self.winSeatId].copyTiles()
        return len(tiles[MHand.TYPE_HAND]) == 1

    def isDuanYaoJiu(self):
        """
        断幺九:每副顺子，刻字，将牌都不包含1或9
        """
        if self.tableConfig.get(MTDefine.DUANYAOJIU, 0) != 1:
            return False
        
        allPlayerTiles = MHand.copyAllTilesToList(self.tableTileMgr.players[self.winSeatId].copyTiles())
        yaoJiuCount = 0
        for tile in allPlayerTiles:
            if MTile.getColor(tile) == MTile.TILE_FENG or tile%10 == 1 or tile%10 == 9:
                yaoJiuCount += 1

        return yaoJiuCount == 0

    def checkMenQing(self):
        """检查门清，没有碰和明杠，点炮也算门清
        """
        if self.tableConfig.get(MTDefine.MEN_CLEAR_DOUBLE, 0) != 1:
            return False
        tiles = self.tableTileMgr.players[self.winSeatId].copyTiles()
        # 没有碰
        if len(tiles[MHand.TYPE_PENG]) > 0:
            return False
	
        # 没有明杠
        for gang in tiles[MHand.TYPE_GANG]:
            if gang['style'] == MPlayerTileGang.MING_GANG:
                return False
	
        return True

    def isJinGouDiao(self):
        """金钩钓: 碰碰，且单吊将
        """
        # 手牌只剩将对
        nowTiles = self.allPlayerTiles[self.winSeatId] # self.tableTileMgr.players[self.winSeatId].copyTiles()
        handTiles = nowTiles[MHand.TYPE_HAND]
        if len(handTiles) == 2 and handTiles[0] == handTiles[1]:
            return True
	
        if len(handTiles) < 2:
            return True

        return False

    def getWinnerGen(self):
        #只要你手上有4个一样的，哪怕是碰了之后自己摸的加杠，或者手上有4张一样的牌，没有杠等等都算一番，你有2根就是2番，*4
        #杠牌个数+手中可暗杠个数
        winnerGen = 0
        handTiles = self.tableTileMgr.players[self.winSeatId].copyHandTiles()
        tileArr = MTile.changeTilesToValueArr(handTiles)
        for tile in range(MTile.TILE_MAX_VALUE):
            if tileArr[tile] == 4:
                winnerGen += 1
        gangTiles = self.tableTileMgr.players[self.winSeatId].copyGangArray()
        winnerGen += len(gangTiles)
	if winnerGen > 0:
            return True,winnerGen
	else:
	    return False,winnerGen

    def getGangCount(self):
        """杠"""
        gangTiles = self.tableTileMgr.players[self.winSeatId].copyGangArray()
        return len(gangTiles)

    def isJiangDui(self):
        """
        将对:在【对对胡】牌型中，都是由2,5,8组成的刻字喝将牌
        """
        #if self.tableConfig.get(MTDefine.JIANGDUI, 0) != 1:
        #    return False
	ftlog.debug('MWinRuleLuosihu.isJiangDui result:1') 
        jiang258 = [2,5,8,12,15,18,22,25,28]
        tiles = self.allPlayerTiles[self.winSeatId]
        handTiles = tiles[MHand.TYPE_HAND]  #  self.tableTileMgr.players[self.winSeatId].copyHandTiles()
        chiTiles  = tiles[MHand.TYPE_CHI]   # self.tableTileMgr.players[self.winSeatId].copyChiArray()
        pengTiles = tiles[MHand.TYPE_PENG] #   self.tableTileMgr.players[self.winSeatId].copyPengArray()#[[4, 4, 4]]
        gangTiles = tiles[MHand.TYPE_GANG] #   self.tableTileMgr.players[self.winSeatId].copyGangArray() #'gang': [{'pattern': [31, 31, 31, 31], 'style': True, 'actionID': 11}]
	ftlog.debug('MWinRuleLuosihu.isJiangDui result:2',handTiles)
        for tile in handTiles:
            if not tile in jiang258:
                return False
	ftlog.debug('MWinRuleLuosihu.isJiangDui result:3',pengTiles)
        if len(chiTiles) > 0:
                return False
        for tilePatten in pengTiles:
            if not tilePatten[0] in jiang258:
                return False
        for tile in gangTiles:
            if not tile['pattern'][0] in jiang258:
                return False

        ftlog.debug('MWinRuleLuosihu.isJiangDui result: True')
        return True

    def isYaoJiu(self,patterns):
        """
        幺九:每副顺子，刻字，将牌都包含1或9
        """
        if not self.tableConfig.get(MTDefine.YAOJIU,0):
            return False
        yaojiu = [1,9,11,19,21,29]

        chiTiles  = self.tableTileMgr.players[self.winSeatId].copyChiArray()
        pengTiles = self.tableTileMgr.players[self.winSeatId].copyPengArray()
        gangTiles = self.tableTileMgr.players[self.winSeatId].copyGangArray()

        for tilePatten in pengTiles:
            if not tilePatten[0] in yaojiu:
                return False
        for tile in gangTiles:
            if not tile['pattern'][0] in yaojiu:
                return False
        if len(chiTiles) > 0:        
            return False
        for pattern in patterns:
            isyaojiu = False
            for tile in pattern:
                if tile in yaojiu:
                    isyaojiu = True
            if isyaojiu != True:
                return False 
        return True


    def _checkKouTiles(self, pattern, winSeatId):
        kouTiles = self.tableTileMgr.players[winSeatId].kouTiles
        if kouTiles:
            for p in pattern:
                if len(p) == 3:
                    if p[0] != p[1] or p[1] != p[2]:
                        # 顺子中包含扣牌，不能胡
                        for kouTilesPattern in kouTiles:
                            if kouTilesPattern[0] in p:
                                return False

                elif len(p) == 2:
                    # 将牌中包含扣牌，不能胡
                    for kouTilesPattern in kouTiles:
                        if kouTilesPattern[0] in p:
                            return False
        ftlog.debug('MWinRuleLuosihu _checkKouTiles: pattern=',pattern,',winSeatId=',winSeatId,',kouTiles=',kouTiles)
        return True


    def getHuPattern(self, tiles, magicTiles = []):
        # 此处有坑，winPattern只有一种牌型，这样有问题，比如：[14,14,14,15,15,16,16,16,19,19,19,20,20]，最后抓15
        # 如果卡五星比碰碰胡番数高，此处应该算卡五星，所以isHu应该返回所有可能的胡的牌型，结算时计算最优的番型
        # 未来有时间需要调整一下

        # 先判断定制的逻辑，防止通用逻辑修改造成业务出错
        result, pattern = self.isQidui(tiles)
        if result:
            # 放炮情况下两番起胡，七对肯定是两番，直接返回
            return result, pattern
        return MWin.isHu(tiles[MHand.TYPE_HAND], magicTiles)


    def canDirectHuAfterTing(self):
        """卡五星麻将，听牌后，抓到要胡的牌直接胡，不再要求确认"""
        #modify by youjun 05.02
        return False

    def isQidui(self, tiles):
        handTiles = copy.deepcopy(tiles[MHand.TYPE_HAND])
        handTilesArr = MTile.changeTilesToValueArr(handTiles)

        if len(handTiles) != 14:
            return False, []

        pattern = []
        for tile in range(MTile.TILE_MAX_VALUE):
            if handTilesArr[tile] == 1 or handTilesArr[tile] == 3:
                # 只要出现单数，必然不是七对
                return False, []
            if handTilesArr[tile] == 2:
                pattern.append([tile, tile])
            if handTilesArr[tile] == 4:
            	# 和LuosihuOneResult配合
                pattern.extend([[tile, tile],[tile, tile]])
        return True, pattern



if __name__ == "__main__":
    tiles = [[11,11,13,13,15,15,18,18,19,19,24,24,24,24], [], [], [], [], []]
    rule = MWinRuleLuosihu()
    result, pattern = rule.isHu(tiles, 24, True, MWinRule.WIN_BY_MYSELF, [], [], 0, 0, 10)
    ftlog.debug(result, pattern)
    assert [[11, 11], [13, 13], [15, 15], [18, 18], [19, 19], [24, 24], [24, 24]] == pattern
