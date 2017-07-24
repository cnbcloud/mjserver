# -*- coding=utf-8
'''
Created on 2016年12月02日
牌桌麻将牌的管理器
包括：
1）发牌
2）牌桌上的出牌
3）宝牌

发牌说明：
发牌涉及到好牌点
@author: dongwei
'''
from majiang2.table_tile.table_tile import MTableTile
from majiang2.table.table_config_define import MTDefine
from freetime.util import log as ftlog
from majiang2.dealer.dealer_factory import DealerFactory

class MTableTileLuosihu(MTableTile):

    def __init__(self, playerCount, playMode, runMode):
        super(MTableTileLuosihu, self).__init__(playerCount, playMode, runMode)
        # 宝牌
        self.__last_special_tiles = None
        # 抢杠胡的规则
        self.setQiangGangRule(0b010)

    def reset(self):
        """重置"""
        super(MTableTileLuosihu, self).reset()
        self.__last_special_tiles = None
    
    def getLastSpecialTiles(self,default=None):
        """随州买马，获取最后的马牌；其他玩法，最后需要多组牌，所以设计成这样的返回值"""
        #if self.__last_special_tiles:
            #return {"ma_tile":self.__last_special_tiles}
        
        return None

    def drawLastSpecialTiles(self, curSeatId, winSeatId):
        """随州买马，抓取最后的马牌"""
	#modify bu youjun 04.27
	return False
        maType = self.tableConfig.get(MTDefine.MAI_MA, 0)
        if maType == 0:
            # 未开启买马
            return False
        if maType == 1:
            # 必须自摸，才能买马
            if curSeatId != winSeatId:
                return False
        if maType == 2:
            # 必须自摸，才能买马
            if curSeatId != winSeatId:
                return False
            # 必须听牌亮倒才能买马
            if not self.players[winSeatId].isTing():
                return False

        if len(self.tiles) == 0:
            #荒庄流局
            return False
        self.__last_special_tiles = self.tiles.pop(-1)
        ftlog.debug( 'MTableTileLuosihu.drawLastSpecialTiles draw last specail tile:', self.__last_special_tiles )
        return True

    def getTingLiangMode(self):
        """卡五星在听牌时，即亮牌"""
	return self.MODE_LIANG_NONE
        # 卡五星默认亮全部手牌
        mode = self.tableConfig.get(MTDefine.LIANG_PAI, self.MODE_LIANG_HAND)
        ftlog.debug( 'MTableTileLuosihu.getTingLiangMode liang mode:', mode )
        ftlog.debug( 'MTableTileLuosihu.getTingLiangMode liang tiles:', self.tiles )
        if len(self.tiles) <= 12 and (self.playMode == 'luosihu-suizhou' or self.playMode == 'luosihu-luosihu' or self.playMode == 'luosihu-yingcheng'):
            return self.MODE_LIANG_TING_TIPS
        if self.playMode == 'luosihu-yingcheng':
            return self.MODE_LIANG_TING
        if mode in [self.MODE_LIANG_HAND, self.MODE_LIANG_TING]:
            return mode
        else:
            ftlog.debug( 'MTableTileLuosihu.getTingLiangMode liang mode to default:', self.MODE_LIANG_HAND )
            return self.MODE_LIANG_HAND

    def canGuoHouBuGang(self):
        """卡五星杠牌之后点过，就再也不能杠了"""
        return True
    
    def canGangAfterPeng(self):
        """卡五星碰牌后，可以马上选择杠牌"""
        return True

    def getTingGangMode(self):
        """卡五星听牌后只能杠扣下的牌"""
        return MTableTile.MODE_TINGGANG_NOCHANGETING

    def canGangLastTile(self):
        """卡五星抓到最后一张牌，不能杠"""
        return False

    def sendInfoNeedMoreInfo(self):
        """断线重连需要更多的信息
        例如:断线重连时里需要玩家碰牌或杠牌来自谁"""
	return True

    def canDuoHu(self):
	if self.playMode == 'luosihu-luosihu':
	    return False
	return True


