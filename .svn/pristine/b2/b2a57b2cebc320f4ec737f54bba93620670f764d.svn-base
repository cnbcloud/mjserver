# -*- coding=utf-8
'''
Created on 2016年9月23日

本副牌局的和牌结果，可能有多个
1）普通麻将一个结果
2）血战到底N-1个结果，N为牌桌人数
3）血流成河有多个结果，直到本局牌全部发完
@author: zhaol
'''
from freetime.util import log as ftlog
from majiang2.win_loose_result.one_result import MOneResult
from majiang2.table.table_config_define import MTDefine

class MRoundResults(object):
    
    def __init__(self):
        super(MRoundResults, self).__init__()
        self.__round_index = 0
        self.__round_results = []
        self.__fan_patterns = []
        self.__score = None
        self.__delta = None
        self.__playMode = ''   
    
    @property
    def playMode(self):
        return self.__playMode
    
    def setPlayMode(self, playMode):
        self.__playMode = playMode
        
    @property
    def delta(self):
        return self.__delta
        
    @property
    def score(self):
        return self.__score

    @property
    def fanPatterns(self):
        return self.__fan_patterns

    @property
    def roundIndex(self):
        return self.__round_index
    
    def setRoundIndex(self, index):
        self.__round_index = index
        
    @property
    def roundResults(self):
        return self.__round_results
    
    def getRoundGangResult(self):
        score = None
        for result in self.roundResults:
            if result.resultType == MOneResult.RESULT_GANG:
                deltaScore = result.results.get(MOneResult.KEY_SCORE, [0 for _ in range(result.playerCount)])
                if not score:
                    score = deltaScore
                else:
                    for index in range(len(score)):
                        score[index] += deltaScore[index]
        return score

    def getRoundWinResult(self):
        score = None
        for result in self.roundResults:
            if result.resultType == MOneResult.RESULT_WIN:
                deltaScore = result.results.get(MOneResult.KEY_SCORE, [0 for _ in range(result.playerCount)])
                if not score:
                    score = deltaScore
                else:
                    for index in range(len(score)):
                        score[index] += deltaScore[index]
        return score

    def addRoundResult(self, result):
        """添加轮次结果"""
        ftlog.debug('MRoundResults.addRoundResult : ', result.results
                , ' now roundIndex:', self.__round_index
                )
        
        if not result.isResultOK():
            return
        
        self.__round_results.append(result)
        self.__delta = result.results.get(MOneResult.KEY_SCORE, [0 for _ in range(result.playerCount)])[:]
        if result.results.has_key(MOneResult.KEY_FAN_PATTERN):
            if self.__fan_patterns == []:
                # 根据返回值的玩家人数，初始化
                self.__fan_patterns = [[] for _ in range(len(result.results[MOneResult.KEY_FAN_PATTERN]))]
            for index in range(len(result.results[MOneResult.KEY_FAN_PATTERN])):
                self.__fan_patterns[index].extend(result.results[MOneResult.KEY_FAN_PATTERN][index])
        #潜江晃晃中途不计算积分
        if self.playMode in ["huanghuang-qianjiang","huanghuang-shiyan"]:
            self.__score = [0 for _ in range(result.playerCount)]    
        elif not self.__score:
            self.__score = self.__delta
        else:
            for index in range(len(self.__delta)):
                self.__score[index] += self.__delta[index]
        ftlog.debug('MRoundResults.addRoundResult totalScore:',self.__score
            , ' deltaScore:', self.__delta)        
        ftlog.debug('MRoundResults.addRoundResult type:', result.results[MOneResult.KEY_TYPE]
            , ' name:', result.results[MOneResult.KEY_NAME]
            , ' totalScore:', self.__score
            , ' deltaScore:', self.__delta
            , ' fanPatterns:', self.__fan_patterns
            )
    
    def getMergeFanPatternList(self):
        
        patternCount = 0
        eachPattern = []
        patternValue = []
        for index in range(len(self.__fan_patterns)):
            fanPatternList = []
            for fan_index in range(len(self.__fan_patterns[index])):
                eachPattern = self.__fan_patterns[index][fan_index]
                patternCount = self.__fan_patterns[index].count(eachPattern)
                if patternCount > 1:
                    patternValue = eachPattern[0]+str(patternCount)
                else:
                    patternValue = eachPattern[0]
                patternValue=[patternValue]
                if self.playMode in ["huanghuang-shiyan","huanghuang-qianjiang","huanghuang-suizhou","huanghuang-test2"]:
                    if patternCount>1:
                        patternValue[0]=eachPattern[0]+"*"+str(patternCount)
                    else:
                        patternValue[0] = eachPattern[0]
                    if eachPattern[1]:
                        patternValue[0]+="#%s"%(str(int(eachPattern[1])*patternCount))
                    patternValue.append(eachPattern[2])
                    
                if patternValue not in fanPatternList:
                    fanPatternList.append(patternValue)
            self.__fan_patterns[index] = fanPatternList
        return self.__fan_patterns;

    #潜江晃晃特定玩法的算分
    def getQianJiangHHScoreList(self,players,BankerSeatId):
        if self.playMode in ["huanghuang-gongan"]:
            return
        #计算赖子杠翻后的分数
        laiziFan=[]
        for cp in players:
            laiziFan.append(pow(2,len(cp.laiziGang)))
        playerCount=len(players)
        allScore=[0 for _ in xrange(playerCount)]
        maTileToSeat=[[] for _ in xrange(playerCount)]
        maTileScore=[]
        maValue=[]
        lastGangResult=[]#记录抢杠胡和热铳时的杠的结果
        lastGangScore=0#记录热铳时放铳玩家笑的总分数
        allGangScore=[]#记录下每个杠最后的得分
        #热铳最后计算分数，加杠的分数
        result=self.__round_results[-1]
        if result.resultType == MOneResult.RESULT_WIN and (result.winRuleMgr.reHu or result.qiangGang):
            gangIndex=self.__round_results.index(result)-1
            gangResult=self.__round_results[gangIndex]
            lastGangResult.append(gangResult)
            lastWinSeat=gangResult.winSeatId
            lastActionID=gangResult.actionID
            if len(self.__round_results)>2:
                for result1 in self.__round_results[:-2][::-1]:
                    if result1.winSeatId == lastWinSeat and (lastActionID-result1.actionID)<=2:
                        lastGangResult.append(result1)
                        lastActionId=result1.actionID
                    else:
                        break
            ftlog.info("getQianJiangHHScoreList reHu:",result.qiangGang,lastActionID,result.actionID)
            result.winRuleMgr.setReHu(0)#重置热铳

        for i in xrange(playerCount):
            cp=players[i]
            for ma in cp.maTiles:
                a=((ma%10)%playerCount)-1
                if a<0:
                    a+=playerCount
                maTileToSeat[i].append((BankerSeatId+a)%playerCount)
                maValue.append((BankerSeatId+a)%playerCount)
                maTileScore.append(0)
            ftlog.debug("getQianJiangHHScoreList:","seatId:",cp.curSeatId,"maTile:",cp.maTiles,maTileToSeat[i],BankerSeatId,laiziFan)

        for resultIndex in xrange(len(self.__round_results)):
            result=self.__round_results[resultIndex]
            ftlog.debug("getQianJiangHHScoreList result.results",result.results)
            if result.resultType == MOneResult.RESULT_FLOW:
                ftlog.info("getQianJiangHHScoreList gameFlow")
                break

            if result.resultType == MOneResult.RESULT_WIN and  lastGangResult:
                for gangScore in allGangScore:
                    for sc in gangScore:
                        if sc>0:
                            lastGangScore+=sc
                        ftlog.info("getQianJiangHHScoreList lastGangScore:",gangScore,lastGangScore)

            if result in lastGangResult:
                tmpMaTileScore=maTileScore[:]#如果是热铳或抢杠胡，保存此时马牌分数

            oneScore=[0 for _ in xrange(playerCount)]
            yingIndex=[]
            shuIndex=[]
            for index in xrange(len(result.results[MOneResult.KEY_SCORE])):
                if result.results[MOneResult.KEY_SCORE][index]>0:
                    yingIndex.append(index)
                elif result.results[MOneResult.KEY_SCORE][index]<0:
                    shuIndex.append(index)
            if len(yingIndex)>len(shuIndex):
                baseScore=-result.results[MOneResult.KEY_SCORE][yingIndex[0]]
            else:
                baseScore=result.results[MOneResult.KEY_SCORE][shuIndex[0]]

            for ying in yingIndex:
                for shu in shuIndex:
                    oneScore[ying]-=laiziFan[ying]*laiziFan[shu]*baseScore
                    oneScore[shu]+=laiziFan[ying]*laiziFan[shu]*baseScore
                    if lastGangScore:
                        oneScore[ying]+=lastGangScore
                        oneScore[shu]-=lastGangScore
                    ftlog.debug("getQianJiangHHScoreList oneScore",oneScore,"maValue",maValue,"maTileScore",maTileScore)
                if maValue:
                    for maIndex in xrange(len(maValue)):
                        if maValue[maIndex] == ying:
                            for shu1 in shuIndex:
                                maTileScore[maIndex]-=laiziFan[ying]*laiziFan[shu1]*baseScore
                                oneScore[shu1]+=laiziFan[ying]*laiziFan[shu1]*baseScore
                                if lastGangScore:
                                    maTileScore[maIndex]+=lastGangScore
                                    oneScore[shu1]-=lastGangScore
                                ftlog.debug("getQianJiangHHScoreList oneScore",oneScore,"maValue",maValue,"maTileScore",maTileScore)
                        elif maValue[maIndex] in shuIndex:
                            oneScore[ying]-=laiziFan[ying]*laiziFan[maValue[maIndex]]*baseScore
                            maTileScore[maIndex]+=laiziFan[ying]*laiziFan[maValue[maIndex]]*baseScore
                            if lastGangScore:
                                oneScore[ying]+=lastGangScore
                                maTileScore[maIndex]-=lastGangScore
                            ftlog.debug("getQianJiangHHScoreList oneScore",oneScore,"maValue",maValue,"maTileScore",maTileScore)
                            for maIndex1 in xrange(len(maValue)):
                                if maValue[maIndex1] == ying:
                                     maTileScore[maIndex1]-=laiziFan[ying]*laiziFan[maValue[maIndex]]*baseScore
                                     maTileScore[maIndex]+=laiziFan[ying]*laiziFan[maValue[maIndex]]*baseScore
                                     if lastGangScore:
                                         maTileScore[maIndex1]+=lastGangScore
                                         maTileScore[maIndex]-=lastGangScore

            #记录被抢杠或着热铳后的计算后得分，以便抢杠胡和热铳时拿出来计算
            if result in lastGangResult:
                maTileScore=tmpMaTileScore#如果是抢杠胡，重置马牌在杠上的得分
                allGangScore.append(oneScore)
                for index in xrange(playerCount):
                    onePattern=result.results[MOneResult.KEY_FAN_PATTERN][index]
                    if onePattern:
                        patternsIndex=self.__fan_patterns[index].index(onePattern[0])
                        self.__fan_patterns[index][patternsIndex]=[onePattern[0][0],str(0),1]

                        #self.__fan_patterns[index][patternsIndex]=[onePattern[0][0],1]
            else:
                for index in xrange(playerCount):
                    onePattern=result.results[MOneResult.KEY_FAN_PATTERN][index]
                    if onePattern:
                        patternsIndex=self.__fan_patterns[index].index(onePattern[0])
                        #self.__fan_patterns[index][patternsIndex]=[onePattern[0][0],self.isYingOrShu(oneScore[index])]
                        self.__fan_patterns[index][patternsIndex]=[onePattern[0][0],str(oneScore[index]),self.isYingOrShu(oneScore[index])]
                    
                    allScore[index]+=oneScore[index]
            ftlog.info("getQianJiangHHScoreList allScore:",allScore,"oneScore:",oneScore,"maValue:",maValue,"maTileScore:",maTileScore,result in lastGangResult,"baseScore:",baseScore)

        #喜相逢分数计算
        xiXiangFengScore=[]
        xXFbase=result.tableConfig.get(MTDefine.XIXIANGFENG,0)
        if xXFbase:
            for seat in xrange(playerCount):
                cp=players[seat]
                if len(cp.laiziGang)==4:
                    xiXiangFengScore=[ -xXFbase for _ in xrange(playerCount)]
                    xiXiangFengScore[seat]=xXFbase*(playerCount-1)
                    if maValue:
                        for maIndex in xrange(len(maValue)):
                            if maValue[maIndex] == seat:
                                for xXFSeat in xrange(playerCount) :
                                    if xXFSeat != seat :
                                        xiXiangFengScore[xXFSeat]-=xXFbase
                                        maTileScore[maIndex]+=xXFbase
                            else:
                                xiXiangFengScore[seat]+=xXFbase
                                maTileScore[maIndex]-=xXFbase
                                for maIndex1 in xrange(len(maValue)):
                                    if maValue[maIndex1]==seat:
                                        maTileScore[maIndex1]+=xXFbase
                                        maTileScore[maIndex]-=xXFbase

                    ftlog.info("getQianJiangHHScoreList xiXiangFeng:",xiXiangFengScore,"xXFbase:",xXFbase,"maTileScore:",maTileScore)

        if xiXiangFengScore:
            for index in xrange(playerCount):
                if xiXiangFengScore[index]>0:
                    result.results[MOneResult.KEY_STAT][index].append({"xiXiangFeng":1})
                allScore[index]+=xiXiangFengScore[index]

        for index in xrange(playerCount):
            cp=result.tableTileMgr.players[index]
            laiziGangCount=len(cp.laiziGang)
            if laiziGangCount:
                if laiziGangCount==1:
                    self.__fan_patterns[index].append(["癞子",0,1])
                else:
                    self.__fan_patterns[index].append(["癞子*"+str(laiziGangCount),0,1])
                if laiziGangCount == 4 and result.tableConfig.get(MTDefine.XIXIANGFENG,0):
                    #self.__fan_patterns[index].append(["喜相逢",1])
                    for xiIndex in xrange(playerCount):
                        self.__fan_patterns[xiIndex].append(["喜相逢",str(xiXiangFengScore[xiIndex]),self.isYingOrShu(xiXiangFengScore[xiIndex])])
                        
        self.__score=allScore[:]
        for seat in xrange(playerCount):
            #self.__fan_patterns[seat].insert(0,["人"+str(allScore[seat]),self.isYingOrShu(allScore[seat])])
            for ma in maTileToSeat[seat]:
                maSeat=maValue.index(ma)
                maScore=maTileScore[maSeat]
                self.__score[seat]+=maScore
                #self.__fan_patterns[seat].append(["买马",self.isYingOrShu(maScore)])
                maMark=self.isYingOrShu(maScore)
                if maScore==0:
                    maMark=2
                self.__fan_patterns[seat].append(["买马",str(maScore),maMark])
        ftlog.info("getQianJiangHHScoreList all",self.__score,"laiziFan",laiziFan,"maTile",maValue,"maTileScore",maTileScore,"maTileSeat",maTileToSeat,BankerSeatId)
    
    def isYingOrShu(self,score):
        if score>=0:
            return 1
        else:
            return 0
