# -*- coding=utf-8
'''
Created on 2016年9月23日
庄家规则
@author: zhaol
'''
from majiang2.ai.play_mode import MPlayMode
from majiang2.banker.banker_random_remain import MBankerRandomRemain
from majiang2.banker.bank_host_win import MBankerHostWin
from majiang2.banker.bank_host_next import MBankerHostNext
from majiang2.banker.banker_random_huangNext_multiPao import MBankerRandomHuangNextMuiltPao
from majiang2.banker.bank_host_win_huang_gang import MBankerHostWinHuangGang
from majiang2.banker.bank_host_next_huang_next import MBankerHostNextHuangNext
from majiang2.banker.bank_host_next_huang_gang import MBankerHostNextHuangGang
from majiang2.banker.banker_host_win_multiPao_jiao import MBankerHostWinMultiPaoJiao

class BankerFactory(object):
    # 初始随机 坐庄玩法
    RANDOM_REMAIN = 'random_remain'
    # 首局房主坐庄 赢家接庄
    HOST_WIN = 'host_win'
    # 首局房主坐庄 输了庄下家接庄
    HOST_NEXT = 'host_next'
    # 初始随机，黄庄下一个人，一炮多响放炮者坐庄
    RANDOM_NEXT_MULTIPAO = 'random_next_multi_pao'
    # 首局房主坐庄 赢家接庄 黄庄按杠坐庄
    HOST_WIN_HUANG_GANG = 'host_win_huang_gang'
    # 首局房主坐庄 下家接庄 黄庄下家坐庄
    HOST_NEXT_HUANG_NEXT = 'host_next_huang_next'
    # 首局房主坐庄 下家接庄 黄庄按杠坐庄
    HOST_NEXT_HUANG_GANG = 'host_next_huang_gang'
    # 螺丝胡 血战到底 庄家规则
    HOST_WIN_MULTIPAO_JIAO = 'host_win_multi_jiao'

    def __init__(self):
        super(BankerFactory, self).__init__()
    
    @classmethod
    def getBankerAI(cls, playMode):
        """庄家规则获取工厂
        输入参数：
            playMode - 玩法
        
        返回值：
            对应玩法的庄家管理规则
        """
        bankerType = cls.getBankerTypeByPlayMode(playMode)
        if bankerType == cls.RANDOM_REMAIN:
            return MBankerRandomRemain()
        if bankerType == cls.RANDOM_NEXT_MULTIPAO:
            return MBankerRandomHuangNextMuiltPao()
        if bankerType == cls.HOST_WIN:
            return MBankerHostWin()
        if bankerType == cls.HOST_NEXT:
            return MBankerHostNext()
        if bankerType == cls.HOST_WIN_HUANG_GANG:
            return MBankerHostWinHuangGang()
        if bankerType == cls.HOST_NEXT_HUANG_NEXT:
            return MBankerHostNextHuangNext()
        if bankerType == cls.HOST_NEXT_HUANG_GANG:
            return MBankerHostNextHuangGang()
        if bankerType == cls.HOST_WIN_MULTIPAO_JIAO:
            return MBankerHostWinMultiPaoJiao()
        return MBankerHostNext()
    
    @classmethod
    def getBankerTypeByPlayMode(cls, playMode):
	if MPlayMode().isSubPlayMode(playMode, MPlayMode.QUESHOU):
            return cls.HOST_NEXT
        elif MPlayMode().isSubPlayMode(playMode, MPlayMode.LUOSIHU):
            if playMode == 'luosihu-luosihu':
                return cls.HOST_NEXT_HUANG_NEXT
            elif playMode == 'luosihu-xuezhan':
                return cls.HOST_WIN_MULTIPAO_JIAO
            elif playMode == 'luosihu-ctxuezhan':
                return cls.HOST_WIN_MULTIPAO_JIAO
        return None
