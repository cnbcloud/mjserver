# -*- coding=utf-8
'''
Created on 2015年8月13日

@author: zhaojiangang
'''
import json
import re

from product.products import product_list, notRecordLastBuy, buyLimits

def writeProductConf(productList):
    conf = {'products':productList}
    jstr = json.dumps(conf, ensure_ascii=False, indent=4)
    f = open('../../game/9999/products/%s.json' % (0), 'w')
    f.write(jstr)
    f.close()
    
def transBuyLimit(buyLimit):
    if 'visibleInStore' not in buyLimit:
        buyLimit['visibleInStore'] = 0
    type_ = buyLimit['type']
    del buyLimit['type']
    if type_ == 'life':
        buyLimit['cycle'] = {'typeId':'life'}
    elif type_ == 'perDay':
        buyLimit['cycle'] = {'typeId':'perDay'}
    elif type_ == 'perMonth':
        buyLimit['cycle'] = {'typeId':'perMonth'}
    return buyLimit 

def transBuyConditions(conditions):
    for cond in conditions:
        if 'visibleInStore' not in cond:
            cond['visibleInStore'] = 0
        
        type_ = cond['type']
        del cond['type'] 
        if type_ == 'vipLevel':
            cond['typeId'] = 'vipLevel'
        elif type_ == 'charmValue':
            cond['typeId'] = 'charmValue'
    return conditions

