# -*- coding=utf-8 -*-
'''
Created on 2015年9月28日

@author: liaoxx
'''

from poker.protocol.decorator import markCmdActionHandler, markCmdActionMethod
from majiang2.servers.util.game_handler import GameTcpHandler

@markCmdActionHandler
class QueshouGameTcpHandler(GameTcpHandler):

    def __init__(self):
        super(QueshouGameTcpHandler, self).__init__()
    
    @markCmdActionMethod(cmd='game', action="quick_start", clientIdVer=0, scope='game', lockParamName="")
    def doGameQuickStart(self, userId, gameId, clientId, roomId0, tableId0, playMode, sessionIndex):
        super(QueshouGameTcpHandler, self).doGameQuickStart(userId, gameId, clientId, roomId0, tableId0, playMode, sessionIndex)

    @markCmdActionMethod(cmd='game', action="award_certificate", clientIdVer=0, scope='game', lockParamName="")
    def doAwardCertificate(self, userId, gameId, match_id, clientId):
        super(QueshouGameTcpHandler, self).doAwardCertificate(userId, gameId, match_id, clientId)
    
    @markCmdActionMethod(cmd='game', action="create_table_info", clientIdVer=0, scope='game', lockParamName="")
    def doGetCreatTableInfo(self, userId, gameId, clientId, hasRobot):
        super(QueshouGameTcpHandler, self).doGetCreatTableInfo(userId, gameId, clientId, hasRobot)
            
    @markCmdActionMethod(cmd='game', action="create_table", clientIdVer=0, scope='game', lockParamName="")
    def doCreateTable(self, userId, gameId, clientId, roomId0, tableId0, playMode, hasRobot):
        super(QueshouGameTcpHandler, self).doCreateTable(userId, gameId, clientId, roomId0, tableId0, playMode, hasRobot)
    
    @markCmdActionMethod(cmd='game', action="join_create_table", clientIdVer=0, scope='game', lockParamName="")
    def doJoinCreateTable(self, userId, gameId, clientId, roomId0, tableId0, playMode):
        super(QueshouGameTcpHandler, self).doJoinCreateTable(userId, gameId, clientId, roomId0, tableId0, playMode)
    
    @markCmdActionMethod(cmd='game', action="create_table_record", clientIdVer=0, scope='game', lockParamName="")
    def doGetCreateTableRecord(self, userId, gameId, clientId):
        super(QueshouGameTcpHandler, self).doGetCreateTableRecord(userId, gameId, clientId)