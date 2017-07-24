# -*- coding=utf-8
'''
Created on 2015年7月30日

@author: zhaojiangang
'''
import json

common_dizhu_double_v3_5='common_dizhu_double_v3_5'
plugin_texas_v3_6_pc_type_1='plugin_texas_v3_6_pc_type_1'
plugin_texas_v3_6_phone_type_1='plugin_texas_v3_6_phone_type_1'
plugin_texas_as_default='plugin_texas_as_default'
plugin_douniu_old100='plugin_douniu_old100'
plugin_dizhu_match_v3_6='plugin_dizhu_match_v3_6'
plugin_dizhu_happy='plugin_dizhu_happy'
plugin_douniu_crazy_v3_502='plugin_douniu_crazy_v3_502'
plugin_douniu_crazy_v3_601='plugin_douniu_crazy_v3_601'
plugin_dizhu_happy_v3_6='plugin_dizhu_happy_v3_6'
plugin_texas_v3_6_phone_type_3='plugin_texas_v3_6_phone_type_3'
plugin_fruit_v3_6='plugin_fruit_v3_6'
common_dizhu_happy_v3_5='common_dizhu_happy_v3_5'
common_dizhu_happy='common_dizhu_happy'
plugin_douniu_old100_v3_5='plugin_douniu_old100_v3_5'
plugin_dizhu_double='plugin_dizhu_double'
plugin_texas_v3_6='plugin_texas_v3_6'
common_mj_xlch_v3_5='common_mj_xlch_v3_5'
plugin_douniu_100_v3_6='plugin_douniu_100_v3_6'
plugin_dizhu_match='plugin_dizhu_match'
common_dizhu_double='common_dizhu_double'
common_next_page_v3_5='common_next_page_v3_5'
plugin_douniu_100='plugin_douniu_100'
common_next_page_v3_6='common_next_page_v3_6'
plugin_fruit_v3_5='plugin_fruit_v3_5'
common_dizhu_single='common_dizhu_single'
plugin_dizhu_single_v3_6='plugin_dizhu_single_v3_6'
common_dizhu_match_v3_5='common_dizhu_match_v3_5'
plugin_majiang='plugin_majiang'
plugin_texas_v3_6_phone_type_4='plugin_texas_v3_6_phone_type_4'
common_dizhu_match='common_dizhu_match'
plugin_fruit='plugin_fruit'
plugin_douniu_100_v3_5='plugin_douniu_100_v3_5'
common_dizhu_laizi='common_dizhu_laizi'
common_mj_blood_v3_5='common_mj_blood_v3_5'
package_v3_5='package_v3_5'
plugin_dizhu_classics_v3_6='plugin_dizhu_classics_v3_6'
plugin_t3flush='plugin_t3flush'
common_dizhu_classics_v3_5='common_dizhu_classics_v3_5'
common_dizhu_classics='common_dizhu_classics'
common_next_page='common_next_page'
common_dizhu_laizi_v3_5='common_dizhu_laizi_v3_5'
plugin_dizhu_single='plugin_dizhu_single'
plugin_dog_ios_v3_5='plugin_dog_ios_v3_5'
plugin_texas_v3_6_pc_type_3='plugin_texas_v3_6_pc_type_3'
plugin_t3card_v3_5='plugin_t3card_v3_5'
plugin_douniu_crazy_v3_5='plugin_douniu_crazy_v3_5'
common_dizhu_single_v3_5='common_dizhu_single_v3_5'
plugin_baohuang='plugin_baohuang'
common_mj_blood='common_mj_blood'
plugin_texas_v3_5='plugin_texas_v3_5'
plugin_dog_v3_6='plugin_dog_v3_6'
plugin_dog_v3_5='plugin_dog_v3_5'
plugin_dizhu_laizi_v3_6='plugin_dizhu_laizi_v3_6'
plugin_texas_v3_6_pc_type_2='plugin_texas_v3_6_pc_type_2'
plugin_t3flush_v3_5='plugin_t3flush_v3_5'
plugin_dizhu_laizi='plugin_dizhu_laizi'
plugin_baohuang_v3_5='plugin_baohuang_v3_5'
plugin_dog='plugin_dog'
plugin_dizhu_classics='plugin_dizhu_classics'
plugin_texas='plugin_texas'
plugin_t3card='plugin_t3card'
plugin_douniu_crazy='plugin_douniu_crazy'
plugin_majiang_v3_5='plugin_majiang_v3_5'
plugin_dizhu_double_v3_6='plugin_dizhu_double_v3_6'
common_mj_xlch='common_mj_xlch'
plugin_texas_v3_6_phone_type_2='plugin_texas_v3_6_phone_type_2'

hall_game_default = [
    {
     "form":"dizhu3x2",
     "nodes":[
              common_dizhu_classics_v3_5,   common_dizhu_happy_v3_5,    common_dizhu_match_v3_5,
              common_dizhu_laizi_v3_5,      common_dizhu_double_v3_5,   common_dizhu_single_v3_5   
              ]
     }
]

# 3.6开发的game_list配置
# package_v3_6 = {
#     "type":"package",
#     "params":{
#         "iconUrl":"",
#         "defaultRes":"PackageDefault",
#         "pages":[
#             {
#                 "form":"dizhu3x2",
#                 "nodes":[
#                     plugin_dizhu_classics_v3_6
#                     , plugin_dizhu_happy_v3_6
#                     , plugin_fruit_v3_6
#                 ]
#             }
#         ]
#     }            
# }

hall_game_3_6 = [
    {
        "form":"dizhu3x2",
        "nodes":[
            plugin_dizhu_classics_v3_6, plugin_dizhu_happy_v3_6, plugin_dizhu_match_v3_6
            , plugin_dizhu_laizi_v3_6, plugin_dizhu_single_v3_6, common_next_page_v3_6
        ]
    }
    , {
        "form":"dizhu3x3",
        "nodes":[
            plugin_dizhu_double_v3_6, plugin_fruit_v3_6, plugin_douniu_crazy_v3_601,
            plugin_dog_v3_6, plugin_douniu_100_v3_6
        ]
    }
]

