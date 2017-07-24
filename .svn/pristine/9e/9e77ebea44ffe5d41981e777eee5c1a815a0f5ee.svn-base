# coding=UTF-8
'''
Created on 2015年6月26日

@author: zqh
'''
import json, gdss
import os, re
from clientid import *
import sys

clientIdMap = gdss.syncDataFromGdss('getClientIdDict')

inctmps = {}
inctmps2 = {}
incclis = {}
fulltmps = {}
fulltmps2 = {}
fullclis = {}
ii = 0

def add_game_item_old(gid, k, datas):
    global ii
    if k.find('inc') > 0 :
        tmps = inctmps
        tmps2 = inctmps2
        clis = incclis 
    elif k.find('full') > 0 :
        tmps = fulltmps
        tmps2 = fulltmps2
        clis = fullclis 

    ds = {}
    for c, v in datas.items() :
        ci = clientIdMap[c]
        tv = json.dumps(v)
        if tv in tmps :
            tk = tmps[tv]
        else:
            ii += 1
            tk = 'template' + str(ii)
            tmps[tv] = tk
            
        ds[ci] = tk
        clis[ci] = tk
        tmps2[tk] = v
        print tk, v
        print ci, tk
    pass


def writeout(name, tmps,clis):
    f = open('./../game/9999/' + name + '/0.json', 'w')
    f.write(json.dumps({'templates' : tmps}, indent=2, ensure_ascii=False))
    f.close()
    for k, v in clis.items() :
        f = open('./../game/9999/' + name + '/'+str(k)+'.json', 'w')
        f.write(json.dumps({'template' : v}, indent=2, ensure_ascii=False))
        f.close()
        
    
# -*- coding=utf-8 -*-

'''
INC update id : clients.inc.upgrade.map
FULL update id: clients.full.upgrade.map
DIFF update id: clients.diff.upgrade.map
'''
# 增量更新
add_game_item_old(9999, 'clients.inc.upgrade.map', {                                                                                                                                                       
  "Android_3.33_360.360.0-hall6.360.laizi360": [
    {
      "force": "0",
      "des": "1、减少耗电量\n2、加快游戏启动速度\n3、解决部分玩家不能比赛的问题\n\n更新文件大小: 162K",
      "path": "http://ddz.dl.tuyoo.com/update/update_package_v3.zip",
      "md5": "ZZZZZZZZZZZZZZZZZZZZZZZZZZ",
      "id": 1,
      "size": "169KB",
      "autoDownloadCondition": 7,
    }
  ],
  "Android_3.33_360.360.0-hall6.360.tu360": [
    {
      "force": "0",
      "des": "1、减少耗电量\n2、加快游戏启动速度\n3、解决部分玩家不能比赛的问题\n\n更新文件大小: 162K",
      "path": "http://ddz.dl.tuyoo.com/update/update_package_v3.zip",
      "md5": "ZZZZZZZZZZZZZZZZZZZZZZZZZZ",
      "id": 1,
      "size": "169KB",
      "autoDownloadCondition": 7,
    }
  ],
  "IOS_3.71_tyGuest,weixin.appStore.0-hall6.tuyoo.huanle": [
    {
      "force": "1",
      "des": "提高游戏流畅性;\n降低网络流量消耗!",
      "path": "http://ddz.dl.tuyoo.com/cdn37/hall/update/hall_update_ios_3.71_alpha_14.zip",
      "md5": "40b1eb308b4fc4b1c10c19946996738a",
      "id": 1,
      "size": "998KB",
      "autoDownloadCondition": 7,
    }
  ],
  "Android_3.72_360.360,yisdkpay.0-hall6.360.day": [
    {
      "force": "1",
      "des": "修复部分游戏不能正常进入的问题",
      "path": "http://ddz.dl.tuyoo.com/cdn37/hall/update/hall_update_android_3.72_alpha_03.zip",
      "md5": "9f6c1c9f74c7cb96f82af0d8829f3b29",
      "id": 1,
      "size": "928KB",
      "autoDownloadCondition": 4,
    }
  ],
  "Android_3.372_360.360,weakChinaMobile,woStore,aigame,YDJD.0-hall6.360.dj": [
    {
      "force": "1",
      "des": "新版发布，更稳定更流畅，超多福利等你来！\n实物大奖赛每周开启；（冰箱、电视、电脑）\n金币带入功能，不再担心一次输光；",
      "path": "http://update.dl.tuyoo.com/cdn37/hall/update/boot_update_4.3.711.360.dj.1599_6.zip",
      "md5": "0f615de7adf1cd995bb0d974e6892a3d",
      "id": 1,
      "size": "90KB",
      "autoDownloadCondition": 7,
    }
  ]
})

