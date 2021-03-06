# -*- coding=utf-8
'''
Created on 2016年9月24日

@author: zhaol
'''
from majiang2.dealer.dealer import Dealer
import random
from majiang2.tile.tile import MTile
from freetime.util import log as ftlog

class TongTiaoWithZhonggDealer(Dealer):
    def __init__(self):
        """初始化
            子类在自己的初始化方法里，初始化麻将牌池范围，准备发牌
            鸡西麻将三人玩法
            包括筒/条三门+红中
        """
        super(TongTiaoWithZhonggDealer, self).__init__()
        # 本玩法包含的花色
        self.__card_colors = [MTile.TILE_TONG, MTile.TILE_TIAO, MTile.TILE_FENG]
        # 风牌的描述
        self.__feng_details = MTile.FENG_ZHONG
        # 花色数量
        self.__card_count = len(self.__card_colors)
        # 初始化本玩法包含的牌
        self.setCardTiles(MTile.getTiles(self.__card_colors, self.__feng_details))
        
    def reset(self):
        """重置"""
        super(TongTiaoWithZhonggDealer, self).reset()
    
    """洗牌/发牌
        子类必须实现
    """
    def shuffle(self, goodPointCount, cardCountPerHand):
        """参数说明
            goodPointCount : 好牌点的人数
            cardCountPerHand ： 每手牌的麻将牌张数
        """
        for color in self.__card_colors:
            print 'cardTiles:', self.cardTiles[color], ' color:', color
            self.addTiles(self.cardTiles[color])

        # 对剩余的牌洗牌
        random.shuffle(self.tiles)
        ftlog.debug('TongTiaoWithZhonggDealer.shuffle tiles:', self.tiles)
            
        return self.tiles
    
if __name__ == "__main__":
    dealer = TongTiaoWithZhonggDealer()
    # 鸡西天胡
    dealer.generateTiles({
                        "seat1": [27,28,29,14,14,14,15,17,15,15,24,25,26],
                        "seat2": [],
                        "seat3": [],
                        "seat4": [],
                        "pool": [16],
                        "magics": [22]
                        })
    
    # 鸡西换宝
    dealer.generateTiles({
                        "seat1": [27,25,26,14,14,14,15,17,15,15,24,25,26],
                        "seat2": [],
                        "seat3": [],
                        "seat4": [],
                        "pool": [22,22,22,29,29,29,28,28,28],
                        "magics": [28,29,22]
                        })