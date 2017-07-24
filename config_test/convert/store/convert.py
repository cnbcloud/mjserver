# -*- coding=utf-8
'''
Created on 2015年8月13日

@author: zhaojiangang
'''
import codecs
import json

import gdss
from store.storeconf import shelves_map, templateMap, template2clientIds, \
    closedLastBuyCLientIds


store_conf = {
    "firstRechargeThreshold":60,
    "pricePics":{
        "1":"${http_download}/hall/store/imgs/price_1.png",
        "2":"${http_download}/hall/store/imgs/price_2.png",
        "5":"${http_download}/hall/store/imgs/price_5.png",
        "6":"${http_download}/hall/store/imgs/price_6.png",
        "8":"${http_download}/hall/store/imgs/price_8.png",
        "10":"${http_download}/hall/store/imgs/price_10.png",
        "12":"${http_download}/hall/store/imgs/price_12.png",
        "18":"${http_download}/hall/store/imgs/price_18.png",
        "30":"${http_download}/hall/store/imgs/price_30.png",
        "50":"${http_download}/hall/store/imgs/price_50.png",
        "68":"${http_download}/hall/store/imgs/price_68.png",
        "100":"${http_download}/hall/store/imgs/price_100.png",
        "128":"${http_download}/hall/store/imgs/price_128.png",
        "300":"${http_download}/hall/store/imgs/price_300.png",
        "1000":"${http_download}/hall/store/imgs/price_1000.png"
    },
    "exchangePricePics":{
        "user:chip":"${http_download}/hall/store/imgs/chip.png",
        "user:diamond":"${http_download}/hall/store/imgs/diamond.png",
        "user:coupon":"${http_download}/hall/store/imgs/coupon.png"
    },
    "lastBuy":{
        "desc":"您上次购买的商品是\\${displayName}，是否依然购买此商品？",
        "subText":"是",
        "subTextExt":"逛逛商城"
    },
    "deliveryConf":{
        "fail":{
            "title":"很抱歉，添加物品失败啦！",
            "timefmt":"%H点%M分%S秒",
            "content":"啊哦~这真是太尴尬了......请您尽快联系我们的客服！我们一定第一时间为您处理！感谢您对我们工作的支持和理解！",
            "tips":"如有问题请拨打客服电话：4008-098-000"
        },
        "succ":{
            "title":"添加物品成功啦！",
            "timefmt":"%H点%M分%S秒",
            "content":"您于\\${datetime}成功购买 \\${productName}\n本次消费：\\${consume}\n添加\\${content}",
            "tips":"如有问题请拨打客服电话：4008-098-000"
        }
    }
}

def writeStoreConf(templateMap):
    conf = {'templates':templateMap}
    conf.update(store_conf)
    jstr = json.dumps(conf, ensure_ascii=False, indent=4)
    f = open('../../game/9999/store/%s.json' % (0), 'w')
    f.write(jstr)
    f.close()

def transShelves(name, productIds):
    if name == 'chip':
        name = 'coin'
    shelvesConf = shelves_map.get(name)
    if shelvesConf:
        return {
            "displayName":shelvesConf['displayName'],
            "name":name,
            "products":productIds,
            "visible":shelvesConf['visibleInStore'],
            "iconType":shelvesConf['iconType'],
            'sort':shelvesConf.get('sort', 0)
        }
    else:
        return {
            "displayName":'',
            "name":name,
            "products":productIds,
            "visible":0,
            "iconType":'coin',
            'sort':0
        }

def transTemplate(name, template):
    shelves = []
    for shelvesName, productIds in template.iteritems():
        shelves.append(transShelves(shelvesName, productIds))
    return shelves

def transTemplates():
    newTemplateMap = {}
    for name, template in templateMap.iteritems():
        newTemplateMap[name] = transTemplate(name, template)
    return newTemplateMap

def writeStoreConfForClientId(clientIdNumber, clientId, templateName):
    d = {
         "template" : templateName
    }
    if clientId in closedLastBuyCLientIds:
        d['closeLastBuy'] = 1
    jstr = json.dumps(d, ensure_ascii=False, indent=4)
    f = open('../../game/9999/store/%s.json' % (clientIdNumber), 'w')
    f.write(jstr)
    f.close()

