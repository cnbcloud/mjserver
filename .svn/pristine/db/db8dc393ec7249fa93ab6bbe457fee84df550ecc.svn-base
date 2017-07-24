# -*- coding=utf-8
'''
Created on 2016年11月26日
庄家规则
@author: luoxf
'''
from majiang2.banker.banker import MBanker

class MBankerHostWinHuangGang(MBanker):
    """
    开始是创建者坐庄,之后胡者接庄,流局有杠，顺时针庄家下家坐庄，无杠由上次庄家继续坐庄,无一炮多响
    """
    def __init__(self):
        super(MBankerHostWinHuangGang, self).__init__()
    
    def getBanker(self, playerCount, isFirst, winLoose, winSeatId, extendInfo = {}):
        """子类必须实现
        参数：
        1）isFirst 是否第一局
        2）winLoose 上局的结果 1分出了胜负 0流局
        3）winSeatId 赢家的座位号，如果第二个参数为0，则本参数为上一局的庄家，如果流局有杠，则是庄家桌位
        """
        if isFirst:
            # 初始化房主
            self.banker = 0
            self.no_result_count = 0
            self.remain_count = 0
        else:
            if winLoose > 0:
                # 有输赢结果
                if winSeatId == self.banker:
                    # 赢得是庄家
                    self.remain_count += 1
                    self.no_result_count = 0
                else:
                    # 赢得是闲家
                    self.banker = winSeatId
                    self.remain_count = 0
                    self.no_result_count = 0
            else:
                # 荒牌，流局，庄家不确定
                self.no_result_count += 1
                if MBanker.GANG_COUNT in extendInfo and extendInfo[MBanker.GANG_COUNT]:
                    self.banker = (self.banker + 1) % playerCount
                    self.remain_count = 0
                else:
                    self.remain_count += 1
                
        return self.banker, self.remain_count, self.no_result_count
    
    def calcNextBanker(self, playerCount, winLoose, winSeatId, extendInfo = {}):
        """子类必须实现
        参数：
        2）winLoose 上局的结果 1分出了胜负 0流局
        3）winSeatId 赢家的座位号，如果第二个参数为0，则本参数为上一局的庄家
        4) isGang为true 庄家下家 false就是庄家
        """
        if winLoose > 0:
            # 有输赢结果
            if winSeatId != self.banker:
                # 赢得是闲家
                nextSeatId = (self.banker + 1) % playerCount
                return nextSeatId
        else:
            if (MBanker.GANG_COUNT in extendInfo) and extendInfo[MBanker.GANG_COUNT]:
                return (self.banker + 1) % playerCount

        return self.banker