# 全量更新
# http://125.39.218.101/open/v3/getUpdateInfo2?gameId=9999&clientId=Android_3.50_360.360.0-hall6.360.day&hallVersion=6&updateVersion=0&nicaiCode=863567814
# autoDownloadCondition 自动下载条件
# updateAt 更新时游戏在哪个界面
#   background - 更新时在后台，点击确定后，开始下载APK，同时游戏进入下一个场景
#   其他值，停留在更新界面下载
# 下载完成后开始APK安装
# alphaVersion 没有该设置则支持所有额包
#   有则支持此版本号的包
# v3.501版本全量非强制非自动提示更新，上线前合并代码需确认
add_game_item_old(9999, 'clients.full.upgrade.map', {
  # 2015.10.08修改 开始
  "Android_3.501_360.360,weakChinaMobile,woStore,aigame,YDJD.0-hall6.360.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.71.360.dj.apk",
      "md5": "80ded1707a60451c568e78853e437f81",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.5010_360.360,weakChinaMobile,woStore,aigame,YDJD.0-hall6.360.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.71.360.dj.apk",
      "md5": "80ded1707a60451c568e78853e437f81",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.503_360.360,weakChinaMobile,woStore,aigame,YDJD.0-hall6.360.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.71.360.dj.apk",
      "md5": "80ded1707a60451c568e78853e437f81",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.5030_360.360,weakChinaMobile,woStore,aigame,YDJD.0-hall6.360.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.71.360.dj.apk",
      "md5": "80ded1707a60451c568e78853e437f81",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.5031_360.360,weakChinaMobile,woStore,aigame,YDJD.0-hall6.360.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.71.360.dj.apk",
      "md5": "80ded1707a60451c568e78853e437f81",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.501_360.360.0-hall6.360.fk": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.701.360.fk.apk",
      "md5": "f283a7a2f54197b98506ee2114577f0a",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.502_360.360.0-hall6.360.fk": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.701.360.fk.apk",
      "md5": "f283a7a2f54197b98506ee2114577f0a",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.60_360.360.0-hall6.360.fk": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.701.360.fk.apk",
      "md5": "f283a7a2f54197b98506ee2114577f0a",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.501_360.360.0-hall6.360.rich": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.701.360.rich.apk",
      "md5": "cd22d12fb91a294287a257a1945f6c0e",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.502_360.360.0-hall6.360.rich": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.701.360.rich.apk",
      "md5": "cd22d12fb91a294287a257a1945f6c0e",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.503_360.360.0-hall6.360.rich": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.701.360.rich.apk",
      "md5": "cd22d12fb91a294287a257a1945f6c0e",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.5030_360.360.0-hall6.360.rich": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.701.360.rich.apk",
      "md5": "cd22d12fb91a294287a257a1945f6c0e",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.501_360.360.0-hall6.360.kuaile": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.701.360.kuale.apk",
      "md5": "dc02a0caeac11f56b3ab37ae78920194",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.502_360.360.0-hall6.360.kuaile": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.701.360.kuale.apk",
      "md5": "dc02a0caeac11f56b3ab37ae78920194",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.503_360.360.0-hall6.360.kuaile": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.701.360.kuale.apk",
      "md5": "dc02a0caeac11f56b3ab37ae78920194",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.5030_360.360.0-hall6.360.kuaile": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.701.360.kuale.apk",
      "md5": "dc02a0caeac11f56b3ab37ae78920194",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.501_360.360,weakChinaMobile.0-hall6.360.laizi": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.71.360.laizi.apk",
      "md5": "17e369ae59b7895aec41f26d213834d0",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.502_360.360,weakChinaMobile.0-hall6.360.laizi": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.71.360.laizi.apk",
      "md5": "17e369ae59b7895aec41f26d213834d0",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.503_360.360,weakChinaMobile.0-hall6.360.laizi": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.71.360.laizi.apk",
      "md5": "17e369ae59b7895aec41f26d213834d0",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.5030_360.360,weakChinaMobile,woStore.0-hall6.360.laizi": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.71.360.laizi.apk",
      "md5": "17e369ae59b7895aec41f26d213834d0",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.50_360.360.0-hall6.360.day": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.71.360.day.apk",
      "md5": "02668ae5c0020d97eb07c7c97a315ac0",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.502_360.360.0-hall6.360.day": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.71.360.day.apk",
      "md5": "02668ae5c0020d97eb07c7c97a315ac0",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.503_360.360.0-hall6.360.day": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.71.360.day.apk",
      "md5": "02668ae5c0020d97eb07c7c97a315ac0",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.70_360.360.0-hall6.360.day": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.71.360.day.apk",
      "md5": "02668ae5c0020d97eb07c7c97a315ac0",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.701_360.360,yisdkpay.0-hall6.360.day": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.71.360.day.apk",
      "md5": "02668ae5c0020d97eb07c7c97a315ac0",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.50_360.360.0-hall6.360.win": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.701.360.win.apk",
      "md5": "64a9eb60505576f9267e54c47ed20b9b",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.502_360.360.0-hall6.360.win": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.701.360.win.apk",
      "md5": "64a9eb60505576f9267e54c47ed20b9b",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.503_360.360.0-hall6.360.win": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.701.360.win.apk",
      "md5": "64a9eb60505576f9267e54c47ed20b9b",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.501_360.360.0-hall6.360.people": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.701.360.people.apk",
      "md5": "028de55ec017b59a0d469963e087eb1a",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.502_360.360.0-hall6.360.people": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.701.360.people.apk",
      "md5": "028de55ec017b59a0d469963e087eb1a",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.60_360.360.0-hall6.360.people": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.701.360.people.apk",
      "md5": "028de55ec017b59a0d469963e087eb1a",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.501_tuyoo.duoku,weakChinaMobile,YDJD.0-hall6.91new.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.71.91new.dj.apk",
      "md5": "36be6df662186181d17c02cd0000f96a",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.503_tuyoo.duoku,weakChinaMobile,woStore,aigame,YDJD.0-hall6.91new.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.71.91new.dj.apk",
      "md5": "36be6df662186181d17c02cd0000f96a",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.501_nearme.nearme,weakChinaMobile,woStore,YDJD.0-hall6.oppo.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.71.oppo.dj.apk",
      "md5": "01d8f4d066903f23d669e2beafd25a0f",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.503_nearme.nearme,weakChinaMobile,woStore,aigame,YDJD.0-hall6.oppo.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.71.oppo.dj.apk",
      "md5": "01d8f4d066903f23d669e2beafd25a0f",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.5010_pps.pps,weakChinaMobile,woStore,aigame,YDJD.0-hall6.pps.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.71.pps.dj.apk",
      "md5": "4843ad9d758fd08fe5d31c902995231a",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.503_pps.pps,weakChinaMobile,woStore,aigame,YDJD.0-hall6.pps.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.71.pps.dj.apk",
      "md5": "4843ad9d758fd08fe5d31c902995231a",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.501_tuyoo.weakChinaMobile,YDJD.0-hall6.wifikey.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.71.wifikey.dj.apk",
      "md5": "0dcb10a1770514a5d0315e313bfb414d",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.5010_tuyoo.weakChinaMobile,YDJD.0-hall6.wifikey.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.71.wifikey.dj.apk",
      "md5": "0dcb10a1770514a5d0315e313bfb414d",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.503_wifikey.weakChinaMobile,woStore,aigame,YDJD.0-hall6.wifikey.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.71.wifikey.dj.apk",
      "md5": "0dcb10a1770514a5d0315e313bfb414d",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.5030_wifikey.weakChinaMobile,woStore,aigame,YDJD.0-hall6.wifikey.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.71.wifikey.dj.apk",
      "md5": "0dcb10a1770514a5d0315e313bfb414d",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.501_tuyoo.weakChinaMobile,YDJD.0-hall6.ali.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.71.ali.dj.apk",
      "md5": "73324f4685ce22137bc10e8ef745b384",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.5010_tuyoo.weakChinaMobile,YDJD.0-hall6.ali.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.71.ali.dj.apk",
      "md5": "73324f4685ce22137bc10e8ef745b384",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.503_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.ali.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.71.ali.dj.apk",
      "md5": "73324f4685ce22137bc10e8ef745b384",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.5030_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.ali.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.71.ali.dj.apk",
      "md5": "73324f4685ce22137bc10e8ef745b384",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.501_tuyoo.duoku,weakChinaMobile,YDJD.0-hall6.baidunew.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.71.baodunew.dj.apk",
      "md5": "9c2aa6f1382c66249bf6316690c57207",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.503_tuyoo.duoku,weakChinaMobile,woStore,aigame,YDJD.0-hall6.baidunew.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.71.baodunew.dj.apk",
      "md5": "9c2aa6f1382c66249bf6316690c57207",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.5030_tuyoo.duoku,weakChinaMobile,woStore,aigame,YDJD.0-hall6.baidunew.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.71.baodunew.dj.apk",
      "md5": "9c2aa6f1382c66249bf6316690c57207",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.503_tuyoo.duoku,weakChinaMobile,woStore,aigame,YDJD.0-hall6.bdtiebanew.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.71.bdtieba.dj.apk",
      "md5": "050db34d1f20bdf7f71a8575d6c008e9",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.501_tuyoo.duoku,weakChinaMobile,YDJD.0-hall6.duokunew.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.71.duokunew.dj.apk",
      "md5": "8d6a02047feabc1f9e2a16e1c457553b",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.503_tuyoo.duoku,weakChinaMobile,woStore,aigame,YDJD.0-hall6.duokunew.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.71.duokunew.dj.apk",
      "md5": "8d6a02047feabc1f9e2a16e1c457553b",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.501_huawei.huawei,weakChinaMobile,woStore,aigame,YDJD.0-hall6.huawei.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.71.huawei.dj.apk",
      "md5": "a3ed3bea80747d8ec14bce2f0339206b",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.503_huawei.huawei,weakChinaMobile,woStore,aigame,YDJD.0-hall6.huawei.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.71.huawei.dj.apk",
      "md5": "a3ed3bea80747d8ec14bce2f0339206b",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.503_huawei.huawei,woStore,aigame,YDJD.0-hall6.huawei.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.71.huawei.dj.apk",
      "md5": "a3ed3bea80747d8ec14bce2f0339206b",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.501_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.jinli.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.71.jinli.dj.apk",
      "md5": "da44681bc046268280a803d97b78f1be",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.5010_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.jinli.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.71.jinli.dj.apk",
      "md5": "da44681bc046268280a803d97b78f1be",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.503_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.jinli.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.71.jinli.dj.apk",
      "md5": "da44681bc046268280a803d97b78f1be",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.5030_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.jinli.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.71.jinli.dj.apk",
      "md5": "da44681bc046268280a803d97b78f1be",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.5031_tuyoo.woStore,aigame,YDJD.0-hall6.jinli.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.71.jinli.dj.apk",
      "md5": "da44681bc046268280a803d97b78f1be",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.501_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.jinligame.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.71.jinligame.dj.apk",
      "md5": "a2cff7a9ad89cd6c3139ea09f59b3f0b",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.503_tuyoo.jinli,weakChinaMobile,woStore,aigame,YDJD.0-hall6.jinligame.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.71.jinligame.dj.apk",
      "md5": "a2cff7a9ad89cd6c3139ea09f59b3f0b",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.503_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.jinligame.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.71.jinligame.dj.apk",
      "md5": "a2cff7a9ad89cd6c3139ea09f59b3f0b",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.501_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.coolpad.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.71.coolpad.dj.apk",
      "md5": "68ba7c51467440a9deb5f02247577aa0",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.503_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.coolpad.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.71.coolpad.dj.apk",
      "md5": "68ba7c51467440a9deb5f02247577aa0",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.5010_tuyoo.weakChinaMobile,YDJD.0-hall6.litianbaoli.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.71.litianbaoli.dj.apk",
      "md5": "3baa26b2ec6e5f5fe88fd2c502cc0270",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.503_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.litianbaoli.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.71.litianbaoli.dj.apk",
      "md5": "3baa26b2ec6e5f5fe88fd2c502cc0270",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.501_tuyoo.lenovo,weakChinaMobile,woStore,aigame,YDJD.0-hall6.lenovo.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.71.lenovo.dj.apk",
      "md5": "94d768e49573ced5e5291ed49d46b329",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.5010_tuyoo.lenovo,weakChinaMobile,woStore,aigame,YDJD.0-hall6.lenovo.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.71.lenovo.dj.apk",
      "md5": "94d768e49573ced5e5291ed49d46b329",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.503_tuyoo.lenovo,weakChinaMobile,woStore,aigame,YDJD.0-hall6.lenovo.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.71.lenovo.dj.apk",
      "md5": "94d768e49573ced5e5291ed49d46b329",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.501_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.sanxing.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.71.sanxin.dj.apk",
      "md5": "78eba626f9d55220d7202d4a3d9bc25f",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.503_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.sanxing.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.71.sanxin.dj.apk",
      "md5": "78eba626f9d55220d7202d4a3d9bc25f",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.501_tuyoo.weakChinaMobile,YDJD.0-hall6.sougou.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.71.sougou.dj.apk",
      "md5": "724397b8aee7ee4473e58daccc15fcc9",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.5010_tuyoo.weakChinaMobile,YDJD.0-hall6.sougou.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.71.sougou.dj.apk",
      "md5": "724397b8aee7ee4473e58daccc15fcc9",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.503_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.sougou.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.71.sougou.dj.apk",
      "md5": "724397b8aee7ee4473e58daccc15fcc9",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.501_tuyoo.weakChinaMobile,YDJD.0-hall6.tianyu.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.71.tianyu.dj.apk",
      "md5": "995f196e0143e440843880c2588ab6ac",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.5010_tuyoo.weakChinaMobile,YDJD.0-hall6.tianyu.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.71.tianyu.dj.apk",
      "md5": "995f196e0143e440843880c2588ab6ac",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.503_tuyoo.weakChinaMobile,aigame,YDJD.0-hall6.tianyu.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.71.tianyu.dj.apk",
      "md5": "995f196e0143e440843880c2588ab6ac",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.501_tuyoo.weakChinaMobile,YDJD.0-hall6.wandou.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.71.wandou.dj.apk",
      "md5": "b1ab578b4250be4e52bd222358aad5e6",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.5010_tuyoo.weakChinaMobile,YDJD.0-hall6.wandou.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.71.wandou.dj.apk",
      "md5": "b1ab578b4250be4e52bd222358aad5e6",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.503_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.wandou.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.71.wandou.dj.apk",
      "md5": "b1ab578b4250be4e52bd222358aad5e6",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.501_mi.mi,weakChinaMobile,woStore,aigame,YDJD.0-hall6.mi.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.71.mi.dj.apk",
      "md5": "635e689fe92093e5a2e101e1e1e5add0",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.5010_mi.mi,weakChinaMobile,woStore,aigame,YDJD.0-hall6.mi.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.71.mi.dj.apk",
      "md5": "635e689fe92093e5a2e101e1e1e5add0",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.503_mi.mi,weakChinaMobile,woStore,aigame,YDJD.0-hall6.mi.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.71.mi.dj.apk",
      "md5": "635e689fe92093e5a2e101e1e1e5add0",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.501_tuyoo.weakChinaMobile,YDJD.0-hall6.qq.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.71.qq.dj.apk",
      "md5": "c5c7a0b746d76f9559e2fb1a1581e97e",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.5010_tuyoo.weakChinaMobile,YDJD.0-hall6.qq.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.71.qq.dj.apk",
      "md5": "c5c7a0b746d76f9559e2fb1a1581e97e",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.503_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.qq.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.71.qq.dj.apk",
      "md5": "c5c7a0b746d76f9559e2fb1a1581e97e",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.5030_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.qq.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.71.qq.dj.apk",
      "md5": "c5c7a0b746d76f9559e2fb1a1581e97e",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.5031_tuyoo.woStore,aigame,YDJD.0-hall6.qq.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.71.qq.dj.apk",
      "md5": "c5c7a0b746d76f9559e2fb1a1581e97e",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.5031_tuyoo.woStore,aigame,YDJD.0-hall6.qqexplorer.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.71.qqexplorer.dj.apk",
      "md5": "0b817d3b32a0812f4343446e85d766dc",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.5031_tuyoo.woStore,aigame,YDJD.0-hall6.qqcustomizedas.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.71.qqdas.dj.apk",
      "md5": "3b070dd0ab6af03d76b98fe8dc499e5f",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.5031_tuyoo.woStore,aigame,YDJD.0-hall6.qqic02.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.71.qqic02.dj.apk",
      "md5": "44b7502232fdef51fdb48b4ce5a16841",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ], "Android_3.5031_tuyoo.woStore,aigame,YDJD.0-hall6.qqgc.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.71.qqtmsgc.dj.apk",
      "md5": "74e65e6b7d09afb3036f7bde0c32855b",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  # 2015.10.08修改 结束
  # 2015.10.21的配置 开始
  "Android_3.5031_360.360,weakChinaMobile,woStore,aigame,YDJD.0-hall6.360.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/4.3.711.360.dj.1599.apk",
      "md5": "dec304c8ed3784dff5235171ee3c6c5c",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.503_360.360,weakChinaMobile,woStore,aigame,YDJD.0-hall6.360.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/4.3.711.360.dj.1599.apk",
      "md5": "dec304c8ed3784dff5235171ee3c6c5c",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.5010_360.360,weakChinaMobile,woStore,aigame,YDJD.0-hall6.360.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/4.3.711.360.dj.1599.apk",
      "md5": "dec304c8ed3784dff5235171ee3c6c5c",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.501_360.360,weakChinaMobile,woStore,aigame,YDJD.0-hall6.360.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/4.3.711.360.dj.1599.apk",
      "md5": "dec304c8ed3784dff5235171ee3c6c5c",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.5030_360.360,weakChinaMobile,woStore,aigame,YDJD.0-hall6.360.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/4.3.711.360.dj.1599.apk",
      "md5": "dec304c8ed3784dff5235171ee3c6c5c",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.5030_360.360,weakChinaMobile,woStore.0-hall6.360.laizi": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/1.3.711.360.laizi.1558.apk",
      "md5": "33fd7d36846a37e0b45dc85b9a12b10f",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.503_360.360,weakChinaMobile.0-hall6.360.laizi": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/1.3.711.360.laizi.1558.apk",
      "md5": "33fd7d36846a37e0b45dc85b9a12b10f",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.502_360.360,weakChinaMobile.0-hall6.360.laizi": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/1.3.711.360.laizi.1558.apk",
      "md5": "33fd7d36846a37e0b45dc85b9a12b10f",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.501_360.360,weakChinaMobile.0-hall6.360.laizi": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/1.3.711.360.laizi.1558.apk",
      "md5": "33fd7d36846a37e0b45dc85b9a12b10f",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.5030_360.360,weakChinaMobile,woStore,aigame,YDJD.0-hall6.360.tu": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/1.3.71.360.tu.1465.apk",
      "md5": "53a75feac67ba3c9d4f0c7f41fc4051e",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.503_360.360,weakChinaMobile,woStore,aigame,YDJD.0-hall6.360.tu": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/1.3.71.360.tu.1465.apk",
      "md5": "53a75feac67ba3c9d4f0c7f41fc4051e",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.501_360.360,weakChinaMobile,woStore,aigame,YDJD.0-hall6.360.tu": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/1.3.71.360.tu.1465.apk",
      "md5": "53a75feac67ba3c9d4f0c7f41fc4051e",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.5030_360.360,weakChinaMobile,woStore,aigame,YDJD.0-hall6.360.happy": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/1.3.71.360.happy.1494.apk",
      "md5": "c1157595f083cb141d260c5274477e46",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.503_360.360,weakChinaMobile,woStore,aigame,YDJD.0-hall6.360.happy": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/1.3.71.360.happy.1494.apk",
      "md5": "c1157595f083cb141d260c5274477e46",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.501_360.360,weakChinaMobile,woStore,aigame,YDJD.0-hall6.360.happy": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/1.3.71.360.happy.1494.apk",
      "md5": "c1157595f083cb141d260c5274477e46",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.503_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.4399.happy": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/1.3.71.360.happy.1494.apk",
      "md5": "c1157595f083cb141d260c5274477e46",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.501_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.4399.happy": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/1.3.71.360.happy.1494.apk",
      "md5": "c1157595f083cb141d260c5274477e46",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.503_tuyoo.duoku,weakChinaMobile,woStore,aigame,YDJD.0-hall6.91new.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/10.3.711.91new.dj.1640.apk",
      "md5": "002f91c3b15f5ed0a221fb9f28a55bba",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.501_tuyoo.duoku,weakChinaMobile,YDJD.0-hall6.91new.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/10.3.711.91new.dj.1640.apk",
      "md5": "002f91c3b15f5ed0a221fb9f28a55bba",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.503_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.HTC.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/20.3.711.htc.dj.1626.apk",
      "md5": "35126de4adf44878f6cc351a81f9a82b",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.501_nearme.nearme,weakChinaMobile,woStore,YDJD.0-hall6.oppo.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/8.3.711.oppo.dj.1639.apk",
      "md5": "e216280950cb19b77fe007f73ab14338",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.503_nearme.nearme,weakChinaMobile,woStore,aigame,YDJD.0-hall6.oppo.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/8.3.711.oppo.dj.1639.apk",
      "md5": "e216280950cb19b77fe007f73ab14338",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.503_nearme.nearme,weakChinaMobile,woStore,aigame,YDJD.0-hall6.oppo.tu": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/4.3.71.oppo.tu.1464.apk",
      "md5": "17b83eae5cbca47db705f70b20836c85",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.503_pps.pps,weakChinaMobile,woStore,aigame,YDJD.0-hall6.pps.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/9.3.711.pps.dj.1634.apk",
      "md5": "091cbd1e74ae7363966a181a2d66646e",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.5010_pps.pps,weakChinaMobile,woStore,aigame,YDJD.0-hall6.pps.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/9.3.711.pps.dj.1634.apk",
      "md5": "091cbd1e74ae7363966a181a2d66646e",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.503_tuyoo.ppzhushou,woStore,aigame,YDJD.0-hall6.ppzhushou.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/16.3.711.ppzhushou.dj.1633.apk",
      "md5": "84e0b1e5a10e06dd474c402e6015ffae",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.5030_wifikey.weakChinaMobile,woStore,aigame,YDJD.0-hall6.wifikey.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/1.3.711.wifikey.dj.1608.apk",
      "md5": "b42fdec354ec48ac2dc2f36d6060e012",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.503_wifikey.weakChinaMobile,woStore,aigame,YDJD.0-hall6.wifikey.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/1.3.711.wifikey.dj.1608.apk",
      "md5": "b42fdec354ec48ac2dc2f36d6060e012",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.5010_tuyoo.weakChinaMobile,YDJD.0-hall6.wifikey.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/1.3.711.wifikey.dj.1608.apk",
      "md5": "b42fdec354ec48ac2dc2f36d6060e012",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.501_tuyoo.weakChinaMobile,YDJD.0-hall6.wifikey.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/1.3.711.wifikey.dj.1608.apk",
      "md5": "b42fdec354ec48ac2dc2f36d6060e012",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.503_wifikey.weakChinaMobile,woStore,aigame,YDJD.0-hall6.wifikey.happy": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/16.3.71.wifikey.happy.1521.apk",
      "md5": "dc18513ed75a6eefca8105a462225007",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.501_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.wifikey.happy": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/16.3.71.wifikey.happy.1521.apk",
      "md5": "dc18513ed75a6eefca8105a462225007",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.5030_wifikey.weakChinaMobile,woStore,aigame,YDJD.0-hall6.wifikey.happy": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/16.3.71.wifikey.happy.1521.apk",
      "md5": "dc18513ed75a6eefca8105a462225007",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.5030_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.ali.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/17.3.711.ali.dj.1600.apk",
      "md5": "5c0acb5ff5917d2c7eee974ce4e32460",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.503_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.ali.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/17.3.711.ali.dj.1600.apk",
      "md5": "5c0acb5ff5917d2c7eee974ce4e32460",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.5010_tuyoo.weakChinaMobile,YDJD.0-hall6.ali.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/17.3.711.ali.dj.1600.apk",
      "md5": "5c0acb5ff5917d2c7eee974ce4e32460",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.501_tuyoo.weakChinaMobile,YDJD.0-hall6.ali.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/17.3.711.ali.dj.1600.apk",
      "md5": "5c0acb5ff5917d2c7eee974ce4e32460",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.503_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.ali.tu": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/6.3.71.ali.tu.1466.apk",
      "md5": "9ed72d020625659663d7da72d9f34ea9",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.5030_tuyoo.duoku,weakChinaMobile,woStore,aigame,YDJD.0-hall6.baidunew.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/11.3.711.baidunew.dj.1641.apk",
      "md5": "a494297d1f0490a74af2c51a14d125ec",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.503_tuyoo.duoku,weakChinaMobile,woStore,aigame,YDJD.0-hall6.baidunew.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/11.3.711.baidunew.dj.1641.apk",
      "md5": "a494297d1f0490a74af2c51a14d125ec",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.501_tuyoo.duoku,weakChinaMobile,YDJD.0-hall6.baidunew.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/11.3.711.baidunew.dj.1641.apk",
      "md5": "a494297d1f0490a74af2c51a14d125ec",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.503_tuyoo.duoku,weakChinaMobile,woStore,aigame,YDJD.0-hall6.bdtiebanew.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/12.3.711.bdtiebanew.dj.1642.apk",
      "md5": "244ca3bb9577ce1901088df301cefc97",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.501_tuyoo.duoku,weakChinaMobile,YDJD.0-hall6.bdtiebanew.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/12.3.711.bdtiebanew.dj.1642.apk",
      "md5": "244ca3bb9577ce1901088df301cefc97",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.503_tuyoo.duoku,weakChinaMobile,woStore,aigame,YDJD.0-hall6.duokunew.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/13.3.711.duokunew.dj.1643.apk",
      "md5": "8890d1ddaf4c606260dd7a27a6f2d92d",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.501_tuyoo.duoku,weakChinaMobile,YDJD.0-hall6.duokunew.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/13.3.711.duokunew.dj.1643.apk",
      "md5": "8890d1ddaf4c606260dd7a27a6f2d92d",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.501_tuyoo.weakChinaMobile,YDJD.0-hall6.duokunew.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/13.3.711.duokunew.dj.1643.apk",
      "md5": "8890d1ddaf4c606260dd7a27a6f2d92d",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.503_huawei.huawei,weakChinaMobile,woStore,aigame,YDJD.0-hall6.huawei.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/5.3.711.huawei.dj.1597.apk",
      "md5": "3a5da3c9b8947ab32e19d6f2fb871801",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.503_huawei.huawei,woStore,aigame,YDJD.0-hall6.huawei.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/5.3.711.huawei.dj.1597.apk",
      "md5": "3a5da3c9b8947ab32e19d6f2fb871801",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.501_huawei.huawei,weakChinaMobile,woStore,aigame,YDJD.0-hall6.huawei.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/5.3.711.huawei.dj.1597.apk",
      "md5": "3a5da3c9b8947ab32e19d6f2fb871801",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.503_huawei.huawei,woStore,aigame,YDJD.0-hall6.huawei.tu": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/2.3.71.huawei.tu.1458.apk",
      "md5": "4d1d7934ea74bf3174cac84f97ff7099",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.5030_huawei.huawei,weakChinaMobile,woStore,aigame,YDJD.0-hall6.huawei.tu": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/2.3.71.huawei.tu.1458.apk",
      "md5": "4d1d7934ea74bf3174cac84f97ff7099",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.501_huawei.huawei,weakChinaMobile,woStore,aigame,YDJD.0-hall6.huawei.tu": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/2.3.71.huawei.tu.1458.apk",
      "md5": "4d1d7934ea74bf3174cac84f97ff7099",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.503_huawei.huawei,weakChinaMobile,woStore,aigame,YDJD.0-hall6.huawei.happy": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/2.3.71.huawei.happy.1586.apk",
      "md5": "8a20547455fb3bdfd566710ff85b6f9c",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.503_huawei.huawei,woStore,aigame,YDJD.0-hall6.huawei.happy": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/2.3.71.huawei.happy.1586.apk",
      "md5": "8a20547455fb3bdfd566710ff85b6f9c",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.503_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.jinli.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/22.3.711.jinli.dj.1602.apk",
      "md5": "f554bfe941378a39f4bedd5b1a7e0463",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.5031_tuyoo.woStore,aigame,YDJD.0-hall6.jinli.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/22.3.711.jinli.dj.1602.apk",
      "md5": "f554bfe941378a39f4bedd5b1a7e0463",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.5030_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.jinli.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/22.3.711.jinli.dj.1602.apk",
      "md5": "f554bfe941378a39f4bedd5b1a7e0463",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.5010_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.jinli.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/22.3.711.jinli.dj.1602.apk",
      "md5": "f554bfe941378a39f4bedd5b1a7e0463",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.501_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.jinli.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/22.3.711.jinli.dj.1602.apk",
      "md5": "f554bfe941378a39f4bedd5b1a7e0463",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.503_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.jinli.tu": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/8.3.71.jinli.tu.1467.apk",
      "md5": "ad751c5e10a41e105fee4b2c595776c8",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.5031_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.jinli.tu": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/8.3.71.jinli.tu.1467.apk",
      "md5": "ad751c5e10a41e105fee4b2c595776c8",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.501_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.jinli.tu": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/8.3.71.jinli.tu.1467.apk",
      "md5": "ad751c5e10a41e105fee4b2c595776c8",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.503_tuyoo.jinli,weakChinaMobile,woStore,aigame,YDJD.0-hall6.jinligame.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/14.3.711.jinligame.dj.1603.apk",
      "md5": "feae8fdf6ebccde2ee1d56191445ccc2",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.503_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.jinligame.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/14.3.711.jinligame.dj.1603.apk",
      "md5": "feae8fdf6ebccde2ee1d56191445ccc2",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.501_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.jinligame.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/14.3.711.jinligame.dj.1603.apk",
      "md5": "feae8fdf6ebccde2ee1d56191445ccc2",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.501_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.kubi.tu": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/23.3.711.kubi.dj.1604.apk",
      "md5": "95b4c80a6ec3c24d5680508c7d68de9e",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.5031_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.kubi.tu": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/23.3.711.kubi.dj.1604.apk",
      "md5": "95b4c80a6ec3c24d5680508c7d68de9e",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.503_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.coolpad.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/18.3.711.coolpad.dj.1601.apk",
      "md5": "6ffe652200cb67b9dc8950fd50d2e0bf",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.501_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.coolpad.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/18.3.711.coolpad.dj.1601.apk",
      "md5": "6ffe652200cb67b9dc8950fd50d2e0bf",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.503_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.coolpad.tu": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/7.3.71.coolpad.tu.1457.apk",
      "md5": "6a5fb2a640ab52b7c718a83c31df9daf",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.501_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.coolpad.tu": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/7.3.71.coolpad.tu.1457.apk",
      "md5": "6a5fb2a640ab52b7c718a83c31df9daf",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.503_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.kunda.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/24.3.711.kunda.dj.1627.apk",
      "md5": "a4edd956f18137d38d5d64372bc12a89",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.5010_tuyoo.weakChinaMobile,YDJD.0-hall6.kunda.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/24.3.711.kunda.dj.1627.apk",
      "md5": "a4edd956f18137d38d5d64372bc12a89",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.501_tuyoo.weakChinaMobile,YDJD.0-hall6.kunda.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/24.3.711.kunda.dj.1627.apk",
      "md5": "a4edd956f18137d38d5d64372bc12a89",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.503_tuyoo.woStore,aigame,YDJD.0-hall6.leshiphone.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/25.3.711.leshiphone.dj.1636.apk",
      "md5": "58b75a78fd6b7b5b22359746484111e0",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.501_tuyoo.woStore,aigame,YDJD.0-hall6.leshiphone.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/25.3.711.leshiphone.dj.1636.apk",
      "md5": "58b75a78fd6b7b5b22359746484111e0",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.503_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.litianbaoli.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/26.3.711.litianbaoli.dj.1628.apk",
      "md5": "3df86e0ac66b214972d225c4db2952f9",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.5010_tuyoo.weakChinaMobile,YDJD.0-hall6.litianbaoli.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/26.3.711.litianbaoli.dj.1628.apk",
      "md5": "3df86e0ac66b214972d225c4db2952f9",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.503_tuyoo.lenovo,weakChinaMobile,woStore,aigame,YDJD.0-hall6.lenovo.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/15.3.711.lenovo.dj.1605.apk",
      "md5": "1b3ca8e21f031c06beed0789973d2a4d",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.5010_tuyoo.lenovo,weakChinaMobile,woStore,aigame,YDJD.0-hall6.lenovo.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/15.3.711.lenovo.dj.1605.apk",
      "md5": "1b3ca8e21f031c06beed0789973d2a4d",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.501_tuyoo.lenovo,weakChinaMobile,woStore,aigame,YDJD.0-hall6.lenovo.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/15.3.711.lenovo.dj.1605.apk",
      "md5": "1b3ca8e21f031c06beed0789973d2a4d",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.503_tuyoo.lenovo,weakChinaMobile,woStore,aigame,YDJD.0-hall6.lenovo.tu": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/5.3.71.lenovo.tu.1463.apk",
      "md5": "f8fb0f83a8125b0162214d581feb958d",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.501_tuyoo.lenovo,weakChinaMobile,woStore,aigame,YDJD.0-hall6.lenovo.tu": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/5.3.71.lenovo.tu.1463.apk",
      "md5": "f8fb0f83a8125b0162214d581feb958d",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.503_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.meitu.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/27.3.711.meitu.dj.1631.apk",
      "md5": "99a45bf1bc795fda6847aa5c0dbd57a9",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.503_meizu.meizu,weakChinaMobile,woStore,aigame,YDJD.0-hall6.meizu.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/6.3.711.meizu.dj.1609.apk",
      "md5": "5c185be627a59b4bf0ffdbea3b488e7f",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.501_meizu.meizu,weakChinaMobile,woStore,aigame,YDJD.0-hall6.meizu.happy": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.3.71.meizu.happy.1462.apk",
      "md5": "0c2c56d4b00f3e5f8c81c6fc2e903b7d",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.503_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.qingmeng.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/28.3.711.qingmeng.dj.1629.apk",
      "md5": "632e4da91b46dc73a9cf0329581c3abc",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.503_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.sanxing.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/43.3.711.sanxing.dj.1630.apk",
      "md5": "3bbab26e98f3e500d129aaae2a68c12c",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.501_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.sanxing.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/43.3.711.sanxing.dj.1630.apk",
      "md5": "3bbab26e98f3e500d129aaae2a68c12c",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.503_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.sanxing.tu": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/10.3.71.sanxing.tu.1481.apk",
      "md5": "f010dc6264c919c36405bcbda4389272",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.503_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.sougou.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/44.3.711.sougou.dj.1606.apk",
      "md5": "edb59c8abb79bf6526f297e5e011087d",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.5010_tuyoo.weakChinaMobile,YDJD.0-hall6.sougou.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/44.3.711.sougou.dj.1606.apk",
      "md5": "edb59c8abb79bf6526f297e5e011087d",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.501_tuyoo.weakChinaMobile,YDJD.0-hall6.sougou.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/44.3.711.sougou.dj.1606.apk",
      "md5": "edb59c8abb79bf6526f297e5e011087d",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.503_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.sougou.tu": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/12.3.71.sougou.tu.1482.apk",
      "md5": "9e95355a452b284e0c6968d96beef58a",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.501_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.sohuvideo.tu": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/11.3.71.sohuvideo.tu.1452.apk",
      "md5": "458c0a2fb0992e9e8227b78320716c6a",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.503_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.sohuvideo.tu": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/11.3.71.sohuvideo.tu.1452.apk",
      "md5": "458c0a2fb0992e9e8227b78320716c6a",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.503_tuyoo.weakChinaMobile,aigame,YDJD.0-hall6.tianyu.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/46.3.711.tianyu.dj.1637.apk",
      "md5": "798cbab97f385937f1d783035bde34c7",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.5010_tuyoo.weakChinaMobile,YDJD.0-hall6.tianyu.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/46.3.711.tianyu.dj.1637.apk",
      "md5": "798cbab97f385937f1d783035bde34c7",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.501_tuyoo.weakChinaMobile,YDJD.0-hall6.tianyu.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/46.3.711.tianyu.dj.1637.apk",
      "md5": "798cbab97f385937f1d783035bde34c7",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.503_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.wandou.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/47.3.711.wandou.dj.1607.apk",
      "md5": "49efd2eeff2e235fa93f8d9f9c10b113",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.5010_tuyoo.weakChinaMobile,YDJD.0-hall6.wandou.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/47.3.711.wandou.dj.1607.apk",
      "md5": "49efd2eeff2e235fa93f8d9f9c10b113",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.501_tuyoo.weakChinaMobile,YDJD.0-hall6.wandou.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/47.3.711.wandou.dj.1607.apk",
      "md5": "49efd2eeff2e235fa93f8d9f9c10b113",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.503_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.wandou.tu": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/14.3.71.wandou.tu.1484.apk",
      "md5": "ce85d4694333f368877dbacbd02c20ec",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.501_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.wandou.tu": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/14.3.71.wandou.tu.1484.apk",
      "md5": "ce85d4694333f368877dbacbd02c20ec",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.503_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.wandou.happy": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/15.3.71.wandou.happy.1520.apk",
      "md5": "cf920d3a5426d512e26a7178a8eb3746",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.501_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.wandou.happy": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/15.3.71.wandou.happy.1520.apk",
      "md5": "cf920d3a5426d512e26a7178a8eb3746",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.503_mi.mi,weakChinaMobile,woStore,aigame,YDJD.0-hall6.mi.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/7.3.711.mi.dj.1610.apk",
      "md5": "fee12f239461b6aed524aa8d8df87606",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.5010_mi.mi,weakChinaMobile,woStore,aigame,YDJD.0-hall6.mi.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/7.3.711.mi.dj.1610.apk",
      "md5": "fee12f239461b6aed524aa8d8df87606",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.501_mi.mi,weakChinaMobile,woStore,aigame,YDJD.0-hall6.mi.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/7.3.711.mi.dj.1610.apk",
      "md5": "fee12f239461b6aed524aa8d8df87606",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.503_mi.mi,weakChinaMobile,woStore,aigame,YDJD.0-hall6.mi.tu": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.3.71.mi.tu.1485.apk",
      "md5": "463c191d749408c568041147f91f2c86",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.501_mi.mi,weakChinaMobile,woStore,aigame,YDJD.0-hall6.mi.tu": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/3.3.71.mi.tu.1485.apk",
      "md5": "463c191d749408c568041147f91f2c86",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.503_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.qq.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/29.3.711.qq.dj.1617.apk",
      "md5": "95bac29fb0e5477a64f8fe3e91f3615a",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.5030_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.qq.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/29.3.711.qq.dj.1617.apk",
      "md5": "95bac29fb0e5477a64f8fe3e91f3615a",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.5031_tuyoo.woStore,aigame,YDJD.0-hall6.qq.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/29.3.711.qq.dj.1617.apk",
      "md5": "95bac29fb0e5477a64f8fe3e91f3615a",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.5010_tuyoo.weakChinaMobile,YDJD.0-hall6.qq.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/29.3.711.qq.dj.1617.apk",
      "md5": "95bac29fb0e5477a64f8fe3e91f3615a",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.501_tuyoo.weakChinaMobile,YDJD.0-hall6.qq.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/29.3.711.qq.dj.1617.apk",
      "md5": "95bac29fb0e5477a64f8fe3e91f3615a",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.503_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.qq.tu": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/9.3.71.qq.tu.1488.apk",
      "md5": "0e7e58e235b5c1b138c96ead3e15bc10",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.501_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.qq.tu": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/9.3.71.qq.tu.1488.apk",
      "md5": "0e7e58e235b5c1b138c96ead3e15bc10",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.503_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.qq.happy": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/5.3.71.qq.happy.1579.apk",
      "md5": "fb51a5fdfd5ae52665d821ea0aa692ac",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.5030_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.qq.happy": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/5.3.71.qq.happy.1579.apk",
      "md5": "fb51a5fdfd5ae52665d821ea0aa692ac",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.5031_tuyoo.woStore,aigame,YDJD.0-hall6.qq.happy": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/5.3.71.qq.happy.1579.apk",
      "md5": "fb51a5fdfd5ae52665d821ea0aa692ac",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.501_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.qq.happy": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/5.3.71.qq.happy.1579.apk",
      "md5": "fb51a5fdfd5ae52665d821ea0aa692ac",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.5031_tuyoo.woStore,aigame,YDJD.0-hall6.qqexplorer.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/33.3.711.qqexplorer.dj.1621.apk",
      "md5": "8276536ce0730dfc7ec610c7dab632ad",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.5031_tuyoo.woStore,aigame,YDJD.0-hall6.qqexplorer.happy": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/9.3.71.qqexplorer.happy.1573.apk",
      "md5": "124403cfde7c7fbc46bcd8f41018ae5a",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.5031_tuyoo.woStore,aigame,YDJD.0-hall6.qqcustomizedas.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/31.3.711.qqcustomizedas.dj.1619.apk",
      "md5": "eff47137aca2aa193f1bd7adea398b0c",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.5031_tuyoo.woStore,aigame,YDJD.0-hall6.qqcustomizedas.happy": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/7.3.71.qqcustomizedas.happy.1571.apk",
      "md5": "7eaa21c5f8d2bf89cbda9fd162afb0e4",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.5031_tuyoo.woStore,aigame,YDJD.0-hall6.qqic02.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/39.3.711.qqic02.dj.1622.apk",
      "md5": "f76393aa4e359ed60a0d5bb6e26d6e74",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.5031_tuyoo.woStore,aigame,YDJD.0-hall6.qqic02.happy": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/11.3.71.qqic02.happy.1575.apk",
      "md5": "d6e32537d911057bcbb1ac1a94ccc0f6",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.5031_tuyoo.woStore,aigame,YDJD.0-hall6.qqgc.dj": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/38.3.711.qqgc.dj.1620.apk",
      "md5": "eed994c1d00cb8d97c70b4e667ae9303",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.5031_tuyoo.woStore,aigame,YDJD.0-hall6.qqgc.happy": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/10.3.71.qqgc.happy.1574.apk",
      "md5": "d94670aead3762634e5b5bddfb47f913",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.503_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.youyoucun.happy": [
    {
      "force": "0",
      "des": "1、用户体验全面升级\n\n2、全新的酷炫界面\n\n3、欢乐的好友功能\n\n更新文件大小: 26M",
      "path": "http://ddz.dl.tuyoo.com/apk/17.3.71.youyoucun.happy.1522.apk",
      "md5": "c2dca38b59c986b2368d63b9f550b872",
      "id": 2,
      "size": "26900KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  # 2015.10.21的配置 结束
  # 以下是10.08之前的配置
  "Android_3.501_tuyoo.weakChinaMobile,YDJD.0-hall6.tuyoo.dj": [
    {
      "force": "0",
      "des": "1、优化游戏性能及体验\n\n2、修复支付宝支付bug\n\n更新文件大小: 19M",
      "path": "http://ddz.dl.tuyoo.com/apk/501shengji.apk",
      "md5": "2ec74a0a52deb1a8c52adce41b9b94a6",
      "id": 1,
      "size": "19200KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.501_tuyoo.weakChinaMobile,YDJD.0-hall6.kunda.dj": [
    {
      "force": "0",
      "des": "1、优化游戏性能及体验\n\n2、修复支付宝支付bug\n\n更新文件大小: 19M",
      "path": "http://ddz.dl.tuyoo.com/apk/501shengji.apk",
      "md5": "2ec74a0a52deb1a8c52adce41b9b94a6",
      "id": 1,
      "size": "19200KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.501_tuyoo.weakChinaMobile,YDJD.0-hall6.litianbaoli.dj": [
    {
      "force": "0",
      "des": "1、优化游戏性能及体验\n\n2、修复支付宝支付bug\n\n更新文件大小: 19M",
      "path": "http://ddz.dl.tuyoo.com/apk/501shengji.apk",
      "md5": "2ec74a0a52deb1a8c52adce41b9b94a6",
      "id": 1,
      "size": "19200KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.501_tuyoo.woStore,aigame,YDJD.0-hall6.leshiphone.dj": [
    {
      "force": "0",
      "des": "1、优化游戏性能及体验\n\n2、修复支付宝支付bug\n\n更新文件大小: 19M",
      "path": "http://ddz.dl.tuyoo.com/apk/501shengji.apk",
      "md5": "2ec74a0a52deb1a8c52adce41b9b94a6",
      "id": 1,
      "size": "19200KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.501_tuyoo.weakChinaMobile,YDJD.0-hall6.duokunew.dj": [
    {
      "force": "0",
      "des": "1、优化游戏性能及体验\n\n2、修复支付宝支付bug\n\n更新文件大小: 19M",
      "path": "http://ddz.dl.tuyoo.com/apk/501shengji.apk",
      "md5": "2ec74a0a52deb1a8c52adce41b9b94a6",
      "id": 1,
      "size": "19200KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ]
})


# # DIFF更新，MD5为PATCH之后的APK的MD5
# # test case
# # http://125.39.218.101/open/v3/getUpdateInfo2?gameId=9999&clientId=Android_3.502_360.360.0-hall6.360.day&hallVersion=6&updateVersion=0&nicaiCode=863567814
# add_game_item_old(9999, 'clients.diff.upgrade.map', {                                                                                                                                                       
#   "Android_3.502_360.360.0-hall6.360.day": [
#     {
#       "force": "0",
#       "des": "1、测试差分更新\n\n更新文件大小: 0.2M",
#       "path": "http://ddz.dl.tuyoo.com/update/update_package_v3.patch",
#       "md5": "ZZZZZZZZZZZZZZZZZZZZZZZZZZ",
#       "id": 1,
#       "size": "169KB",
#       "autoDownloadCondition": 7,
#       "updateAt": "background",
#     }
#   ]
# })

writeout('upgrade_inc', inctmps2, incclis)
writeout('upgrade_full', fulltmps2, fullclis)

