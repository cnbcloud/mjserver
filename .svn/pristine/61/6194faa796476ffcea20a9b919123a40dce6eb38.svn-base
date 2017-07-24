# coding=UTF-8
'''
Created on 2015年6月26日

@author: zqh
'''
import json
import os, re
from clientid import *
import sys


def convert_more_games(k, v):
    tkeys = v.keys()
    tkeys.sort()
    plugs = {}
    i = 0
    temps = {}
    for tkey in tkeys :
        mores = v[tkey]
        temps[tkey] = []
        for m in mores :
            ms = json.dumps(m, sort_keys=True)  # indent=2,
            if ms not in plugs.values() :
                x = tkey[10:] + '_' + m['game_mark']
                if x in plugs :
                    x = x + '_' + str(i)
                    i += 1
                plugs[x ] = m
                temps[tkey].append(x)
            else:
                for x, y in plugs.items() :
                    if y == ms :
                        temps[tkey].append(x)
    datas = {'plugins' : plugs, 'templates' : temps}
    datas = json.dumps(datas, indent=2, sort_keys=True)
    if not os.path.isdir('./9999/more.games') :
        os.makedirs('./9999/more.games')
    f = open('./9999/more.games/0.json', 'w')
    f.write(datas)
    f.close()


def convert_more_games_clientid(k, v):
    datas = {}
    for x, y in v.items() :
        for cid in y :
            icid = getIntClientId(cid)
            if icid > 0 :
                gid = getGameIdFromHallClientId(cid)
                if gid not in datas :
                    datas[gid] = {}
                datas[gid][icid] = x
    for gid, ids in datas.items() :
        p = './' + str(gid) + '/more.games'
        if not os.path.isdir(p) :
            os.makedirs(p)
        for icid, t in ids.items() :
            datas = json.dumps({'template' : t}, indent=2, sort_keys=True)
            f = open(p + '/' + str(icid) + '.json', 'w')
            f.write(datas)
            f.close()


def convert_rooms(k, v):
    print k, v


QUICK_CONF = {}
def convert_quickpay_conf(k, v):
    print k, v
    for x, y in v.items() :
        print x, y
        if x in QUICK_CONF :
            if QUICK_CONF[x] != y :
                raise Exception
        else:
            QUICK_CONF[x] = y


def convert_quickpay(k, v):
    gid = int(k.split(':')[2])
    print gid, v
    cdatas = {}
    for rid, cs in v.items() :
        rid = int(rid)
        rid = ROOMIDMAP.get(rid, rid)
        for cid, prodalias in cs.items() :
            cid = getIntClientId(cid)
            if cid > 0 :
                data = cdatas.get(cid)
                if data == None :
                    data = {}
                    cdatas[cid] = data
                if QUICK_CONF[prodalias] :
                    data[rid] = QUICK_CONF[prodalias] 
    
    ctmps = {}
    tmps = []
    ts = {}
    for cid, conf in cdatas.items() :
        if conf not in tmps :
            tmps.append(conf)
        ti = 'quick%d' % (tmps.index(conf))
        ctmps[cid] = ti
        ts[ti] = conf


    p = './' + str(gid) + '/table.quickpay'
    if not os.path.isdir(p) :
        os.makedirs(p)
    fp = open(p + '/0.json', 'w')
    fp.write(json.dumps({'templates' : ts}, indent=2, sort_keys=True))
    fp.close()

    for x, y in ctmps.items() :
        fp = open(p + '/' + str(x) + '.json', 'w')
        fp.write(json.dumps({'template' : y}, indent=2, sort_keys=True))
        fp.close()
        
VIP_SPECIAL = {}
def convert_vip_special_right(k, v):
    gid = int(k.split(':')[2])
    print gid, v
    VIP_SPECIAL[gid] = v


def convert_room_smiles(k, v):
    gid = int(k.split(':')[2])
    print gid, v
    datas = {}
    for sm, xlist in v.items() :
        for x in xlist :
            rlist = x['roomlist']
            for rid in rlist :
                rid = ROOMIDMAP.get(rid, rid)
                rdata = datas.get(rid, None)
                if not rdata :
                    rdata = {}
                    datas[rid] = rdata
                assert(sm not in rdata)
                rdata[sm] = {'other_charm': x['other_charm'], 'price': x['price'], 'self_charm': x['self_charm']}
    print datas
    rooms = {}
    ts = {}
    tmps = []
    for rid, conf in datas.items() :
        if not conf in tmps :
            tmps.append(conf)
        i = tmps.index(conf)
        rooms[rid] = 'conf%d' % (i)
        ts['conf%d' % (i)] = conf
    
    alls = {'rooms' : rooms, 'templates' : ts, "vip_special" : VIP_SPECIAL[gid]['smile']}

    p = './' + str(gid) + '/table.smilies'
    if not os.path.isdir(p) :
        os.makedirs(p)
    fp = open(p + '/0.json', 'w')
    fp.write(json.dumps(alls, indent=2, sort_keys=True))
    fp.close()
    
    
    
def walkdatas(datas , key, fun):
    for k, v, in datas.items() :
        if k.find(key) >= 0 :
            fun(k, v)
        

if __name__ == '__main__':
    
    fp = open('configure.json', 'r')
    allcmds = json.load(fp)
    fp.close()
    alldatas = {}
    for x in allcmds :
        alldatas[x[1]] = x[2]

#     walkdatas(alldatas, ':hall.more.games.conf', convert_more_games)
#     walkdatas(alldatas, ':clientid.moregame.map', convert_more_games_clientid)
#     walkdatas(alldatas, ':global:rooms', convert_rooms)

#     walkdatas(alldatas, ':table.quickpay.item.conf', convert_quickpay_conf)
#     walkdatas(alldatas, ':table.quickpay.conf', convert_quickpay)

    walkdatas(alldatas, ':vip_special_right', convert_vip_special_right)
    walkdatas(alldatas, ':room.smilies.cost', convert_room_smiles)

    # printClientIdNotFound()