new_templates = {
"goods_conf_3.7_alpha":[
    {
        "sort": 0, 
        "displayName": "特价专区", 
        "name": "activity", 
        "visible": 1, 
        "products": [
            "TY9999D0001003",
            "TY9999D0008012", 
            "TY9999R0050001", 
        ], 
        "iconType": "diamond"
    }, 
    {
        "sort": 1, 
        "displayName": "购买金币", 
        "name": "coin", 
        "visible": 1, 
        "products": [
            "TY9999D0002001",
            "TY9999D0008005",
            "TY9999D0030001", 
            "TY9999D0050001", 
            "TY9999D0100001", 
            "TY9999D0300001", 
            "TY9999D1000001", 
        ], 
        "iconType": "coin"
    }, 
    {
        "sort": 2, 
        "displayName": "钻石商城", 
        "name": "diamond", 
        "visible": 1, 
        "products": [
            "TY9999D0000102", 
            "TY9999R0000101",
            "TY9999R0008005", 
            "TY9999R0050001", 
            "TY9999R0100001", 
            "TY0006D0002001", 
            "TY0006D0002002", 
            "TY0006D0010001", 
            "TY9999D0008006"
        ], 
        "iconType": "diamond"
    }, 
    {
        "sort": 5, 
        "displayName": "装饰道具", 
        "name": "charm", 
        "visible": 1, 
        "products": [
            "TY9999C0003001",
            "TY9999C0006001",
            "TY9999C0001501",
            "TY9999C0003002",
            "TY9999D0012001", 
            "TY9999D0002003", 
            "TY9999D0006008", 
            "TY9999D0006009", 
            "TY9999D0030004", 
            "TY9999D0030005", 
            "TY9999D0100002", 
            "TY9999D0100003", 
            "TY9999D0100004"
        ], 
        "iconType": "diamond"
    }, 
    {
        "sort": 6, 
        "displayName": "奖品兑换", 
        "name": "coupon", 
        "visible": 1, 
        "products": [
            "TY9999Q0000101", "TY9999Q0000401",
            "TY9999Q0000601", "TY9999Q0001001"
        ], 
        "iconType": "diamond"
    },
    {
        "sort": 1, 
        "displayName": "", 
        "name": "raffle", 
        "visible": 0, 
        "products": [
            "TY9999D0008001"
        ], 
        "iconType": "coin"
    }, 
    {
        "sort": 0, 
        "displayName": "", 
        "name": "winlead", 
        "visible": 0, 
        "products": [
            "TY9999D0008025",
            "TY9999D0030012",
            "TY9999D0050008",
            "TY9999D0100012"
        ], 
        "iconType": "coin"
    }, 
    {
        "sort": 0, 
        "displayName": "", 
        "name": "zhuanyun", 
        "visible": 0, 
        "products": [
            "TY9999D0008026",
            "TY9999D0030011",
            "TY9999D0050007",
            "TY9999D0100011"
        ], 
        "iconType": "coin"
    }, 
    {
        "sort": 2, 
        "displayName": "道具商城", 
        "name": "item", 
        "visible": 1, 
        "products": [], 
        "iconType": "coin"
    }, 
    {
        "sort": 0, 
        "displayName": "", 
        "name": "quick", 
        "visible": 0, 
        "products": [], 
        "iconType": "coin"
    }, 
    {
        "sort": 0, 
        "displayName": "", 
        "name": "lessbuychip", 
        "visible": 0, 
        "products": [
            "TY9999D0002001",
            "TY9999D0008005",
            "TY9999D0030001", 
            "TY9999D0050001", 
            "TY9999D0100001", 
            "TY9999D0300001", 
            "TY9999D1000001", 
            "TY0006D0030002", 
            "TY0006D0100002"
        ], 
        "iconType": "coin"
    }, 
    {
        "sort": 0, 
        "displayName": "", 
        "name": "member", 
        "visible": 0, 
        "products": [
            "TY9999D0001003", "TY9999D0012003"
        ], 
        "iconType": "coin"
    }
]}

def readOldMemberProductIds():
    ret = set([])
    f = codecs.open('./old_members.txt')
    for line in f.readlines():
        line = line.strip()
        ret.add(line)
    return ret

if __name__ == '__main__':
    oldMemberProductIds = readOldMemberProductIds()
    newTemplateMap = transTemplates()
    for n, t in newTemplateMap.iteritems():
        for shelves in t:
            products = []
            for p in shelves['products']:
                if p not in oldMemberProductIds:
                    products.append(p)
            shelves['products'] = products
            
    newTemplateMap.update(new_templates)
    
    writeStoreConf(newTemplateMap)
    clientIdMap = gdss.syncDataFromGdss('getClientIdDict')
      
    # key=clientId, list<templateName>
    clientId2templateNameList = {}
    unknownClientIds = set()
      
    template2clientIds['goods_conf_3.7_alpha'] = [
        "Android_3.70_360.360.0-hall6.360.day",
        "IOS_3.70_360.360.0-hall6.360.day"
    ]
      
    for templateName, template in newTemplateMap.iteritems():
        clientIds = template2clientIds.get(templateName)
        if clientIds:
            for clientId in clientIds:
                clientIdNumber = clientIdMap.get(clientId)
                if clientId in ('Android_3.70_360.360.0-hall6.360.day', 'IOS_3.70_360.360.0-hall6.360.day'):
                    print '***********', clientId, 'clientIdNumber', clientIdNumber, 'templateName', templateName
                if not clientIdNumber:
                    unknownClientIds.add(clientId)
                    continue
                templateNameList = clientId2templateNameList.get(clientId)
                if not templateNameList:
                    templateNameList = []
                    clientId2templateNameList[clientId] = templateNameList
                templateNameList.append(templateName)
                if len(templateNameList) <= 1:
                    writeStoreConfForClientId(clientIdNumber, clientId, templateName)
                    if clientId in ('Android_3.70_360.360.0-hall6.360.day', 'IOS_3.70_360.360.0-hall6.360.day'):
                        print 'write***********', clientId, 'clientIdNumber', clientIdNumber, 'templateName', templateName
  
    f = open('./unknown.clientIds.txt', 'w')
    jstr = json.dumps(list(unknownClientIds), indent=4, ensure_ascii=False)
    f.write(jstr)
    f.close()
      
    duplicateClientIds = {}
    for clientId, templateNameList in clientId2templateNameList.iteritems():
        if len(templateNameList) > 1:
            duplicateClientIds[clientId] = templateNameList
    f = open('./duplicate.clientIds.txt', 'w')
    jstr = json.dumps(duplicateClientIds, indent=4, ensure_ascii=False)
    f.write(jstr)
    f.close()
     

