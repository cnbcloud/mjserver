#! -*- coding:utf-8 -*-
# Author:   qianyong
# Created:  2017/4/12

from majiang2.win_loose_result.one_result import MOneResult
from freetime.util import log as ftlog
from majiang2.tile.tile import MTile
from majiang2.player.hand.hand import MHand
from majiang2.table.table_config_define import MTDefine
from majiang2.ai.win import MWin


def isBaoJiang(self, isZiMo):
    """
    是否报警成功，返回的结果是是否放炮者一人包
    """
    # [{"style":1,"pattern":[]}]
    if len(self.alarmNodes) == 0:
        return False

    # 只有双四核报警会被取消，所以只判断双四核的
    for alarms in self.alarmNodes:
        ftlog.debug('MWuHuOneResult.isBaoJiang alarms style: ', alarms.style, 'pattern:', alarms.pattern)
        if alarms.style == 2 and not isZiMo:
            return True
        if alarms.style == 1:
            # QINGORHUN_ALARM = 1 清混一色 [{'pattern': [8, 8, 8], 'seatId': 0}]
            seatIdArr = []
            for pengs in alarms.pattern:
                seatIdArr.append(pengs["seatId"])

            isTrueAlarm = 0
            # 找出关键的颜色
            seatIdArrCount = MTile.changeTilesToValueArr(seatIdArr)
            for seatId in range(len(seatIdArrCount)):
                if seatIdArrCount[seatId] >= 3:
                    # 如果是同一个人打的 重置self.lastSeatId
                    isTrueAlarm = 1
                    self.setLastSeatId(seatId)
                    ftlog.debug('MWuHuOneResult.isBaoJiang alarmNodes succeed seatId:', seatId)
            if isZiMo and isTrueAlarm == 0:
                return False
            return True
        if alarms.style == 3 and not isZiMo:
            # DOUBLEFOUR_ALARM =3 双四核 pattern:[3,4]碰的tile
            if self.winTile in alarms.pattern:
                return True

    return False

