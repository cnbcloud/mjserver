# -*- coding=utf-8 -*-
'''
Created on 2015年9月28日

@author: liaoxx
'''


from poker.protocol.decorator import markCmdActionHandler, markCmdActionMethod
from majiang2.servers.util.hall_handler import GameTcpHandler

@markCmdActionHandler
class LuosihuGameTcpHandler(GameTcpHandler):

    def __init__(self):
        super(LuosihuGameTcpHandler, self).__init__()

    @markCmdActionMethod(cmd='game', action="room_list", clientIdVer=0, scope='game', lockParamName="")
    def doRoomList(self, userId, gameId):  
        super(LuosihuGameTcpHandler, self).doRoomList(userId, gameId) 
 
    @markCmdActionMethod(cmd='user', action='mj_timestamp', scope='game')
    def curTimestemp(self, gameId, userId):
        super(LuosihuGameTcpHandler, self).curTimestemp(gameId, userId)
        
    @markCmdActionMethod(cmd='hall', action='vipTableList', scope='game')
    def getVipTableList(self, userId, clientId):
        pass

    @markCmdActionMethod(cmd='hall', action='vipTableListUpdate', scope='game')
    def getVipTableListUpdate(self, userId, clientId):
        pass
    
    @markCmdActionMethod(cmd='user', action='info', scope='game')
    def getUserInfoSimple(self, userId, gameId, roomId0, tableId0, clientId):
        super(LuosihuGameTcpHandler, self).getUserInfoSimple(userId, gameId, roomId0, tableId0, clientId)

    @markCmdActionMethod(cmd='user', action='get_richman_list', scope='game')
    def getRichManList(self, userId, gameId, clientId):
        pass

    @markCmdActionMethod(cmd='user', action='conpon_exchange_infos', scope='game')
    def getConponExchangeInfos(self, userId, gameId, clientId):
        pass

    @markCmdActionMethod(cmd='user', action='sale_charge', scope='game')
    def getSaleChargeInfos(self, userId, gameId, clientId):
        pass
    
    @markCmdActionMethod(cmd='user', action='cumulate_recharge_infos', scope='game')
    def getCumulateChargeInfos(self, gameId, userId, clientId):
        pass
    
    @markCmdActionMethod(cmd='user', action='open_cumulate_recharge_box', scope='game')
    def openCumulateChargeBox(self, gameId, userId, clientId):
        pass
    
    @markCmdActionMethod(cmd='user', action='majiang_item', scope='game')
    def doGetMajiangItem(self, gameId, userId, clientId):
        super(LuosihuGameTcpHandler, self).doGetMajiangItem(gameId, userId, clientId)
