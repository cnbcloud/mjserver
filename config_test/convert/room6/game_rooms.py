# -*- coding: utf-8 -*-
from game_match import match_conf_627, match_conf_632, match_conf_633, \
    match_conf_610, match_conf_611, match_conf_612, match_conf_614, match_conf_615, \
    match_conf_619, match_conf_622, match_conf_626, match_conf_634, match_conf_635, \
    match_conf_636, match_conf_637, match_conf_638


# def filter_room_des(desc) :
#     if  not 'condition' in desc :
#         raise Exception('房间信息condition丢失') 
#     if  not 'minCoin' in desc :
#         desc['minCoin'] = 0
#     if  not 'maxCoin' in desc :
#         desc['maxCoin'] = -1
#     if  not 'maxCoinQS' in desc :
#         desc['maxCoinQS'] = -1
#     if  not 'playType' in desc :
#         desc['playType'] = ''
#     if  not 'roomFee' in desc :
#         desc['roomFee'] = 0
#     if  not 'winDesc' in desc :
#         desc['winDesc'] = ''
#     if  not 'playDesc' in desc :
#         desc['playDesc'] = '' 
#     if  not 'roomMutil' in desc :
#         desc['roomMutil'] = 1
#     if  not 'matchScoreRatio' in desc :
#         desc['matchScoreRatio'] = 1
#     if  not 'matchName' in desc :
#         desc['matchName'] = ''
#     if  not 'maxLevel' in desc :
#         desc['maxLevel'] = -1
#     if  not 'sendCoupon' in desc :
#         desc['sendCoupon'] = 0
#     if  not 'category' in desc :
#         raise Exception('房间信息category丢失') 
#     if  not 'showCard' in desc :
#         desc['showCard'] = 0 
#     if  not 'playMode' in desc :
#         desc['playMode'] = 'happy'
#     if  not 'buyinchip' in desc :
#         desc['buyinchip'] = 0
#     return desc
# 
# # 斗地主桌子配置
# def filter_table_config(tableDesc, roomDesc):
#     if 'extdict' in tableDesc :
#         return [tableDesc['extdict']]
#     return [tableDesc.get('grab', 1),  # 1  #本桌是否支持抢地主,0表示不支持
#             tableDesc.get('basebet', 1),  # 2  #初始倍数
#             tableDesc.get('maxseat', 3),  # 3  #座位数，现在总是3
#             roomDesc.get('minCoin', 0),  # 4  #入场最小金币，一般是基数的几十倍
#             roomDesc.get('maxCoin', -1),  # 5  #入场最大金币，一般是基数的几十倍
#             tableDesc.get('coin2chip', 1),  # 6  #为了平台兼容，几乎总是1
#             tableDesc.get('optime', 20),  # 7  #操作时间秒数单位
#             roomDesc.get('roomFee', 0),  # 8  #服务费用(系统抽成), 要和addRoom中的配置一致
#             tableDesc.get('basemulti', 1),  # 9  #基本的倍率
#             roomDesc.get('roomMutil', 1),  # 10 #房间倍率，8倍场，20倍场中的倍数，要和addRoom中的roomMulti一致
#             tableDesc.get('lucky', 0),  # 11 #多发炸弹的概率
#             tableDesc.get('gslam', 128),  # 12 #大满贯倍数
#             tableDesc.get('passtime', 5),  # 13表示如果自己管不上上家的牌，显示自己的出牌时间。如果没有则等同opTime
#             tableDesc.get('canchat', 0),  # 14 1 -- 可以聊天， 0 -- 不可以聊天
#             tableDesc.get('unticheat', 0),  # 15 1 -- 防作弊， 0 -- 普通
#             tableDesc.get('autochange', 1),  # 16 1 -- 每局结束后自动换桌， 0 -- 不自动换桌
#             tableDesc.get('tbbox', 0),  # 17 1 -- 有宝箱， 0 -- 无宝箱
#             tableDesc.get('robottimes', 2),  # 18 n - 超时n次后， 托管状态
#             tableDesc.get('rangpaiMultiType', 1),  # 19 1 - 让牌倍数+1  2 - 让牌倍数*2
#             ]

# def add_dizhu_room(roomId, tableCount, serverIds, roomName, roomDesc, tableDesc):
#     roomDesc = filter_room_des(roomDesc)
#     add_room(roomId, serverIds, roomName, roomDesc, False, 6)
#     tableconf = filter_table_config(tableDesc, roomDesc)
#     add_table_config(roomId, tableconf)
#     add_table(roomId, roomId, tableCount, serverIds)