hall_game_3_6_ddz_pc = [
    {
        "form":"dizhu3x2",
        "nodes":[
            plugin_dizhu_classics_v3_6, 
            plugin_dizhu_happy_v3_6, 
            plugin_dizhu_match_v3_6, 
            plugin_dizhu_laizi_v3_6
        ]
    }
]

hall_game_texas_3_6_pc = [
    {
        "form":"dizhu3x2",
        "nodes":[
                plugin_texas_v3_6_pc_type_1,
                plugin_texas_v3_6_pc_type_2,
                plugin_texas_v3_6_pc_type_3,
            # plugin_dizhu_classics_v3_6
            # , plugin_fruit_v3_6
            # , plugin_dizhu_happy_v3_6
            # , plugin_dizhu_match_v3_6
            # , plugin_dizhu_laizi_v3_6
            # , common_next_page_v3_6
        ]
    }
    # , {
    #     "form":"dizhu3x3",
    #     "nodes":[
    #         plugin_dizhu_double_v3_6
    #         , plugin_dizhu_single_v3_6
    #     ]
    # }
]

hall_game_texas_3_6_phone = [
    {
        "form":"texas1x5",
        "nodes":[
                plugin_texas_v3_6_phone_type_2,
                plugin_texas_v3_6_phone_type_3,
                plugin_texas_v3_6_phone_type_4,
                plugin_texas_v3_6_phone_type_1,
        ]
    }
]

hall_game_3_5 = [
    {
     "form":"dizhu3x2",
     "nodes":[
              common_dizhu_classics_v3_5,   common_dizhu_happy_v3_5,    common_dizhu_match_v3_5,
              common_dizhu_laizi_v3_5,      common_dizhu_single_v3_5,   common_next_page_v3_5
              ]
     },
    {
     "form":"dizhu3x3",
     "nodes":[
              common_dizhu_double_v3_5, plugin_douniu_crazy_v3_5,   plugin_douniu_100_v3_5,
              plugin_t3card_v3_5,       plugin_fruit_v3_5,          plugin_texas_v3_5,
              plugin_majiang_v3_5,      plugin_dog_v3_5,            plugin_t3flush_v3_5
              ]
     }
]

hall_game_3_5_ios = [
    {
     "form":"dizhu3x2",
     "nodes":[
              common_dizhu_classics_v3_5,   common_dizhu_happy_v3_5,    common_dizhu_match_v3_5,
              common_dizhu_laizi_v3_5,      common_dizhu_single_v3_5,   common_next_page_v3_5
              ]
     },
    {
     "form":"dizhu3x3",
     "nodes":[
              common_dizhu_double_v3_5, plugin_douniu_crazy_v3_5,   plugin_douniu_100_v3_5,
              plugin_t3card_v3_5,       plugin_fruit_v3_5,          plugin_texas_v3_5,
              plugin_majiang_v3_5,      plugin_dog_ios_v3_5,            plugin_t3flush_v3_5
              ]
     }
]

hall_game_mj_3_5 = [
    {
     "form":"dizhu3x2",
     "nodes":[
              common_dizhu_classics_v3_5,   common_dizhu_double_v3_5,    common_dizhu_match_v3_5,
              common_dizhu_single_v3_5,      common_mj_blood_v3_5,   common_next_page_v3_5
              ]
     },
    {
     "form":"dizhu3x3",
     "nodes":[
              common_dizhu_laizi_v3_5, common_mj_xlch_v3_5,        common_dizhu_happy_v3_5,
              plugin_t3card_v3_5,       plugin_fruit_v3_5,          plugin_texas_v3_5,
              plugin_douniu_crazy_v3_5,  plugin_douniu_100_v3_5,    plugin_baohuang_v3_5
              ]
     }
]

hall_game_mj_3_5_huawei = [
    {
     "form":"dizhu3x2",
     "nodes":[
              common_dizhu_classics_v3_5,   common_dizhu_double_v3_5,    common_dizhu_match_v3_5,
              common_dizhu_single_v3_5,      common_mj_blood_v3_5,   common_next_page_v3_5
              ]
     },
    {
     "form":"dizhu3x3",
     "nodes":[
              common_dizhu_laizi_v3_5, common_mj_xlch_v3_5,        common_dizhu_happy_v3_5,
              plugin_fruit_v3_5,          plugin_texas_v3_5,       plugin_dog_v3_5,
              plugin_baohuang_v3_5
              ]
     }
]

hall_game_mj_ios_3_5 = [
    {
     "form":"dizhu3x2",
     "nodes":[
              common_dizhu_classics_v3_5,   common_dizhu_double_v3_5,    common_dizhu_match_v3_5,
              common_dizhu_laizi_v3_5,      common_dizhu_single_v3_5,   common_next_page_v3_5
              ]
     },
    {
     "form":"dizhu3x3",
     "nodes":[
              common_dizhu_happy_v3_5, common_mj_blood_v3_5,         common_mj_xlch_v3_5,
              plugin_t3card_v3_5,       plugin_fruit_v3_5,          plugin_texas_v3_5,
              plugin_douniu_crazy_v3_5,  plugin_douniu_100_v3_5,     plugin_baohuang_v3_5
              ]
     }
]

hall_game_3_5_no_plugin = [
    {
     "form":"dizhu3x2",
     "nodes":[
              common_dizhu_classics_v3_5,   common_dizhu_happy_v3_5,    common_dizhu_match_v3_5,
              common_dizhu_laizi_v3_5,      common_dizhu_double_v3_5,   common_dizhu_single_v3_5
              ]
     }
]

hall_game_3_5_no_plugin_no_single = [
    {
     "form":"dizhu3x2",
     "nodes":[
              common_dizhu_classics_v3_5,   common_dizhu_happy_v3_5,    common_dizhu_match_v3_5,
              common_dizhu_laizi_v3_5,      common_dizhu_double_v3_5
              ]
     }
]

hall_game_3_5_no_single = [
    {
     "form":"dizhu3x2",
     "nodes":[
              common_dizhu_classics_v3_5,   common_dizhu_happy_v3_5,    common_dizhu_match_v3_5,
              common_dizhu_laizi_v3_5,      common_dizhu_double_v3_5,   common_next_page_v3_5
              ]
     },
    {
     "form":"dizhu3x3",
     "nodes":[
              plugin_douniu_crazy_v3_5,   plugin_douniu_100_v3_5,   plugin_t3card_v3_5,       
              plugin_fruit_v3_5,          plugin_texas_v3_5,        plugin_majiang_v3_5,
              plugin_dog_v3_5   ]
     }
]



