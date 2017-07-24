# -*- coding=utf-8
'''
Created on 2016年9月24日

@author: zhaol
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
"""
class AllColorDealer(Dealer):
    def __init__(self):
        """初始化
            子类在自己的初始化方法里，初始化麻将牌池范围，准备发牌
            包含所有的牌
        """
        super(AllColorDealer, self).__init__()
        # 本玩法包含的花色
        self.__card_colors = [MTile.TILE_WAN, MTile.TILE_TONG, MTile.TILE_TIAO, MTile.TILE_FENG]
        # 花色数量
        self.__card_count = len(self.__card_colors)
        # 初始化本玩法包含的牌
        self.setCardTiles(MTile.getTiles(self.__card_colors))
        ftlog.debug(self.cardTiles)

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
    dealer = AllColorDealer()
    
    # 山东清一色
    # {"seat1": [13, 13, 14, 14, 15, 15, 16, 16, 17, 11, 11, 12, 12], "seat2": [1, 11, 2, 21, 3, 21, 19, 19, 19, 21, 22, 23, 24], "seat3": [1, 2, 3, 4, 5, 7, 8, 9, 4, 12, 6, 16, 27], "seat4": [1, 2, 3, 4, 5, 7, 8, 9, 17, 17, 18, 18, 27], "jing": [], "pool": [6, 9, 21, 17, 6, 18, 18, 6, 16, 15, 15, 13, 14, 13, 14, 19, 1, 2, 3, 4, 5, 12, 8, 7, 5, 8, 9, 11, 22, 22, 22, 23, 23, 23, 24, 24, 24, 25, 25, 25, 25, 26, 26, 26, 26, 27, 27, 28, 28, 28, 28, 29, 29, 29, 29, 35, 35, 35, 35, 36, 36, 36, 36, 37, 37, 37, 37, 7], "laizi": []}
    
    # 山东混一色
    # {"seat1": [31, 31, 31, 32, 32, 32, 33, 33, 33, 34, 34, 34, 1], "seat2": [13, 9, 27, 24, 27, 5, 28, 34, 35, 11, 9, 29, 24], "seat3": [3, 13, 14, 22, 19, 8, 18, 19, 36, 29, 26, 18, 17], "seat4": [8, 7, 21, 7, 25, 4, 8, 17, 1, 12, 16, 25, 13], "pool": [2, 11, 22, 3, 1, 5, 24, 36, 22, 37, 4, 15, 2, 27, 12, 15, 35, 19, 23, 24, 14, 6, 11, 15, 9, 32, 21, 6, 16, 14, 37, 13, 36, 8, 15, 12, 35, 37, 23, 23, 3, 14, 1, 28, 37, 18, 2, 29, 17, 3, 26, 23, 6, 7, 11, 27, 28, 4, 16, 25, 6, 25, 18, 5, 36, 35, 12, 26, 17, 2, 7, 21, 21, 9, 29, 31, 19, 26, 5, 33, 28, 22, 16, 4], "jing": [], "laizi": []}
#     dealer.generateTiles({
#                         "seat1": [31,31,31,32,32,32,33,33,33,34,34,34,1],
#                         "seat2": [],
#                         "seat3": [],
#                         "seat4": [],
#                         "pool": [2,0,0,0,1],
#                         "magics": []
#                         })
    
    # 山东风一色
#     {"seat1": [31, 31, 31, 32, 32, 32, 33, 33, 33, 34, 34, 34, 35], "seat2": [21, 24, 3, 18, 21, 5, 1, 7, 5, 17, 8, 12, 7], "seat3": [4, 13, 14, 22, 29, 1, 23, 37, 25, 29, 15, 28, 26], "seat4": [5, 22, 9, 4, 37, 35, 16, 8, 12, 33, 22, 12, 4], "pool": [2, 16, 14, 4, 35, 23, 15, 27, 19, 23, 16, 11, 1, 16, 13, 25, 8, 26, 28, 14, 2, 22, 27, 15, 13, 2, 8, 23, 28, 35, 15, 21, 11, 28, 29, 36, 12, 36, 11, 9, 19, 19, 6, 1, 17, 24, 18, 6, 19, 7, 9, 3, 24, 3, 17, 31, 2, 37, 6, 14, 26, 36, 18, 27, 26, 9, 5, 36, 25, 17, 32, 6, 24, 18, 27, 37, 34, 21, 11, 7, 3, 13, 29, 25], "jing": [], "laizi": []}
#     dealer.generateTiles({
#                         "seat1": [31,31,31,32,32,32,33,33,33,34,34,34,35],
#                         "seat2": [],
#                         "seat3": [],
#                         "seat4": [],
#                         "pool": [2,0,0,0,35],
#                         "magics": []
#                         })

# 山东碰碰胡
#     dealer.generateTiles({
#                         "seat1": [31,31,31,12,12,12,23,23,23,34,34,34,35],
#                         "seat2": [],
#                         "seat3": [],
#                         "seat4": [],
#                         "pool": [2,0,0,0,35],
#                         "magics": []
#                         })
    
    # 山东七对
#     dealer.generateTiles({
#                         "seat1": [31,32,33,34,35,36,37,1,9,11,19,21,29],
#                         "seat2": [],
#                         "seat3": [],
#                         "seat4": [],
#                         "pool": [2,0,0,0,31],
#                         "magics": []
#                         })
    
    dealer.generateTiles({
                        "seat1": [1,1,1,2,2,2,3,3,3,4,4,6,7],
                        "seat2": [11,11,11,12,12,12,13,13,13,14,14,6,7],
                        "seat3": [21,21,21,22,22,22,23,23,23,24,24,6,7],
                        "seat4": [31,31,31,32,32,32,33,33,33,34,34,6,7],
                        "pool": [5,5,5,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        "magics": []
                        })