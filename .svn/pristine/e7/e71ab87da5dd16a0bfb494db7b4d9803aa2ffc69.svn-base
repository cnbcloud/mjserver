# -*- coding=utf-8
'''
Created on 2016年9月23日
庄家规则
@author: zhaol
'''

class MBanker(object):
    # 普通输赢
    ONE_WIN_ONE_LOOSE = 1
    # 黄庄，流局
    NO_WIN_NO_LOOSE = 0
    # 一炮多响
    MULTI_WIN_ONE_LOOSE = 2
    # 是否有杠
    GANG_COUNT = 'gangCount'
    
    def __init__(self):
        """类成员变量可继承
        """
        super(MBanker, self).__init__()
        self.banker = 0
        self.remain_count = 0
        self.no_result_count = 0
        
    def reset(self):
        """重置"""
        self.banker = 0
        self.remain_count = 0
        self.no_result_count = 0
        
    @property
    def bankerRemainCount(self):
        return self.remain_count
    
    def getBanker(self, playerCount, isFirst, winLoose, winSeatId, extendInfo = {}):
        """子类必须实现
        参数：
        1）isFirst 是否第一句
        2）winLoose 上局的结果 1分出了胜负 0流局
        3）winSeatId 赢家的座位号，如果第二个参数为0，则本参数为上一局的庄家
        """
        return 0, 0, 0

    def queryBanker(self):
        """查询当前的庄家
        """
        return self.banker
    
    def calcNextBanker(self, playerCount, winLoose, winSeatId, extendInfo = {}):
        """ 计算下一个庄家
            只是计算，不是真的设置庄家
            设置庄家请继续使用getBanker接口
            
        返回值
            计算不出下一局的庄家是，返回0
        """
        return 0