def calcScore(self):
    """算分"""

    # 序列化
    self.serialize()

    self.results[self.KEY_TYPE] = ''
    self.results[self.KEY_NAME] = ''
    self.results[self.KEY_SCORE] = [0 for _ in range(self.playerCount)]
    self.results[self.KEY_FAN_PATTERN] = [[] for _ in range(self.playerCount)]
    self.results[self.KEY_WIN_MODE] = [MOneResult.WIN_MODE_LOSS for _ in range(self.playerCount)]
    # 在和牌时统计自摸，点炮，最大番数
    self.results[self.KEY_STAT] = [[] for _ in range(self.playerCount)]
    extendsLen = len(self.tableConfig.get(MTDefine.DISPLAY_EXTEND_TITLES, []))
    displayExtends = [[0] * extendsLen for _ in xrange(self.playerCount)]

    # 流局不走后面的结算,确保没有设置的值不会被使用
    if self.resultType == self.RESULT_FLOW:
        self.results[self.KEY_TYPE] = MOneResult.KEY_TYPE_NAME_FLOW
        ftlog.debug("MWuHuOneResult calcScore Type = RESULT_FLOW return")
        return

    ftlog.debug('MWuHuOneResult.calcScore playerAllTiles=', self.playerAllTiles)
    # 番分重置
    self.setFanXingIndex()
    # 手牌胡牌牌型 如：[[7, 7], [4, 5, 6], [1, 2, 3]]
    self.setHandWinPattern()
    ftlog.debug('MWuHuOneResult.calcScore handHuPattern: ', self.handHuPattern)
    # 嘴子计算 混一色、通天、四核、对对胡、杠后开花 存嘴子的结果 如果全部都有 则为[1,1,1,1,1]
    zuiZiArr = []
    zuiZiArr.append([self.HUNYISE, self.isHunyise()])
    zuiZiArr.append([self.TONGTIAN, self.isTongTian()])
    zuiZiArr.append([self.SIHE, self.isSiHe()])
    zuiZiArr.append([self.DUIDUIHU, self.isDuiDuiHu()])
    zuiZiArr.append([self.GANGKAI, self.gangKai])
    for result in zuiZiArr:
        if result[1]:
            name = self.fanXing[result[0]]['name']
            index = self.fanXing[result[0]]['index']
            self.addWinFanPattern(name, index)

    # 比较特殊
    if self.isShuangSiHe():
        zuiZiArr.append([self.SIHE, 1])
        zuiZiArr.append([self.SIHE, 1])

    isZiMo = self.winSeatId == self.lastSeatId
    # 是否是交牌
    isJiaoPai, isHunYise = self.isJiaoPai(zuiZiArr)
    mingScore, anScore = self.calcGangFan(isJiaoPai)
    self._MWuHuOneResult__countByJiao = isJiaoPai
    ftlog.debug("MWuHuOneResult calcScore isJiaoPai:", isJiaoPai, "isHunYise:", isHunYise, 'winType:',
                self.winRuleMgr.winType)
    if isJiaoPai:
        name = self.fanXing[self.JIAOPAI]['name']
        index = self.fanXing[self.JIAOPAI]['index']
        self.addWinFanPattern(name, index)

        fanScore = self.calcJiaoPsiScore(isJiaoPai, zuiZiArr, isZiMo, isHunYise)
        ftlog.debug("MWuHuOneResult calcScore fanScore:", fanScore, "self.playerCount:", self.playerCount)
        if self.isBaoJiang(isZiMo):
            # 报警成功 一家付支付
            self.results[self.KEY_SCORE][self.lastSeatId] = -fanScore * (self.playerCount - 1)
            self.results[self.KEY_SCORE][self.winSeatId] = fanScore * (self.playerCount - 1)
        else:
            winScore = 0
            if isZiMo:
                for i in range(self.playerCount):
                    failScore = fanScore
                    if self.winSeatId != i:
                        if self.jiaoPaiConf["base_caps"] > 0:
                            # 有封顶
                            failScore = min(failScore, self.jiaoPaiConf["base_caps"])

                        self.results[self.KEY_SCORE][i] = -failScore
                        winScore += failScore

                self.results[self.KEY_SCORE][self.winSeatId] = winScore
            elif self.winRuleMgr.winType == MTDefine.WIN_TYPE1:  # 胡牌赢三家
                for i in range(self.playerCount):
                    failScore = fanScore
                    if self.winSeatId != i:
                        if self.lastSeatId == i:
                            failScore += 10  # 点炮者单独附加10分
                        if self.jiaoPaiConf["base_caps"] > 0:
                            # 有封顶
                            failScore = min(failScore, self.jiaoPaiConf["base_caps"])

                        self.results[self.KEY_SCORE][i] = -failScore
                        winScore += failScore

                self.results[self.KEY_SCORE][self.winSeatId] = winScore
            elif self.winRuleMgr.winType == MTDefine.WIN_TYPE2:  # 点炮包三家
                if self.jiaoPaiConf["base_caps"] > 0:
                    fanScore = min(fanScore, self.jiaoPaiConf["base_caps"])
                self.results[self.KEY_SCORE][self.winSeatId] = fanScore * (self.playerCount - 1)
                self.results[self.KEY_SCORE][self.lastSeatId] = -fanScore * (self.playerCount - 1)

        for i in range(self.playerCount):
            self.results[self.KEY_STAT][i].append({MOneResult.STAT_JIAOPAI: self.results[self.KEY_SCORE][i]})
    else:
        fanScore, zuiziScore = self.calcBaseFan(zuiZiArr)  # 底番 嘴子加分
        zuiziScore += mingScore + anScore
        zhiCount = self.getZhiCount()  # 支数
        yaScore = self.getYaoCount()  # 押分
        ftlog.debug("MWuHuOneResult calcScore zhiCount:", zhiCount, "yaScore:", yaScore, "isZiMo:", isZiMo,
                    "isbanker", self.winSeatId == self.bankerSeatId)

        winScore = 0
        if self.multiple == 1:  # 30个牌码
            tempBaseScore = (zhiCount + yaScore) * 2 / 10.0
        else:
            tempBaseScore = (zhiCount + yaScore) / 2.0

        if isZiMo:
            for i in range(self.playerCount):
                if self.winSeatId != i:
                    if self.winSeatId == self.bankerSeatId or i == self.bankerSeatId:
                        # 点炮者支付的算分和庄家一样
                        failScore = int(round(tempBaseScore * 2)) + fanScore * 2 + zuiziScore
                    else:
                        failScore = int(round(tempBaseScore * 2)) + fanScore + zuiziScore

                    self.results[self.KEY_SCORE][i] = -failScore
                    winScore += failScore

            self.results[self.KEY_SCORE][self.winSeatId] = winScore
        elif self.winRuleMgr.winType == MTDefine.WIN_TYPE1:  # 胡牌赢三家
            for i in range(self.playerCount):
                if self.winSeatId != i:
                    if self.multiple == 1:  # 30个牌码
                        etraAddScore = 1
                    else:
                        etraAddScore = 2

                    if self.lastSeatId == i and i == self.bankerSeatId:
                        # 庄家点炮多加2分
                        failScore = int(round(tempBaseScore)) + fanScore * 2 + zuiziScore + etraAddScore
                    elif self.winSeatId == self.bankerSeatId and self.lastSeatId == i:
                        # 点给庄家多加2分
                        failScore = int(round(tempBaseScore)) + fanScore * 2 + zuiziScore + etraAddScore
                    elif self.winSeatId == self.bankerSeatId or self.lastSeatId == i or i == self.bankerSeatId:
                        # 点炮者支付的算分和庄家一样
                        failScore = int(round(tempBaseScore)) + fanScore * 2 + zuiziScore
                    else:
                        failScore = int(round(tempBaseScore)) + fanScore + zuiziScore

                    self.results[self.KEY_SCORE][i] = -failScore
                    winScore += failScore

            self.results[self.KEY_SCORE][self.winSeatId] = winScore
        elif self.winRuleMgr.winType == MTDefine.WIN_TYPE2:  # 点炮包三家
            for i in range(self.playerCount):
                if self.winSeatId != i:
                    if self.winSeatId == self.bankerSeatId or i == self.bankerSeatId:
                        failScore = int(round(tempBaseScore)) + fanScore * 2 + zuiziScore
                    else:
                        failScore = int(round(tempBaseScore)) + fanScore + zuiziScore
                    winScore += failScore

            self.results[self.KEY_SCORE][self.winSeatId] = winScore
            self.results[self.KEY_SCORE][self.lastSeatId] = -winScore

    if self.gangKai:
        self.results[self.KEY_WIN_MODE][self.winSeatId] = MOneResult.WIN_MODE_GANGKAI
    elif isZiMo:
        self.results[self.KEY_WIN_MODE][self.winSeatId] = MOneResult.WIN_MODE_ZIMO
    elif self.qiangGang:
        self.results[self.KEY_WIN_MODE][self.winSeatId] = MOneResult.WIN_MODE_QIANGGANGHU
        self.results[self.KEY_WIN_MODE][self.lastSeatId] = MOneResult.WIN_MODE_DIANPAO
    else:
        self.results[self.KEY_WIN_MODE][self.winSeatId] = MOneResult.WIN_MODE_PINGHU
        self.results[self.KEY_WIN_MODE][self.lastSeatId] = MOneResult.WIN_MODE_DIANPAO

    # 不是交牌 要判断输的分数不能超过玩家积分
    if not isJiaoPai:
        tempWinScore = 0
        for i in range(self.playerCount):
            if i != self.winSeatId:
                tempScore = self.results[self.KEY_SCORE][i]
                curScore = self.playerCurScore[i]
                if (tempScore + curScore) <= 0:
                    self.results[self.KEY_SCORE][i] = -curScore
                tempWinScore += -self.results[self.KEY_SCORE][i]

        self.results[self.KEY_SCORE][self.winSeatId] = tempWinScore

    # 需要统计的 胡牌 坐庄 交牌
    self.results[self.KEY_STAT][self.winSeatId].append({MOneResult.STAT_WIN: 1})
    self.results[self.KEY_STAT][self.bankerSeatId].append({MOneResult.STAT_BANKER: 1})

    if isZiMo or self.winRuleMgr.winType == MTDefine.WIN_TYPE1:
        for i in range(self.playerCount):
            if self.winSeatId == i:
                displayExtends[i][self.MING_GANG_INDEX] = mingScore * (self.playerCount - 1)
                displayExtends[i][self.AN_GANG_INDEX] = anScore * (self.playerCount - 1)
                displayExtends[i][self.WIN_INDEX] = self.results[self.KEY_SCORE][i] - \
                                                    mingScore * (self.playerCount - 1) - anScore * (
                self.playerCount - 1)
            else:
                displayExtends[i][self.WIN_INDEX] = self.results[self.KEY_SCORE][i] + mingScore + anScore
                displayExtends[i][self.MING_GANG_INDEX] = -mingScore
                displayExtends[i][self.AN_GANG_INDEX] = -anScore
    elif self.winRuleMgr.winType == MTDefine.WIN_TYPE2:  # 点炮包三家
        displayExtends[self.winSeatId][self.MING_GANG_INDEX] = mingScore * (self.playerCount - 1)
        displayExtends[self.winSeatId][self.AN_GANG_INDEX] = anScore * (self.playerCount - 1)
        displayExtends[self.winSeatId][self.WIN_INDEX] = self.results[self.KEY_SCORE][self.winSeatId] - \
                                                         mingScore * (self.playerCount - 1) - anScore * (
        self.playerCount - 1)

        displayExtends[self.lastSeatId][self.MING_GANG_INDEX] = -displayExtends[self.winSeatId][
            self.MING_GANG_INDEX]
        displayExtends[self.lastSeatId][self.AN_GANG_INDEX] = -displayExtends[self.winSeatId][self.AN_GANG_INDEX]
        displayExtends[self.lastSeatId][self.WIN_INDEX] = -displayExtends[self.winSeatId][self.WIN_INDEX]

    self.results[self.KEY_DISPLAY_EXTEND] = displayExtends
    self.results[self.KEY_TYPE] = MOneResult.KEY_TYPE_NAME_HU
    self.results[self.KEY_FAN_PATTERN][self.winSeatId] = self.winFanPattern

    ftlog.debug('MWuHuOneResult calcScore:KEY_DISPLAY_EXTEND:', self.results[self.KEY_DISPLAY_EXTEND])
    ftlog.debug('MWuHuOneResult calcScore:KEY_SCORE:', self.results[self.KEY_SCORE])
    ftlog.debug('MWuHuOneResult calcScore:KEY_TYPE:', self.results[self.KEY_TYPE])
    ftlog.debug('MWuHuOneResult calcScore:KEY_WIN_MODE:', self.results[self.KEY_WIN_MODE])
    ftlog.debug('MWuHuOneResult calcScore:KEY_FAN_PATTERN:', self.results[self.KEY_FAN_PATTERN])
    ftlog.debug('MWuHuOneResult calcScore:KEY_STAT:', self.results[self.KEY_STAT])


from majiang2.win_loose_result.wuhu_one_result import MWuHuOneResult
MWuHuOneResult.isBaoJiang = isBaoJiang
MWuHuOneResult.calcScore = calcScore