new_products = [
    {
        "buyType":"consume",
        "content":{
            "desc":"青春派头像10天+20万金币+会员10天+特惠礼包",
            "items":[
                {
                    "count":10,
                    "itemId":"item:4109"
                },
                {
                    "count":10,
                    "itemId":"item:4110"
                },
                {
                    "count":200000,
                    "itemId":"user:chip"
                },
                {
                    "count":10,
                    "itemId":"item:89"
                },
                {
                    "count":1,
                    "itemId":"item:1012"
                }
            ],
            "typeId":"FixedContent"
        },
        "desc":"赠送20万金币，10天会员，特惠礼包",
        "diamondExchangeRate":0,
        "displayName":"青春派会员10天",
        "displayNamePic":"",
        "mail":"购买\\${displayName}，获得\\${content}",
        "pic":"${http_download}/hall/pdt/goods_TY9999D0030006.png",
        "price":"30",
        "priceDiamond":"300",
        "productId":"TY9999D0030009",
        "recordLastBuy":1
    },
    {
        "buyType":"direct",
        "content":{
            "desc":"会员1天",
            "items":[
                {
                    "count":1,
                    "itemId":"item:89"
                }
            ],
            "typeId":"FixedContent"
        },
        "desc":"1天会员体验",
        "diamondExchangeRate":0,
        "displayName":"1天会员",
        "displayNamePic":"",
        "mail":"购买\\${displayName}，获得\\${content}",
        "pic":"${http_download}/hall/pdt/imgs/member.png",
        "price":"1",
        "priceDiamond":"10",
        "productId":"TY9999D0001003",
        "recordLastBuy":1
    },
    {
        "buyType":"consume",
        "content":{
            "desc":"5天会员",
            "items":[
                {
                    "count":5,
                    "itemId":"item:89"
                }
            ],
            "typeId":"FixedContent"
        },
        "desc":"5天内每天登录送1万金币",
        "diamondExchangeRate":0,
        "displayName":"5天会员卡",
        "displayNamePic":"",
        "mail":"购买\\${displayName}，获得\\${content}",
        "pic":"${http_download}/hall/pdt/imgs/member.png",
        "price":"8",
        "priceDiamond":"80",
        "productId":"TY9999D0008020",
        "recordLastBuy":1
    },
    {
        "buyType":"consume",
        "content":{
            "desc":"改名卡1张",
            "items":[
                {
                    "count":1,
                    "itemId":"item:2001"
                }
            ],
            "typeId":"FixedContent"
        },
        "desc":"增加一次更改昵称的机会哦～",
        "diamondExchangeRate":0,
        "displayName":"改名卡",
        "displayNamePic":"",
        "mail":"购买\\${displayName}，获得\\${content}",
        "pic":"${http_download}/hall/item/imgs/item_2001.png",
        "price":"50",
        "priceDiamond":"500",
        "productId":"TY9999D0050009",
        "recordLastBuy":0
    },
    {
        "buyType":"exchange",
        "content":{
            "desc":"激萌忍者3天",
            "items":[
                {
                    "count":3,
                    "itemId":"item:4139"
                }
            ],
            "typeId":"FixedContent"
        },
        "exchangeFeeContent":{
            "itemId":"user:chip",
            "count":30000
        },
        "exchangeFeeNotEnoughText":"亲，您的剩余\\${feeName}不足，不能兑换此商品哦～",
        "desc":"动态头像，装扮不一样的你",
        "diamondExchangeRate":0,
        "displayName":"激萌忍者3天",
        "displayNamePic":"",
        "mail":"购买\\${displayName}，获得\\${content}",
        "pic":"${http_download}/hall/item/imgs/item_4139.png",
        "price":"30000",
        "priceDiamond":"1000",
        "productId":"TY9999C0003001",
        "recordLastBuy":0
    },
    {
        "buyType":"exchange",
        "content":{
            "desc":"俏皮girl3天",
            "items":[
                {
                    "count":3,
                    "itemId":"item:4140"
                }
            ],
            "typeId":"FixedContent"
        },
        "exchangeFeeContent":{
            "itemId":"user:chip",
            "count":60000
        },
        "exchangeFeeNotEnoughText":"亲，您的剩余\\${feeName}不足，不能兑换此商品哦～",
        "desc":"动态头像，装扮不一样的你",
        "diamondExchangeRate":0,
        "displayName":"俏皮girl3天",
        "displayNamePic":"",
        "mail":"购买\\${displayName}，获得\\${content}",
        "pic":"${http_download}/hall/item/imgs/item_4140.png",
        "price":"",
        "priceDiamond":"1000",
        "productId":"TY9999C0006001",
        "recordLastBuy":0
    },
    {
        "buyConditions":[
            {
                "failure":"亲，您的魅力值不够哦～快去召集小伙伴吧~【兑换该商品需要魅力值3000】",
                "startCharm":3000,
                "typeId":"charmValue",
                "visibleInStore":0
            }
        ],
        "buyType":"exchange",
        "content":{
            "desc":"自然力量3天",
            "items":[
                {
                    "count":3,
                    "itemId":"item:4135"
                }
            ],
            "typeId":"FixedContent"
        },
        "exchangeFeeContent":{
            "itemId":"user:chip",
            "count":15000
        },
        "exchangeFeeNotEnoughText":"亲，您的剩余\\${feeName}不足，不能兑换此商品哦～",
        "desc":"魅力值达到3000可购买",
        "diamondExchangeRate":0,
        "displayName":"自然力量3天",
        "displayNamePic":"",
        "mail":"购买\\${displayName}，获得\\${content}",
        "pic":"${http_download}/hall/item/imgs/item_4135.png",
        "price":"15000",
        "priceDiamond":"1000",
        "productId":"TY9999C0001501",
        "recordLastBuy":0
    },
    {
        "buyConditions":[
            {
                "failure":"亲，您的魅力值不够哦～快去召集小伙伴吧~【兑换该商品需要魅力值50000】",
                "startCharm":50000,
                "typeId":"charmValue",
                "visibleInStore":0
            }
        ],
        "buyType":"exchange",
        "content":{
            "desc":"金属时代3天",
            "items":[
                {
                    "count":3,
                    "itemId":"item:4137"
                }
            ],
            "typeId":"FixedContent"
        },
        "exchangeFeeContent":{
            "itemId":"user:chip",
            "count":30000
        },
        "exchangeFeeNotEnoughText":"亲，您的剩余\\${feeName}不足，不能兑换此商品哦～",
        "desc":"魅力值达到50000可购买",
        "diamondExchangeRate":0,
        "displayName":"金属时代3天",
        "displayNamePic":"",
        "mail":"购买\\${displayName}，获得\\${content}",
        "pic":"${http_download}/hall/item/imgs/item_4137.png",
        "price":"30000",
        "priceDiamond":"1000",
        "productId":"TY9999C0003002",
        "recordLastBuy":0
    },
    {
        "buyConditions":[
            {
                "failure":"对不起，亲！该商品属于VIP限购商品，需要达到VIP3以上才可以购买，您的VIP等级还不够呦。加油！",
                "startLevel":3,
                "endLevel":-1,
                "typeId":"vipLevel",
                "visibleInStore":0
            }
        ],
        "buyType":"exchange",
        "content":{
            "desc":"羊年金条",
            "items":[
                {
                    "count":1,
                    "itemId":"item:4138"
                }
            ],
            "typeId":"FixedContent"
        },
        "exchangeFeeContent":{
            "itemId":"user:chip",
            "count":1050000
        },
        "exchangeFeeNotEnoughText":"亲，您的剩余\\${feeName}不足，不能兑换此商品哦～",
        "desc":"羊年定制，收藏必备",
        "diamondExchangeRate":0,
        "displayName":"羊年金条",
        "displayNamePic":"",
        "mail":"购买\\${displayName}，获得\\${content}",
        "pic":"${http_download}/hall/item/imgs/item_4138.png",
        "price":"105万",
        "priceDiamond":"1000",
        "productId":"TY9999C0105001",
        "recordLastBuy":0
    },
    {
        "buyType":"exchange",
        "content":{
            "desc":"冰箱兑换券",
            "items":[
                {
                    "count":1,
                    "itemId":"item:4145"
                }
            ],
            "typeId":"FixedContent"
        },
        "exchangeFeeContent":{
            "itemId":"user:coupon",
            "count":200000
        },
        "exchangeFeeNotEnoughText":"亲，您的剩余\\${feeName}不足，不能兑换此商品哦～",
        "desc":"货真价实冰箱兑换券哦～",
        "diamondExchangeRate":0,
        "displayName":"冰箱兑换券",
        "displayNamePic":"",
        "mail":"购买\\${displayName}，获得\\${content}",
        "pic":"${http_download}/hall/item/imgs/item_4145.png",
        "price":"20万",
        "priceDiamond":"20000",
        "productId":"TY9999Q0020001",
        "recordLastBuy":0
    },
    {
        "buyType":"exchange",
        "content":{
            "desc":"10元话费卡",
            "items":[
                {
                    "count":1,
                    "itemId":"item:4141"
                }
            ],
            "typeId":"FixedContent"
        },
        "exchangeFeeContent":{
            "itemId":"user:coupon",
            "count":1180
        },
        "exchangeFeeNotEnoughText":"亲，您的剩余\\${feeName}不足，不能兑换此商品哦～",
        "desc":"可兑换10元话费",
        "diamondExchangeRate":0,
        "displayName":"10元话费卡",
        "displayNamePic":"",
        "mail":"购买\\${displayName}，获得\\${content}",
        "pic":"${http_download}/hall/item/imgs/item_4141.png",
        "price":"1180",
        "priceDiamond":"120",
        "productId":"TY9999Q0000101",
        "recordLastBuy":0
    },
    {
        "buyType":"exchange",
        "content":{
            "desc":"30元话费卡",
            "items":[
                {
                    "count":1,
                    "itemId":"item:4142"
                }
            ],
            "typeId":"FixedContent"
        },
        "exchangeFeeContent":{
            "itemId":"user:coupon",
            "count":3450
        },
        "exchangeFeeNotEnoughText":"亲，您的剩余\\${feeName}不足，不能兑换此商品哦～",
        "desc":"可兑换30元话费",
        "diamondExchangeRate":0,
        "displayName":"30元话费卡",
        "displayNamePic":"",
        "mail":"购买\\${displayName}，获得\\${content}",
        "pic":"${http_download}/hall/item/imgs/item_4142.png",
        "price":"3450",
        "priceDiamond":"400",
        "productId":"TY9999Q0000401",
        "recordLastBuy":0
    },
    {
        "buyType":"exchange",
        "content":{
            "desc":"50元话费卡",
            "items":[
                {
                    "count":1,
                    "itemId":"item:4143"
                }
            ],
            "typeId":"FixedContent"
        },
        "exchangeFeeContent":{
            "itemId":"user:coupon",
            "count":5500
        },
        "exchangeFeeNotEnoughText":"亲，您的剩余\\${feeName}不足，不能兑换此商品哦～",
        "desc":"可兑换50元话费",
        "diamondExchangeRate":0,
        "displayName":"50元话费卡",
        "displayNamePic":"",
        "mail":"购买\\${displayName}，获得\\${content}",
        "pic":"${http_download}/hall/item/imgs/item_4143.png",
        "price":"5500",
        "priceDiamond":"600",
        "productId":"TY9999Q0000601",
        "recordLastBuy":0
    },
    {
        "buyType":"exchange",
        "content":{
            "desc":"100元话费卡",
            "items":[
                {
                    "count":1,
                    "itemId":"item:4144"
                }
            ],
            "typeId":"FixedContent"
        },
        "exchangeFeeContent":{
            "itemId":"user:coupon",
            "count":10000
        },
        "exchangeFeeNotEnoughText":"亲，您的剩余\\${feeName}不足，不能兑换此商品哦～",
        "desc":"可兑换100元话费",
        "diamondExchangeRate":0,
        "displayName":"100元话费卡",
        "displayNamePic":"",
        "mail":"购买\\${displayName}，获得\\${content}",
        "pic":"${http_download}/hall/item/imgs/item_4144.png",
        "price":"10000",
        "priceDiamond":"1000",
        "productId":"TY9999Q0001001",
        "recordLastBuy":0
    }
]

