# coding=UTF-8
'''
Created on 2015年6月26日

@author: zqh
'''
import json, gdss
import os, re
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


def writejson(fname, jsondata):
    jsondata = json.dumps(jsondata, indent=2, separators=(', ', ' : '), sort_keys=True, ensure_ascii=False)
    lines = jsondata.split('\n')
    for x in xrange(len(lines)) :
        lines[x] = lines[x].rstrip()
    jsondata = '\n'.join(lines)
    f = open(fname, 'w')
    f.write(jsondata)
    f.close()

print os.getcwd()

updata = '''
    roomId        roomMutil        roomFee        maxCoinQS        buyinchip
欢乐新手场    6001    60    60    25    20    2000    2500    1500    1800
欢乐中级场    6002    350    350    80    80    30000    42001    20000    20000
欢乐高级场    6003    1500    1500    600    450    80000    102001    60000    80000
欢乐大师场    6004    8000    8000    3000    2500    -1    -1    650000    650000
经典初级场    6011    50    50    25    20    2000    2500    1500    1800
经典中级场    6012    200    200    60    60    30000    42001    20000    20000
经典高级场    6013    1000    1000    550    500    80000    102001    60000    80000
经典大师场    6014    6000    6000    3500    3000    -1    1000000    650000    650000
星耀大师场    6015    30000    30000    15000    13000    -1    -1    0    2000000
癞子新手场    6021    30    30    25    20    2500    2500    1500    1800
癞子中级场    6022    150    150    80    80    40000    42001    20000    20000
癞子高级场    6023    800    800    600    500    100000    102001    60000    60000
癞子大师场    6024    3000    3000    3000    2200    -1    -1    650000    650000
二人新手场    6031    120    120    35    25    2000    2500    1500    1800
二人中级场    6032    600    600    120    100    30000    42001    20000    20000
二人高级场    6033    3500    3500    750    650    80000    102001    60000    80000
二人大师场    6034    12000    12000    3000    2500    -1    -1    650000    650000
'''
lines = []
for l in updata.split('\n') :
    l = l.strip()
    if l :
        l = l.replace('\t', ' ')
        ld = l.split(' ')
        if ld :
            la = []
            lines.append(la)
            for x in ld :
                if x :
                    la.append(x)

title = lines[0]
del lines[0]
print title

delc = len(title) - 1
for l in lines :
    for x in xrange(delc, -1, -1) :
        del l[x * 2 - 2]
    print l

ROOM_JSON = './../../release-config/game/6/room/0.json'
f = open(ROOM_JSON, 'r')
datas = json.load(f)
f.close()

for upd in lines :
    roomId = upd[0]
    room = datas[roomId]
    for x in xrange(1, len(title)) :
        k = title[x]
        v = upd[x]
        ov = room[k]
        v = type(ov)(v)
        print roomId, k, ov, v
        room[k] = v

writejson(ROOM_JSON, datas)

if title[1] == 'roomMutil' :
    ROOM_JSON = './../../release-config/game/6/hall.info/0.json'
    f = open(ROOM_JSON, 'r')
    datas = json.load(f)
    f.close()
    
    for upd in lines :
        roomId = upd[0]
        roomMutil = upd[1]
        for x in datas['room_items'] :
            room = datas['room_items'][x]
            if str(room['id']) == roomId :
                room['least'] = int(roomMutil)
                room['entry'] = '底注' + str(room['least']) + '金币'
    writejson(ROOM_JSON, datas)

