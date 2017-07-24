# -*- coding=utf-8
'''
Created on 2016年9月23日
听牌规则
@author: zhaol
'''

class MTingRule(object):
    """听牌规则"""
    def __init__(self):
        super(MTingRule, self).__init__()
        self.__win_rule_mgr = None
        self.__table_tile_mgr = None
        self.__table_config = {}
        
    def setTableConfig(self, config):
        """设置牌桌配置"""
        self.__table_config = config
        
    @property
    def tableConfig(self):
        return self.__table_config
    
    def getTableConfig(self, key, default):
        """
        获取牌桌配置
        key : 要获取的配置
        default: 默认值，必须填
        """
        if not self.__table_config:
            return default
        
        return self.__table_config.get(key, default)
        
    @property
    def tableTileMgr(self):
        return self.__table_tile_mgr
    
    def setTableTileMgr(self, mgr):
        self.__table_tile_mgr = mgr
        
    @property
    def winRuleMgr(self):
        return self.__win_rule_mgr
    
    def setWinRuleMgr(self, mgr):
        self.__win_rule_mgr = mgr
    
    
    def canTing(self, tiles, leftTiles, tile, magicTiles = [], curSeatId = 0, winSeatId = 0, actionID = 0):
        """子类必须实现
        参数：
        1）tiles 该玩家的手牌，二位数组，包含玩家的手持牌，吃牌，碰牌，杠牌，胡牌等所有信息
        
        返回值：
        是否可以听牌，听牌详情
        """
        return False, []
    
    def canTingBeforeAddTile(self, tiles, leftTiles, magicTiles = [], curSeatId = 0, winSeatId = 0, actionID = 0):
        return False, []

    def canTingAfterPeng(self, tiles):
        """"碰之后是否可以马上听牌"""
        # 和抢听是矛盾的，非抢听情况下，玩家正常碰牌后，是否可以马上弹出听牌按钮
        return False