hall_game_3_5_not3card = [
    {
     "form":"dizhu3x2",
     "nodes":[
              common_dizhu_classics_v3_5,   common_dizhu_happy_v3_5,    common_dizhu_match_v3_5,
              common_dizhu_laizi_v3_5,      common_dizhu_single_v3_5,   common_next_page_v3_5
              ]
     },
    {
     "form":"dizhu3x3",
     "nodes":[
              common_dizhu_double_v3_5, plugin_douniu_crazy_v3_5,   plugin_douniu_100_v3_5,
              plugin_fruit_v3_5,          plugin_texas_v3_5,    plugin_majiang_v3_5,
              plugin_dog_v3_5]
     }
]

hall_game_3_5_not3card_nodouniu = [
    {
     "form":"dizhu3x2",
     "nodes":[
              common_dizhu_classics_v3_5,   common_dizhu_happy_v3_5,    common_dizhu_match_v3_5,
              common_dizhu_laizi_v3_5,      common_dizhu_single_v3_5,   common_next_page_v3_5
              ]
     },
    {
     "form":"dizhu3x2",
     "nodes":[
              common_dizhu_double_v3_5,     plugin_fruit_v3_5,          plugin_texas_v3_5,
              plugin_majiang_v3_5,          plugin_dog_v3_5
              ]
     }
]

hall_game_3_5_t3flush = [
    {
     "form":"dizhu3x2",
     "nodes":[
              common_dizhu_classics_v3_5,   common_dizhu_happy_v3_5,    common_dizhu_match_v3_5,
              common_dizhu_laizi_v3_5,      common_dizhu_single_v3_5,   common_next_page_v3_5
              ]
     },
    {
     "form":"dizhu3x3",
     "nodes":[
              common_dizhu_double_v3_5, plugin_douniu_crazy_v3_5,   plugin_douniu_100_v3_5,
              plugin_t3card_v3_5,       plugin_fruit_v3_5,          plugin_texas_v3_5,
              plugin_majiang_v3_5,      plugin_dog_v3_5,            plugin_t3flush_v3_5
              ]
     }
]

hall_game_3_5_02 = [
    {
     "form":"dizhu3x2",
     "nodes":[
              common_dizhu_classics_v3_5,   common_dizhu_happy_v3_5,    common_dizhu_match_v3_5,
              common_dizhu_laizi_v3_5,      common_dizhu_single_v3_5,   common_next_page_v3_5
              ]
     },
    {
     "form":"dizhu3x3",
     "nodes":[
              common_dizhu_double_v3_5, plugin_douniu_crazy_v3_502,    plugin_douniu_100_v3_5,
              plugin_t3card_v3_5,       plugin_fruit_v3_5,          plugin_texas_v3_5,
              plugin_dog_v3_5,          plugin_t3flush_v3_5]
     }
]

hall_game_3_5_02_ios = [
    {
     "form":"dizhu3x2",
     "nodes":[
              common_dizhu_classics_v3_5,   common_dizhu_happy_v3_5,    common_dizhu_match_v3_5,
              common_dizhu_laizi_v3_5,      common_dizhu_single_v3_5,   common_next_page_v3_5
              ]
     },
    {
     "form":"dizhu3x3",
     "nodes":[
              common_dizhu_double_v3_5, plugin_douniu_crazy_v3_502,    plugin_douniu_100_v3_5,
              plugin_t3card_v3_5,       plugin_fruit_v3_5,          plugin_texas_v3_5,
              plugin_dog_ios_v3_5,          plugin_t3flush_v3_5]
     }
]


hall_game_3_5_03 = [
    {
     "form":"dizhu3x2",
     "nodes":[
              common_dizhu_classics_v3_5,   common_dizhu_happy_v3_5,    common_dizhu_match_v3_5,
              common_dizhu_laizi_v3_5,      common_dizhu_single_v3_5,   common_next_page_v3_5
              ]
     },
    {
     "form":"dizhu3x3",
     "nodes":[
              common_dizhu_double_v3_5, plugin_douniu_crazy_v3_502,    plugin_douniu_100_v3_5,
              plugin_t3card_v3_5,     plugin_fruit_v3_5,          plugin_texas_v3_5,
              plugin_dog_v3_5,         plugin_baohuang_v3_5,  plugin_t3flush_v3_5]
     }
]

hall_game_3_5_03_ios = [
    {
     "form":"dizhu3x2",
     "nodes":[
              common_dizhu_classics_v3_5,   common_dizhu_happy_v3_5,    common_dizhu_match_v3_5,
              common_dizhu_laizi_v3_5,      common_dizhu_single_v3_5,   common_next_page_v3_5
              ]
     },
    {
     "form":"dizhu3x3",
     "nodes":[
              common_dizhu_double_v3_5, plugin_douniu_crazy_v3_502,    plugin_douniu_100_v3_5,
              plugin_t3card_v3_5,     plugin_fruit_v3_5,          plugin_texas_v3_5,
              plugin_dog_ios_v3_5,          plugin_t3flush_v3_5]
     }
]

hall_game_3_5_03_not3card = [
    {
     "form":"dizhu3x2",
     "nodes":[
              common_dizhu_classics_v3_5,   common_dizhu_happy_v3_5,    common_dizhu_match_v3_5,
              common_dizhu_laizi_v3_5,      common_dizhu_single_v3_5,   common_next_page_v3_5
              ]
     },
    {
     "form":"dizhu3x3",
     "nodes":[
              common_dizhu_double_v3_5,     plugin_douniu_crazy_v3_502,    plugin_douniu_100_v3_5,
              plugin_fruit_v3_5,            plugin_texas_v3_5,             plugin_dog_v3_5]
     }
]

hall_game_3_5_03_huawei = [
    {
     "form":"dizhu3x2",
     "nodes":[
              common_dizhu_classics_v3_5,   common_dizhu_happy_v3_5,    common_dizhu_match_v3_5,
              common_dizhu_laizi_v3_5,      common_dizhu_single_v3_5,   common_next_page_v3_5
              ]
     },
    {
     "form":"dizhu3x3",
     "nodes":[
              common_dizhu_double_v3_5,     plugin_fruit_v3_5,            plugin_texas_v3_5,             
              plugin_dog_v3_5]
     }
]

