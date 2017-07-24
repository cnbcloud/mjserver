# -*- coding=utf-8 -*-
'''
Created on 2015年9月28日

@author: liaoxx
'''


import time
import freetime.util.log as ftlog
from hall.servers.common.base_checker import BaseMsgPackChecker
from poker.protocol import runcmd, router
from freetime.entity.msg import MsgPack
from poker.entity.configure import gdata
from poker.entity.biz import bireport
from majiang2.entity.item import MajiangItem
from majiang2.table.friend_table_define import MFTDefine

class GameTcpHandler(BaseMsgPackChecker):

    def __init__(self):
        pass

    def doRoomList(self, userId, gameId):        
        msg = runcmd.getMsgPack()
        playMode = msg.getParam('play_mode')
        if playMode is None or playMode == 'default':
            playMode = 'harbin'
        
        room_infos = self._fetchAllRoomInfos(userId, gameId, playMode)
        vardata = msg.getParam('vardata', 0)
        message = MsgPack()
        message.setCmd('room_list')
        message.setResult('play_mode', playMode)
        message.setResult('gameId', gameId)
        message.setResult('baseUrl', 'http://www.tuyoo.com/')
        if vardata == 0:
            message.setResult('rooms', room_infos)
        else:
            room_list = []
            for info in room_infos:
                room_list.append([info[0], info[1]])
            message.setResult('rooms', room_list)
        router.sendToUser(message, userId)
        
    def _fetchAllRoomInfos(self, uid, gid, playMode):
        ftlog.debug("|gameId, roomIds:", gid, [room.roomId for room in gdata.roomIdDefineMap().values() if room.gameId == gid])
        ftlog.debug("|gameId, bigRoomIds:", gid, list(gdata.gameIdBigRoomidsMap()[gid]))
        ctlRoomIds = [bigRoomId * 10000 + 1000 for bigRoomId in gdata.gameIdBigRoomidsMap()[gid]]
        ctlRoomIds.sort()
        ftlog.debug("|gameId, ctrRoomIds:", gid, ctlRoomIds)
        roomInfos = []
        ucount_infos = bireport.getRoomOnLineUserCount(gid, True)
        ftlog.debug("_fetchAllRoomInfosxxxxxxxx", ucount_infos)
        if playMode :
            for ctlRoomId in ctlRoomIds :
                roomDef = gdata.roomIdDefineMap()[ctlRoomId]
                ftlog.debug('_generateRoomList ', 'roomDef=', roomDef)
                roomConfig = roomDef.configure
                if roomConfig.get('playMode', None) == playMode \
                    and (not roomConfig.get('ismatch', 0)) \
                    and (not roomConfig.get(MFTDefine.IS_CREATE, 0)):
                    # 有playMode 非比赛 非自建桌
                    roomDesc = {}
                    roomDesc["play_mode"] = roomConfig["playMode"]
                    roomDesc["min_coin"] = roomConfig["minCoin"]
                    roomDesc["max_coin"] = roomConfig["maxCoin"]
                    roomDesc["base_chip"] = roomConfig["tableConf"]["base_chip"]
                    roomDesc["service_fee"] = roomConfig["tableConf"]["service_fee"]
                    playerCount = ucount_infos[1].get(str(roomDef.bigRoomId), 0)
                    ftlog.debug("_fetchAllRoomInfosxxxxxxxx", ucount_infos[1], roomDef.bigRoomId, ctlRoomId, playerCount)
                    roomInfos.append([
                                        ctlRoomId,
                                        playerCount,
                                        "",
                                        "",
                                        "",
                                        roomDesc                                      
                                      ])
        return roomInfos
 
    def curTimestemp(self, gameId, userId):
        msg = MsgPack()
        msg.setCmd('user')
        msg.setResult('action', 'mj_timestamp')
        msg.setResult('gameId', gameId)
        msg.setResult('userId', userId)
        current_ts = int(time.time())
        msg.setResult('current_ts', current_ts)
        router.sendToUser(msg, userId)
        
    def getVipTableList(self, userId, clientId):
        """ 客户端获取 <vip桌子列表>
        """
        pass

    def getVipTableListUpdate(self, userId, clientId):
        """ 客户端获取 <vip桌子列表变化信息>
        """
        pass
    
    def getUserInfoSimple(self, userId, gameId, roomId0, tableId0, clientId):
        """ 客户端获取vip桌子上，玩家简单个人信息
        """
        pass

    def getRichManList(self, userId, gameId, clientId):
        """ 客户端请求 <土豪列表>
        """
        pass

    def getConponExchangeInfos(self, userId, gameId, clientId):
        """ 麻将大厅主界面 <实物兑换>
        """
        pass

    def getSaleChargeInfos(self, userId, gameId, clientId):
        """ 麻将大厅主界面 <特惠充值>
        """
        pass
    
    def getCumulateChargeInfos(self, gameId, userId, clientId):
        """ 麻将大厅主界面 <累计充值>
        """
        pass
    
    def openCumulateChargeBox(self, gameId, userId, clientId):
        """ 客户端打开累计充值宝箱
        """
        pass
    
    def doGetMajiangItem(self, gameId, userId, clientId):
        """ 客户端获取麻将道具数量
        """
        tabs = MajiangItem.queryUserItemTabsV3_7(gameId, userId)
        MajiangItem.sendItemListResponse(gameId, userId, tabs)