# #版本号，float类型
# add_game_item_old(6, 'game.buyin.conf', {
#                         'start_version': 3.502,
#                         'closed':[],
#                         'tip': '客官，此房间最多允许带入{BUYIN_CHIP}金币哦!',
#                         'tip_auto': '系统自动为您补充了金币',
#                     })
# 
# #服务费抽取
# add_game_item_old(6, 'game.roomfee.conf', {
#                         'basic': 0.6,
#                         'winner_chip': 0.03
#                     })
# 
# add_game_item_old(6, 'high.multi.fee.conf', {
#                         'high.multi':32,
#                         'fee.multi':2.0,
#                     }) # 高级服务费倍数
# 
# add_game_item_old(6, 'high.room.cheat.conf', {
#                         'open':1,
#                         'roomIds':[605, 653, 673, 693],
#                         'delayLimit': 4
#                     }) # 高级服务费倍数


add_dizhu_room(601, 1000,
        [60100, 60101, 60102, 60103, 60104, 60105, 60106, 60107, 60108, 60109,
         60110, 60111, 60112, 60113, 60114, 60115, 60116, 60117, 60118, 60119,
         60120, 60121, 60122, 60123, 60124, 60125, 60126, 60127, 60128, 60129,
         60130, 60131 ],
         '欢乐新手场',
        {
         'condition':'300~6.5万金币准入',
         'minCoin':300,
         'buyinchip' : 30000, 
         'maxCoin':65000,
         'maxCoinQS':2800,
         'roomFee':45,
         'roomMutil':50,
         'category':'free',
         'showCard':1,
         'goodCard':1,
         },
        {'lucky':60, 'unticheat':0 , 'tbbox':0})
add_dizhu_room(603, 1000,
         [60300, 60301, 60302, 60303, 60304, 60305, 60306, 60307, 60308, 60309, 
          60310, 60311, 60312, 60313, 60314, 60315, 60316, 60317, 60318, 60319,
          60320, 60321, 60322, 60323 ],
         '欢乐中级场',
        {
         'condition':'2500~8万金币准入',
         'minCoin':2500,
         'buyinchip' : 50000,
         'maxCoin':80000,
         'maxCoinQS':28000,
         'roomFee':150,
         'roomMutil':250,
         'category':'free',
         'showCard':1,
         'goodCard':1,
         },
        {'lucky':60, 'unticheat':0, 'tbbox':1})
add_dizhu_room(607, 1000,
         [60700, 60701, 60702, 60703],
         '欢乐高级场',
        {
         'condition':'1.5万~100万金币准入',
         'minCoin':20000,
         'buyinchip' : 400000,
         'maxCoin':1000000,
         'maxCoinQS':80000,
         'roomFee':750,
         'roomMutil':1200,
         'category':'high',
         'showCard':1,
         'goodCard':1,
         'winDesc' : '连续玩6局,开启宝箱送2个奖券',
         },
        {'lucky':60, 'unticheat':0 , 'tbbox':1})
add_dizhu_room(605, 1000,
         [60500, 60501],
         '欢乐大师场',
        {
         'condition':'大于5万金币',
         'minCoin':50000,
         'buyinchip' : 1000000,
         'maxCoin':-1,
         'maxCoinQS':-1,
         'roomFee':2800,
         'roomMutil':5000,
         'category':'high',
         'showCard':1,
         'goodCard':1,
         'winDesc' : '连续玩6局,开启宝箱送5个奖券',
         },
        {'lucky':60, 'unticheat':0 , 'tbbox':1})
# 添加123分房间
add_dizhu_room(650, 1000,
        [65000, 65001, 65002, 65003, 65004, 65005, 65006, 65007,
         65008, 65009, 65010, 65011, 65012, 65013, 65014, 65015],
        '经典新手场',
        {
         'condition':'300~6.5万金币准入',
         'minCoin':300,
         'buyinchip' : 30000,
         'maxCoin':65000,
         'maxCoinQS':2800,
         'roomFee':65,
         'roomMutil':100,
         'category':'free',
         'playMode':'123',
         'goodCard':1,
         },
        {'grab':0, 'lucky':60, 'canchat':1})
