# -*- coding=utf-8
'''
Created on 2016年9月23日
牌桌麻将牌的管理器
包括：
1）发牌
2）牌桌上的出牌
3）宝牌

发牌说明：
发牌涉及到好牌点
@author: zhaol
'''

class MTableTileTest(object):
    
    def __init__(self, playerCount, playMode):
        super(MTableTileTest, self).__init__()
        # 手牌
        self.__hand_tiles = [[] for _ in range(playerCount)]
        # 牌桌的牌
        self.__tiles = []
        # 人数
        self.__player_count = playerCount
        self.__play_mode = playMode
        self.__last_special_tiles = None
        
    @property
    def playerCount(self):
        return self.__player_count
    
    @property
    def playMode(self):
        return self.__play_mode
        
    def initTiles(self):
        """初始化手牌"""
        return False
    
    @property
    def handTiles(self):
        return self.__hand_tiles
    
    def setHandTiles(self, handTiles):
        """设置玩家手牌"""
        self.__hand_tiles = handTiles
        
    def setTiles(self, tiles):
        """设置牌桌手牌"""
        self.__tiles = tiles
    
    @property
    def tiles(self):
        return self.__tiles

    def getTilesLeftCount(self):
        """获取剩余手牌数量"""
        return len(self.__tiles)

    def getLastSpecialTiles(self,default=None):
        """随州买马，获取最后的马牌；其他玩法，最后需要多组牌，所以设计成这样的返回值"""
        if self.__last_special_tiles:
            return {"ma_tile":self.__last_special_tiles}
        
        return None
