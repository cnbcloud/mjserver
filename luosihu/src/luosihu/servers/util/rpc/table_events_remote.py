# -*- coding=utf-8 -*-
'''
Created on 2015年10月22日

@author: liaoxx
'''
from poker.protocol.rpccore import markRpcCall
import freetime.util.log as ftlog
from majiang2.entity.events.events import UserTablePlayEvent
from poker.entity.dao import gamedata

@markRpcCall(groupName="userId", lockName="", syncCall=1)
def gamePlay(userId, gameId, roomId, tableId, banker):
    ftlog.debug('table_events_remote trigger event UserTablePlayEvent...')
    from luosihu.game import TGLuosihu
    TGLuosihu.getEventBus().publishEvent(UserTablePlayEvent(gameId
            , userId
            , roomId
            , tableId
            , banker))
    gamedata.incrGameAttr(userId, gameId, 'play_game_count', 1)