add_dizhu_room(651, 1000,
        [ 65100, 65101, 65102, 65103, 65104, 65105, 65106, 65107, 65108, 65109,
          65110, 65111, 65112, 65113, 65114, 65115] ,
        '经典中级场',
        {
         'condition':'2500~8万金币准入',
         'minCoin':2500,
         'buyinchip' : 50000,
         'maxCoin':80000,
         'maxCoinQS':28000,
         'roomFee':220,
         'roomMutil':400,
         'category':'free',
         'playMode':'123',
         'goodCard':1,
         },
        {'grab':0, 'lucky':60, 'canchat':1})
add_dizhu_room(652, 1000,
        [65200, 65201, 65202, 65203],
        '经典高级场',
        {
         'condition':'1.5万~100万金币准入',
         'minCoin':20000,
         'buyinchip' : 400000,
         'maxCoin':1000000,
         'maxCoinQS':80000,
         'roomFee':1200,
         'roomMutil':1500,
         'category':'free',
         'playMode':'123',
         'goodCard':1,
         'winDesc' : '连续玩6局,开启宝箱送2个奖券',
         },
        {'grab':0, 'lucky':60, 'canchat':1, 'tbbox':1})
add_dizhu_room(653, 1000,
        [65300],
        '经典大师场',
        {
         'condition':'大于5万金币准入',
         'minCoin':50000,
         'buyinchip' : 1000000,
         'maxCoin':-1,
         'maxCoinQS':-1,
         'roomFee':4600,
         'roomMutil':6000,
         'category':'free',
         'playMode':'123',
         'goodCard':1,
         'winDesc' : '连续玩6局,开启宝箱送5个奖券',
         },
        {'grab':0, 'lucky':60, 'canchat':1, 'tbbox':1, 'unticheat':0})
# 添加癞子房间
add_dizhu_room(670, 1000,
        [67000, 67001, 67002, 67003, 67004, 67005, 67006, 67007,
         67008, 67009, 67010, 67011, 67012, 67013, 67014, 67015],
        '癞子新手场',
        {
         'condition':'300~6.5万金币准入',
         'minCoin':300,
         'buyinchip' : 30000,
         'maxCoin':65000,
         'maxCoinQS':2800,
         'roomFee':50,
         'roomMutil':30,
         'category':'free',
         'goodCard':1,
         'playMode':'laizi',
         },
        {'luck':60, 'canchat':1})
add_dizhu_room(671, 1000,
        [67100, 67101, 67102, 67103, 67104, 67105, 67106, 67107, 67108, 67109,
         67110, 67111, 67112, 67113, 67114, 67115],
        '癞子中级场',
        {
         'condition':'2500~8万金币准入',
         'minCoin':2500,
         'buyinchip' : 50000,
         'maxCoin':80000,
         'maxCoinQS':28000,
         'roomFee':180,
         'roomMutil':150,
         'category':'free',
         'playMode':'laizi',
         'goodCard':1,
         },
        {'luck':60, 'canchat':1, 'tbbox':1})
add_dizhu_room(672, 1000,
        [67200, 67201, 67202, 67203],
        '癞子高级场',
        {
         'condition':'1.5万~100万金币准入',
         'minCoin':20000,
         'buyinchip' : 400000,
         'maxCoin':1000000,
         'maxCoinQS':80000,
         'roomFee':900,
         'roomMutil':700,
         'category':'free',
         'playMode':'laizi',
         'goodCard':1,
         'winDesc' : '连续玩6局,开启宝箱送2个奖券',
         },
        {'luck':60, 'canchat':1, 'tbbox':1})
add_dizhu_room(673, 1000,
        [67300],
        '癞子大师场',
        {
         'condition':'大于5万金币准入',
         'minCoin':50000,
         'buyinchip' : 1000000,
         'maxCoin':-1,
         'maxCoinQS':-1,
         'roomFee':3500,
         'roomMutil':2500,
         'category':'free',
         'playMode':'laizi',
         'goodCard':1,
         'winDesc' : '连续玩6局,开启宝箱送5个奖券',
         },
        {'luck':60, 'canchat':1, 'unticheat':0, 'tbbox':1})
# 添加二斗房间
add_dizhu_room(690, 1000,
        [69000, 69001, 69002, 69003, 69004, 69005],
        '二人新手场',
        {
         'condition':'300~6.5万金币准入',
         'minCoin':300,
         'buyinchip' : 30000,
         'maxCoin':65000,
         'maxCoinQS':2800,
         'roomFee':65,
         'roomMutil':180,
         'category':'free',
         'playMode':'erdou',
         },
        {'luck':60, 'canchat':1, 'maxseat':2, 'rangpaiMultiType':2})
