# coding=UTF-8
'''
Created on 2015年6月26日

@author: zqh
'''
import json
import os, re
from clientid import ROOMIDMAP, CLIENDIDS

def getGameIdFromHallClientId(clientId):
    try:
        gid = re.match('^.*-hall(\\d+)\\..*$', clientId).group(1)
        return int(gid)
    except:
        return 0

def filter_room_des(desc, name, tableCount, shaowCoutn) :
    if  not 'condition' in desc :
        raise Exception('房间信息condition丢失') 
    dd = {}
    dd['buyinchip'] = 0
    dd['controlServerCount'] = 1
    dd['controlTableCount'] = 0
    dd['gameServerCount'] = shaowCoutn
    dd['gameTableCount'] = tableCount
    dd['goodCard'] = 0
    dd['ismatch'] = 0 if 'bigmatch' in desc else 1
    dd['matchConf'] = None if not 'bigmatch' in desc else desc['bigmatch']
    dd['maxCoin'] = -1
    dd['maxCoinQS'] = -1
    dd['maxLevel'] = -1
    dd['minCoin'] = 0
    dd['minCoinQS'] = 0
    dd['name'] = name
    dd['playDesc'] = '' 
    dd['roomFee'] = 0
    dd['roomMutil'] = 1
    dd['sendCoupon'] = 0
    dd['showCard'] = 0 
    dd['typeName'] = 'normal'
    dd['playMode'] = 'happy'
    dd['winDesc'] = ''
    dd['dummyUserCount'] = 0

    for k, v in dd.items() :
        if not k in desc :
            desc[k] = v
    
    for k in desc.keys() :
        if not k in dd :
            del desc[k]
            
    return desc

def d1(d, k, v):
    if not k in d :
        d[k] = v

# 斗地主桌子配置
def filter_table_config(desc, roomDesc):
    if 'extdict' in desc :
        return desc['extdict']
    dd = {}
    d1(dd, 'grab', 1)  # 1  #本桌是否支持抢地主,0表示不支持
    d1(dd, 'basebet', 1)  # 2  #初始倍数
    d1(dd, 'maxSeatN', 3)  # 3  #座位数，现在总是3
#     roomDesc.get('minCoin', 0)   # 4  #入场最小金币，一般是基数的几十倍
#     roomDesc.get('maxCoin', -1)   # 5  #入场最大金币，一般是基数的几十倍
    d1(dd, 'coin2chip', 1)  # 6  #为了平台兼容，几乎总是1
    d1(dd, 'optime', 20)  # 7  #操作时间秒数单位
#     roomDesc.get('roomFee', 0)   # 8  #服务费用(系统抽成)  要和addRoom中的配置一致
    d1(dd, 'basemulti', 1)  # 9  #基本的倍率
#     roomDesc.get('roomMutil', 1)   # 10 #房间倍率，8倍场，20倍场中的倍数，要和addRoom中的roomMulti一致
    d1(dd, 'lucky', 0)  # 11 #多发炸弹的概率
    d1(dd, 'gslam', 128)  # 12 #大满贯倍数
    d1(dd, 'passtime', 5)  # 13表示如果自己管不上上家的牌，显示自己的出牌时间。如果没有则等同opTime
    d1(dd, 'canchat', 0)  # 14 1 -- 可以聊天， 0 -- 不可以聊天
    d1(dd, 'unticheat', 0)  # 15 1 -- 防作弊， 0 -- 普通
    d1(dd, 'autochange', 1)  # 16 1 -- 每局结束后自动换桌， 0 -- 不自动换桌
    d1(dd, 'tbbox', 0)  # 17 1 -- 有宝箱， 0 -- 无宝箱
    d1(dd, 'robottimes', 2)  # 18 n - 超时n次后， 托管状态
    d1(dd, 'rangpaiMultiType', 1)  # 19 1 - 让牌倍数+1  2 - 让牌倍数*2
    
    for k, v in dd.items() :
        if not k in desc :
            desc[k] = v
    
    for k in desc.keys() :
        if not k in dd :
            del desc[k]
    
    return desc
allrooms = {}
def add_dizhu_room(roomId, tableCount, serverIds, roomName, roomDesc, tableDesc):
    if roomId in ROOMIDMAP :
        roomDesc = filter_room_des(roomDesc, roomName, tableCount, len(serverIds))
        tableconf = filter_table_config(tableDesc, roomDesc)
        roomId = ROOMIDMAP[roomId]
        allrooms[roomId] = [roomDesc, tableconf]
        print 'add_table_config->', roomId, json.dumps(roomDesc, sort_keys=True), json.dumps(tableconf, sort_keys=True)

execfile('./game_rooms.py')


for rid in allrooms.keys() :
    mid = rid + 100
    if mid in allrooms :
        allrooms[rid][0]['matchConf'] = allrooms[mid][0]['matchConf']
        del allrooms[mid]

rkeys = allrooms.keys()
rkeys.sort()

for rid in rkeys :
    r = allrooms[rid]
    r[0]['tableConf'] = r[1]
    print '"%d":' % (rid), json.dumps(r[0], sort_keys=True), ','

if __name__ == '__main__':
    pass
