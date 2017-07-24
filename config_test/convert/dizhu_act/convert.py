# -*- coding=utf-8
'''
Created on 2015年8月6日

@author: zhaojiangang
'''
import json

import gdss


act_conf = {
    'default':{
               'url' : 'activities/83.html',
               'lpic' : 'huodong_3_0_left_20150729.jpg',
               'rpic' : 'huodong_3_0_right_20150604.jpg'
    },
    'default_old':{
                   'url' : 'activities/81.html',
                   'lpic' : 'huodong_3_0_left_20150610_others.jpg',
                   'rpic' : 'huodong_3_0_right_20150604.jpg'
    },
    'byclientids':[
        {
            'url' : 'activities/43.html',
            'lpic' : 'huodong_3_0_left_20150114.jpg',
            'rpic' : 'huodong_3_0_20150204_new.jpg',
            'clientIds':[
                'Android_3.363_360.360.0-hall6.360cp.tu',
                'Android_3.35_360.360.0-hall6.360.laizi360'
            ]
        },
        {
            'directBuy':1,
            'clientIds':[
                'Android_3.37_tuyoo.lenovodj.0-hall6.lianxiang.dj',
                'Android_3.37_tuyoo.lenovodj.0-hall6.lianxiangyouxi.dj',
            ]
        },
        {
            'url' : 'activities/80.html',
            'lpic' : 'huodong_3_0_left_20150729.jpg',
            'rpic' : 'huodong_3_0_right_new.jpg',
            'clientIds':[
                        'IOS_3.502_tuyoo.appStore.0-hall6.tuyoo.huanle',
                        'IOS_3.501_tuyoo.appStore.0-hall6.tuyoo.cherry',
                        'IOS_3.60_360.360.0-hall6.360.day',
                        'IOS_3.50_tuyoo.tuyoo.0-hall6.tuyoo.dj',
            ]
        },
        {
            'url' : 'activities/80.html',
            'lpic' : 'huodong_3_0_left_20150610_others.jpg',
            'rpic' : 'huodong_3_0_right_new.jpg',
            'clientIds':[
                'IOS_3.372_tuyoo.appStore.0-hall6.tuyoo.huanle',
                'IOS_3.37_tuyoo.appStore.0-hall6.appStore.zhafantian',
            ]
        },     
        {
            'url' : 'activities/82.html',
            'lpic' : 'huodong_3_0_left_20150617.jpg',
            'rpic' : 'huodong_3_0_right_new.jpg',
            'clientIds':[
                'IOS_3.371_tuyoo.appStore.0-hall6.appStore.zhafantian',
            ]
        },
        {
            'url' : 'activities/75.html',
            'lpic' : 'huodong_3_0_left_20150527.jpg',
            'rpic' : 'huodong_3_0_right_new.jpg',
            'clientIds':[
                'IOS_3.372_tuyoo.appStore.0-hall6.appStore.zhafantian',
            ]
        },
    ],
    'clientId_close':[
                'Android_3.503_tuyoo.weakChinaMobile,woStore.0-hall6.ali.laizi',
                'Android_3.503_tuyoo.YDJD.0-hall6.360.laizi',
                'Android_3.503_tuyoo.YDJD.0-hall6.huawei.happy',
                'Android_3.503_tuyoo.maopao,weakChinaMobile,woStore,aigame,YDJD.0-hall6.maopaoshichang.dj',
                'Android_3.503_tuyoo.maopao,weakChinaMobile,woStore,aigame,YDJD.0-hall6.maopaoshequ.dj',
                'Android_3.503_tuyoo.maopao,weakChinaMobile,woStore,aigame,YDJD.0-hall6.maopaoyouxi.dj',
                'Android_3.503_tuyoo.maopao,weakChinaMobile,woStore,aigame,YDJD.0-hall6.maopaoliulanqi.dj',
                'Android_3.503_tuyoo.aigame.0-hall6.aigame.dingzhidj',
                'Android_3.503_tuyoo.YDJD.0-hall6.ppzhushou.dj',
                'Android_3.503_tuyoo.weakChinaMobile,woStore.0-hall6.ali.laizi',
                'Android_3.503_tuyoo.tuyoo,weakChinaMobile,woStore,aigame,YDJD.0-hall6.ali.happy',
                'Android_3.503_tuyoo.weakChinaMobile.0-hall6.ydmm.mayor',
                'Android_3.503_tuyoo.aigame.0-hall6.aigame.laizi',
                'Android_3.503_tuyoo.YDJD.0-hall6.maopao.dj',
                'Android_3.503_tuyoo.weakChinaMobile.0-hall6.ydmm.dingzhidj',
                'Android_3.503_YDJD.YDJD.0-hall6.ydjd.dingzhidj',
    
                'Android_3.503_tuyoo.weakChinaMobile.0-hall6.ydmm.laizi',
                'Android_3.503_YDJD.YDJD.0-hall6.ydjd.laizi',
                'Android_3.503_tuyoo.woStore.0-hall6.ltwo.laizi',
                
                'Android_3.503_tuyoo.YDJD.0-hall6.jinri.jinri',
    
                'Android_3.503_tuyoo.woStore.0-hall6.ltwo.jinri',
                'Android_3.503_YDJD.YDJD.0-hall6.ydjd.jinri',
                'Android_3.503_tuyoo.weakChinaMobile.0-hall6.ydmm.kugou',
                'Android_3.503_tuyoo.woStore.0-hall6.ltwo.kugou',
                'Android_3.503_tuyoo.weakChinaMobile.0-hall6.ydmm.midanji',
                'Android_3.503_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.tianqiwang.tu',
                'Android_3.503_tuyoo.weakChinaMobile.0-hall6.ydmm.happy',
                'Android_3.503_tuyoo.weakChinaMobile.0-hall6.ydmm.tu',
                'Android_3.503_youku.youku,weakChinaMobile,woStore,aigame,YDJD.0-hall6.youku.happy',
                'Winpc_3.372_360.360.0-hall6.360.zd',
                'Android_3.501_tuyoo.weakChinaMobile.0-hall6.ydmm.happy',
                'Android_3.501_tuyoo.weakChinaMobile.0-hall6.ydmm.tu',
                'Android_3.501_tuyoo.YDJD.0-hall6.sohuvideo.tu',
              'Android_3.501_meizu.YDJD.0-hall6.meizu.dj',
              'Android_3.501_meizu.YDJD.0-hall6.meizu.happy',
              'Android_3.501_tuyoo.jinri,jinritoutiao.0-hall6.jinri.jinri',
              'Android_3.501_tuyoo.YDJD.0-hall6.leshiydjd.dj',
              'Android_3.501_tuyoo.YDJD.0-hall6.miydjd.midanji',
              'Android_3.501_meizu.meizu,weakChinaMobile,woStore,aigame,YDJD.0-hall6.meizu.dj',
            'Android_3.5011_nearme.nearme,weakChinaMobile,woStore,YDJD.0-hall6.oppo.dj',
            'Android_3.5011_nearme.nearme,weakChinaMobile,woStore,YDJD.0-hall6.oppo.tu',
            'Android_3.501_tuyoo.weakChinaMobile.0-hall6.ydmm.jinri',
            'Android_3.501_YDJD.YDJD.0-hall6.YDJD.jinri',
            'Android_3.501_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.leshi.dj',
            'Android_3.5010_nearme.nearme,weakChinaMobile,woStore,aigame,YDJD.0-hall6.oppo.dj',
            'Android_3.5012_nearme.nearme,weakChinaMobile,woStore,YDJD.0-hall6.oppo.tu',
    ]
}

