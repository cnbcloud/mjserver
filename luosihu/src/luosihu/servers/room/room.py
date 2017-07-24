# -*- coding=utf-8 -*-
'''
Created on 2015年10月25日

@author: liaoxx
'''
from poker.protocol.decorator import markCmdActionHandler, markCmdActionMethod
from majiang2.servers.room.room import RoomTcpHandler

@markCmdActionHandler
class LuosihuRoomTcpHandler(RoomTcpHandler):

    def __init__(self):
        super(LuosihuRoomTcpHandler, self).__init__()
        
    @markCmdActionMethod(cmd='room', action="quick_start", clientIdVer=0, scope='game')
    def doRoomQuickStart(self, roomId, userId):
        super(LuosihuRoomTcpHandler, self).doRoomQuickStart(roomId, userId)
        
    @markCmdActionMethod(cmd='room', action="match_state", clientIdVer=0, scope='game', lockParamName="")
    def doMatchState(self, userId, gameId, roomId):
        super(LuosihuRoomTcpHandler, self).doMatchState(userId, gameId, roomId)
        
    @markCmdActionMethod(cmd='room', action="match_award_certificate", clientIdVer=0, scope='game', lockParamName="")
    def doMatchAwardCertificate(self, userId, gameId, roomId, match_id):
        super(LuosihuRoomTcpHandler, self).doMatchAwardCertificate(userId, gameId, roomId, match_id)
    
    @markCmdActionMethod(cmd='room', action='majiang_m_signin_next', scope='game')
    def signinNextMatch(self, gameId, userId):
        """报名下一场比赛
        """
        super(LuosihuRoomTcpHandler, self).signinNextMatch(gameId, userId)
    
    @markCmdActionMethod(cmd='room', action="create_table", clientIdVer=0, scope='game', lockParamName="")
    def doCreateTable(self, userId, gameId, roomId):
        super(LuosihuRoomTcpHandler, self).doCreateTable(userId, gameId, roomId)

    @markCmdActionMethod(cmd='room', action="join_create_table", clientIdVer=0, scope='game', lockParamName="")
    def doJoinCreateTable(self, userId, gameId, roomId):
        super(LuosihuRoomTcpHandler, self).doJoinCreateTable(userId, gameId, roomId)
