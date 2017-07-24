# -*- coding=utf-8 -*-
'''
Created on 2015年9月29日

@author: liaoxx
'''

from hall.servers.common.base_checker import BaseMsgPackChecker
from poker.entity.configure import gdata

class TableTcpHandler(BaseMsgPackChecker):
    
    def __init__(self):
        pass
    
    def _check_param_grab_times(self, msg, key, params):
        grab_times = msg.getParam('grab_times')
        if isinstance(grab_times, int) :
            return None, grab_times
        return 'ERROR of grab_times !' + str(grab_times), None

    def _check_param_envelope_num(self, msg, key, params):
        envelope_num = msg.getParam('envelope_num')
        if  isinstance(envelope_num, int) :
            return None, envelope_num
        return 'ERROR of envelope_num !' + str(envelope_num), None


    def _check_param_interval(self, msg, key, params):
        interval = msg.getParam('interval')
        if  isinstance(interval, int) :
            return None, interval
        return 'ERROR of interval !' + str(interval), None


    def _check_param_chatMsg(self, msg, key, params):
        chatMsg = msg.getParam('msg')
        if chatMsg and isinstance(chatMsg, (str, unicode, dict)) :
            return None, chatMsg
        return 'ERROR of chatMsg !' + str(chatMsg), None


    def _check_param_isFace(self, msg, key, params):
        isFace = msg.getParam(key)
        if not isinstance(isFace, int) :
            isFace = 0
        return None, isFace


    def _check_param_voiceIdx(self, msg, key, params):
        voiceIdx = msg.getParam(key)
        if not isinstance(voiceIdx, int) :
            voiceIdx = -1
        return None, voiceIdx

    def doTableChat(self, userId, roomId, tableId, seatId, isFace, voiceIdx, chatMsg):
        room = gdata.rooms()[roomId]
        table = room.maptable[tableId]
        table.doTableChat(userId, seatId, isFace, voiceIdx, chatMsg)

    def _check_param_smilies(self, msg, key, params):
        smilies = msg.getParam(key)
        if isinstance(smilies, (str, unicode)) :
            return None, smilies
        return 'ERROR of smilies !' + str(smilies), None

    def _check_param_toseat(self, msg, key, params):
        seatId = msg.getParam(key)
        if isinstance(seatId, int) and seatId > 0:
            return None, seatId
        return 'ERROR of toseat !' + str(seatId), None
    
    def _check_param_ledMsg(self, msg, key, params):
        ledMsg = msg.getParam('ledMsg')
        if ledMsg and isinstance(ledMsg, (str, unicode)) :
            return None, ledMsg
        return 'ERROR of ledMsg !' + str(ledMsg), None

    def doTableSmilies(self, userId, roomId, tableId, seatId, smilies, toseat):
        room = gdata.rooms()[roomId]
        table = room.maptable[tableId]
        table.doTableSmilies(userId, seatId, smilies, toseat)

    def doRedEnvelopeStart(self, roomId, grab_times, envelope_num, interval):
        pass

    def doRedEnvelopeLed(self, roomId, ledMsg):
        pass

    def doTableSceneLeave(self, userId, roomId, tableId, seatId):
        """
        客户端离开牌桌场景时通知服务器 added by nick.kai.lee
        客户端离开场景时主动发消息告知服务器,服务器可以推送一些消息,比如免费金币的todotask给客户端,当客户端返回房间列表时触发
        不能复用leave消息,因为客户端结算时会leave,点击返回按钮时还会leave一次.
        """
        room = gdata.rooms()[roomId]
        table = room.maptable[tableId]
        table._send_win_sequence_led_message(userId)
