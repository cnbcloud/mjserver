# coding=UTF-8
'''
Created on 2015年6月26日

@author: zqh
'''
import json
import os, re
from game.convert.clientid import CLIENDIDS

def getGameIdFromHallClientId(clientId):
    try:
        gid = re.match('^.*-hall(\\d+)\\..*$', clientId).group(1)
        return int(gid)
    except:
        return 0

def add_global_item(k, v):
    if k == 'hall.more.games.conf' :
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
        # print datas
        print '==========='
        return
    print k
    
    datas = {}
    if k == 'clientid.moregame.map' :
        for x, y in v.items() :
            for cid in y :
                icid = CLIENDIDS.get(cid, -1)
                if icid <= 0 :
                    print x, cid, icid
                else:
                    gid = getGameIdFromHallClientId(cid)
                    if gid not in datas :
                        datas[gid] = {}
                    datas[gid][icid] = x
        print json.dumps(datas, indent=2, sort_keys=True)
        for gid, ids in datas.items() :
            p = './' + str(gid) + '/more.games'
            if not os.path.isdir(p) :
                os.makedirs(p)
            for icid, t in ids.items() :
                datas = json.dumps({'template' : t}, indent=2, sort_keys=True)
                f = open(p + '/' + str(icid) + '.json', 'w')
                f.write(datas)
                f.close()
                print p + '/0.json', datas

        pass
    
execfile('./game_plugins.py')




if __name__ == '__main__':
    pass
