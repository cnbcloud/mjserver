# -*- coding=utf-8
'''
Created on 2016年9月24日

@author: zhaol
'''
import copy

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
class MTile(object):
    TILE_NONE = -1
    # 万
    TILE_WAN = 0
    # 筒
    TILE_TONG = 1
    # 条
    TILE_TIAO = 2
    # 风
    TILE_FENG = 3
    # 花
    TILE_FLOWER = 4
    # 花色个数
    COLOR_COUNT = 4
    
    TILE_DONG_FENG = 31
    TILE_NAN_FENG = 32
    TILE_XI_FENG = 33
    TILE_BEI_FENG = 34
    TILE_HONG_ZHONG = 35
    TILE_FA_CAI = 36
    TILE_BAI_BAN = 37

    TILE_FLOWER_CHUN = 41
    TILE_FLOWER_XIA = 42
    TILE_FLOWER_QIU = 43
    TILE_FLOWER_DONG = 44
    TILE_FLOWER_MEI = 45
    TILE_FLOWER_LAN = 46
    TILE_FLOWER_ZHU = 47
    TILE_FLOWER_JU = 48


    
    TILE_ONE_WAN = TILE_WAN * 10 + 1
    TILE_TWO_WAN = TILE_WAN * 10 + 2
    TILE_THREE_WAN = TILE_WAN * 10 + 3
    TILE_FOUR_WAN = TILE_WAN * 10 + 4
    TILE_FIVE_WAN = TILE_WAN * 10 + 5
    TILE_SIX_WAN = TILE_WAN * 10 + 6
    TILE_SEVEN_WAN = TILE_WAN * 10 + 7
    TILE_EIGHT_WAN = TILE_WAN * 10 + 8
    TILE_NINE_WAN = TILE_WAN * 10 + 9
    
    TILE_ONE_TONG = TILE_TONG * 10 + 1
    TILE_TWO_TONG = TILE_TONG * 10 + 2
    TILE_THREE_TONG = TILE_TONG * 10 + 3
    TILE_FOUR_TONG = TILE_TONG * 10 + 4
    TILE_FIVE_TONG = TILE_TONG * 10 + 5
    TILE_SIX_TONG = TILE_TONG * 10 + 6
    TILE_SEVEN_TONG = TILE_TONG * 10 + 7
    TILE_EIGHT_TONG = TILE_TONG * 10 + 8
    TILE_NINE_TONG = TILE_TONG * 10 + 9
    
    TILE_ONE_TIAO = TILE_TIAO * 10 + 1
    TILE_TWO_TIAO = TILE_TIAO * 10 + 2
    TILE_THREE_TIAO = TILE_TIAO * 10 + 3
    TILE_FOUR_TIAO = TILE_TIAO * 10 + 4
    TILE_FIVE_TIAO = TILE_TIAO * 10 + 5
    TILE_SIX_TIAO = TILE_TIAO * 10 + 6
    TILE_SEVEN_TIAO = TILE_TIAO * 10 + 7
    TILE_EIGHT_TIAO = TILE_TIAO * 10 + 8
    TILE_NINE_TIAO = TILE_TIAO * 10 + 9

    # 连江判断听，排除花牌将 TILE_MAX_VALUE = 50 改为 TILE_MAX_VALUE = 30 modify by youjun 06.26    
    TILE_MAX_VALUE = 50
    
    FENG_DONG  = 0b1
    FENG_NAN   = 0b10
    FENG_XI    = 0b100
    FENG_BEI   = 0b1000
    FENG_ZHONG = 0b10000
    FENG_FA    = 0b100000
    FENG_BAI   = 0b1000000
    
    def __init__(self):
        super(MTile, self).__init__()
        
    @classmethod
    def changeTilesToValueArr(cls, tiles):
        """
        将牌转化为张数数组
        """
        tileArr = [0 for _ in range(cls.TILE_MAX_VALUE)]
        for tile in tiles:
            tileArr[tile] += 1
        return tileArr
    
    @classmethod
    def getColorCount(cls, tileArr):
        """获取听牌花色数量"""
        count = 0
        for tile in MTile.traverseTile(MTile.TILE_WAN):
            if tileArr[tile]:
                count += 1
                break
            
        for tile in MTile.traverseTile(MTile.TILE_TONG):
            if tileArr[tile]:
                count += 1
                break
            
        for tile in MTile.traverseTile(MTile.TILE_TIAO):
            if tileArr[tile]:
                count += 1
                break
            
        for tile in MTile.traverseTile(MTile.TILE_FENG):
            if tileArr[tile]:
                count += 1
                break
            
        return count
    
    @classmethod
    def getTileCountByColor(cls, tileArr, color):
        """获取某一类花色的数量"""
        count = 0
        for tile in MTile.traverseTile(color):
            count += tileArr[tile]
        return count
    
    @classmethod
    def getYaoJiuCount(cls, tileArr):
        """获取幺九的数量"""   
        yaoCount = tileArr[MTile.TILE_ONE_WAN] + tileArr[MTile.TILE_ONE_TONG] + tileArr[MTile.TILE_ONE_TIAO]
        jiuCount = tileArr[MTile.TILE_NINE_WAN] + tileArr[MTile.TILE_NINE_TONG] + tileArr[MTile.TILE_NINE_TIAO]
        return yaoCount+jiuCount
                                         
    @classmethod
    def traverseTile(cls, tileType):
        """返回遍历tileType的索引"""
        if tileType == cls.TILE_WAN:
            return range(cls.TILE_ONE_WAN, cls.TILE_NINE_WAN + 1)
        
        if tileType == cls.TILE_TONG:
            return range(cls.TILE_ONE_TONG, cls.TILE_NINE_TONG + 1)
        
        if tileType == cls.TILE_TIAO:
            return range(cls.TILE_ONE_TIAO, cls.TILE_NINE_TIAO + 1)
        
        if tileType == cls.TILE_FENG:
            return range(cls.TILE_DONG_FENG, cls.TILE_BAI_BAN + 1)
        
        return []
    
    @classmethod
    def cloneTiles(cls, tiles):
        """
        拷贝手牌
        """
        re = copy.deepcopy(tiles)
        return re
    
    @classmethod
    def getTileCount(cls,tile, tiles):
        """
        获取tile在tiles里面的个数
        """
        newTilesArr = MTile.changeTilesToValueArr(tiles)
        return newTilesArr[tile]
    
    @classmethod
    def getTileCountArr(cls,tileArr, tile):
        """
        获取tile在tileArr里面的个数
        """
        return tileArr[tile]
    
    @classmethod
    def getColor(cls, tile):
        """获取手牌颜色"""
        return tile / 10
    
    @classmethod
    def getValue(cls, tile):
        """获取手牌"""
        return tile % 10 
        
    @classmethod
    def getTiles(cls, colors, fengDetails=0b1111111):
        """
        获取某个花色的所有牌
        """
        cards = []
        if cls.TILE_WAN in colors:           
            ct = []
            allValue = 9
            for index in range(allValue):
                for _ in range(cls.COLOR_COUNT):
                    ct.append(index + 1 + cls.TILE_WAN * 10)
            cards.append(ct)
        else:
            cards.append([])
            
        if cls.TILE_TONG in colors:           
            ct = []
            allValue = 9
            for index in range(allValue):
                for _ in range(cls.COLOR_COUNT):
                    ct.append(index + 1 + cls.TILE_TONG * 10)
            cards.append(ct)
        else:
            cards.append([])
            
        if cls.TILE_TIAO in colors:           
            ct = []
            allValue = 9
            for index in range(allValue):
                for _ in range(cls.COLOR_COUNT):
                    ct.append(index + 1 + cls.TILE_TIAO * 10)
            cards.append(ct)
        else:
            cards.append([])
            
        if cls.TILE_FENG in colors:           
            ct = []
            if fengDetails & cls.FENG_DONG:
                for _ in range(cls.COLOR_COUNT):
                    ct.append(31)
             
            if fengDetails & cls.FENG_NAN:
                for _ in range(cls.COLOR_COUNT):
                    ct.append(32)
            
            if fengDetails & cls.FENG_XI:
                for _ in range(cls.COLOR_COUNT):
                    ct.append(33)
                    
            if fengDetails & cls.FENG_BEI:
                for _ in range(cls.COLOR_COUNT):
                    ct.append(34)
              
            if fengDetails & cls.FENG_ZHONG:
                for _ in range(cls.COLOR_COUNT):
                    ct.append(35)
                    
            if fengDetails & cls.FENG_FA:
                for _ in range(cls.COLOR_COUNT):
                    ct.append(36)
                    
            if fengDetails & cls.FENG_BAI:
                for _ in range(cls.COLOR_COUNT):
                    ct.append(37)
                                   
            cards.append(ct)
        else:
            cards.append([])

        if cls.TILE_FLOWER in colors:
            ct = []
            ct.append(cls.TILE_FLOWER_CHUN)
            ct.append(cls.TILE_FLOWER_XIA)
            ct.append(cls.TILE_FLOWER_QIU)
            ct.append(cls.TILE_FLOWER_DONG)
            ct.append(cls.TILE_FLOWER_MEI)
            ct.append(cls.TILE_FLOWER_LAN)
            ct.append(cls.TILE_FLOWER_ZHU)
            ct.append(cls.TILE_FLOWER_JU)
            cards.append(ct)
        else:
            cards.append([])
                
        return cards
    
    @classmethod
    def isFeng(cls, tile):
        fengs = [cls.TILE_DONG_FENG, cls.TILE_NAN_FENG, cls.TILE_XI_FENG, cls.TILE_BEI_FENG]
        return tile in fengs
    
    @classmethod
    def isArrow(cls, tile):
        arrows = [cls.TILE_HONG_ZHONG, cls.TILE_FA_CAI, cls.TILE_BAI_BAN]
        return tile in arrows

    @classmethod
    def isFlower(cls, tile):
        flowers = [cls.TILE_FLOWER_CHUN, cls.TILE_FLOWER_XIA, cls.TILE_FLOWER_QIU,cls.TILE_FLOWER_DONG,cls.TILE_FLOWER_MEI,cls.TILE_FLOWER_LAN,cls.TILE_FLOWER_ZHU,cls.TILE_FLOWER_JU,]
        return tile in flowers
    
    @classmethod
    def calcGangCount(self,gangtiles):
        """计算明杠/暗杠个数"""
        tempMingCount = 0
        tempAnCount = 0
        for gangObj in gangtiles:
            if gangObj['style'] == 1:
                tempMingCount += 1
            elif gangObj['style'] == 0:
                tempAnCount += 1
            
        return tempMingCount,tempAnCount
