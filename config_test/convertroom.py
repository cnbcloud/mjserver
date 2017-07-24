# -*- coding: utf-8 -*-

import os
import json
import sys


def convertByMod(rf):
    pdir = os.path.dirname(rf)
    datas = readJsonFile(rf)
    for k, v in datas.items():
        if len(v) == 4:
            return

    room0 = {}
    for k, v in datas.items():
        room0[k] = {
            "controlServerCount": v['controlServerCount'],
            "controlTableCount": v['controlTableCount'],
            "gameServerCount": v['gameServerCount'],
            "gameTableCount": v['gameTableCount']
        }
        del v['controlServerCount']
        del v['controlTableCount']
        del v['gameServerCount']
        del v['gameTableCount']
        rfx = pdir + '/' + str(k) + '.json'
        writeJsonFile(rfx, v)
    writeJsonFile(rf, room0)


def convertByGameid(gameid):
    try:
        int(gameid)
    except:
        return
    rf = './game/' + str(gameid) + '/room/0.json'
    if os.path.isfile(rf):
        convertByMod(rf)


def main():
    gameids = os.listdir('./game')
    for gameid in gameids:
        convertByGameid(gameid)


def readJsonFile(fpath):
    fp = None
    try:
        fp = open(fpath, 'r')
        datas = json.load(fp)
        fp.close()
        return datas
    finally:
        try:
            fp.close()
        except:
            pass


def writeJsonFile(fpath, jsondata):
    jsondata = json.dumps(jsondata, indent=2, separators=(', ', ' : '), sort_keys=True, ensure_ascii=False)
    jsondata = jsondata.encode('utf-8')
    lines = jsondata.split('\n')
    for x in xrange(len(lines)):
        lines[x] = lines[x].rstrip()
    jsondata = '\n'.join(lines)
    rfile = None
    try:
        rfile = open(fpath, 'wb+')
        rfile.write(jsondata)
        rfile.close()
    except:
        print repr(jsondata)
        raise
    finally:
        try:
            rfile.close()
        except:
            pass

if __name__ == '__main__':
    main()