add_dizhu_room(691, 1000,
        [69100, 69101, 69102, 69103],
        '二人中级场',
        {
         'condition':'2500~8万金币准入',
         'minCoin':2500,
         'buyinchip' : 50000,
         'maxCoin':80000,
         'maxCoinQS':28000,
         'roomFee':250,
         'roomMutil':800,
         'category':'free',
         'playMode':'erdou',
         },
        {'luck':60, 'canchat':1, 'maxseat':2, 'rangpaiMultiType':2})
add_dizhu_room(692, 1000,
        [69200, 69201],
        '二人高级场',
        {
         'condition':'1.5万~100万金币准入',
         'minCoin':20000,
         'buyinchip' : 400000,
         'maxCoin':1000000,
         'maxCoinQS':80000,
         'roomFee':1200,
         'roomMutil':3000,
         'category':'free',
         'playMode':'erdou',
         'winDesc' : '连续玩6局,开启宝箱送4个奖券',
         },
        {'luck':60, 'canchat':1, 'maxseat':2, 'tbbox':1, 'rangpaiMultiType':2})
add_dizhu_room(693, 1000,
        [69300],
        '二人大师场',
        {
         'condition':'大于5万金币准入',
         'minCoin':50000,
         'buyinchip' : 1000000,
         'maxCoin':-1,
         'maxCoinQS':-1,
         'roomFee':5000,
         'roomMutil':8000,
         'category':'free',
         'playMode':'erdou',
         'winDesc' : '连续玩6局,开启宝箱送10个奖券',
         },
        {'luck':60, 'canchat':1, 'maxseat':2, 'unticheat':0, 'tbbox':1, 'rangpaiMultiType':2})

# 水果游戏
add_dizhu_room(680, 1,
        [68000],
        "水果大亨",
        {"condition":"",
         "category":"free",
         "playMode":"fruit"
         },
        {'extdict':{
                    "fruitGameId":11,
                    "fruitRoomId":1101,
                    "fruitTableId":11010
        }})
# 添加比赛场
add_dizhu_room(61001, 300,
         [61001, 61002, 61003, 61004, 61005, 61006, 61007, 61008],
         '新手免费快速赛',
        {
         'condition':'',
         'minCoin':0,
         'maxCoin':-1,
         'maxCoinQS':-1,
         'roomFee':45,
         'roomMutil':50,
         'category':'free',
         'showCard':0,
         'goodCard':0,
         'bigmatchId':610,
         },
        {'optime':20, 'unticheat':1})

add_dizhu_room(610, 1,
        [610],
        '新手免费快速赛',
        {
         'condition':'满18人开赛',
         'sendCoupon':1,
         'category':'bigmatch',
         'rooms':[
            61001
         ],
         'bigmatch':match_conf_610,
        },
        {'optime':20, 'unticheat':1})

add_dizhu_room(61101, 300,
         [61101, 61102, 61103, 61104, 61105, 61106, 61107, 61108],
         '九人快速赛',
        {
         'condition':'',
         'minCoin':0,
         'maxCoin':-1,
         'maxCoinQS':-1,
         'roomFee':45,
         'roomMutil':50,
         'category':'free',
         'showCard':0,
         'goodCard':0,
         'bigmatchId':611,
         },
        {'optime':20, 'unticheat':1})

add_dizhu_room(611, 1,
        [611],
        '九人快速赛',
        {
         'condition':'满9人开赛,报名费2000金币',
         'sendCoupon':1,
         'category':'bigmatch',
         'rooms':[
            61101
         ],
         'bigmatch':match_conf_611,
        },
        {'optime':20, 'unticheat':1})

add_dizhu_room(61201, 300,
         [61201, 61202, 61203, 61204, 61205, 61206, 61207, 61208],
         '三人超快赛',
        {
         'condition':'',
         'minCoin':0,
         'maxCoin':-1,
         'maxCoinQS':-1,
         'roomFee':45,
         'roomMutil':50,
         'category':'free',
         'showCard':0,
         'goodCard':0,
         'bigmatchId':612,
         },
        {'optime':20, 'unticheat':1})

add_dizhu_room(612, 1,
        [612],
        '三人超快赛',
        {
         'condition':'满3人开赛,报名费5000金币',
         'sendCoupon':1,
         'category':'bigmatch',
         'rooms':[
            61201
         ],
         'bigmatch':match_conf_612,
        },
        {'optime':20, 'unticheat':1})

