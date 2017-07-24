# -*- coding=utf-8
'''
Created on 2016年9月23日

@author: zhaol
'''
from majiang2.msg_handler.msg import MMsg
from majiang2.table_state.state import MTableState
from majiang2.action_handler.action_handler import ActionHandler
from freetime.util import log as ftlog

class MMsgConsole(MMsg):
    
    def __init__(self):
        super(MMsgConsole, self).__init__()
        
    def table_call_fang_mao(self
                             , player
                             , mao
                             , maos
                             , state
                             , seatId
                             , timeOut
                             , actionID
                             , extend):
        self.table_call_add_card(player, 0, state, seatId, timeOut, actionID, extend, player.userId)
    
        
    def table_call_add_card(self, player, tile, state, seatId, timeOut, actionId, extendInfo, recordUserIds):
        """通知庄家游戏开始
        参数
        player - 庄家
        tile - 摸牌
        """
        ftlog.debug( 'seat:', player.curSeatId )
        ftlog.debug( player.printTiles() )
        ftlog.debug( 'Add tile:', tile, ' U can:' )
        if state & MTableState.TABLE_STATE_CHI:
            ftlog.debug( 'CHI, enter ', ActionHandler.ACTION_CHI )
            
        if state & MTableState.TABLE_STATE_PENG:
            ftlog.debug( 'PENG, enter ', ActionHandler.ACTION_PENG )
            
        if state & MTableState.TABLE_STATE_GANG:
            ftlog.debug( 'GANG, enter ', ActionHandler.ACTION_GANG )
            
        if state & MTableState.TABLE_STATE_HU:
            ftlog.debug( 'HU, enter ', ActionHandler.ACTION_HU )
            
        if state & MTableState.TABLE_STATE_DROP:
            ftlog.debug( 'DROP, enter ', ActionHandler.ACTION_DROP )
            
        if state & MTableState.TABLE_STATE_FANGMAO:
            ftlog.debug( 'MAO/DAN, enter ', ActionHandler.ACTION_MAO )
    
    def table_call_add_card_broadcast(self, seatId, timeOut, actionId, userId, tile):
        """通知其他人游戏开始
        参数
        pBanker - 庄家
        player - 待通知玩家
        tile - 庄家摸牌
        """
        pass
    
    def table_call_fang_mao_broadcast(self
                        , seatId
                        , timeOut
                        , actionID
                        , userId
                        , maos
                        , mao):
        pass
        
    def table_call_drop(self, seatId, player, tile, state, extendInfo, actionId, timeOut, winTiles=None):
        """通知玩家出牌
        参数：
            player - 做出牌操作的玩家
            winTiles - 可能胡哪些牌，某些玩法没有听牌功能，但也要每次提示玩家可胡哪些牌
        """
        if state == MTableState.TABLE_STATE_NEXT:
            return
        
        ftlog.debug( 'seat:', player.curSeatId )
        ftlog.debug( player.printTiles() )
        ftlog.debug( 'Drop by other player:', tile, ' U can:' )
            
        if state & MTableState.TABLE_STATE_CHI:
            ftlog.debug( 'CHI, enter ', ActionHandler.ACTION_CHI )
            
        if state & MTableState.TABLE_STATE_PENG:
            ftlog.debug( 'PENG, enter ', ActionHandler.ACTION_PENG )
            
        if state & MTableState.TABLE_STATE_GANG:
            ftlog.debug( 'GANG, enter ', ActionHandler.ACTION_GANG )
            
        if state & MTableState.TABLE_STATE_HU:
            ftlog.debug( 'HU, enter ', ActionHandler.ACTION_HU )
            
        if state & MTableState.TABLE_STATE_DROP:
            ftlog.debug( 'DROP, enter ', ActionHandler.ACTION_DROP )
            
        ftlog.debug( 'CANCEL, enter ', 0 )
        return None
    
    def send_message(self, message, uidList):
        """发送消息"""
        pass