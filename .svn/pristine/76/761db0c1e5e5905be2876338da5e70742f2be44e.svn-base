# -*- coding=utf-8
'''
Created on 2016年9月23日

@author: zhaol

说明：
摸牌 吃碰杠胡 这些状态都通过msg和actionHandler去驱动，不要在里面直接跳转状态。
这样会把基本api的功能搞的非常复杂。
比如dropHu，louHu
加一个状态，在下一次的timer tick或者msg handle里面自动处理就行了

这么做有两个好处：
1）交互比较清晰，前端有机会看的清楚摸牌，打牌的操作
2）基本api逻辑简单清楚

任何操作都可以导致胡牌或者别的操作，通过状态去调度。
不要直接在状态间切换，比如在dropTile里面gameWin或者，在addTile里面gameWin，补花
这样，很快逻辑就臃肿的没法儿看了。

'''

class MTableState(object):
    """开始打牌后的牌桌状态
    状态的位数代表了优先级，位数越高，优先级越高
    """
    # 牌桌无状态，未开始
    TABLE_STATE_NONE        = -1
    # 给下家发牌，next
    TABLE_STATE_NEXT        = 0
    # 二进制第一位 等待出牌，出牌的座位号是当前座位号
    TABLE_STATE_DROP        = 0b1
    # 二进制第二位 等待吃牌，吃牌的座位号是当前座位号的下一个
    TABLE_STATE_CHI         = 0b10
    # 二进制第三位 等待碰牌，碰牌的座位号可以是其他的任何人
    TABLE_STATE_PENG        = 0b100
    # 二进制第四位 等待杠牌，杠牌的座位号可以使任何一个人，当杠牌座位号与当前座位号相同时，为暗杠；当碰牌座位号与当前座位号不同时，为明杠
    TABLE_STATE_GANG        = 0b1000
    # 二进制第五位，听牌，表示只和听牌后的这几张牌
    TABLE_STATE_TING        = 0b10000
    # 二进制第六位，抢听，抢先停牌
    TABLE_STATE_GRABTING    = 0b100000
    # 二进制第七位，翻屁股，云南幺鸡麻将的特殊玩法
    TABLE_STATE_FANPIGU     = 0b1000000
    # 二进制第八位，定缺，特殊玩法，四川玩法具有定缺规则
    TABLE_STATE_ABSENCE     = 0b10000000
    # 二进制第九位，换宝牌，交换原先杠牌/吃牌中的宝牌
    TABLE_STATE_CHANGE_MAGIC= 0b100000000
    # 二进制第十位，抢杠和，抢回头杠，碰杠的和牌
    TABLE_STATE_QIANGGANG   = 0b1000000000
    # 二进制第十一位，鸡西粘牌
    TABLE_STATE_ZHAN        = 0b10000000000
    # 二进制第十二位，平度飘牌
    TABLE_STATE_PIAO        = 0b100000000000

    
    '''
    威海放锚
    把东西南北中发白作为锚牌，起手抓完牌，手中至少包含三张符合条件的锚牌，才可以选择放锚
    。也可以选择不放锚，不能在中间的过程中放锚。选择放锚后，手中所有的锚牌都摆在门前，如果
    锚牌超过三张，多几张就从杠尾补几张，如果补回来的还是锚牌，继续从杠尾补。后续抓牌时的锚牌，
    也必须摆在门前，不能放在手中做掌和副，并从杠尾补一张，放锚的牌，其他三家不能碰和杠。
    
    每个人第一次出牌的时候定是否放锚
    放锚的话全放，不给玩家其他选择
    不放，则失去放锚机会
    后续摸上来的牌自动不锚
    
    '''

    #放锚
    TABLE_STATE_FANGMAO     = 0b1000000000000
    #白城麻将 有玩家补锚的时候，可以抢碰
    TABLE_STATE_QIANG_EXMAO = 0b10000000000000
    #白城麻将 有玩家补锚的时候，可以抢胡
    TABLE_STATE_QIANG_EXMAO_HU=0b100000000000000
    # 二进制第十五位，漏胡
    TABLE_STATE_PASS_HU       = 0b100000000000000
    # 二进制第十六位，加倍
    TABLE_STATE_DOUBLE        = 0b1000000000000000
    # 二进制第十七位 等待和牌，和牌的座位号可以使任何一个人，当和牌座位号与当前座位号相同时，为自摸；当和牌座位号与当前座位号不同时，为吃和
    TABLE_STATE_HU            = 0b10000000000000000
    # 二进制第十八位，血战到底，三个人和牌或者牌都发完后结束
    TABLE_STATE_XUEZHAN       = 0b100000000000000000
    # 二进制第十九位，血流成河，所有牌发完后结束
    TABLE_STATE_XUELIU        = 0b1000000000000000000
    # 二进制第二十位，补花 玩家摸到花牌事可以补花
    TABLE_STATE_BUFLOWER      = 0b10000000000000000000
    # 二进制第二十一位，济南掷骰子
    TABLE_STATE_SAIZI         = 0b100000000000000000000
    # 二进制第二十二位，福州开金
    TABLE_STATE_KAIJIN        = 0b1000000000000000000000
    # 二进制第二十三位，福州抢金庄
    TABLE_STATE_QIANGJIN_B    = 0b10000000000000000000000
    # 二进制第二十四位，福州抢金
    TABLE_STATE_QIANGJIN      = 0b100000000000000000000000
    # 二进制第二十三位，福州三金倒
    TABLE_STATE_SANJINDAO     = 0b1000000000000000000000000
    # 二进制第二十五位，福州天胡
    TABLE_STATE_TIANHU        = 0b10000000000000000000000000
    # 二进制第三十二位 和牌之后牌局结束
    TABLE_STATE_GAME_OVER     = 0b10000000000000000000000000000000
    
    def __init__(self):
        super(MTableState, self).__init__()
        self.__states = 0
        # 超时可以按照状态定制
        self.__time_out_setting = [9 for _ in range(32)]
        self.__time_out_setting[5] = 0
        self.__play_mode=None
        
    def getStandUpSchedule(self, state = TABLE_STATE_NONE):
        """获取每一小局的发牌流程"""
        return MTableState.TABLE_STATE_NEXT

    def setState(self, state):
        """设置状态"""
        self.__states = self.__states | state
    
    @property
    def playMode(self):
        return self.__play_mode
    
    def setPlayMode(self,playMode):
        self.__play_mode=playMode
    
    def clearState(self, state):
        """清除状态"""
        if self.__states & state:
            self.__states = self.__states ^ state
            
    @property
    def states(self):
        """获取牌桌状态设置"""
        return self.__states
    
    def getTimeOutByState(self, state):
        """超时设置"""
        bigger = self.__time_out_setting[0]
        if state & self.TABLE_STATE_ABSENCE:
            if self.__time_out_setting[6] > bigger:
                bigger = self.__time_out_setting[6]
        
        return bigger

    def enableSpecialStateByTableConfig(self, tableConfig):
        pass