needWriteClosedClientIds = set()

def adjustTemplate(template):
    replacekvs = [('url', '${http_download}/dizhu2/'),
            ('lpic', '${http_download}/6/'),
            ('rpic', '${http_download}/6/'),
            ('mpic', '${http_download}/6/')]
    
    for k, v in template.iteritems():
        for name, value in replacekvs:
            if k == name and value:
                template[k] = value + v
            
def writeTemplateClientIds(name, template, closedClientIds, clientIdMap):
    for clientId in template.get('clientIds', []):
        d = {'template':name}
        if clientId in closedClientIds:
            d['closed'] = 1
            needWriteClosedClientIds.discard(clientId)
        writeByClientId(d, clientId, clientIdMap)

def writeByClientId(d, clientId, clientIdMap):
    if clientId not in clientIdMap:
        print 'clientId %s not in gdss' % (clientId)
        return
    clientIdNumber = clientIdMap.get(clientId)
    jstr = json.dumps(d, ensure_ascii=False, indent=4)
    f = open('../../game/6/pop.activity/%s.json' % (clientIdNumber), 'w')
    f.write(jstr)
    f.close()
    
def pickTemplates():
    templateMap = {}
    for k, v in act_conf.iteritems():
        if k in ('default', 'default_old'):
            templateMap[k] = v
        elif k == 'byclientids':
            for i, t in enumerate(v):
                name = 'template%s' % (i+1)
                templateMap[name] = t
    return templateMap

def pickClosedClientIds():
    return act_conf.get('clientId_close', [])

if __name__ == '__main__':
    templateMap = pickTemplates()
    clientIdMap = gdss.syncDataFromGdss('getClientIdDict')
    closedClientIds = pickClosedClientIds()
    needWriteClosedClientIds = set(closedClientIds)
    for name, template in templateMap.iteritems():
        adjustTemplate(template)
        writeTemplateClientIds(name, template, closedClientIds, clientIdMap)
        if 'clientIds' in template:
            del template['clientIds']
    jstr = json.dumps({'templates':templateMap}, ensure_ascii=False, indent=4)
    f = open('../../game/6/pop.activity/0.json', 'w')
    f.write(jstr)
    f.close()
    
    # 写关闭的clientId
    for clientId in needWriteClosedClientIds:
        writeByClientId({'template':'default', 'closed':1}, clientId, clientIdMap)
    
