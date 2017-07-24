# -*- coding=utf-8
'''
Created on 2016年9月23日

一条和牌结果

@author: zhaol
'''
from majiang2.player.player import MPlayerTileGang
from freetime.util import log as ftlog
from majiang2.table.table_config_define import MTDefine

class MOneResult(object):
    # 杠牌，刮风下雨
    RESULT_GANG = 1
    # 和牌
    RESULT_WIN = 2
    # 流局
    RESULT_FLOW = 3
    #杠牌和胡牌都会产生一个OneResult 在OneResult中存放winMode,番型,统计信息 每局输赢后提供数据给客户端，最后牌桌结束后一起将统计数据提供给客户端
    KEY_TYPE = 'type' #杠牌 和牌 
    KEY_NAME = 'name' #明杠 暗杠
    KEY_SCORE = 'score' #每局的分数(变化部分)统计 [seatId] = value
    KEY_WIN_MODE = 'winMode' #输赢类型 [seatId] = value
    KEY_FAN_PATTERN = 'fanPattern' #番型统计 [seatId] = value
    KEY_STAT = 'stat' # 最后大结算需要的统计数据 [seatId] = value {"desc":"自摸","value":0},{"desc":"点炮","value":0},{"desc":"明杠","value":0},{"desc":"暗杠","value":0},{"desc":"最大番数","value":2}
    KEY_AWARD_INFO = 'awardInfo'
    KEY_AWARD_SCORE = 'awardScore'
    KEY_GANG_STYLE_SCORE = 'gangStyleScore' #杠牌时，无论是否放杠，此杠型的分数，返回这个，记录在牌桌上，用于后续处理，如杠上杠、杠上炮算分
    KEY_PIAO_POINTS = 'piaoPoints'  # 玩家各自飘的分
    KEY_FLOWER_SCORES = 'flowerScores'  # 玩家各自花分
    KEY_MOZI = 'mozi'  # 摸子分(和县)
    KEY_LIANZHUANG = 'lianzhuang'
    KEY_DISPLAY_EXTEND = 'displayExtend'  # 显示额外信息，江西安徽使用

    KEY_TYPE_NAME_GANG = '杠牌'
    KEY_TYPE_NAME_HU = '和牌'
    KEY_TYPE_NAME_FLOW = '流局'
    
    # stat type
    STAT_WIN = 'win'
    STAT_ZIMO = 'ziMO'
    STAT_MOBAO = 'moBao'
    STAT_DIANPAO = 'dianPao'
    STAT_MINGGANG = 'mingGang'
    STAT_ANGANG = 'anGang'
    STAT_ZFBGANG = 'zfbGang'
    STAT_YAOJIUGANG = 'yaojiuGang'
    STAT_ExmaoGANG = 'exmaoGang'
    STAT_BaoZhongGANG = 'BaoZhongGang'
    STAT_GANG = 'gang'
    STAT_ZUIDAFAN = 'zuiDaFan'
    STAT_BANKER = 'banker'
    STAT_JIAOPAI = 'jiaopai'
    STAT_MOZI = 'mozi'  # 摸子积分
    STAT_PINGNA = 'pingna'  # 平拿积分
    STAT_QINGNA = 'qingna'  # 清水拿分

    # winMode
    WIN_MODE_CHAHUAZHU = -5
    WIN_MODE_CHADAJIAO = -4
    WIN_MODE_DIANPAO_BAOZHUANG = -3
    WIN_MODE_LOSS = -2
    WIN_MODE_DIANPAO = -1
    WIN_MODE_ZIMO = 0
    WIN_MODE_PINGHU = 1
    WIN_MODE_GANGKAI = 2
    WIN_MODE_QIANGGANGHU = 3
    WIN_MODE_WUDUIHU = 4
    WIN_MODE_TIANHU = 5
    WIN_MODE_LOUHU = 6
    WIN_MODE_baozhongbao = 7
    WIN_MODE_guadafeng = 8
    WIN_MODE_hongzhongbao = 9
    WIN_MODE_mobao = 10
    WIN_MODE_piaohu = 11
    WIN_MODE_qidui = 12
    WIN_MODE_qingyise = 13
    
    def __init__(self):
        super(MOneResult, self).__init__()
        self.__result_type = None
        # 玩法
        self.__play_mode = None
        # 庄家座位号
        self.__banker_seat_id = None
        """
        1）自摸 self.__win_seat_id == self.__last_seat_id
        2）点炮 self.__win_seat_id != self.__last_seat_id
        """
        # 获胜一方的桌子号
        self.__win_seat_id = None
        # 获胜的桌子号
        self.__win_seats = None
        # 上一轮的桌子号
        self.__last_seat_id = None
        
        """通过__table_tile_mgr获取__win_tile是否是宝牌，是否是宝中宝"""
        # 获胜牌
        self.__win_tile = None
        # 牌桌手牌管理器
        self.__table_tile_mgr = None
        # 获胜时的actionID
        self.__action_id = 0
        # 扎鸟的个数
        self.__zha_niao_count = None
        """
        1）通过获胜手牌与获胜手牌组合判断是否是夹牌
        2）通过获胜手牌组合判断是否是大扣等
        """
        # 获胜的手牌组合
        self.__win_pattern = None
        # 仅由获胜牌组合定义的番型，比如九莲宝灯，金钩和，七对等
        self.__win_pattern_type = None
        # style
        self.__style = 0
        # 结果
        self.__results = {}
        # 听牌详情
        self.__win_nodes = None
        # 报警详情
        self.__alarm_nodes = None
        # 杠开
        self.__gang_kai = False
        self.__gang_kai_last_seatId = -1
        self.__gang_kai_seatId = -1
        # 花呲
        self.__hua_ci = False
        # 宝中宝 上听后手里的刻牌为宝牌的情况
        self.__bao_zhong_bao = False
        # 听牌之后是宝牌时直接和牌
        self.__magic_after_ting = False
        # 宝牌
        self.__magics = None
        # 天胡(鸡西)
        self.__tian_hu = False
        # 无对胡(鸡西)
        self.__wu_dui_hu = False
        # 抢杠
        self.__qiang_gang = False
        # 牌桌配置
        self.__table_config = None
        # 门清状态
        self.__men_state = None
        # 听牌状态 'tingState': [0, 0, 0, 0]
        self.__ting_state = None
        # 明牌状态
        self.__ming_state = None
        # 花色状态 demo 'colorState': [1, 3, 3, 3]
        self.__color_state = None
        # 字牌状态 [[0,4,1,2,3,1,2],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]]
        # 4个玩家手上的字牌,数字代表31到37七张牌的张数
        self.__zi_state = None
        # 大风
        self.__da_feng = None
        # 大扣
        self.__da_kou = None
        # 玩家个数
        self.__player_count = 0
        
        self.__win_fan_pattern = []
        # 所有玩家的所有牌，按手牌格式的数组
        self.__player_all_tiles = []
        # 所有玩家的所有牌，合到一个数组
        self.__player_all_tiles_arr = []
        # 所有玩家手牌
        self.__player_hand_tiles = []
        # 所有玩家杠牌情况
        self.__player_gang_tiles = []
        # 飘处理器
        self.__piao_processor = None
        # 交牌积分规则
        self.__jiaopai_conf = None
        # 番型积分规则
        self.__fan_rule_conf = None
        # 玩家当前积分
        self.__cur_player_score = []
        # 玩家是否加倍
        self.__double_points = []

        # 本局玩家杠的得分信息
        self.__gang_scores = []

        self.__stat_type = {
            self.STAT_WIN: {"name":"胡牌"},
            self.STAT_ZIMO: {"name":"自摸"},
            self.STAT_MOBAO: {"name":"摸宝"},
            self.STAT_DIANPAO: {"name":"点炮"},
            self.STAT_MINGGANG: {"name": "明杠"},
            self.STAT_ANGANG: {"name": "暗杠"},
            self.STAT_BaoZhongGANG: {"name": "宝中杠"},            
            self.STAT_GANG: {"name": "杠牌"},
            self.STAT_ZUIDAFAN: {"name": "单局最佳"},
            self.STAT_BANKER: {"name": "坐庄"},
            self.STAT_JIAOPAI: {"name": "交牌计分"},
            self.STAT_MOZI: {"name": "摸子积分"},
            self.STAT_PINGNA: {"name": "平拿积分"},
            self.STAT_QINGNA: {"name": "清水拿分"},
        }
        
        # 倍数
        self.__multiple = 1
        # 杠牌上家的座位号,－1表示上家没杠牌
        self.__latest_gang_state = -1
        # 是否出牌胡,曲靖特殊胡,此时获胜牌型显示的是打出的牌
        self.__drop_hu_flag = 0
        # 抽奖用的牌(根据配置，多张)
        self.__award_tiles = []
        # 赢规则管理器
        self.__win_rule_mgr=None
        
    @property
    def doublePoints(self):
        return self.__double_points
    
    def setDoublePoints(self, points):
        self.__double_points = points

    @property
    def piaoProcessor(self):
        return self.__piao_processor
    
    def setPiaoProcessor(self, piaoProcessor):
        self.__piao_processor = piaoProcessor
        
    def isResultOK(self):
        return (self.KEY_TYPE in self.results) and (self.KEY_SCORE in self.results)
    
    @property
    def awardTiles(self):
        return self.__award_tiles
    
    def setAwardTiles(self, awardTiles):
        self.__award_tiles = awardTiles
    
    @property
    def dropHuFlag(self):
        return self.__drop_hu_flag
    
    def setDropHuFlag(self, flag):
        self.__drop_hu_flag = flag
    
    @property
    def latestGangState(self):
        return self.__latest_gang_state
    
    def setLatestGangState(self, state):
        self.__latest_gang_state = state
        
    @property
    def multiple(self):
        return self.__multiple
    
    def setMultiple(self, playerMultiple):
        self.__multiple = playerMultiple
            
    @property
    def statType(self):
        return self.__stat_type
    
    @property
    def winFanPattern(self):
        return self.__win_fan_pattern
    
    def clearWinFanPattern(self):
        self.__win_fan_pattern = []
        
    def addWinFanPattern(self, name, index):
        self.__win_fan_pattern.append([name.strip(),str(index) + "番"])

    @property
    def winRuleMgr(self):
        return self.__win_rule_mgr

    def setWinRuleMgr(self,winRuleMgr):
        self.__win_rule_mgr=winRuleMgr

    def serialize(self):
        """序列化"""
        obj = {}
        if self.playMode:
            obj['playMode'] = self.playMode
        if self.bankerSeatId:
            obj['bankerSeatId'] = self.bankerSeatId
        if self.winSeatId:
            obj['winSeatId'] = self.winSeatId
        if self.lastSeatId:
            obj['lastSeatId'] = self.lastSeatId
        if self.winTile:
            obj['winTile'] = self.winTile
        if self.actionID:
            obj['actionID'] = self.actionID
        if self.zhaNiaoCount:
            obj['zhaNiaoCount'] = self.zhaNiaoCount
        if self.winPattern:
            obj['winPattern'] = self.winPattern
        if self.winPatternType:
            obj['winPatternType'] = self.winPatternType
        if self.playerCount:
            obj['playCount'] = self.playerCount
        if self.style:
            obj['style'] = self.style
        if self.winNodes:
            obj['winNodes'] = self.winNodes
        if self.huaCi:
            obj['huaCi'] = self.huaCi
        if self.gangKai:
            obj['gangKai'] = self.gangKai
        if self.baoZhongBao:
            obj['baoZhongBao'] = self.baoZhongBao
        if self.qiangGang:
            obj['qiangGang'] = self.qiangGang
        if self.tableConfig:
            obj['tableConfig'] = self.tableConfig
        if self.menState:
            obj['menState'] = self.menState
        if self.tingState:
            obj['tingState'] = self.tingState
        if self.colorState:
            obj['colorState'] = self.colorState
        if self.daFeng:
            obj['daFeng'] = self.daFeng
        if self.daKou:
            obj['daKou'] = self.daKou
        if self.magics:
            obj['magics'] = self.magics
        if self.alarmNodes:
            obj['alarmNodes'] = self.alarmNodes
        if self.jiaoPaiConf:
            obj['jiaoPaiConf'] = self.jiaoPaiConf
        if self.fanRuleConf:
            obj['fanRuleConf'] = self.fanRuleConf
        if self.playerCurScore:
            obj['playerCurScore'] = self.playerCurScore

        ftlog.debug('MOneResult.serialize: ', obj)
        
    def unSerialize(self, obj):
        """反序列化"""
        ftlog.debug('MOneResult.unSerialize: ', obj)
        self.__play_mode = obj.get('playMode', None)
        self.__banker_seat_id = obj.get('bankerSeatId', None)
        self.__win_seat_id = obj.get('winSeatId', None)
        self.__last_seat_id = obj.get('lastSeatId', None)
        self.__win_tile = obj.get('winTile', 0)
        self.__action_id = obj.get('actionID', 0)
        self.__zha_niao_count = obj.get('zhaNiaoCount', 0)
        self.__win_pattern = obj.get('winPattern', [])
        self.__win_pattern_type = obj.get('winPatternType', 0)
        self.__player_count = obj.get('playCount', 4)
        self.__style = obj.get('style', 0)
        self.__win_nodes = obj.get('winNodes', None)
        self.__alarm_nodes = obj.get('alarmNodes', None)
        self.__jiaopai_conf = obj.get('jiaoPaiConf', None)
        self.__fan_rule_conf = obj.get('fanRuleConf', None)
        self.__hua_ci = obj.get('huaCi', False)
        self.__gang_kai = obj.get('gangKai', False)
        self.__gang_kai_last_seatId = obj.get('gangKaiLastSeatId', -1)
        self.__gang_kai_seatId = obj.get('gangKaiSeatId', -1)
        self.__bao_zhong_bao = obj.get('baoZhongBao', False)
        self.__magic_after_ting = obj.get('magicAfertTing', False)
        self.__magics = obj.get('magics', None)
        self.__tian_hu = obj.get('tianHu', False)
        self.__wu_dui_hu = obj.get('wuDuiHu', False)
        self.__qiang_gang = obj.get('qiangGang', False)
        self.__table_config = obj.get('tableConfig', None)
        self.__men_state = obj.get('menState', None)
        self.__ting_state = obj.get('tingState', None)
        self.__color_state = obj.get('colorState', None)
        self.__da_feng = obj.get('daFeng', False)
        self.__da_Kou = obj.get('daKou', False)
        self.__cur_player_score = obj.get('playerCurScore', [])
        self.__double_points = obj.get('doublePoints', [])

    @property
    def gangScores(self):
        return self.__gang_scores
    
    def setGangScores(self,gangScores):
        self.__gang_scores = gangScores

    @property
    def playerCount(self):
        return self.__player_count
    
    def setPlayerCount(self, count):
        self.__player_count = count
    
    @property
    def daFeng(self):
        return self.__da_feng
    
    def setDaFeng(self, daFeng):
        self.__da_feng = daFeng
        
    @property
    def daKou(self):
        return self.__da_feng
    
    def setDaKou(self, daKou):
        self.__da_kou = daKou
        
    @property
    def colorState(self):
        return self.__color_state
    
    def setColorState(self, color):
        self.__color_state = color
        
    @property
    def tingState(self):
        return self.__ting_state
    
    def setTingState(self, ting):
        self.__ting_state = ting
    
    @property
    def ziState(self):
        return self.__zi_state
    
    def setZiState(self, zi):
        self.__zi_state = zi    
    @property
    def menState(self):
        return self.__men_state
        
    def setMenState(self, men):
        self.__men_state = men

    @property
    def mingState(self):
        return self.__ming_state
        
    def setMingState(self, ming):
        self.__ming_state = ming

    
    @property
    def playerAllTiles(self):
        return self.__player_all_tiles
        
    def setPlayerAllTiles(self, playerAllTiles):
        self.__player_all_tiles = playerAllTiles
    
    @property
    def playerGangTiles(self):
        return self.__player_gang_tiles
        
    def setPlayerGangTiles(self, playerGangTiles):
        self.__player_gang_tiles = playerGangTiles

    @property
    def tableConfig(self):
        return self.__table_config
    
    def setTableConfig(self, config):
        self.__table_config = config

    @property
    def huaCi(self):
        return self.__hua_ci

    def setHuaCi(self, huaCi):
        self.__hua_ci = huaCi

    @property
    def gangKai(self):
        return self.__gang_kai
    
    def setGangKai(self, gangKai):
        self.__gang_kai = gangKai
        
    @property
    def gangKaiLastSeatId(self):
        return self.__gang_kai_last_seatId
    
    def setGangKaiLastSeatId(self, gangKaiLastSeatId):
        self.__gang_kai_last_seatId = gangKaiLastSeatId
        
    @property
    def gangKaiSeatId(self):
        return self.__gang_kai_seatId
    
    def setGangKaiSeatId(self, gangKaiSeatId):
        self.__gang_kai_seatId = gangKaiSeatId
        
    @property
    def baoZhongBao(self):
        return self.__bao_zhong_bao
    
    def setBaoZhongBao(self, baoZhongBao):
        self.__bao_zhong_bao = baoZhongBao 
        
    @property
    def magicAfertTing(self):
        return self.__magic_after_ting
    
    def setMagicAfertTing(self, magicAfertTing):
        self.__magic_after_ting = magicAfertTing
        
    @property
    def magics(self):
        return self.__magics
    
    def setMagics(self, magics):
        self.__magics = magics
        
    @property
    def tianHu(self):
        return self.__tian_hu
    
    def setTianHu(self, tianHu):
        self.__tian_hu = tianHu
        
    @property
    def wuDuiHu(self):
        return self.__wu_dui_hu
    
    def setWuDuiHu(self, wuDuiHu):
        self.__wu_dui_hu = wuDuiHu
        
    @property
    def qiangGang(self):
        return self.__qiang_gang
    
    def setQiangGang(self, qiangGang):
        self.__qiang_gang = qiangGang

    @property
    def winNodes(self):
        return self.__win_nodes
    
    def setWinNodes(self, wNodes):
        self.__win_nodes = wNodes

    @property
    def alarmNodes(self):
        return self.__alarm_nodes

    def setAlarmNodes(self, wNodes):
        self.__alarm_nodes = wNodes

    @property
    def jiaoPaiConf(self):
        return self.__jiaopai_conf

    def setJiaoPaiConf(self, ruleConf):
        self.__jiaopai_conf = ruleConf

    @property
    def fanRuleConf(self):
        return self.__fan_rule_conf

    def setFanRuleConf(self, ruleConf):
        self.__fan_rule_conf = ruleConf

    @property
    def playerCurScore(self):
        return self.__cur_player_score

    def setPlayerCurScore(self, score):
        self.__cur_player_score = score

    @property
    def results(self):
        return self.__results
    
    def setStyle(self, style):
        self.__style = style
        
    @property
    def style(self):
        return self.__style 
    
    def setZhaNiaoCount(self, count):
        """设置扎鸟的个数"""
        self.__zha_niao_count = count
        
    @property
    def zhaNiaoCount(self):
        return self.__zha_niao_count
        
    def setResultType(self, rType):
        """设置结算类型"""
        self.__result_type = rType
        
    @property
    def resultType(self):
        return self.__result_type
        
    def setActionID(self, actionId):
        """设置操作号"""
        ftlog.info('oneResult.setActionId now:', self.__action_id
                   , ' actionId:', actionId) 
        self.__action_id = actionId
    
    @property    
    def actionID(self):
        return self.__action_id
        
    def setBankerSeatId(self, seatId):
        """设置庄家座位号"""
        self.__banker_seat_id = seatId
        
    @property
    def bankerSeatId(self):
        return self.__banker_seat_id
        
    def setPlayMode(self, mode):
        """设置玩法"""
        self.__play_mode = mode
        
    @property
    def playMode(self):
        return self.__play_mode
        
    def setWinSeatId(self, seatId):
        """赢家座位号"""
        self.__win_seat_id = seatId
        
    @property
    def winSeatId(self):
        return self.__win_seat_id

    def setWinSeats(self, seats):
        """赢家座位号"""
        self.__win_seats = seats
        
    @property
    def winSeats(self):
        return self.__win_seats
        
    def setLastSeatId(self, seatId):
        """上家座位号"""
        self.__last_seat_id = seatId
        
    @property
    def lastSeatId(self):
        return self.__last_seat_id
        
    def setWinTile(self, wTile):
        """设置获胜手牌"""
        self.__win_tile = wTile
        
    @property
    def winTile(self):
        return self.__win_tile
     
    def setTableTileMgr(self, tableTileMgr):
        """设置手牌管理器"""
        self.__table_tile_mgr = tableTileMgr
     
    @property   
    def tableTileMgr(self):
        return self.__table_tile_mgr 
        
    def setWinPattern(self, pattern):
        """设置赢牌手牌组合"""
        self.__win_pattern = pattern

    @property
    def winPattern(self):
        return self.__win_pattern
        
    def setWinPatternType(self, wType):
        """原始番型"""
        self.__win_pattern_type = wType
        
    @property
    def winPatternType(self):
        return self.__win_pattern_type

    def calcGang(self):
        """计算杠的输赢"""
        
        #明杠暗杠统计
        resultStat = [[] for _ in range(self.playerCount)]
        
        self.__results[self.KEY_TYPE] = MOneResult.KEY_TYPE_NAME_GANG
        base = self.tableConfig.get(MTDefine.GANG_BASE, 0)
        if self.style == MPlayerTileGang.AN_GANG:
            self.__results[self.KEY_NAME] = "暗杠"
            base *= 2
            resultStat[self.winSeatId].append({MOneResult.STAT_ANGANG:1})
        else:
            self.__results[self.KEY_NAME] = "明杠"
            resultStat[self.winSeatId].append({MOneResult.STAT_MINGGANG:1})
        resultStat[self.winSeatId].append({MOneResult.STAT_GANG:1})
         
        if self.lastSeatId != self.winSeatId: #放杠
            scores = [0 for _ in range(self.playerCount)]
            scores[self.lastSeatId] = -base
            scores[self.winSeatId] = base
        else:
            scores = [-base for _ in range(self.playerCount)]
            scores[self.winSeatId] = (self.playerCount - 1) * base
        
        ftlog.debug('MOneResult.calcGang gangType:', self.__results[self.KEY_NAME], ' scores', scores)
        self.__results[self.KEY_SCORE] = scores
        self.__results[self.KEY_STAT] = resultStat
    
    def calcWin(self):
        """计算和牌的输赢"""
        pass
        
    def calcScore(self):
        """计算输赢数值"""
        pass

    def isCountByJiao(self):
        """是否是交牌"""
        return False

    def isCountByTongDi(self):
        """是否是通底"""
        return False
