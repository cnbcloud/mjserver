# -*- coding=utf-8
'''
Created on 2016年12月11日
牌型整理
@author: dongwei
'''
from majiang2.ai.win import MWin
from majiang2.player.hand.hand import MHand
from majiang2.tile.tile import MTile
from majiang2.table.table_config_define import MTDefine
from majiang2.table_tile.table_tile_factory import MTableTileFactory
from freetime.util import log as ftlog
import copy

class MTilePatternChecker(object):
    """卡五星胡牌
    多支持七对胡
    """
    def __init__(self):
        super(MTilePatternChecker, self).__init__()
        # 获胜一方的桌子号
        self.__win_seat_id = None
        # 上一轮的桌子号
        self.__last_seat_id = None
        # 获胜牌
        self.__win_tile = None
        # 牌桌手牌管理器
        self.__table_tile_mgr = None
        # 获胜时的actionID
        self.__aciton_id = 0
        # 所有玩家的所有牌，按手牌格式的数组
        self.__player_all_tiles = []
        # 所有玩家的所有牌，合到一个数组
        self.__player_all_tiles_arr = []
        # 所有玩家手牌
        self.__player_hand_tiles_with_hu = []

    def setWinSeatId(self, seatId):
        """赢家座位号"""
        self.__win_seat_id = seatId

    @property
    def winSeatId(self):
        return self.__win_seat_id
        
    def setLastSeatId(self, seatId):
        """上家座位号"""
        self.__last_seat_id = seatId
        
    @property
    def lastSeatId(self):
        return self.__last_seat_id
        
    def setWinTile(self, wTile):
        """设置获胜手牌"""
        self.__win_tile = wTile
        
    @property
    def winTile(self):
        return self.__win_tile
     
    def setTableTileMgr(self, tableTileMgr):
        """设置手牌管理器"""
        self.__table_tile_mgr = tableTileMgr
     
    @property   
    def tableTileMgr(self):
        return self.__table_tile_mgr 

    def setActionID(self, actionId):
        """设置操作号"""
        ftlog.info('tilePattern.setActionId now:', self.__aciton_id , ' actionId:',actionId) 
        self.__aciton_id = actionId
    
    @property    
    def actionID(self):
        return self.__aciton_id

    @property
    def tableConfig(self):
        return self.__table_config
    
    def setTableConfig(self, config):
        self.__table_config = config

    @property
    def playerAllTiles(self):
        return self.__player_all_tiles

    def setPlayerAllTiles(self, tiles):
        # 仅用于测试
        self.__player_all_tiles = tiles

    @property
    def playerAllTilesArr(self):
        return self.__player_all_tiles_arr

    def setPlayerAllTilesArr(self, tiles):
        # 仅用于测试
        self.__player_all_tiles_arr = tiles

    @property
    def playerHandTilesWithHu(self):
        return self.__player_hand_tiles_with_hu

    def setPlayerHandTilesWithHu(self, tiles):
        # 仅用于测试
        self.__player_hand_tiles_with_hu = tiles


    def initChecker(self, playersAllTiles, winTile, tableTileMgr, isWinTileOnHand, curSeatId, winSeatId, actionID = 0):
        self.setLastSeatId(curSeatId)
        self.setWinSeatId(winSeatId)
        self.setActionID(actionID)
        self.setWinTile(winTile)
        self.setTableTileMgr(tableTileMgr)
        self.setTableConfig(self.tableTileMgr.tableConfig)
        self.__player_all_tiles = [[] for _ in range(self.tableTileMgr.playCount)]
        self.__player_all_tiles_arr = [[] for _ in range(self.tableTileMgr.playCount)]
        self.__player_hand_tiles_with_hu = [[] for _ in range(self.tableTileMgr.playCount)]

        # 不要用tableTileMgr.player里面的牌，因为可能这些牌还没抓到用户手里，以传入的playersAllTiles为准
        for seatId in range(len(playersAllTiles)):
            # 按手牌格式的数组
            self.__player_all_tiles[seatId] = copy.deepcopy(playersAllTiles[seatId])
            # 合到一个数组中
            self.__player_all_tiles_arr[seatId].extend(MHand.copyAllTilesToList(self.__player_all_tiles[seatId]))
            # 只获取手牌，此时手牌包含所胡的牌
            self.__player_hand_tiles_with_hu[seatId] = copy.deepcopy(playersAllTiles[seatId][MHand.TYPE_HAND])
            if not isWinTileOnHand and seatId == winSeatId:
                self.__player_hand_tiles_with_hu[seatId].append(winTile)

        ftlog.info('MTilePatternChecker.calcScore __player_all_tiles=', self.__player_all_tiles)
        ftlog.info('MTilePatternChecker.calcScore __player_all_tiles_arr=', self.__player_all_tiles_arr)
        ftlog.info('MTilePatternChecker.calcScore __player_hand_tiles_with_hu=', self.__player_hand_tiles_with_hu)

    def isQingyise(self):
        """
        清一色：由同一门花色（筒子或条子）组成的和牌牌型
        """
        colorArr = [0,0,0,0]
        for tile in self.playerAllTilesArr[self.winSeatId]:
            color = MTile.getColor(tile)
            colorArr[color] = 1
         
        colorCount = 0
        for eachColor in colorArr:
            if eachColor:
                colorCount += 1
        if colorCount > 1:
            ftlog.debug('MTilePatternChecker.isQingyise result: False')
            return False
        ftlog.debug('MTilePatternChecker.isQingyise result: True')
        return True

    def isHaidilao(self):
        """
        海底捞：最后一张牌自摸和牌
        """  
        if self.lastSeatId == self.winSeatId:
            if self.tableTileMgr and self.tableTileMgr.getTilesLeftCount() == 0:
                ftlog.debug('MTilePatternChecker.isHaidilao result: True')
                return True
        
        ftlog.debug('MTilePatternChecker.isHaidilao result: False')
        return False

    def isShouzhuayi(self):
        """
        手抓一：胡牌时自己手上只有一张牌，和牌手牌应该是一对
        """ 
        if self.playerHandTilesWithHu and len(self.playerHandTilesWithHu[self.winSeatId]) == 2:
            ftlog.debug('MTilePatternChecker.isShouzhuayi result: True')
            return True

        ftlog.debug('MTilePatternChecker.isShozhuayi result: False')
        return False

    def isPengpenghu (self, pattern):
        """
        碰碰胡：由四个刻子（杠）和一对组成的胡牌牌型
        """
        ftlog.debug('MTilePatternChecker.isPengpenghu pattern: ',pattern)
        pengpengCount = 0
        pengpengList = []
        # pattern中只有手牌
        for p in pattern:
            if len(p) == 4:
                pengpengCount += 1
                pengpengList.append(p[0])
            if len(p) == 3:
                if p[0] == p[1] and p[1] == p[2]:
                    pengpengCount += 1
                    pengpengList.append(p[0])
        # winNode的pattern计算有问题，有时包含碰牌或杠牌，下面排下重
        for gang in self.playerAllTiles[self.winSeatId][MHand.TYPE_GANG]:
            if gang['pattern'][0] not in pengpengList:
                pengpengCount += 1

        for peng in self.playerAllTiles[self.winSeatId][MHand.TYPE_PENG]:
            if peng[0] not in pengpengList:
                pengpengCount += 1

        if pengpengCount == 4:
            ftlog.debug('MTilePatternChecker.isPengpenghu result: True')
            return True
        ftlog.debug('MTilePatternChecker.isPengpenghu result: False')
        return False

    def isQidui (self, pattern):
        """
        七对：手中有七个对子的胡牌牌型，碰出的牌不算
        """ 
        tileCountArr = [0 for _ in range(MTile.TILE_MAX_VALUE)]
        jiangCount = 0
        for p in pattern:
            if len(p) == 2:
                jiangCount += 1
                for tile in p:
                    tileCountArr[tile] += 1

        fourCount = 0
        if jiangCount == 7:
            for tileCount in tileCountArr:
                if tileCount == 4:
                    fourCount += 1
            if fourCount == 0:
                ftlog.debug('MTilePatternChecker.isQidui result: True')
                return True
        ftlog.debug('MTilePatternChecker.isQidui result: False')
        return False

    def isQiduiHao (self, pattern):
        """
        豪华七对：有四个相同的牌当做两个对子使用
        """ 
        tileCountArr = [0 for _ in range(MTile.TILE_MAX_VALUE)]
        jiangCount = 0
        for p in pattern:
            if len(p) == 2:
                jiangCount += 1
                for tile in p:
                    tileCountArr[tile] += 1

        fourCount = 0
        if jiangCount == 7:
            for tileCount in tileCountArr:
                if tileCount == 4:
                    fourCount += 1
            if fourCount == 1:
                ftlog.debug('MTilePatternChecker.isQiduiHao result: True')
                return True
        ftlog.debug('MTilePatternChecker.isQiduiHao result: False')
        return False

    def isQiduiChaoHao (self, pattern):
        """
        超豪华七对：有两个四个相同的牌当做四个对子使用
        """ 
        tileCountArr = [0 for _ in range(MTile.TILE_MAX_VALUE)]
        jiangCount = 0
        for p in pattern:
            if len(p) == 2:
                jiangCount += 1
                for tile in p:
                    tileCountArr[tile] += 1

        fourCount = 0
        if jiangCount == 7:
            for tileCount in tileCountArr:
                if tileCount == 4:
                    fourCount += 1
            if fourCount == 2:
                ftlog.debug('MTilePatternChecker.isQiduiChaoHao result: True')
                return True
        ftlog.debug('MTilePatternChecker.isQiduiChaoHao result: False')
        return False

    def isQiduiChaoChaoHao (self, pattern):
        """
        超超豪华七对：有三个四个相同的牌当做六个对子使用
        """
        tileCountArr = [0 for _ in range(MTile.TILE_MAX_VALUE)]
        jiangCount = 0
        for p in pattern:
            if len(p) == 2:
                jiangCount += 1
                for tile in p:
                    tileCountArr[tile] += 1

        fourCount = 0
        if jiangCount == 7:
            for tileCount in tileCountArr:
                if tileCount == 4:
                    fourCount += 1
            if fourCount == 3:
                ftlog.debug('MTilePatternChecker.isQiduiChaoChaoHao result: True')
                return True
        ftlog.debug('MTilePatternChecker.isQiduiChaoChaoHao result: False')
        return False

    def isXiaosanyuan (self):
        """
        小三元：胡牌时 如果牌面上有中、发、白中的任意2种（每种牌3张，碰杠都算），并且牌面中还有其余1对
        中发白胡牌时，只能时按照将，刻，杠，不可能按照顺子来胡牌，所以不用看胡牌牌型
        """ 
        tileCountArr = [0 for _ in range(MTile.TILE_MAX_VALUE)]
        for tile in self.playerAllTilesArr[self.winSeatId]:
            tileCountArr[tile] += 1
        kegangCount = 0
        jiangCount = 0    
        for tileCheck in [MTile.TILE_HONG_ZHONG, MTile.TILE_FA_CAI, MTile.TILE_BAI_BAN]:
            if tileCountArr[tileCheck] >=3:
                kegangCount += 1
            elif tileCountArr[tileCheck] == 2:
                jiangCount += 1
        if kegangCount == 2 and jiangCount == 1:
            ftlog.debug('MTilePatternChecker.isXiaosanyuan result: True')
            return True
        ftlog.debug('MTilePatternChecker.isXiaosanyuan result: False')
        return False

    def isDasanyuan (self):
        """
        大三元：胡牌时 如果牌面上有中、发、白每种3张（碰杠都算），称为大三元
        """ 
        tileCountArr = [0 for _ in range(MTile.TILE_MAX_VALUE)]
        for tile in self.playerAllTilesArr[self.winSeatId]:
            tileCountArr[tile] += 1
        if tileCountArr[MTile.TILE_HONG_ZHONG] >= 3 and tileCountArr[MTile.TILE_FA_CAI] >= 3 and tileCountArr[MTile.TILE_BAI_BAN] >= 3:
            ftlog.debug('MTilePatternChecker.isDasanyuan result: True')
            return True
        ftlog.debug('MTilePatternChecker.isDasanyuan result: False')
        return False

    def isHaidipao(self):
        """
        海底炮：最后一张打出去的牌 放炮
        """ 
        if self.lastSeatId != self.winSeatId:
            if self.tableTileMgr and self.tableTileMgr.getTilesLeftCount() == 0:
                ftlog.debug('MTilePatternChecker.isHaidipao result: True')
                return True
        ftlog.debug('MTilePatternChecker.isHaidipao result: False')
        return False

    def isGangshangpao(self):
        """
        杠上炮：杠后打出的牌被别人胡，杠钱照算
        """ 
        lastGangActionID = 0
        if self.lastSeatId != self.winSeatId:
            for gangArr in self.playerAllTiles[self.lastSeatId][MHand.TYPE_GANG]:
                ftlog.debug(gangArr)
                if gangArr['actionID'] >= lastGangActionID:
                    lastGangActionID = gangArr['actionID']
            if lastGangActionID > 0:
		# modify by yj 05.19 
                # 杠牌1步，杠牌后抓牌1步，出牌1步，如果放炮，actionID差值4
                if (self.actionID - lastGangActionID) == 4:
                    ftlog.debug('MTilePatternChecker.isGangShangPao result: True, actionID:', self.actionID, 'lastGangActionID:', lastGangActionID)
                    return True
        ftlog.debug('MTilePatternChecker.isGangShangPao result: False, actionID:', self.actionID, 'lastGangActionID:', lastGangActionID)
        return False


