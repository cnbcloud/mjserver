# -*- coding=utf-8
'''
Created on 2017年6月6日
牌型整理
@author: youjun
'''
from majiang2.ai.win import MWin
from majiang2.player.hand.hand import MHand
from majiang2.tile.tile import MTile
from majiang2.table.table_config_define import MTDefine
from majiang2.table_tile.table_tile_factory import MTableTileFactory
from majiang2.tile_pattern_checker.tile_pattern_checker import MTilePatternChecker
from freetime.util import log as ftlog
import copy

class MTilePatternCheckerQueshou(MTilePatternChecker):
    """卡五星胡牌
    多支持七对胡
    """
    def __init__(self):
        super(MTilePatternCheckerQueshou, self).__init__()
        # 获胜一方的桌子号
        self.__win_seat_id = None
        # 上一轮的桌子号
        self.__last_seat_id = None
        # 获胜牌
        self.__win_tile = None
        # 牌桌手牌管理器
        self.__table_tile_mgr = None
        # 获胜时的actionID
        self.__aciton_id = None
        # 所有玩家的所有牌，按手牌格式的数组
        self.__player_all_tiles = []
        # 所有玩家的所有牌，合到一个数组
        self.__player_all_tiles_arr = []
        # 所有玩家手牌
        self.__player_hand_tiles_with_hu = []

