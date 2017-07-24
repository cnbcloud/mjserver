# -*- coding=utf-8 -*-
'''
Created on 2015年11月4日

@author: liaoxx
'''
from poker.protocol.rpccore import markRpcCall
from poker.entity.configure import gdata
from freetime.util import log as ftlog



@markRpcCall(groupName="roomId", lockName="", syncCall=1)
def checkCanEnter(roomId, userId, userChip):
    ftlog.debug('checkCanEnter, input:', roomId, userId, userChip)
    return gdata.rooms()[roomId].check_enter(userId, userChip)
    

@markRpcCall(groupName="roomId", lockName="", syncCall=1)
def reportGameStart(roomId, tableId, matchId, userIds):
    ftlog.debug('reportGameStart, input:', roomId, tableId, matchId, userIds)
    return gdata.rooms()[roomId].mark_game_start(tableId, matchId, userIds)
    
@markRpcCall(groupName="roomId", lockName="", syncCall=1)
def reportGameEnd(roomId, tableId, matchId, userIds):
    ftlog.debug('reportGameEnd, input:', roomId, tableId, matchId, userIds)
    return gdata.rooms()[roomId].mark_game_end(tableId, matchId, userIds)

@markRpcCall(groupName="roomId", lockName="", syncCall=1)
def getMatchInfoAbstract(roomId, gameId, userId, notAwardList=False):
    ftlog.debug('getMatchInfoAbstract, input: ',roomId, gameId, userId, notAwardList)
    return gdata.games()[gameId].getBigMatchPlugin().getMatchInfoAbstract(gdata.rooms()[roomId], userId, notAwardList)

@markRpcCall(groupName="roomId", lockName="", syncCall=1)
def getMatchSimpleInfo(roomId, gameId, userId):
    ftlog.debug('getMatchSimpleInfo, input: ',roomId, gameId, userId)
    return gdata.games()[gameId].getBigMatchPlugin().getMatchSimpleInfo(gdata.rooms()[roomId], userId)

@markRpcCall(groupName="roomId", lockName="", syncCall=1)
def getMatchAwardListInfo(roomId, gameId, userId):
    ftlog.debug('getMatchAwardListInfo, input: ',roomId, gameId, userId)
    return gdata.games()[gameId].getBigMatchPlugin().getMatchAwardListInfo(gdata.rooms()[roomId], userId)

@markRpcCall(groupName="roomId", lockName="", syncCall=1)
def isUserInMatch(roomId, matchInstId, gameId, userId):
    ftlog.debug('isUserInMatch, input: ',roomId, gameId, userId, matchInstId)
    return gdata.games()[gameId].getBigMatchPlugin().isUserInMatch(gdata.rooms()[roomId], userId, matchInstId)

@markRpcCall(groupName="roomId", lockName="", syncCall=1)
def signinNextMatch(roomId, matchInstId, gameId, userId):
    ftlog.debug('signinNextMatch, input: ',roomId, gameId, userId, matchInstId)
    return gdata.rooms()[roomId].mj_signin_next_match(userId, roomId)
         
@markRpcCall(groupName="roomId", lockName="", syncCall=1)
def getCreateTableByRoomId(roomId):
    from majiang2.entity.create_table_list import CreateTable
    return CreateTable.get_create_table_by_roomid(roomId)


    