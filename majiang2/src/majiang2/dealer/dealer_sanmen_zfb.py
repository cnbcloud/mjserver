# -*- coding=utf-8
'''
Created on 2016年9月24日

@author: zhaol
'''
from majiang2.dealer.dealer import Dealer
import random
from majiang2.tile.tile import MTile
from freetime.util import log as ftlog

class SanMenWithZFBDealer(Dealer):
    def __init__(self):
        """初始化
            子类在自己的初始化方法里，初始化麻将牌池范围，准备发牌
            包括万/筒/条三门+中发白
        """
        super(SanMenWithZFBDealer, self).__init__()
        # 本玩法包含的花色
        self.__card_colors = [MTile.TILE_WAN, MTile.TILE_TONG, MTile.TILE_TIAO, MTile.TILE_FENG]
        # 风牌的描述
        self.__feng_details = MTile.FENG_ZHONG | MTile.FENG_FA | MTile.FENG_BAI
        # 花色数量
        self.__card_count = len(self.__card_colors)
        # 初始化本玩法包含的牌
        self.setCardTiles(MTile.getTiles(self.__card_colors, self.__feng_details))
        
    def reset(self):
        """重置"""
        super(SanMenWithZFBDealer, self).reset()
    
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
        ftlog.debug('SanMenWithZhonggDealer.shuffle tiles:', self.tiles)
            
        return self.tiles
    
if __name__ == "__main__":
    dealer = SanMenWithZFBDealer()
    dealer.shuffle(1, 13)