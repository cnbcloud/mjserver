# -*- coding=utf-8 -*-
'''
Created on 2015年9月25日

@author: liaoxx
'''

import freetime.util.log as ftlog
from poker.entity.configure import configure, pokerconf
from majiang2.entity.uploader import uploadVideo as naviteUploadVideo
import copy

PLAYMODE_SICHUAN = 'sichuan'
PLAYMODE_GUOBIAO = 'guobiao'
PLAYMODE_HARBIN = 'harbin'
PLAYMODE_GUOBIAO_EREN = 'guobiao2ren'
PLAYMODE_SICHUAN_DQ = 'sichuan_dq'
PLAYMODE_SICHUAN_XLCH = 'sichuan_xlch'
PLAYMODE_GUOBIAO_VIP = 'guobiaovip'
PLAYMODE_GUOBIAO_MATCH = 'guobiaomatch'
PLAYMODE_GUOBIAO_EREN_MATCH = 'guobiao2renmatch'
PLAYMODE_SICHUAN_MATCH = 'sichuanmatch'
PLAYMODE_HARBIN_MATCH = 'harbinmatch'

MAJIANG2 = 9996

def getMajiangConf(gameId, mainKey, subKey, defaultRet = None):
    return configure.getGameJson(gameId, mainKey, {}).get(subKey, defaultRet)

def getTableRecordConfig():
    return configure.getGameJson(MAJIANG2, 'table_record', {})

def getRobotInterval(gameId):
    return getMajiangConf(gameId, 'public', "robot-interval", 1)

def get_medal_ui_config(gameId):
    """ 获取medal的ui配置
    """
    key = 'ui.config'
    ui_config = configure.getGameJson(gameId, key, {}).get('medal.ui.config', {})
    return ui_config

def get_room_other_config(gameId):
    """获取房间相关的其他配置"""
    key = 'room.other'
    config = configure.getGameJson(gameId, key, {})
    return copy.deepcopy(config)

def getCreateTableConfig(gameId, playMode, key, itemId):
    """获取自建房的配置"""
    config = get_room_other_config(gameId)
    createTable = config.get('create_table_config', {})

    playModeSetting = createTable.get(playMode, None)
    if not playModeSetting:
        return None
    
    itemSetting = playModeSetting.get(key, None)
    if not itemSetting:
        return None
    
    for item in itemSetting:
        if item['id'] == itemId:
            return item
        
    return None

def getCreateTableTotalConfig(gameId):
    """获取自建桌的大配置"""
    config = get_room_other_config(gameId)
    createTable = config.get('create_table_config', {})
    return createTable

def get_play_mode_config_by_clientId(clientId):
    """根据clientId获取自建桌支持的玩法列表"""
    key = 'room.other'
    intClientId = pokerconf.clientIdToNumber(clientId)
    play_mode_list = configure.getTcContentByClientId(key, None, intClientId, [])
    ftlog.debug('get_play_mode_config_by_clientId | clientId:', clientId, '| intClientId:', intClientId, '| play_mode_list:', play_mode_list)
    return play_mode_list

def get_table_record_msg_path(tableRecordKey, cardCount):
    """ 获取单局牌桌协议文件下载路径
    """
    trConfig = getTableRecordConfig()
    downloadPath = trConfig.get('trDownloadPath', '')
    return '%s%s' % (downloadPath, get_table_record_msg_fileName(tableRecordKey, cardCount))

def get_table_record_msg_fileName(gameId, tableRecordKey, cardCount):
    """ 获取单局牌桌协议文件名
    """
    trConfig = getTableRecordConfig()
    filePath = trConfig.get('trFilePath', '')
    return  '%s/record_%s_%s_%s' % (filePath, gameId, tableRecordKey, cardCount)

def uploadVideo(key, data):
    '''
    key:文件名
    data:文件内容
    '''
    trConfig = getTableRecordConfig()
    uploadKey = trConfig.get('trUploadKey', '')
    uploadUrl = trConfig.get('trUploadUrl', '')
    return naviteUploadVideo(uploadUrl, uploadKey, key, data)
