# -*- coding=utf-8
'''
Created on 2016年9月23日
庄家规则
@author: zhaol
'''
from majiang2.banker.banker import MBanker
import random

class MBankerRandomRemain(MBanker):
    """
    开局随机庄家，之后连庄的规则
    庄家赢，连庄
    闲家赢，闲家坐庄
    """
    def __init__(self):
        super(MBankerRandomRemain, self).__init__()
    
    def getBanker(self, playerCount, isFirst, winLoose, winSeatId, extendInfo = {}):
        """子类必须实现
        参数：
        1）isFirst 是否第一句
        2）winLoose 上局的结果 1分出了胜负 0流局
        3）winSeatId 赢家的座位号，如果第二个参数为0，则本参数为上一局的庄家
        """
        if isFirst:
            # 初始化，随机选庄
            self.banker = random.randint(0, playerCount - 1)
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
                # 荒牌，流局，庄家继续，荒牌次数加一，坐庄次数加一
                self.no_result_count += 1
                self.remain_count += 1
                
        return self.banker, self.remain_count, self.no_result_count

    def calcNextBanker(self, playerCount, winLoose, winSeatId, extendInfo = {}):
        """ 计算下一个庄家
            只是计算，不是真的设置庄家
            设置庄家请继续使用getBanker接口
        """

        if winLoose > 0:
            # 有输赢结果
            if winSeatId == self.banker:
                return self.banker
            else:
                return winSeatId
                
        return self.banker