add_dizhu_room(61401, 300,
         [61401, 61402, 61403, 61404, 61405, 61406, 61407, 61408],
         '2元话费赛',
        {
         'condition':'',
         'minCoin':0,
         'maxCoin':-1,
         'maxCoinQS':-1,
         'roomFee':45,
         'roomMutil':50,
         'category':'free',
         'showCard':0,
         'goodCard':0,
         'bigmatchId':614,
         },
        {'optime':20, 'unticheat':1})

add_dizhu_room(614, 1,
        [614],
        '2元话费赛',
        {
         'condition':'全民参与,免费参加',
         'sendCoupon':1,
         'category':'bigmatch',
         'rooms':[
            61401
         ],
         'bigmatch':match_conf_614,
        },
        {'optime':20, 'unticheat':1})

add_dizhu_room(61501, 300,
         [61501, 61502, 61503, 61504, 61505, 61506, 61507, 61508],
         '高手百元赛',
        {
         'condition':'',
         'minCoin':0,
         'maxCoin':-1,
         'maxCoinQS':-1,
         'roomFee':45,
         'roomMutil':50,
         'category':'free',
         'showCard':0,
         'goodCard':0,
         'bigmatchId':615,
         },
        {'optime':20, 'unticheat':1})

add_dizhu_room(615, 1,
        [615],
        '高手百元赛',
        {
         'condition':'5000金币',
         'sendCoupon':1,
         'category':'bigmatch',
         'rooms':[
            61501
         ],
         'bigmatch':match_conf_615,
        },
        {'optime':20, 'unticheat':1})

add_dizhu_room(62701, 300,
        [62701, 62702, 62703, 62704, 62705, 62706, 62707, 62708],
         '免费百元话费赛',
        {
         'condition':'',
         'minCoin':0,
         'maxCoin':-1,
         'maxCoinQS':-1,
         'roomFee':45,
         'roomMutil':50,
         'category':'free',
         'showCard':0,
         'goodCard':0,
         'bigmatchId':627,
         },
        {'optime':20, 'unticheat':1, 'tbbox':0})

add_dizhu_room(627, 1,
        [627],
        '免费百元话费赛',
        {
         'condition':'免费参与',
         'sendCoupon':1,
         'category':'bigmatch',
         'rooms':[
            62701
         ],
         'bigmatch':match_conf_627,
        },
        {'optime':20, 'unticheat':1})

add_dizhu_room(63201, 300,
        [63201, 63202, 63203, 63204, 63205, 63206, 63207, 63208],
         '免费百元话费赛',
        {
         'condition':'',
         'minCoin':0,
         'maxCoin':-1,
         'maxCoinQS':-1,
         'roomFee':45,
         'roomMutil':50,
         'category':'free',
         'showCard':0,
         'goodCard':0,
         'bigmatchId':632,
         },
        {'optime':20, 'unticheat':1, 'tbbox':0})

add_dizhu_room(632, 1,
        [632],
        '免费百元话费赛',
        {
         'condition':'免费参与',
         'sendCoupon':1,
         'category':'bigmatch',
         'rooms':[
            63201
         ],
         'bigmatch':match_conf_632,
        },
        {'optime':20, 'unticheat':1})

add_dizhu_room(63301, 300,
        [63301, 63302, 63303, 63304, 63305,
         63306, 63307, 63308, 63309, 63310,
         63311, 63312, 63313, 63314, 63315,
         63316, 63317, 63318, 63319, 63320],
         '欢乐新手场',
        {
         'condition':'',
         'minCoin':0,
         'maxCoin':-1,
         'maxCoinQS':-1,
         'roomFee':45,
         'roomMutil':50,
         'category':'free',
         'showCard':0,
         'goodCard':0,
         'bigmatchId':633,
         },
        {'optime':20, 'unticheat':1, 'tbbox':0})
 
add_dizhu_room(633, 1,
        [633],
        '腊八节冰箱赛',
        {
         'condition':'免费参与',
         'sendCoupon':1,
         'category':'bigmatch',
         'rooms':[
            63301
         ],
         'bigmatch':match_conf_633
        },
        {'optime':20, 'unticheat':1})