if __name__ == '__main__':
    new_product_ids = set([p['productId'] for p in new_products])
    itemPicProductIds = set(['TY9999D0008017', 'TY9999D0008018'])
    for product in product_list:
        productId = product['productId']
        if productId in new_product_ids:
            continue
        pic = product.get('pic')
        if pic:
            if productId in itemPicProductIds:
                product['pic'] = '${http_download}/hall/item/imgs/%s' % (pic)
            else:
                product['pic'] = '${http_download}/hall/pdt/imgs/%s' % (pic)
        if productId in notRecordLastBuy:
            product['recordLastBuy'] = 0
        else:
            product['recordLastBuy'] = 1
        mail = product.get('mail')
        if mail:
            mail = mail.replace('${displayName}', '\\${displayName}')
            mail = mail.replace('${content}', '\\${content}')
            mail = mail.replace('${count}', '\\${count}')
            product['mail'] = mail
        if 'isMultiLang' in product:
            del product['isMultiLang']
        if 'category' in product:
            del product['category']
             
        if productId in buyLimits:
            limit = buyLimits[productId]
            print 'product', productId, 'limit=', limit
            if 'conditions' in limit:
                product['buyConditions'] = transBuyConditions(limit['conditions'])
            if 'buyLimit' in limit:
                product['buyCountLimit'] = transBuyLimit(limit['buyLimit'])
                 
                 
    needReplaceList = [
        ('1', 'user:chip'),
        ('2', 'user:coupon'),
        ('1007', 'item:1007'),
        ('2003', 'item:2003'),
        ('3001', 'item:3001')
    ]
    
    all_product_list = []
    for p in product_list:
        if p['productId'] not in new_product_ids:
            all_product_list.append(p)
    all_product_list.extend(new_products)
    product_list = all_product_list
    
    jstr = json.dumps({"products":product_list}, ensure_ascii=False, indent=4, sort_keys=True, separators=(',',':'))
    for oldId, newId in needReplaceList:
        oldStr = 'itemId":%s,' % (oldId)
        newStr = 'itemId":"%s",' % (newId)
        jstr = jstr.replace(oldStr, newStr)
         
        oldStr = 'itemId":%s\n' % (oldId)
        newStr = 'itemId":"%s"\n' % (newId)
        jstr = jstr.replace(oldStr, newStr)
         
    l = [
         ('"type":"FixedContent"', '"typeId":"FixedContent"'),
         ('"type":"CompositeContent"', '"typeId":"CompositeContent"'),
         ('"type":"RandomContent"', '"typeId":"RandomContent"'),
         ('"type":"EmptyContent"', '"typeId":"EmptyContent"')
    ]
    for oldStr, newStr in l:
        jstr = jstr.replace(oldStr, newStr)
         
    p = re.compile('"itemId":[0-9]+')
    foundList = p.findall(jstr)
    for oldStr in set(foundList):
        itemId = oldStr.split(':')[1]
        jstr = jstr.replace(oldStr, '"itemId":"item:%s"' % (itemId))
         
    f = open('../../game/9999/products/%s.json' % (0), 'w')
    f.write(jstr)
    f.close()
     


