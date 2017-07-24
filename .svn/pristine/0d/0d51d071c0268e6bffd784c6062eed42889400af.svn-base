# -*- coding=utf-8 -*-
'''
Created on 2016年11月29日

@author: zhaol
'''
from poker.entity.events.tyevent import UserEvent

class UserTableEvent(UserEvent):
    '''
    牌桌事件的基类
    '''
    def __init__(self, gameId, userId, roomId, tableId):
        super(UserTableEvent, self).__init__(userId, gameId)
        self.roomId = roomId
        self.tableId = tableId
        
class UserTablePlayEvent(UserTableEvent):
    '''
    牌局开始事件
    '''
    def __init__(self, gameId, userId, roomId, tableId, banker):
        super(UserTablePlayEvent, self).__init__(gameId, userId, roomId, tableId)
        self.banker = banker
        
class UserTableWinLooseEvent(UserTableEvent):
    '''
    牌局结算事件
    '''
    def __init__(self, gameId, userId, roomId, tableId, winLoose, score):
        super(UserTablePlayEvent, self).__init__(gameId, userId, roomId, tableId)
        self.winLoose = winLoose
        self.score = score