hall_game_3_5_03_baohuang_beta = [
    {
     "form":"dizhu3x2",
     "nodes":[
              common_dizhu_classics_v3_5,   common_dizhu_happy_v3_5,    common_dizhu_match_v3_5,
              common_dizhu_laizi_v3_5,      common_dizhu_single_v3_5,   common_next_page_v3_5
              ]
     },
    {
     "form":"dizhu3x3",
     "nodes":[
              common_dizhu_double_v3_5,     plugin_fruit_v3_5,            plugin_texas_v3_5,             
              plugin_dog_v3_5,              plugin_baohuang_v3_5]
     }
]

templates = {
    "hall_game_default"         : hall_game_default,
    "hall_game_3_5"             : hall_game_3_5,
    "hall_game_3_5_ios"         : hall_game_3_5_ios,
    "hall_game_3_5_02"          : hall_game_3_5_02,
    "hall_game_3_5_02_ios"      : hall_game_3_5_02_ios,
    "hall_game_3_5_03"          : hall_game_3_5_03,
    "hall_game_3_5_03_ios"      : hall_game_3_5_03_ios,
    "hall_game_3_5_03_not3card" : hall_game_3_5_03_not3card,
    'hall_game_3_5_03_huawei'   : hall_game_3_5_03_huawei,
    "hall_game_mj_3_5"          : hall_game_mj_3_5,
    "hall_game_3_5_no_plugin"   : hall_game_3_5_no_plugin,
    "hall_game_3_5_no_plugin_no_single" : hall_game_3_5_no_plugin_no_single,
    "hall_game_3_5_no_single"   : hall_game_3_5_no_single,
    "hall_game_3_5_not3card"    : hall_game_3_5_not3card,
    "hall_game_3_5_not3card_nodouniu" : hall_game_3_5_not3card_nodouniu,
    "hall_game_3_5_03_baohuang_beta" : hall_game_3_5_03_baohuang_beta,
    "hall_game_3_5_t3flush"     : hall_game_3_5_t3flush,
    "hall_game_3_6"             : hall_game_3_6,
    "hall_game_3_6_ddz_pc"      : hall_game_3_6_ddz_pc,
    "hall_game_texas_3_6_pc"    : hall_game_texas_3_6_pc,
    "hall_game_mj_ios_3_5"      : hall_game_mj_ios_3_5,
    "hall_game_texas_3_6_phone" : hall_game_texas_3_6_phone,
}
    
