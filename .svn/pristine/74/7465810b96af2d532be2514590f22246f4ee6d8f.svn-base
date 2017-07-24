# -*- coding=utf-8 -*-
'''
Created on 2015年9月29日

@author: liaoxx
'''

from poker.protocol.decorator import markCmdActionHandler, markCmdActionMethod
from majiang2.servers.table.table import TableTcpHandler

@markCmdActionHandler
class QueshouTableTcpHandler(TableTcpHandler):
    
    def __init__(self):
        super(QueshouTableTcpHandler, self).__init__()
        
    @markCmdActionMethod(cmd='table', action="chat", clientIdVer=0, scope='game')
    def doTableChat(self, userId, roomId, tableId, seatId, isFace, voiceIdx, chatMsg):
        super(QueshouTableTcpHandler, self).doTableChat(userId, roomId, tableId, seatId, isFace, voiceIdx, chatMsg)
    
    @markCmdActionMethod(cmd='table', action="smilies", clientIdVer=0, scope='game')
    def doTableSmilies(self, userId, roomId, tableId, seatId, smilies, toseat):
        super(QueshouTableTcpHandler, self).doTableSmilies(userId, roomId, tableId, seatId, smilies, toseat)

    @markCmdActionMethod(cmd='mj_red_envelope_start', action="", clientIdVer=0, lockParamName = "",scope='game')
    def doRedEnvelopeStart(self, roomId, grab_times, envelope_num, interval):
        pass

    @markCmdActionMethod(cmd='mj_red_envelope_led', action="", clientIdVer=0, lockParamName = "",scope='game')
    def doRedEnvelopeLed(self, roomId, ledMsg):
        pass

    @markCmdActionMethod(cmd='table_call', action="leave_table_scene", clientIdVer=0, scope='game')
    def doTableSceneLeave(self, userId, roomId, tableId, seatId):
        super(QueshouTableTcpHandler, self).doTableSceneLeave(userId, roomId, tableId, seatId)