# add_dizhu_room(63401, 300,
#         [63401],
#          '斗地主内部赛',
#         {
#          'condition':'',
#          'minCoin':0,
#          'maxCoin':-1,
#          'maxCoinQS':-1,
#          'roomFee':45,
#          'roomMutil':50,
#          'category':'free',
#          'showCard':0,
#          'goodCard':0,
#          'bigmatchId':634,
#          },
#         {'optime':20, 'unticheat':1, 'tbbox':0})
# 
# add_dizhu_room(634, 1,
#         [634],
#         '斗地主内部赛',
#         {
#          'condition':'免费参与',
#          'sendCoupon':1,
#          'category':'bigmatch',
#          'rooms':[
#             63401
#          ],
#          'bigmatch':match_conf_634,
#         },
#         {'optime':20, 'unticheat':1})

add_dizhu_room(63501, 300,
        [63501, 63502, 63503, 63504, 63505,
         63506, 63507, 63508, 63509, 63510,
         63511, 63512, 63513, 63514, 63515,
         63516, 63517, 63518, 63519, 63520,
         ],
         '斗地主内部赛',
        {
         'condition':'',
         'minCoin':0,
         'maxCoin':-1,
         'maxCoinQS':-1,
         'roomFee':45,
         'roomMutil':50,
         'category':'free',
         'showCard':0,
         'goodCard':0,
         'bigmatchId':635,
         },
        {'optime':20, 'unticheat':1, 'tbbox':0})

add_dizhu_room(635, 1,
        [635],
        '情人节礼物赛',
        {
         'condition':'免费参与',
         'sendCoupon':1,
         'category':'bigmatch',
         'rooms':[
            63501
         ],
         'bigmatch':match_conf_635,
        },
        {'optime':20, 'unticheat':1})

add_dizhu_room(63601, 300,
        [63601, 63602, 63603, 63604, 63605,
         63606, 63607, 63608, 63609, 63610
         ],
         '新春5元赛',
        {
         'condition':'',
         'minCoin':0,
         'maxCoin':-1,
         'maxCoinQS':-1,
         'roomFee':45,
         'roomMutil':50,
         'category':'free',
         'showCard':0,
         'goodCard':0,
         'bigmatchId':636,
         },
        {'optime':20, 'unticheat':1, 'tbbox':0})

add_dizhu_room(636, 1,
        [636],
        '新春5元赛',
        {
         'condition':'报名费:999金币',
         'sendCoupon':1,
         'category':'bigmatch',
         'rooms':[
            63601
         ],
         'bigmatch':match_conf_636,
        },
        {'optime':20, 'unticheat':1})

add_dizhu_room(63701, 300,
        [63701, 63702, 63703, 63704, 63705,
         63706, 63707, 63708, 63709, 63710,
         63711, 63712, 63713, 63714, 63715,
         63716, 63717, 63718, 63719, 63720,
         ],
         '春节电视赛',
        {
         'condition':'',
         'minCoin':0,
         'maxCoin':-1,
         'maxCoinQS':-1,
         'roomFee':45,
         'roomMutil':50,
         'category':'free',
         'showCard':0,
         'goodCard':0,
         'bigmatchId':637,
         },
        {'optime':20, 'unticheat':1, 'tbbox':0})

add_dizhu_room(637, 1,
        [637],
        '春节电视赛',
        {
         'condition':'免费参与',
         'sendCoupon':1,
         'category':'bigmatch',
         'rooms':[
            63701
         ],
         'bigmatch':match_conf_637,
        },
        {'optime':20, 'unticheat':1})

add_dizhu_room(63801, 300,
        [63801, 63802, 63803, 63804, 63805,
         63806, 63807, 63808, 63809, 63810,
         63811, 63812, 63813, 63814, 63815,
         63816, 63817, 63818, 63819, 63820,
         ],
         '高手大奖赛',
        {
         'condition':'',
         'minCoin':0,
         'maxCoin':-1,
         'maxCoinQS':-1,
         'roomFee':45,
         'roomMutil':50,
         'category':'free',
         'showCard':0,
         'goodCard':0,
         'bigmatchId':638,
         },
        {'optime':20, 'unticheat':1, 'tbbox':0})

add_dizhu_room(638, 1,
        [638],
        '高手大奖赛',
        {
         'condition':'免费参与',
         'sendCoupon':1,
         'category':'bigmatch',
         'rooms':[
            63801
         ],
         'bigmatch':match_conf_638,
        },
        {'optime':20, 'unticheat':1})

# if service['mode'] != 1 or service['simulation'] == 1:
#     add_robot(0, 601, 603, 607, 605, 650, 651, 652, 653, 670, 671, 672, 673, 690, 691, 692, 693)
#     add_robot(1, 610, 611, 612)