template2clientIds = {
    "hall_game_3_5":[
        'Android_3.5030_360.360,weakChinaMobile,woStore,aigame,YDJD.0-hall6.360.dj',
        'Android_3.5030_360.360,weakChinaMobile,woStore,aigame,YDJD.0-hall6.360.happy',
        'Android_3.5030_360.360,weakChinaMobile,woStore.0-hall6.360.laizi',
        'Android_3.5030_360.360,weakChinaMobile,woStore,aigame,YDJD.0-hall6.360.tu',
        'Android_3.503_kugou.weakChinaMobile,woStore,aigame.0-hall6.kugou.kugou',
        'Android_3.5030_360.360.0-hall6.360.kuaile',
        'Android_3.5030_360.360.0-hall6.360.rich',
        'Android_3.503_tuyoo.jinritoutiao,weakChinaMobile,woStore,YDJD.0-hall6.jinri.jinri',
        'Android_3.503_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.ali.tu',
        'Android_3.503_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.sanxing.tu',
        'Android_3.503_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.jinli.tu',
        'Android_3.503_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.sohuvideo.tu',
        'Android_3.503_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.jinligame.dj',
        'Android_3.503_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.meitu.dj',
        'Android_3.503_tuyoo.lenovo,weakChinaMobile,woStore,aigame,YDJD.0-hall6.lenovo.tu',
        'Android_3.503_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.2345.tu',
        'Android_3.503_meizu.meizu,weakChinaMobile,woStore,aigame,YDJD.0-hall6.meizu.happy',
        'Android_3.503_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.apphui.happy',
        'Android_3.503_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.wandou.happy',
        'Android_3.503_wifikey.weakChinaMobile,woStore,aigame,YDJD.0-hall6.wifikey.happy',
        'Android_3.503_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.chongchongzhushou.happy',
        'Android_3.503_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.youyoucun.happy',
        'Android_3.503_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.baidusearch.tu',
        'Android_3.503_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.360search.tu',
        "Android_3.5010_kugou.tuyoo.0-hall6.kugou.kugou",
        "Android_3.501_tuyoo.weakChinaMobile.0-hall6.ydmm.tu",
        "Android_3.501_360.360,weakChinaMobile.0-hall6.360.laizi",
        "Android_3.501_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.wandou.happy",
        "Android_3.501_kugou.tuyoo.0-hall6.kugou.kugou",
        "Android_3.501_tuyoo.jinri,jinritoutiao.0-hall6.jinri.jinri",
        "Android_3.501_tuyoo.weakChinaMobile.0-hall6.ydmm.happy",
        "Android_3.50_tuyoo.tuyoo.0-hall6.tuyoo.dj",
        "Android_3.50_360.360.0-hall6.360.day",
        "Android_3.50_360.360.0-hall6.360.win",
        "Android_3.51_360.360.0-hall6.360.day",
        'Android_3.501_360.360,weakChinaMobile,woStore,aigame,YDJD.0-hall6.360.dj',
        'Android_3.501_tuyoo.weakChinaMobile,YDJD.0-hall6.qq.dj',
        'Android_3.501_tuyoo.weakChinaMobile,YDJD.0-hall6.wandou.dj',
        'Android_3.501_tuyoo.lenovo,weakChinaMobile,woStore,aigame,YDJD.0-hall6.lenovo.dj',
        'Android_3.501_mi.mi,weakChinaMobile,woStore,aigame,YDJD.0-hall6.mi.dj',
        'Android_3.501_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.jinli.dj',
        'Android_3.501_tuyoo.weakChinaMobile,YDJD.0-hall6.tuyoo.dj',
        'Android_3.501_tuyoo.weakChinaMobile,YDJD.0-hall6.ali.dj',
        'Android_3.501_tuyoo.weakChinaMobile,YDJD.0-hall6.kunda.dj',
        'Android_3.501_tuyoo.weakChinaMobile,YDJD.0-hall6.litianbaoli.dj',
        'Android_3.501_tuyoo.weakChinaMobile,YDJD.0-hall6.sougou.dj',
        'Android_3.501_tuyoo.weakChinaMobile,YDJD.0-hall6.tianyu.dj',
        'Android_3.501_tuyoo.weakChinaMobile,YDJD.0-hall6.wifikey.dj',
        'Android_3.501_pps.pps,weakChinaMobile,woStore,aigame,YDJD.0-hall6.pps.dj',
        'Android_3.501_tuyoo.YDJD,woStore,aigame.0-hall6.sohuvideo.dj',
        'Android_3.501_tuyoo.weakChinaMobile,YDJD.0-hall6.googleplay.dj',
        'Android_3.501_yyduowan.yyduowan.0-hall6.yygame.dj',
        'Android_3.5010_tuyoo.weakChinaMobile,YDJD.0-hall6.qq.dj',
        'Android_3.5010_tuyoo.weakChinaMobile,YDJD.0-hall6.wandou.dj',
        'Android_3.5010_pps.pps,weakChinaMobile,woStore,aigame,YDJD.0-hall6.pps.dj',
        'Android_3.5010_tuyoo.weakChinaMobile,YDJD.0-hall6.tuyoo.dj',
        'Android_3.5010_360.360,weakChinaMobile,woStore,aigame,YDJD.0-hall6.360.dj',
        'Android_3.5010_pps.pps.weakChinaMobile,woStore,aigame,YDJD.0-hall6.pps.dj',
        'Android_3.5010_tuyoo.weakChinaMobile,YDJD.0-hall6.wifikey.dj',
        'Android_3.501_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.4399.happy',
        'Android_3.501_meizu.meizu,weakChinaMobile,woStore,aigame,YDJD.0-hall6.meizu.happy',
        'Android_3.501_tuyoo.weakChinaMobile,YDJD.0-hall6.qingcheng.dj',
        'Android_3.501_tuyoo.duoku,weakChinaMobile,YDJD.0-hall6.duokunew.dj',
        'Android_3.501_tuyoo.weakChinaMobile,YDJD.0-hall6.bdtiebanew.dj',
        'Android_3.501_tuyoo.weakChinaMobile,YDJD.0-hall6.baidunew.dj',
        'Android_3.501_tuyoo.weakChinaMobile,YDJD.0-hall6.91new.dj',
        'Android_3.501_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.wifikey.happy',
        'Android_3.501_360.360.0-hall6.360.kuaile',
        'Android_3.501_360.360.0-hall6.360.people',
        'Android_3.501_360.360.0-hall6.360.fk',
        'Android_3.501_360.360.0-hall6.360.rich',
        'Android_3.501_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.tuyoo.tu',
        'Android_3.501_360.360,weakChinaMobile,woStore,aigame,YDJD.0-hall6.360.tu',
        'Android_3.501_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.qq.tu',
        'Android_3.501_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.2345.tu',
        'Android_3.501_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.coolpad.dj',
        'Android_3.501_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.360search.tu',
        'Android_3.501_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.wandou.tu',
        'Android_3.501_mi.mi,weakChinaMobile,woStore,aigame,YDJD.0-hall6.mi.tu',
        'Android_3.501_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.coolpad.tu',
        'Android_3.501_tuyoo.duoku,weakChinaMobile,YDJD.0-hall6.baidunew.dj',
        'Android_3.501_tuyoo.duoku,weakChinaMobile,YDJD.0-hall6.bdtiebanew.dj',
        'Android_3.501_tuyoo.duoku,weakChinaMobile,YDJD.0-hall6.91new.dj',
        'Android_3.501_youku.youku,weakChinaMobile,aigame,YDJD.0-hall6.youku.happy',
        'Android_3.501_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.jinli.tu',
        'Android_3.5010_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.jinli.dj',
    ],
    "hall_game_3_5_ios": [
        'IOS_3.501_tuyoo.appStore.0-hall6.tuyoo.cherry',
        "IOS_3.5_tuyoo.tuyoo.0.tuyoo.dj",
        "IOS_3.50_tuyoo.tuyoo.0-hall6.tuyoo.dj",
    ],
    "hall_game_3_5_02":[
        "Android_3.502_360.360.0-hall6.360.day",
        "Android_3.502_360.360.0-hall6.360.win",
        "Android_3.502_360.360,weakChinaMobile.0-hall6.360.laizi",
        'Android_3.502_360.360.0-hall6.360.fk',
        'Android_3.502_360.360.0-hall6.360.kuaile',
        'Android_3.502_360.360.0-hall6.360.people',
        'Android_3.502_360.360.0-hall6.360.rich',
    ],
    "hall_game_3_5_02_ios":[
        'IOS_3.502_tuyoo.appStore.0-hall6.tuyoo.huanle',
    ],
    "hall_game_3_5_03":[
        'Android_3.503_360.360,weakChinaMobile.0-hall6.360.laizi',
        'Android_3.503_360.360.0-hall6.360.kuaile',
        'Android_3.503_360.360.0-hall6.360.people',
        'Android_3.503_360.360.0-hall6.360.fk',
        'Android_3.503_360.360.0-hall6.360.rich',

        'Android_3.503_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.sougou.tu',
        'Android_3.503_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.wandou.tu',
        'Android_3.503_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.sanxing.dj',
        'Android_3.503_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.4399.happy',
        # 'Android_3.503_tuyoo.duoku,weakChinaMobile,woStore,aigame,YDJD.0-hall6.bdtiebanew.dj',
        # 'Android_3.503_nearme.nearme,weakChinaMobile,woStore,aigame,YDJD.0-hall6.oppo.dj',
        'Android_3.503_tuyoo.duoku,weakChinaMobile,woStore,aigame,YDJD.0-hall6.91new.dj',
        'Android_3.503_tuyoo.duoku,weakChinaMobile,woStore,aigame,YDJD.0-hall6.baidunew.dj',
        'Android_3.503_tuyoo.duoku,weakChinaMobile,woStore,aigame,YDJD.0-hall6.duokunew.dj',
        # 'Android_3.503_tuyoo.duoku,weakChinaMobile,woStore,aigame,YDJD.0-hall6.bdtiebanew.dj',
        'Android_3.503_pps.pps,weakChinaMobile,woStore,aigame,YDJD.0-hall6.pps.dj',
        'Android_3.503_360.360,weakChinaMobile,woStore,aigame,YDJD.0-hall6.360.tu',
        'Android_3.503_mi.mi,weakChinaMobile,woStore,aigame,YDJD.0-hall6.mi.tu',
        'Android_3.503_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.coolpad.tu',
        'Android_3.503_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.qq.tu',
        'Android_3.503_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.tuyoo.tu',
        'Android_3.503_360.360,weakChinaMobile,woStore,aigame,YDJD.0-hall6.360.happy',
        'Android_3.503_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.qingmeng.dj',
        'Android_3.503_meizu.meizu,weakChinaMobile,woStore,aigame,YDJD.0-hall6.meizu.dj',
        'Android_3.503_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.HTC.dj',
        # 'Android_3.503_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.sohuvideo.tu',
        'Android_3.503_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.kubi.tu',
        # 'Android_3.503_tuyoo.woStore,aigame,YDJD.0-hall6.cocosplay.tu',
        'Android_3.503_yyduowan.yyduowan.0-hall6.yygame.dj',
        'Android_3.503_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.googleplay.dj',
        'Android_3.503_tuyoo.woStore,aigame,YDJD.0-hall6.leshiphone.dj',
        'Android_3.503_tuyoo.weakChinaMobile,aigame,YDJD.0-hall6.guangsheng.dj',
        'Android_3.503_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.wandou.dj',
        'Android_3.503_360.360,weakChinaMobile,woStore,aigame,YDJD.0-hall6.360.dj',
        'Android_3.503_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.kunda.dj',
        'Android_3.503_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.litianbaoli.dj',
        'Android_3.503_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.qq.dj',
        'Android_3.503_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.ruilongxingkong.dj',
        'Android_3.503_wifikey.weakChinaMobile,woStore,aigame,YDJD.0-hall6.wifikey.dj',
        'Android_3.503_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.muzhi.dj',
        'Android_3.503_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.ali.dj',
        'Android_3.503_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.sougou.dj',
        'Android_3.503_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.jinli.dj',
        'Android_3.503_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.coolpad.dj',
    ],
    "hall_game_3_5_03_ios": [
        
    ],
    "hall_game_3_5_03_baohuang_beta" : [
        'Android_3.503_huawei.huawei,weakChinaMobile,woStore,aigame,YDJD.0-hall6.huawei.dj',
        'Android_3.503_tuyoo.lenovo,weakChinaMobile,woStore,aigame,YDJD.0-hall6.lenovo.dj',
        'Android_3.501_huawei.huawei,weakChinaMobile,woStore,aigame,YDJD.0-hall6.huawei.dj',
        'Android_3.5010_tuyoo.lenovo,weakChinaMobile,woStore,aigame,YDJD.0-hall6.lenovo.dj',
    ],
    "hall_game_3_5_03_not3card":[
        'Android_3.503_mi.mi,weakChinaMobile,woStore,aigame,YDJD.0-hall6.mi.dj',
        'Android_3.503_midanji.midanji,weakChinaMobile,woStore,aigame,YDJD.0-hall6.mi.midanji',
    ],
    "hall_game_3_5_03_huawei":[
        'Android_3.503_huawei.huawei,weakChinaMobile,woStore,aigame,YDJD.0-hall6.huawei.tu',
    ],
    "hall_game_3_5_no_plugin": [    
        'Android_3.502_tuyoo.YDJD.0-hall7.leshi.dj',
        'Android_3.502_tuyoo.YDJD.0-hall7.maopao.dj',
        'Android_3.502_tuyoo.YDJD.0-hall7.huancheng.dj',

        'Android_3.502_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall7.ppzhushou.dj',

        'Android_3.503_tuyoo.weakChinaMobile.0-hall6.ydmm.laizi',
        'Android_3.503_YDJD.YDJD.0-hall6.ydjd.laizi',
        'Android_3.503_tuyoo.woStore.0-hall6.ltwo.laizi',

        'Android_3.503_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.ppzhushou.dj',
        'Android_3.503_tuyoo.woStore.0-hall6.ltwo.jinri',

        'Android_3.503_tuyoo.woStore,aigame,YDJD.0-hall6.cocosplay.tu',

        'Android_3.501_nearme.nearme,weakChinaMobile,woStore,YDJD.0-hall6.oppo.dj',
        'Android_3.502_YDJD.YDJD.0-hall7.ydjd.jinri',
        'Android_3.503_wifikey.weakChinaMobile,YDJD.0-hall6.wifikeydemo.dj',
        'Android_3.503_tuyoo.weakChinaMobile,YDJD.0-hall6.wifikeydemo.dj',
        'Android_3.503_tuyoo.weakChinaMobile,aigame,YDJD.0-hall6.tianyu.dj',
        'Android_3.503_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.coolpad.dj',
        'Android_3.503_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.kubi.dj',
        'Android_3.501_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.kubi.tu',
        'Android_3.503_uc.uc.0-hall6.uc.dj',
        'Android_3.501_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.leshi.dj',
        'Android_3.5010_nearme.nearme,weakChinaMobile,woStore,aigame,YDJD.0-hall6.oppo.dj',
        'Android_3.501_nearme.nearme,weakChinaMobile,woStore,YDJD.0-hall6.oppo.tu',
        'Android_3.501_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.baidusearch.tu',
        'Android_3.501_tuyoo.lenovo,weakChinaMobile,woStore,aigame,YDJD.0-hall6.lenovo.tu',
        'Android_3.501_meizu.meizu,weakChinaMobile,woStore,aigame,YDJD.0-hall6.meizu.dj',
        'Android_3.501_tuyoo.YDJD.0-hall6.meitu.dj',
        'Android_3.501_tuyoo.YDJD.0-hall6.sohuvideo.tu',
        'Android_3.501_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.sougou.tu',
        'Android_3.501_huawei.huawei,weakChinaMobile,woStore,aigame,YDJD.0-hall6.huawei.tu',
        'Android_3.501_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.tianqiwang.tu',
        'Android_3.5010_tuyoo.weakChinaMobile,YDJD.0-hall6.sougou.dj',
        'Android_3.5010_tuyoo.YDJD,woStore,aigame.0-hall6.sohuvideo.dj',
        'Android_3.5010_tuyoo.weakChinaMobile,YDJD.0-hall6.kunda.dj',
        'Android_3.5010_tuyoo.weakChinaMobile,YDJD.0-hall6.googleplay.dj',
        'Android_3.5010_tuyoo.weakChinaMobile,YDJD.0-hall6.litianbaoli.dj',
        'Android_3.5010_tuyoo.weakChinaMobile,YDJD.0-hall6.tianyu.dj',
        'Android_3.5010_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.coolpad.dj',
        'Android_3.501_tuyoo.huabeidianhua.0-hall6.huabeidianhua.dj',
        'Android_3.501_YDJD.YDJD.0-hall6.YDJD.midanji',
        'Android_3.501_YDJD.YDJD.0-hall6.ydjd.midanji',
        'Android_3.501_tuyoo.YDJD.0-hall6.huanliang.dj',
        'Android_3.501_tuyoo.woStore,aigame,YDJD.0-hall6.leshiphone.dj',
        'Android_3.501_tuyoo.YDJD.0-hall6.baidusearch.tu',
        'Android_3.501_tuyoo.YDJD.0-hall6.qihoosearch.tu',
        'Android_3.501_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.meitu.dj',
        'Android_3.501_tuyoo.YDJD.0-hall6.ydjd.tu',
        'Android_3.501_tuyoo.YDJD.0-hall6.mi.tu',
        'Android_3.501_tuyoo.YDJD.0-hall6.nearme.tu',
        'Android_3.501_tuyoo.YDJD.0-hall6.coolpad.tu',
        'Android_3.501_tuyoo.YDJD.0-hall6.vivo.tu',
        'Android_3.501_tuyoo.YDJD.0-hall6.lenovo.tu',
        'Android_3.501_tuyoo.YDJD.0-hall6.huawei.tu',
        'Android_3.501_tuyoo.YDJD.0-hall6.ydjd.happy',
        'Android_3.501_tuyoo.YDJD.0-hall6.youku.happy',
        'Android_3.501_tuyoo.YDJD.0-hall6.apphui.happy',
        'Android_3.501_YDJD.YDJD.0-hall6.ydjd.dj',
        'Android_3.501_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.jinligame.dj',
        'Android_3.501_tuyoo.woStore.0-hall6.ltwo.dj',
        'Android_3.501_tuyoo.woStore,aigame,YDJD.0-hall6.leshi.dj',
        'Android_3.501_YDJD.YDJD.0-hall6.ydjd.happy',
        'Android_3.501_YDJD.YDJD.0-hall6.ydjd.tu',
        'Android_3.501_meizu.meizu,weakChinaMobile,woStore,aigame,YDJD.0-hall6.meizu.dj',
        'Android_3.501_oppo.oppo,weakChinaMobile,woStore,YDJD.0-hall6.oppo.dj',
        'Android_3.501_tuyoo.lenovodj,weakChinaMobile,woStore,aigame,YDJD.0-hall6.lenovo.dj',
        'Android_3.501_tuyoo.weakChinaMobile,YDJD.0-hall6.aidebao.dj',
        'Android_3.501_tuyoo.weakChinaMobile,YDJD.0-hall6.huanliang1.dj',
        'Android_3.501_tuyoo.weakChinaMobile,YDJD.0-hall6.huanliang2.dj',
        'Android_3.501_tuyoo.weakChinaMobile,YDJD.0-hall6.huanliang3.dj',
        'Android_3.501_tuyoo.weakChinaMobile,YDJD.0-hall6.huanliang4.dj',
        'Android_3.501_tuyoo.weakChinaMobile,YDJD.0-hall6.huanliang5.dj',
        'Android_3.501_tuyoo.weakChinaMobile,YDJD.0-hall6.huashuo.dj',
        'Android_3.501_tuyoo.weakChinaMobile,YDJD.0-hall6.paojiao.dj',
        'Android_3.501_tuyoo.weakChinaMobile,YDJD.0-hall6.wangyi.dj',
        'Android_3.501_tuyoo.weakChinaMobile,YDJD.0-hall6.yehuo.dj',
        'Android_3.501_tuyoo.weakChinaMobile,YDJD.0-hall6.zanpu.dj',
        'Android_3.501_tuyoo.weakChinaMobile.0-hall6.wpsj.dj',
        'Android_3.501_tuyoo.woStore,aigame,YDJD.0-hall6.leshi.dj',
        'Android_3.501_uc.uc.0-hall6.uc.dj',
        'Android_3.501_vivo.vivo,weakChinaMobile,woStore,aigame,YDJD.0-hall6.vivo.dj',
        'Android_3.501_zhangyue.zhangyue,weakChinaMobile,woStore,aigame,YDJD.0-hall6.zhangyue.dj',
        'Android_3.501_tuyoo.woStore.0-hall6.itwo.dj',
        'Android_3.501_tuyoo.weakChinaMobile.0-hall6.ydmm.dj',
        'Android_3.501_tuyoo.weakChinaMobile,YDJD.0-hall6.duokunew.dj',
        'Android_3.501_tuyoo.aigame.0-hall6.huabeidianhua.dj',
        'Android_3.501_huawei.huawei,weakChinaMobile,woStore,aigame,YDJD.0-hall6.huawei.tu',
        'Android_3.501_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.huanliang1.dj',
        'Android_3.501_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.huanliang2.dj',
        'Android_3.501_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.huanliang3.dj',
        'Android_3.501_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.huanliang4.dj',
        'Android_3.501_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.huanliang5.dj',
        'Android_3.501_tuyoo.woStore,aigame,YDJD.0-hall6.leshiphone.dj',
        'Android_3.501_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.qq.happy',
        'Android_3.502_YDJD.YDJD.0-hall7.ydjd.tu',
        'Android_3.502_YDJD.YDJD.0-hall7.ydjd.fk',
        'Android_3.502_tuyoo.weakChinaMobile.0-hall7.ydmm.fk',
        'Android_3.502_tuyoo.weakChinaMobile.0-hall7.ydmm.dj',
        'Android_3.502_tuyoo.weakChinaMobile.0-hall7.ydmm.sc',
        'Android_3.502_tuyoo.weakChinaMobile.0-hall7.ydmm.happy',
        'Android_3.502_tuyoo.weakChinaMobile.0-hall7.ydmm.kkhlm',
        'Android_3.372_tuyoo.weakChinaMobile.0-hall7.ydmm.tu',
        'Android_3.502_tuyoo.YDJD.0-hall7.oppo.dj',
        'Android_3.502_tuyoo.YDJD.0-hall7.wifikey.happy',
        'Android_3.502_tuyoo.YDJD.0-hall7.ydjd.happy',
        'Android_3.502_tuyoo.YDJD.0-hall7.ydjd.sc',
        'Android_3.502_tuyoo.YDJDDanji.0-hall7.mi.dj',
        'Android_3.502_tuyoo.YDJDDanji.0-hall7.apphui.dj',
        'Android_3.502_tuyoo.YDJDDanji.0-hall7.huawei.dj',
        'Android_3.502_tuyoo.YDJDDanji.0-hall7.lenovo.dj',
        'Android_3.502_tuyoo.YDJDDanji.0-hall7.oppo.dj',
        'Android_3.502_tuyoo.YDJDMain.0-hall7.wifikey.happy',
        'Android_3.502_tuyoo.YDJDMain.0-hall7.ydjd.happy',
        'Android_3.502_tuyoo.YDJDMain.0-hall7.ydjd.sc',
        'Android_3.502_tuyoo.YDJD.0-hall7.mi.dj',
        'Android_3.502_tuyoo.YDJD.0-hall7.apphui.dj',
        'Android_3.502_tuyoo.YDJD.0-hall7.huawei.dj',
        'Android_3.502_tuyoo.YDJD.0-hall7.lenovo.dj',
        'Android_3.502_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall7.huashuo.dj',
        'Android_3.502_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall7.meizu.dj',
        'Android_3.502_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall7.qingcheng.dj',
        'Android_3.502_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall7.kubi.dj',
        'Android_3.502_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall7.meitu.dj',
    ],
    "hall_game_3_5_not3card":[
        'Android_3.5010_mi.mi,weakChinaMobile,woStore,aigame,YDJD.0-hall6.mi.dj',
        'Android_3.5010_tuyoo.weakChinaMobile,YDJD.0-hall6.ali.dj',
        'Android_3.372_huawei.huawei,weakChinaMobile,woStore,aigame,YDJD.0-hall6.huawei.dj',
    ],
    "hall_game_3_5_t3flush":[
        'Android_3.501_360.360,weakChinaMobile,woStore,aigame,YDJD.0-hall6.360.happy',
    ],
    "hall_game_3_5_no_plugin_no_single":[ 
    ],
    "hall_game_3_5_not3card_nodouniu":[
        'Android_3.501_huawei.huawei,weakChinaMobile,woStore,aigame,YDJD.0-hall6.huawei.tu'
    ],
    "hall_game_3_5_no_single":[
        'Android_3.501_youku.youku,weakChinaMobile,woStore,aigame,YDJD.0-hall6.youku.happy',
        'Android_3.501_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.apphui.happy',
        'Android_3.501_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.yingyonghui.happy',
    ],
    "hall_game_mj_3_5": [
        'Android_3.50_360.360,weakChinaMobile.0-hall7.360.fk',
        'Android_3.50_tuyoo.weakChinaMobile.0-hall7.qq.dj',
        'Android_3.502_tuyoo.tuyoo.0-hall7.360.fk', 
        'Android_3.502_360.360,weakChinaMobile.0-hall7.360.fk',
        'Android_3.502_360.360,weakChinaMobile,woStore,aigame,YDJD.0-hall7.360.dj',
        'Android_3.502_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall7.ali.dj',
        'Android_3.502_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall7.googleplay.dj',
        'Android_3.502_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall7.coolpad.dj',
        'Android_3.502_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall7.qq.dj',
        'Android_3.502_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall7.sougou.dj',
        'Android_3.502_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall7.tianyu.dj',
        'Android_3.502_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall7.wifikey.dj',
        'Android_3.502_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall7.4399.dj',
        'Android_3.502_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall7.youyoucun.dj',
        'Android_3.502_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall7.jinli.dj',
        'Android_3.502_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall7.wandou.dj',
    ],
    "hall_game_mj_3_5_huawei": [
        'Android_3.502_huawei.huawei,weakChinaMobile,woStore,aigame,YDJD.0-hall7.huawei.dj',
    ],
    "hall_game_mj_ios_3_5": [
        'IOS_3.50_tuyoo.tuyoo.0-hall7.tuyoo.dj',
        'IOS_3.502_tuyoo.tuyoo.0-hall7.tuyoo.dj',
        'IOS_3.502_tuyoo.appStore.0-hall7.appStore.kuaile',
        'IOS_3.501_tuyoo.appStore.0-hall7.tuyoo.cherry',
    ],
    "hall_game_3_6":[
        "Android_3.60_360.360.0-hall6.360.people", 
        "Android_3.60_360.360.0-hall6.360.fk",
        "Android_3.60_360.360.0-hall6.360.day", 
        "IOS_3.60_360.360.0-hall6.360.day",
        "Android_3.61_360.360.0-hall6.360.day",
        'Android_3.70_360.360.0-hall6.360.day',
        'IOS_3.70_360.360.0-hall6.360.day',
        'Android_3.601_360.360.0-hall6.360.dj',
    ],
    "hall_game_3_6_ddz_pc": [
        "IOS_3.60_360.360.0-hall8.360.pcddz",
    ],
    "hall_game_texas_3_6_pc":[
        'Winpc_3.60_360.360.0-hall8.360.texas',
        #"IOS_3.60_360.360.0-hall8.360.day",  # 开发阶段用
    ],
    "hall_game_texas_3_6_phone":[
        "IOS_3.60_360.360.0-hall8.360.day",  # 开发阶段用
    ],
}

