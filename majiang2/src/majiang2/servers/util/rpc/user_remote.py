# -*- coding=utf-8 -*-
'''
Created on 2016年12月06日

@author: zhaol
'''
from poker.protocol.rpccore import markRpcCall
from majiang2.entity.item import MajiangItem
from poker.entity.dao import onlinedata
from freetime.util import log as ftlog

@markRpcCall(groupName="userId", lockName="userId", syncCall=1)
def getItemCount(userId, itemId):
    """获取房卡数"""
    user_fangka_count = MajiangItem.getUserItemCountByKindId(userId, itemId)
    return user_fangka_count

@markRpcCall(groupName="userId", lockName="userId", syncCall=1)
def consumeItem(userId, gameId, itemId, count, roomId, bigRoomId):
    """消费房卡，加锁操作"""
    user_fangka_count = MajiangItem.getUserItemCountByKindId(userId, itemId)
    if user_fangka_count >= count:
        consumeResult = MajiangItem.consumeItemByKindId(userId
            , gameId
            , itemId
            , count
            , 'MAJIANG_FANGKA_CONSUME'
            , bigRoomId)
        return consumeResult
    return False

@markRpcCall(groupName="userId", lockName="userId", syncCall=1)
def resumeItemFromRoom(userId, gameId, itemId, count, roomId, bigRoomId):
    """退还房卡，加锁操作"""
    MajiangItem.addUserItemByKindId(userId
            , gameId
            , itemId
            , count
            , 'MAJIANG_FANGKA_RETURN_BACK'
            , bigRoomId)
    
@markRpcCall(groupName="userId", lockName="userId", syncCall=1)
def resumeItemFromTable(userId, gameId, itemId, count, roomId, tableId, bigRoomId):
    """退还房卡，加锁操作"""
    ftlog.debug('user_remote resumeItemFromTable userId:', userId
            , ' gameId:', gameId
            , ' itemId:', itemId
            , ' count:', count
            , ' roomId:', roomId
            , ' tableId:', tableId
            , ' bigRoomId:', bigRoomId
    )
    
    lseatId = onlinedata.getOnlineLocSeatId(userId, roomId, tableId)
    ftlog.debug('user_remote resumeItemFromTable lseatId:', lseatId)
    
    if lseatId < 0:
        ftlog.info('user_remote resumeItemFromTable loc not match, do not resume item. userId:', userId
                , ' gameId:', gameId
                , ' itemId:', itemId
                , ' count:', count
                , ' roomId:', roomId
                , ' tableId:', tableId
                , ' seatId:', lseatId)
        return
        
    MajiangItem.addUserItemByKindId(userId
            , gameId
            , itemId
            , count
            , 'MAJIANG_FANGKA_RETURN_BACK'
            , bigRoomId)