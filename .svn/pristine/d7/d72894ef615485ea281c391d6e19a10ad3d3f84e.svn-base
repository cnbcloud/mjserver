# -*- coding=utf-8
'''
Created on 2016年9月23日
庄家规则
@author: zhaol
'''

class MWinRule(object):
    """胡牌规则
    """
    WIN_BY_MYSELF = 0
    WIN_BY_OTHERS = 1
    WIN_BY_QIANGGANGHU = 2
    LOOSE = -1
    
    def __init__(self):
        super(MWinRule, self).__init__()
        self.__table_tile_mgr = None
        # 倍数,由玩家建房参数带入
        self.__multiple = 1
        # 胡牌方式,由玩家建房参数带入
        self.__winType = 0
        # 当前杠牌人座位信息,内容为当前杠牌人的座位号
        self.__last_gang_seat = -1
        # 当前操作者的位置
        self.__curSeatId = -1
        # 所有玩家的牌引用(只给鸡西判断特大夹使用)
        self.__all_player_tiles = {}
        self.__table_config = {}
        self.__banker_id = 0
        # 玩家的缺门情况
        self.__absenceColor = []
            
    @property
    def tableConfig(self):
        return self.__table_config
    
    def setTableConfig(self, config):
        """设置牌桌配置"""
        self.__table_config = config
    
    @property
    def curSeatId(self):
        return self.__curSeatId
    
    def setCurSeatId(self,seatId):
        self.__curSeatId = seatId
        
    @property
    def lastGangSeat(self):
        return self.__last_gang_seat
    
    def setLastGangSeat(self, seat):
        self.__last_gang_seat = seat
        
    @property
    def tableTileMgr(self):
        return self.__table_tile_mgr
    
    def setTableTileMgr(self, mgr):
        self.__table_tile_mgr = mgr
        
    @property
    def allPlayerTiles(self):
        return self.__all_player_tiles
    
    def setAllPlayerTiles(self, tiles):
        self.__all_player_tiles = tiles
        
    def isHu(self, tiles, tile, isTing, getTileType, magicTiles = [], tingNodes = [], curSeatId = 0, winSeatId = 0, actionID = 0, isGangKai = False,isForHu = True):
        """子类必须实现
        参数：
        1）tiles 该玩家的手牌
        2）isTinge 是否听牌
        3) tingNodes为听牌之后胡牌把听牌条件附带过来，按照听牌的胡牌规则来
        4) getTileType 获取tile的方式,0为摸牌,1为要别人打出的牌
        """
        return False, [],None
    
    def isPassHu(self):
        """是否有漏胡规则"""
        return False
    
    def isDropHu(self, player):
        """出牌立即胡牌的类型判断"""
        
        return False, []
    
    def isAddHu(self, player, tile):
        """上牌后立即判胡的类型"""
        return False

    def canDirectHuAfterTing(self):
        """默认不允许听牌后，能和牌时直接胡"""
        return False

    # 鸡西麻将用 听牌之后如果和的是宝牌 那么直接算和
    def isMagicAfertTingHu(self, isTing, winNodes, magicTiles, extendInfo = {}):
        return False
    
    # 鸡西麻将用 三人麻将无对胡
    def isWuDuiHu(self, allTiles, winTile, curSeatId, playerCount):
        return False, -1
        
    def canWinAfterChiPengGang(self, tiles):
        return True
    
    @property
    def multiple(self):
        return self.__multiple
    
    def setMultiple(self, playerMultiple):
        self.__multiple = playerMultiple

    @property
    def winType(self):
        return self.__winType

    def setWinType(self, type):
        self.__winType = type

    def isNeedBankId(self):
        """是需要庄家id"""
        return False

    @property
    def bankerId(self):
        return self.__banker_id

    def setBankerId(self, bankerId):
        self.__banker_id = bankerId

    @property
    def absenceColor(self):
        return self.__absenceColor

    def setAbsenceColor(self, absenceColor):
        self.__absenceColor = absenceColor

    def calcWinTiles(self, tiles):
        """判断能胡哪些牌
        """
        return []
