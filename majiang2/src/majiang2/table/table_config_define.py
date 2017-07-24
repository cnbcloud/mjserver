# -*- coding=utf-8
'''
Created on 2016年9月23日

@author: zhaol
'''

class MTDefine(object):
    """麻将牌桌配置，room.json中的tableConfig"""
    # 用户坐下后的准备状态
    READY_AFTER_SIT = 'ready_after_sit'
    # 清一色是否可以听牌
    YISE_CAN_TING = 'qingyise_can_ting'
    # 牌池还剩多少张牌时不可点炮，只能自摸
    TILES_NO_PAO = 'tiles_no_pao'
    # 手牌张数
    HAND_COUNT = 'hand_tiles_count'
    # 手牌默认张数
    HAND_COUNT_DEFAULT = 13
    # 杠牌的默认积分
    GANG_BASE = 'gang_base'
    # 和牌的起始倍数
    WIN_BASE = 'win_base'
    # 用户的积分带入
    SCORE_BASE = 'score_base'
    # 输分最大限制
    MAX_LOSS_SCORE = 'max_loss_score'
    # 房卡支付方式 
    FANGKA_PAY = 'fangka_pay'
    # 番型对应的输赢倍数
    FAN_LIST = 'fan_list'
    # 哈麻中边牌的倍数
    BIAN_MULTI = 'bian_multi'
    # 换宝，哈麻中的换宝开关
    CHANGE_MAGIC = 'change_baopai'
    # 最小赢牌倍数
    MIN_MULTI = 'min_multi'
    # 大扣
    DA_KOU = 'da_kou'
    # 单吊算夹
    DAN_DIAO_JIA = 'dan_diao_jia'
    # 红中宝开关
    HONG_ZHONG_BAO = 'hong_zhong_bao'
    # 闭门算番(鸡西麻将默认闭门不算番)
    BI_MEN_FAN = 'bi_men_fan'
    # 天胡可选玩法
    TIAN_HU = 'tian_hu'
    # 地胡可选玩法
    DI_HU = 'di_hu'
    # 盘锦玩法
    JI_HU = 'ji_hu'
    QIONG_HU = 'qiong_hu'
    JUE_HU = 'jue_hu'
    HUI_PAI = 'hui_pai'
    #白城责任制：点炮包庄，点杠包杠
    BAOZHUANG_BAOGANG = 'baozhuang_baogang'
    #白城两头夹算单调
    LIANGTOU_JIA = 'liangtou_jia'
    # 最后兑奖算番(鸡西麻将默认最后抽奖的数量)
    AWARD_TILE_COUNT = 'award_tile_count'
    # 暗宝开关(鸡西麻将默认宝牌隐藏并且没人听牌宝牌不更新)
    MAGIC_HIDE = 'magic_hide'
    # 软19开关
    RUAN_YAO_JIU = 'ruan_yao_jiu'
    # 刮大风开关
    GUA_DA_FENG = 'gua_da_feng'
    # 对宝开关
    DUI_BAO = 'dui_bao'
    # 卡五星中频道
    PIN_DAO = 'pin_dao'
    # 卡五星中跑恰摸八
    PAOQIAMOBA = 'paoqiamoba'
    # 卡五星中定漂
    DING_PIAO = 'ding_piao'
    # 卡五星中买马
    MAI_MA = 'mai_ma'
    # 卡五星中数坎
    SHU_KAN = 'shu_kan'
    # 卡五星中听牌时亮牌规则
    LIANG_PAI = 'liang_pai'
    # 托管配置
    TRUSTTEE_TIMEOUT = 'trustee_timeout'
    NEVER_TIMEOUT = -1
    # 牌桌人数
    MAXSEATN = 'maxSeatN'
    # 无效的座位号
    INVALID_SEAT = -1
    # 最大番数
    MAX_FAN = 'max_fan'
    # 卡五星番数
    LUOSIHU_FAN = 'luosihu_fan'
    # 碰碰胡番数
    PENGPENGHU_FAN = 'pengpenghu_fan'
    #换三张
    CHANGE3TILES = 'change_3Tiles'
    # 杠上花番数
    GANGSHANGHUA_FAN = 'gangshanghua_fan'
    #对亮对翻
    DUILIANGDUIFAN = 'duiliangduifan'
    # 是否有AI
    HAS_ROBOT = 'hasrobot'
    # AI级别
    ROBOT_LEVEL = 'robotLevel'
    # 傻瓜级别，抓什么打什么，不吃不碰不杠
    ROBOT_FOOLISH = 0
    # 聪明级别，合理出牌，默认聪明级别
    ROBOT_SMART = 1
    # 牌桌类型
    TABLE_TYPE = 'tableType'
    TABLE_TYPE_NORMAL = 'normal'
    TABLE_TYPE_CREATE = 'create'
    # 牌局ID，统计使用
    TABLE_ROUND_ID = 'tableRoundId'
    # 游戏开始后，是否允许返还房卡
    RESUME_ITEM_AFTER_BEGIN = 'resume_item_after_begin'
    # 吃牌的设置，在有些玩法里，吃牌是个可选项
    CHIPENG_SETTING = 'chipengsetting'
    NOT_ALLOW_CHI = 1 # 不允许吃
    ALLOW_CHI = 2     # 允许吃
    
    GANG_SETTING = 'gangsetting'
    
    # 胡牌倍数
    MULTIPLE = 'multiple'
    MULTIPLE_MIN = 1
    MULTIPLE_MAX = 8
    # 是否飘的超时
    PIAO_ORNOT_TIMEOUT = 'piao_or_not_timeOut'
    # 是否接受飘的超时
    ACCEPT_PIAO_ORNOT_TIMEOUT = 'accept_piao_or_not_timeOut'
    # 是否飘一直等待
    PIAO_WAIT_FOREVER = 'piao_wait_forever'
    # 飘得配置
    PIAO_LIST = 'piao_list'
    # 必漂配置
    BIPIAO_POINT = 'bipiao_point'
    # 听牌后只能自摸
    ZIMO_AFTER_TING = 'zimo_after_ting'
    # 不摸不胡
    WIN_BY_ZIMO = 'win_by_zimo'
    WIN_BY_ZIMO_OK = 1
    WIN_BY_ZIMO_NO = 0
    # 牌桌定时器单位
    TABLE_TIMER = 0.2
    #潜江晃晃（必杠模式）
    BI_GANG = 'bigang'
    XIXIANGFENG = 'xixiangfeng'
    # 托管行为循环时间
    TABLE_AUTO_DECIDE_TIMER = 0.8
    # 锚蛋设置
    MAO_DAN_SETTING = 'maoDanSetting'
    MAO_DAN_NO = 0

    MAO_DAN_ZFB = 0b1      # 末尾为1 只能由中发白组成锚/蛋
    MAO_DAN_ZFB_NAME = "旋风杠"

    MAO_DAN_DNXB = 0b10     # 二进制第二位为1 只能由东南西北组成锚/蛋
    MAO_DAN_DNXB_NAME = "风锚"

    MAO_DAN_DNXBZFB = 0b100 # 二进制第三位为1 可以由东南西北中发白组成锚/蛋
    MAO_DAN_DNXBZFB_NAME = "乱锚"

    MAO_DAN_YAO = 0b1000    # 幺蛋   8
    MAO_DAN_YAO_NAME = "幺蛋"

    MAO_DAN_JIU = 0b10000   # 九蛋   16
    MAO_DAN_JIU_NAME = "九蛋"
    '''
        eg: 0x11 可以由中发白/或者东南西北组成锚/蛋
        1）乱锚时， maoDanSetting = 4
        2）不乱锚时
        2.1）只有中发白 maoDanSetting = 1
        2.2）只有东南西北 maoDanSetting = 2
        2.3）东南西北中发白都有 maoDanSetting = 3
    '''
    MAO_DAN_FANG_TIME = 'maoDanFangSetting'
    MAO_DAN_FANG_FIRST_CARD = 1 # 第一手牌可以放蛋
    MAO_DAN_FENG_EVERY_CARD = 2 # 随时可以放蛋
    # 去掉风牌
    REMOVE_FENG_ARROW_TILES = 'remove_feng_arrow_tiles'
    # 庄家翻倍
    BANKER_DOUBLE = 'banker_double'
    # 门清翻倍
    MEN_CLEAR_DOUBLE = 'men_clear_double'
    # 二五八作将
    ONLY_JIANG_258 = 'only_jiang_258'
    # 是否乱锚
    LUAN_MAO = 'luanMao'
    # 是否自动胡
    WIN_AUTOMATICALLY = 'win_automatically'
    # 刮大风的时候计算宝牌刮大风
    GUA_DA_FENG_CALC_MAGIC = 'gua_da_feng_calc_magic'
    # 报警开关之芜湖麻将
    SWITCH_FOR_ALARM = 'switch_for_alarm'
    # 游戏结束通过玩家分数 之芜湖麻将
    OVER_BY_SCORE = 'over_by_score'
    # 交牌计算之芜湖麻将
    JIAOPAI_RULE = 'jiaopai_rule'
    # winlose响应里是否要加winModeDesc字段
    WINLOSE_WINMODE_DESC = 'winlose_need_winmode_desc'
    # winlose响应里是否要加display_extend字段
    WINLOSE_DISPLAY_EXTEND = 'winlose_need_display_extend'
    # 怀宁麻将平胡底分
    PINGHU_BASE_SCORE = 'baseScore'
    # 结算界面显示分值列表
    DISPLAY_EXTEND_TITLES = 'display_extend_titles'
    # 是否均摊房卡
    SHARE_FANGKA = 'share_fangka'
    # 加倍超时
    DOUBLE_TIMEOUT = 'double_timeOut'
    # 在摸牌前听牌
    TING_BEFORE_ADD_TILE = 'ting_before_add_tile'
    # 在游戏开始钱报听 天听
    TING_WITH_BEGIN = 'ting_with_begin'
    # 没出过牌的摸牌报听 天听
    TING_WITH_NO_DROP_TILE = 'ting_with_no_drop_tile'
    # 听的设置
    TING_SETTING = 'ting_setting',
    TING_YES = 1
    TING_NO = 0
    TING_UNDEFINE = -1
    # 漂的设置
    PIAO_SETTING = 'piao_setting',
    PIAO_YES = 1
    PIAO_NO = 0
    PIAO_UNDEFINE = -1
    # 加倍的设置
    DOUBLE_SETTING = 'double_setting'
    DOUBLE_YES = 1
    DOUBLE_NO = 0
    DOUBLE_UNDEFINE = -1
    # 被抢杠时，从被抢者手牌里移除被抢这张牌
    REMOVE_GRABBED_GANG_TILE = 'remove_grabbed_gang_tile'
    # 胡牌方式设置
    WIN_SETTING = 'win_setting'
    WIN_TYPE1 = 1 #胡牌三家付
    WIN_TYPE2 = 2 #点炮包三家
    #发牌时选择中发白
    CHOOSE_ZFB = 'nozfb'
    GANGWITHTING = 'gangWithTing'
    #modify by youjun 05.03
    JIANGDUI = "jiangdui"
    LIANGGANGMANFAN = "lianggangmanfan"
    ZIMOJIAFEN = 'zimojiafen'
    ZIMODOUBLE = 'zimoDouble'
    QINGYISEDOUBLE = 'qingyiseDouble'
    QIDUIDOUBLE = 'qiduiDouble'
    GANGSHANGPAO = 'gangshangpaoFan'
    JINGOUDIAODOUBLE = 'jingoudiaoDouble'
    YAOJIU = 'yaojiu'
    DUANYAOJIU = 'duanyaojiu'
    DIANGANGHUA = 'dianganghua'
    # 血战中定缺
    DING_QUE = 'ding_que'
    HUJIAOZHUANYI = 'hujiaozhuanyi'
    GANGSHANGGANG = 'gangshanggang'
    QINGHUNYISE = 'qinghunyise'
    JINQUEKAIKOU ='jinquekaikou'
    DANDIAOSHENGJIN='dandiaoshengjin'
    FANGHU = 'fangHu'
    LIANZHUANGJIAJU = 'lianzhuangjiaju'
    def __init__(self):
        super(MTDefine, self).__init__()