if __name__ == "__main__":
    checker = MTilePatternChecker()
    checker.setTableConfig({})
    checker.setWinSeatId(1)
    tableTileMgr = MTableTileFactory.getTableTileMgr(3, 'luosihu', 1)

    """只设置所有牌list"""
    checker.setPlayerAllTilesArr([[],[16, 16, 15, 16, 17, 14, 15, 16, 11, 12, 13],[]])
    assert True == checker.isQingyise()
    checker.setPlayerAllTilesArr([[],[16, 16, 15, 16, 17, 14, 15, 16, 21, 22, 23],[]])
    assert False == checker.isQingyise()
    checker.setPlayerAllTilesArr([[],[37, 37, 35, 35, 35, 36, 36, 36, 15, 16, 17],[]])
    assert True == checker.isXiaosanyuan()
    assert False == checker.isDasanyuan()
    checker.setPlayerAllTilesArr([[],[15, 15, 35, 35, 35, 36, 36, 36, 37, 37, 37],[]])
    assert False == checker.isXiaosanyuan()
    assert True == checker.isDasanyuan()

    """清空所有的牌，只设置手牌"""
    checker.setPlayerAllTilesArr([[],[],[]])
    checker.setPlayerHandTilesWithHu([[],[11, 11],[]])
    assert True == checker.isShouzhuayi()
    checker.setPlayerHandTilesWithHu([[],[11, 12, 13, 22, 22],[]])
    assert False == checker.isShouzhuayi()

    """清空所有的牌，只设置winNode"""
    checker.setPlayerAllTiles([[],[],[]])
    checker.setPlayerAllTilesArr([[],[],[]])
    assert True == checker.isQidui([[16, 16], [17, 17], [18, 18], [19, 19], [13, 13], [14, 14], [15, 15]])
    assert False == checker.isQidui([[16, 16], [17, 17], [18, 18], [19, 19], [13, 13], [14, 14], [14, 14]])
    assert True == checker.isQiduiHao([[16, 16], [17, 17], [18, 18], [19, 19], [13, 13], [14, 14], [14, 14]])
    assert False == checker.isQiduiChaoHao([[16, 16], [17, 17], [18, 18], [19, 19], [13, 13], [14, 14], [14, 14]])
    assert True == checker.isQiduiChaoHao([[16, 16], [17, 17], [18, 18], [13, 13], [13, 13], [14, 14], [14, 14]])

    checker.setWinTile(29)
    checker.setPlayerAllTiles([[],{MHand.TYPE_PENG:[[22, 22, 22]], MHand.TYPE_GANG:[{'pattern': [15, 15, 15, 15], 'style': 0, 'actionID': 15}, {'pattern': [35, 35, 35, 35], 'style': True, 'actionID': 40}]},[]])
    # winNode的patten计算有问题，上述用例是实际的情况，先兼容这中错误情况
    assert True == checker.isPengpenghu([[24, 24], [29, 29, 29], [35, 35, 35]])

    # 杠上炮
    checker.setLastSeatId(1)
    checker.setWinSeatId(0)
    checker.setActionID(22)
    checker.setPlayerAllTiles([[],{MHand.TYPE_GANG:[{'pattern': [15, 15, 15, 15], 'style': 0, 'actionID': 1}, {'pattern': [35, 35, 35, 35], 'style': True, 'actionID': 20}]},[]])
    assert True == checker.isGangshangpao()


