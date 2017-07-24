# -*- coding=utf-8
'''
Created on 2017年6月06日
牌桌麻将牌的管理器
包括：
1）发牌
2）牌桌上的出牌
3）宝牌

发牌说明：
发牌涉及到好牌点
@author: youjun
'''
from majiang2.table_tile.table_tile import MTableTile
from majiang2.table.table_config_define import MTDefine
from majiang2.tile.tile import MTile
from majiang2.table_state.state import MTableState
from freetime.util import log as ftlog
from majiang2.dealer.dealer_factory import DealerFactory

class MTableTileQueshou(MTableTile):

    def __init__(self, playerCount, playMode, runMode):
        super(MTableTileQueshou, self).__init__(playerCount, playMode, runMode)
        # 宝牌
	self.__magic_tile = 0
        # 抢杠胡的规则
        self.setQiangGangRule(0b010)

    def reset(self):
        """重置"""
        super(MTableTileQueshou, self).reset()
   	self.__magic_tile = 0
    '''    
    def shuffle(self, goodPointCount, handTileCount):
        """
        洗牌器 
        添加特殊逻辑，宝牌
        """
        super(MTableTileQueshou, self).shuffle(goodPointCount, handTileCount)
        if len(self.tiles) > 0:
            self.__magic_tile = self.tiles.pop(-1)
            self.addSpecialTile(self.__magic_tile)
        
            ftlog.debug( 'MTableTileQueshou.shuffle changed tile:', self.__magic_tile )
    '''

    def allowMagicChiPengGang(self, isTing = False):
        """是否允许宝牌／会牌参与吃碰杠"""
        """按照现在代码逻辑 需要 默认可以参与，但是盘锦不可以参与"""
        return False
    
    def canUseMagicTile(self, state):
        """牌桌状态state，是否可使用癞子牌"""
        if state & MTableState.TABLE_STATE_HU:
            return True
        
        return False

    def setMagicTile(self,tile):
        self.__magic_tile = tile

    def getMagicTiles(self, isTing = False):
        """获取宝牌，采用数组，有的游戏有多个宝牌"""
        if self.__magic_tile:
            return [self.__magic_tile]
        
        return []
    
    def getMagicTile(self):
        return self.__magic_tile
    
    def getTingLiangMode(self):
        """卡五星在听牌时，即亮牌"""
	return self.MODE_LIANG_NONE

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

    def isFlower(self, tile):
        """判断tile是否花牌"""
        return tile > 30

    def canDuoHu(self):
        return True

    def selectGangAfterTing(self):
        """听牌之后杠是否需要选择"""
        return False

    def getCheckFlowCount(self):
        """覆盖父类方法,荒庄牌的数量"""
        fakeRemainCount = len(self.tiles)
        if fakeRemainCount <= 20:
            return 0
        return fakeRemainCount
    
    def getFlowCount(self):
        return 20
    
    def getTilesNoDropCount(self):
        """获取用于最后几张只摸不打"""
        
        return self.playCount

