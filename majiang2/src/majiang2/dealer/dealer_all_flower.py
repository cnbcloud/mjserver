# -*- coding=utf-8
'''
Created on 2016年9月24日

@author: yawen
'''
from majiang2.dealer.dealer import Dealer
import random
from majiang2.tile.tile import MTile
from freetime.util import log as ftlog

"""
麻将手牌编码
万 1-9
筒 11-19
条 21-29
东 31
南 32
西 33
北 34
中 35
发 36
白 37
春 41
夏 42
秋 43
冬 44
梅 45
兰 46
竹 47
菊 48
"""
class AllFlowerDealer(Dealer):
    def __init__(self):
        """初始化
            子类在自己的初始化方法里，初始化麻将牌池范围，准备发牌
            包含所有的牌
        """
        super(AllFlowerDealer, self).__init__()
        # 本玩法包含的花色
        self.__card_colors = [MTile.TILE_WAN, MTile.TILE_TONG, MTile.TILE_TIAO, MTile.TILE_FENG,MTile.TILE_FLOWER]
        # 花色数量
        self.__card_count = len(self.__card_colors)
        # 初始化本玩法包含的牌
        self.setCardTiles(MTile.getTiles(self.__card_colors))

    @property
    def cardColors(self):
        return self.__card_colors
    
    def setCardColors(self, cardColors):
        self.__card_colors = cardColors
        
    @property
    def cardCount(self):
        return self.__card_count
    
    def setCardCount(self, cardCount):
        self.__card_count = cardCount
        
    """洗牌/发牌
        子类必须实现
    """
    def shuffle(self, goodPointCount, cardCountPerHand):
        """参数说明
            goodPointCount : 好牌点的人数
            cardCountPerHand ： 每手牌的麻将牌张数
        """
        # 初始化一下cardTiles,因为每设置一次好牌点都会从里面弹出13张牌
        self.setCardTiles(MTile.getTiles(self.__card_colors))
        
        left_tiles = []    
        for color in self.__card_colors:
            left_tiles.extend(self.cardTiles[color])
        # 对剩余的牌洗牌
        random.shuffle(left_tiles)
        self.addTiles(left_tiles)

        return self.tiles
    
    def getGoodCard(self, cardCountPerHand):
        """发一个人的好牌
        """
        count = self.getGoodCardCount(cardCountPerHand)
        ftlog.debug( 'count:', count )
        
        color = random.randint(0, self.__card_count -1)
        cards = []
        cLen = len(self.cardTiles[color])
        if count > cLen:
            count = cLen
            
        # 发好牌
        for _ in range(count):
            cards.append(self.cardTiles[color].pop(0))
        
        # 发第二门
        count1 = (cardCountPerHand - count) / 2
        color = (color + 1) % self.__card_count
        for _ in range(count1):
            cards.append(self.cardTiles[color].pop(0))
        
        # 发最后一门
        left = cardCountPerHand - count - count1
        color = (color + 1) % self.__card_count
        for _ in range(left):
            cards.append(self.cardTiles[color].pop(0))
         
        return cards
        
    def getGoodCardCount(self, count):
        """好牌一门的数量
        """
        middle = count / 2
        choice = random.randint(0, 99)
        if choice > 90:
            middle += 2;
        elif choice > 60:
            middle += 1;
        
        return middle
    
if __name__ == "__main__":
    dealer = AllFlowerDealer()
    
    # case 1
#     dealer.generateTiles({
#                     "seat1": [21, 22, 14, 36, 35, 15, 7, 6, 23, 8, 16, 12, 12],
#                     "seat2": [],
#                     "seat3": [14,14,14,15,15,15,16,16,16,11,13,19,19],
#                     "seat4": [],
#                     "pool": [1,12,25,25,25,12],
#                     "magics": []
#                     })
    
    # case 2，流程错乱，越人发牌
    dealer.generateTiles({
                    "seat1": [2,2,2,5,5,5,8,8,8,12,15,18,15],
                    "seat2": [1,4,7,12,15,18,23,26,29,31,32,33,34],
                    "seat3": [2,5,8,12,15,18,22,25,28,22,25,28,25],
                    "seat4": [11,14,17,22,35,28,3,6,9,33,34,35,14],
                    "pool": [25],
                    "magics": []
                    })