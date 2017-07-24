# -*- coding=utf-8
'''
Created on 2016年9月23日
麻将核心玩法中用到的玩家对象
@author: zhaol
'''
from majiang2.player.hand.hand import MHand
from majiang2.tile.tile import MTile
import copy
from majiang2.table_state.state import MTableState
from majiang2.table_tile.table_tile import MTableTile
from majiang2.win_rule.win_rule import MWinRule
from freetime.util import log as ftlog
from majiang2.table.table_config_define import MTDefine
from majiang2.ai.play_mode import MPlayMode

class MPlayerTileMao(object):
    """锚牌"""
    def __init__(self, pattern, actionId, maoDanType):
        super(MPlayerTileMao, self).__init__()
        self.__pattern = pattern
        self.__actionId = actionId
        self.__mao_type = maoDanType
        
    def copyData(self):
        data = {}
        data['pattern'] = self.pattern
        data['type'] = self.maoType
        data['action_id'] = self.actionId
        return data
    
    def extendTile(self, tile):
        self.pattern.append(tile)
        
    @property
    def actionId(self):
        return self.__actionId
    
    def setActionId(self, actionId):
        ftlog.info('player.setActionId now:', self.__actionId
                   , ' actionId:', actionId) 
        self.__actionId = actionId
        
    @property
    def pattern(self):
        return self.__pattern
    
    def setPattern(self, pattern):
        self.__pattern = pattern
        
    @property
    def maoType(self):
        return self.__mao_type
    
    def setMaoType(self, maoType):
        self.__mao_type = maoType
        
class MPlayerTileChi(object):
    """玩家手牌的吃牌"""
    def __init__(self, tile, pattern, actionId):
        super(MPlayerTileChi, self).__init__()
        self.__tile = tile
        self.__pattern = pattern 
        self.__actionId = actionId
        
    @property
    def tile(self):
        return self.__tile
    
    @property
    def pattern(self):
        return self.__pattern
    
    def setPattern(self, newPattern):
        """设置吃牌组"""
        self.__pattern = newPattern
    
    @property
    def actionID(self):
        return self.__actionId
    
class MPlayerTilePeng(object):
    """玩家手牌的吃牌"""
    def __init__(self, tile, pattern, actionId):
        super(MPlayerTilePeng, self).__init__()
        self.__tile = tile
        self.__pattern = pattern 
        self.__actionId = actionId
        
    @property
    def tile(self):
        return self.__tile
    
    @property
    def pattern(self):
        return self.__pattern
    
    def setPattern(self, newPattern):
        """设置牌组"""
        self.__pattern = newPattern
    
    @property
    def actionID(self):
        return self.__actionId

class MPlayerTileGang(object):
    MING_GANG = 1
    AN_GANG = 0
    ZFB_GANG =2
    YAOJIU_GANG =3
    EXMao_GANG =4
    CHAOTIANXIAO_MING=6# 明杠朝天笑
    CHAOTIANXIAO_AN=7#暗杠朝天笑
    BaoZhong_MING_GANG =8
    BaoZhong_AN_GANG =9
    """玩家手牌的吃牌"""
    def __init__(self, tile, pattern, actionId, style):
        super(MPlayerTileGang, self).__init__()
        self.__tile = tile
        self.__pattern = pattern 
        self.__actionId = actionId
        self.__gang_style = style
        self.__gang_style_score = None
     
    def isMingGang(self):
        """是否明杠"""
        return self.__gang_style == self.MING_GANG
        
    @property
    def tile(self):
        return self.__tile
    
    @property
    def pattern(self):
        return self.__pattern
    
    def setPattern(self, pattern):
        """设置碰牌组"""
        self.__pattern = pattern
    
    @property
    def actionID(self):
        return self.__actionId 
    
    @property
    def style(self):
        return self.__gang_style

    @property
    def styleScore(self):
        return self.__gang_style_score

    def setStyleScore(self, score):
        """设置分数，这个是按照杠型计算的分数，与赔付关系无关"""
        self.__gang_style_score = score

class MPlayerTileAlarm(object):
    QINGORHUN_ALARM = 1   #清一色或混一色报警
    DOUBLEEIGHT_ALARM = 2 #双八支报警
    DOUBLEFOUR_ALARM = 3  #双四核报警

    """
    玩家报警信息： 存储每个玩家报警的方式，可能由多个
    记录每个碰对应出牌人的id，碰影响结算，如果结算时没有1的报警，可忽略pattern
    """
    def __init__(self, tile, pattern, style):
        super(MPlayerTileAlarm, self).__init__()
        self.__tile = tile
        self.__pattern = pattern #[{"pattern":[1,1,1],"seatId":1}]
        self.__alarm_style = style

    @property
    def tile(self):
        return self.__tile

    @property
    def pattern(self):
        return self.__pattern

    @property
    def style(self):
        return self.__alarm_style

    def setPattern(self, pattern):
        """设置碰牌组"""
        self.__pattern = pattern

class MPlayer(object):
    """
    麻将的玩家类
    本类主要描述一下几种信息
    1）玩家的个人信息，包括姓名，性别，userId，积分等等
    2）手牌，包括握在手里的牌，吃牌，碰牌，杠牌
    3）打牌行为的响应，是否吃牌，是否碰牌，是否杠牌，是否胡牌，是否过胡翻倍
    """
    
    """玩家游戏状态，只关心用户的游戏状态，用户的准备状态由继承框架TYTable的MajiangTable来处理
    """

    # 用户刚坐下，需要点击准备按钮
    PLAYER_STATE_NORMAL = 'sit'
    # 用户已准备
    PLAYER_STATE_READY = 'ready'
    # 用户在游戏中
    PLAYER_STATE_PLAYING = 'play'
    # 特殊的游戏状态，听牌状态
    PLAYER_STATE_TING = 'ting'
    # 特殊的游戏状态，明牌状态
    PLAYER_STATE_MING = 'ming'
    # 特殊的游戏状态，用户已经和牌
    PLAYER_STATE_WON = 'win'
    # 前台
    FORE_GROUND = 1
    # 后台
    BACK_GROUND = 0

    
    def __init__(self, name, sex, userId, score, purl = '', coin = 0, clientId = ''):
        super(MPlayer, self).__init__()
        # 1 姓名
        self.__name = name
        # 2 性别
        self.__sex = sex
        self.__purl = purl
        self.__coin = coin
        # 3 用户ID
        self.__userId = userId
        self.__clientId = clientId
        # 5 手牌
        self.__hand_tiles = []
        # 6 吃牌
        self.__chi_tiles = []
        # 7 碰牌
        self.__peng_tiles = []
        # 8 杠牌
        self.__gang_tiles = []
        # 9 报警
        self.__alarm_info = []
        #这个与上面的区别是存的是字典，包括打牌的人id，如果碰被杠了，不影响该数组{"pattern":[1,1,1],"seatId":1}
        self.__peng_tiles_for_alarm = []
        # 10 和牌，血流有多次胡牌的设计
        self.__hu_tiles = []
        # 和牌自摸，放炮标记
        self.__hu_modes = []
        # 粘牌 鸡西玩法 粘之后存储在player中 下发协议时用来塞选手牌
        self.__zhan_tiles = []
        # 听牌同时亮牌，需要等待杠的牌，扣下来
        self.__kou_tiles = []
        # 听牌同时亮牌，亮牌列表
        self.__ting_liang_tiles = []
        # 放锚的牌
        self.__mao_tiles = []
        # 11 状态
        self.__state = self.PLAYER_STATE_NORMAL
        # 12 当前手牌
        self.__cur_tile = 0
        # 13 座位号
        self.__cur_seat_id = -1
        # 14 定缺
        self.__absence_color = MTile.TILE_NONE
        # 15 托管
        self.__auto_decide = False
        # 听牌方案
        self.__win_nodes = []
        # 听牌同时亮牌，操作id
        self.__ting_liang_actionId = None
        # 听牌同时亮牌，要胡的牌，同时也是其他人不能打牌
        self.__ting_liang_winTiles = []
        # 用户离线状态
        self.__online_state = 1
        # 用户离开状态
        self.__back_fore_state = 1
        # 赖子（潜江晃晃）
        self.__laizi=[]
        # 赖子杠（潜江晃晃）
        self.__laiziGang=[]
        # 马牌（潜江晃晃）
        self.__ma_tiles = []
        # 赖子皮(潜江晃晃）
        self.__laiziPi=[]
        #赖子杠补牌
        self.__laiziGangBuTile=0
        # 牌码底分
        self.__cur_score = None
        # 交牌底分
        self.__cur_jiao_score = None
        # 通底底分
        self.__cur_tongdi_score = None
        # 摸子分
        self.__mozi_score = 0
        # 平拿分
        self.__pingna_score = 0
        # 清水拿分
        self.__qingshui_score = 0
        #吃牌吃哪张
        self.__chi_tiles_with_tile = []
        #碰牌来自谁
        self.__peng_tiles_from_seat=[]
        #杠牌来自谁
        self.__gang_tiles_from_seat=[]
        # 花牌
        self.__flowers = []
        # 花分
        self.__flower_scores = 0
        # 过碰的哪些牌，过碰期间的牌不可再碰
        self.__guo_peng_tiles = set()
        # 过胡分数，过胡期间需要出现分数更大的番才能胡
        self.__guo_hu_point = -1
        # 连杠次数
        self.__lian_gang_nums = set()  # 曾经的多次连杠次数
        self.__cur_lian_gang_num = -1  # 当前连杠次数
        # 每次吃碰的对象座位ID, 辅助计算怀宁的多次喂牌的计分惩罚
        self.__chipengSeats = []
        # 能胡牌时，胡牌番型
        self.__winTypes = []
        # 能胡牌时，胡牌附加分类型
        self.__winExtendTypes = []
        # 能胡牌时，胡牌分数点集合
        self.__winPoints = []  # 怀宁：花，明杠，暗杠，连杠，明杠风，暗杠风，胡分数
        self.__totalWinPoint = 0  # 总的可胡牌分
        self.__penaltyPoints = []  # 胡牌时，额外的对恶意喂牌行为的惩罚分点。按座位id从0，1，2，3
        # 打出过的牌数
        self.__dropNum = 0
        # 听牌结果
        self.__ting_result = []
        #已经和牌的标记,用于血战
        self.__has_hu = False
        #血战用户的和牌顺序
        self.__xuezhan_rank = 100
	self.__limit_tiles = []
	self.__jinkanState = False
	self.__jinkanDrop = []
	self.__win_mode = 0

    def reset(self):
        """重置
        """
        self.__hand_tiles = []
        self.__chi_tiles = []
        self.__peng_tiles = []
        self.__gang_tiles = []
        self.__alarm_info = []
        self.__hu_tiles = []
        self.__hu_modes = []
        self.__zhan_tiles = []
        self.__kou_tiles = []
        self.__mao_tiles = []
        self.__ma_tiles = []
        self.__state = self.PLAYER_STATE_NORMAL
        self.__cur_tile = 0
        self.__win_nodes = []
        self.__ting_liang_tiles = []
        self.__ting_liang_actionId = None
        self.__ting_liang_winTiles = []
        self.__laizi=[] 
        self.__laiziGang=[]
        self.__laiziPi=[]
        #吃牌吃哪张
        self.__chi_tiles_with_tile = []
        self.__peng_tiles_from_seat=[]
        self.__gang_tiles_from_seat=[]
        self.__laiziGangBuTile=0
        self.__flowers = []
        self.__flower_scores = 0
        self.resetGuoPengTiles()
        self.resetGuoHuPoint()
        self.resetLianGangData()
        self.resetWinTypes()
        self.resetWinExtendTypes()
        self.resetWinPoints()
        self.resetTotalWinPoint()
        self.__chipengSeats = []
        self.__penaltyPoints = []
        self.__peng_tiles_for_alarm = []
        self.__dropNum = 0
        self.__ting_result = []
        self.__mozi_score = 0
        self.__pingna_score = 0
        self.__qingshui_score = 0
        self.__has_hu = False
        #self.__xuezhan_rank = 100
        self.__absence_color = MTile.TILE_NONE
	self.__limit_tiles = []
	self.__jinkanState = False
	self.__jinkanDrop = []
	self.__win_mode = 0

    @property
    def winMode(self):
        return self.__win_mode

    def setWinMode(self,winMode):
        self.__win_mode = winMode

    @property
    def limitTiles(self):
        return self.__limit_tiles

    @property
    def xuezhanRank(self):
        return self.__xuezhan_rank
    
    def setXuezhanRank(self, xuezhanRank):
	ftlog.debug('MPlayer.setXuezhanRank seatId',self.curSeatId,xuezhanRank,self.__xuezhan_rank)
        self.__xuezhan_rank = xuezhanRank

    @property
    def hasHu(self):
        return self.__has_hu
    
    def setHasHu(self, hasHu):
        self.__has_hu = hasHu

    @property
    def tingResult(self):
        return self.__ting_result

    def setTingResult(self, tingResult):
        self.__ting_result = tingResult

    @property
    def name(self):
        """获取名称"""
        return self.__name
    
    @property
    def maoTiles(self):
        return self.__mao_tiles
    
    def setMaoTiles(self, maoTiles):
        self.__mao_tiles = maoTiles
    
    @property
    def clientId(self):
        return self.__clientId
    
    @property
    def winNodes(self):
        """获取听牌方案
        例子：
        [{'winTile': 1, 'winTileCount': 3, 'pattern': [[6, 6], [5, 6, 7], [4, 5, 6], [1, 2, 3]]}
        """
        return self.__win_nodes
    
    def setWinNodes(self, winNodes):
        """设置听牌信息"""
        self.__win_nodes = winNodes
    
    @property
    def sex(self):
        """获取用户性别"""
        return self.__sex
    
    @property
    def purl(self):
        """获取用户头像"""
        return self.__purl
    
    @property
    def coin(self):
        """获取用户金币"""
        return self.__coin
    
    @property
    def curTile(self):
        """当前手牌"""
        return self.__cur_tile
    
    @property
    def curSeatId(self):
        """玩家当前座位号"""
        return self.__cur_seat_id
    
    def setSeatId(self, seat):
        """设置座位号"""
        self.__cur_seat_id = seat

    @property
    def curScore(self):
        """玩家当前某个底的分数"""
        return self.__cur_score

    def getCurScoreByBaseCount(self, index):
        """玩家当前某个底的分数"""
        return self.__cur_score[index-1]

    def setScore(self, score, index):
        """设置分数"""
        self.__cur_score[index-1] = score

    def initScores(self, score, times):
        """设置分数"""
        self.__cur_score = [ score for _ in range(times) ]
        self.__cur_jiao_score = [0 for _ in range(times)]
        self.__cur_tongdi_score = [0 for _ in range(times)]

    def getCurJiaoScoreByBaseCount(self, index):
        """玩家当前某个底的交牌分数"""
        return self.__cur_jiao_score[index-1]

    def setJiaoScore(self, score, index):
        """设置交牌分数"""
        self.__cur_jiao_score[index-1] = score

    def getCurTongDiScoreByBaseCount(self, index):
        """玩家当前某个底的通底分数"""
        return self.__cur_tongdi_score[index - 1]

    def setTongDiScore(self, score, index):
        """设置通底分数"""
        self.__cur_tongdi_score[index - 1] = score

    @property
    def moziScore(self):
        return self.__mozi_score

    @moziScore.setter
    def moziScore(self, value):
        self.__mozi_score = value

    @property
    def pingnaScore(self):
        return self.__pingna_score

    @pingnaScore.setter
    def pingnaScore(self, value):
        self.__pingna_score = value

    @property
    def qingshuiScore(self):
        return self.__qingshui_score

    @qingshuiScore.setter
    def qingshuiScore(self, value):
        self.__qingshui_score = value

    @property
    def curOnlineState(self):
        """玩家当前在线状态"""
        return self.__online_state
    
    @property
    def backForeState(self):
        '''
        玩家当前的离开状态
        '''
        return self.__back_fore_state
    
    def setBackForeState(self, state):
        '''
        设置玩家当前的离开状态
        '''
        self.__back_fore_state = state
    
    def setOffline(self):
        """设置用户离线"""
        self.__online_state = 0
    
    @property
    def laizi(self):
        """赖子潜江晃晃"""
        return self.__laizi

    def setLaizi(self,laizi):
        """设置赖子"""
        self.__laizi.append(laizi)
    
    @property
    def laiziPi(self):
        """赖子皮潜江晃晃"""
        return self.__laiziPi

    def setLaiziPi(self,laiziPi):
        """设置赖子皮"""
        self.__laiziPi.append(laiziPi)
    
    @property
    def laiziGang(self):
        """赖子潜江晃晃"""
        return self.__laiziGang

    def setLaiziGang(self,laiziGang):
        """设置赖子"""
        self.__laiziGang.append(laiziGang)
    
    @property
    def laiziGangBuTile(self):
        """赖子潜江晃晃"""
        return self.__laiziGangBuTile

    def setLaiziGangBuTile(self,tile):
        """设置赖子补牌"""
        self.__laiziGangBuTile=tile

    def setOnline(self):
        """设置用户在线"""
        self.__online_state = 1
    
    @property
    def userId(self):
        """获取用户ID"""
        return self.__userId
    
    @property
    def handTiles(self):
        """获取手牌"""
        return self.__hand_tiles
    
    @property
    def maTiles(self):
        """获取手牌"""
        return self.__ma_tiles

    def setMaTiles(self,maTile):
        """设置马牌（潜江晃晃"""
        self.__ma_tiles.append(maTile)

    @property
    def chiTiles(self):
        """获取吃牌"""
        return self.__chi_tiles

    @property
    def pengTiles(self):
        """获取听牌"""
        return self.__peng_tiles
    
    @property
    def gangTiles(self):
        """获取暗杠牌"""
        return self.__gang_tiles

    @property
    def chiTilesWithTile(self):
        return self.__chi_tiles_with_tile

    @property
    def pengTilesFromSeat(self):
        return self.__peng_tiles_from_seat

    @property
    def gangTilesFromSeat(self):
        return self.__gang_tiles_from_seat

    @property
    def pengTilesForAlarm(self):
        """获取碰牌杠牌"""
        return self.__peng_tiles_for_alarm

    @property
    def alarmInfo(self):
        """获取报警消息"""
        return self.__alarm_info

    @property
    def dropNum(self):
        return self.__dropNum

    @dropNum.setter
    def dropNum(self, value):
        self.__dropNum = value

    @property
    def huTiles(self):
        """胡牌"""
        return self.__hu_tiles

    @property
    def huModes(self):
        """胡牌mode"""
        return self.__hu_modes
    
    @property
    def zhanTiles(self):
        """粘牌"""
        if self.__zhan_tiles:
            zhanTiles = []
            zhanTiles.append(self.__zhan_tiles)
            return zhanTiles
        else:
            return self.__zhan_tiles
    
    def setZhanTiles(self, zhanSolution):
        self.__zhan_tiles = zhanSolution

    @property
    def tingLiangTiles(self):
        """听牌亮牌的牌列表"""
        return self.__ting_liang_tiles

    @property
    def tingLiangTilesCurrent(self):
        """听牌亮牌的牌列表,舍掉扣牌"""
        tingLiangTilesCurrent = copy.deepcopy(self.tingLiangTiles)
        kouTiles = []
        for kouPattern in self.__kou_tiles:
            for kouTile in kouPattern:
                kouTiles.append(kouTile)
                break
        for gangObj in self.__gang_tiles:
            for gangTile in gangObj.pattern:
                if gangTile in kouTiles and gangTile in tingLiangTilesCurrent:
                    tingLiangTilesCurrent.remove(gangTile)
        return tingLiangTilesCurrent

    @property
    def tingLiangActionID(self):
        """听牌亮牌时的actionId，后面用来确认谁先亮牌"""
        return self.__ting_liang_actionId

    @property
    def tingLiangWinTiles(self):
        """听牌亮牌要胡的牌列表，也是对方禁止打的牌的列表"""
        return self.__ting_liang_winTiles

    @property
    def kouTiles(self):
        """听牌亮牌时候，需要扣掉的手牌，听牌的时候就可以杠牌了"""
        return self.__kou_tiles

    @property
    def jinkanState(self):
        return self.__jinkanState

    @property
    def jinkanDrop(self):
        return self.__jinkanDrop

    def setJinkanDrop(self,jinkanDrop = []):
        self.__jinkanDrop = jinkanDrop

    @property
    def state(self):
        """获取当前玩家状态"""
        return self.__state

    #modify by yj 05.08 有定缺玩法的缺门记录
    @property
    def absenceColor(self):
        """获取定缺花色"""
        return self.__absence_color

    def setAbsenceColor(self,color):
        self.__absence_color = color

    @property
    def autoDecide(self):
        """是否托管"""
        return self.__auto_decide

    @property
    def flowers(self):
        """花牌"""
        return self.__flowers

    def addFlowers(self,flower_tile):
        self.__flowers.append(flower_tile)

    @property
    def flowerScores(self):
        return  self.__flower_scores

    def addFlowerScores(self,score):
        self.__flower_scores += score

    @property
    def guoPengTiles(self):
        """过碰牌集合"""
        return self.__guo_peng_tiles

    def resetGuoPengTiles(self):
        """重置过碰牌集合，每次出牌要重置"""
        self.guoPengTiles.clear()

    @property
    def guoHuPoint(self):
        """过胡分数"""
        return self.__guo_hu_point

    @guoHuPoint.setter
    def guoHuPoint(self, value):
        """设置过胡分数"""
        self.__guo_hu_point = value

    def resetGuoHuPoint(self):
        """重置过胡分数，每次摸牌出牌要重置"""
        self.guoHuPoint = -1

    @property
    def curLianGangNum(self):
        """连杠次数"""
        return self.__cur_lian_gang_num

    @curLianGangNum.setter
    def curLianGangNum(self, value):
        """设置连杠次数"""
        self.__cur_lian_gang_num = value

    def maxLianGangNum(self):
        """本局里玩家的最大连杠次数"""
        num = self.__cur_lian_gang_num
        if len(self.__lian_gang_nums) > 0:
            num = max(num, max(self.__lian_gang_nums))

        return num if num >= 0 else 0

    def recordAndResetLianGangNum(self):
        """记录连杠次数，每次出牌要判断，记录并重置"""
        if self.curLianGangNum != -1:
            self.__lian_gang_nums.add(self.curLianGangNum)
            self.curLianGangNum = -1

    def resetLianGangData(self):
        """重置连杠数据，每次开局要重置"""
        self.__lian_gang_nums.clear()
        self.__cur_lian_gang_num = -1

    @property
    def winTypes(self):
        """胡牌番型列表"""
        return self.__winTypes

    @winTypes.setter
    def winTypes(self, value):
        self.__winTypes = value

    def resetWinTypes(self):
        del self.__winTypes[:]

    @property
    def winExtendTypes(self):
        """胡牌附加分类型列表"""
        return self.__winExtendTypes

    @winExtendTypes.setter
    def winExtendTypes(self, value):
        self.__winExtendTypes = value

    def resetWinExtendTypes(self):
        del self.__winExtendTypes[:]

    @property
    def winPoints(self):
        """胡牌分数集合：各种分相加，花牌分，杠分等等"""
        return self.__winPoints

    @winPoints.setter
    def winPoints(self, value):
        self.__winPoints = value

    def resetWinPoints(self):
        del self.__winPoints[:]

    @property
    def totalWinPoint(self):
        """胡牌总分"""
        return self.__totalWinPoint

    @totalWinPoint.setter
    def totalWinPoint(self, value):
        self.__totalWinPoint = value

    def resetTotalWinPoint(self):
        self.__totalWinPoint = 0

    @property
    def chipengSeats(self):
        return self.__chipengSeats

    @property
    def penaltyPoints(self):
        return self.__penaltyPoints

    @penaltyPoints.setter
    def penaltyPoints(self, value):
        self.__penaltyPoints = value

    def setAutoDecide(self, value):
        """设置是否托管
        参数
        1）value，托管设置
        True 托管
        False 不托管
        """
        ftlog.debug('MPlayer.setAutoDecide value:', value
                , ' player:', self.name
                , ' userId:', self.userId)
        self.__auto_decide = value
        
    def ready(self):
        """设置准备状态"""
        ftlog.debug('MPlayer changeState to ready, userId:', self.userId
                    , ' seatId:', self.curSeatId)
        self.__state = self.PLAYER_STATE_READY
        
    def isReady(self):
        return self.__state == self.PLAYER_STATE_READY
        
    def play(self):
        """设置游戏状态"""
        ftlog.debug('MPlayer changeState to play, userId:', self.userId
                    , ' seatId:', self.curSeatId)
        self.__state = self.PLAYER_STATE_PLAYING
        
    def wait(self):
        """设置准备状态"""
        ftlog.debug('MPlayer changeState to wait, userId:', self.userId
                    , ' seatId:', self.curSeatId)
        self.__state = self.PLAYER_STATE_NORMAL
    
    def isWon(self):
        """是否和牌"""
        return self.__state == self.PLAYER_STATE_WON
    
    def isTing(self):
        """是否听牌"""
        return self.__state == self.PLAYER_STATE_TING

    def isTingLiang(self):
        """是否听牌同时亮牌"""
        if self.__ting_liang_tiles:
            return True
        else:
            return False
    
    def isMing(self):
        """是否明牌"""
        return self.__state == self.PLAYER_STATE_MING
        
    def isRobot(self):
        """是否是机器人"""
        if self.__userId < 10000:
            return True
        return False
    
    def canGang(self, gang, hasGang, _tiles, tile, winRuleMgr, magicTiles, extendInfo = {}):
        if not hasGang:
            return False
        
        if not self.isTing() and not self.isWon():
            return True
        
        tiles = copy.deepcopy(_tiles)
        tingGangMode = winRuleMgr.tableTileMgr.getTingGangMode()
        isLouHu = extendInfo.get('louhu', 0)
        if isLouHu:
            tingGangMode = MTableTile.MODE_TINGGANG_TINGKOU_LEFT

        ftlog.debug('MPlayer.canGang gang:', gang
                    , ' hasGang:', hasGang
                    , ' tiles:', tiles
                    , ' tile:', tile
                    , ' magicTiles:', magicTiles
                    , ' extendInfo:', extendInfo
                    , ' tingGangMode:', tingGangMode)
    
        if tingGangMode == MTableTile.MODE_TINGGANG_NONE:
            return False
        elif tingGangMode == MTableTile.MODE_TINGGANG_KOU:
            if [tile,tile,tile] in tiles[MHand.TYPE_PENG]:
                # 蓄杠在亮牌后，需要看是否有人胡这张牌，如果有，不能杠，否则是抢杠胡
                for player in winRuleMgr.tableTileMgr.players:
                    if player.curSeatId != self.curSeatId and tile in player.tingLiangWinTiles:
                        return False
                ftlog.debug( 'MPlayer.canGang xu gang',  [tile,tile,tile])
                return True
            if self.kouTiles:
                # 扣牌是暗杠，不会抢杠胡，可以杠牌
                for kouPattern in self.kouTiles:
                    if tile in kouPattern:
                        return True
            return False
        elif tingGangMode == MTableTile.MODE_TINGGANG_NOCHANGETING or \
                        tingGangMode == MTableTile.MODE_TINGGANG_WITH_ANGANG:

            # 当前听牌，只能暗杠
            if gang['style'] == MPlayerTileGang.MING_GANG and tingGangMode == MTableTile.MODE_TINGGANG_WITH_ANGANG:
                return False
            # 当前听牌，检查杠牌是否影响听牌，先去掉手牌中的杠牌
            if gang['style'] == MPlayerTileGang.AN_GANG:
                for tile in gang['pattern']:
                    tiles[MHand.TYPE_HAND].remove(tile)
                    
            if gang['style'] == MPlayerTileGang.MING_GANG:
                if [tile,tile,tile] in tiles[MHand.TYPE_PENG]:
                    # 蓄杠，手牌仅清掉一张牌
                    tiles[MHand.TYPE_HAND].remove(tile)
                else:
                    for tile in gang['pattern']:
                        # 这里需要考虑3张牌在手上，最后一张明杠，清掉所有手上杠牌用掉的牌
                        if tile in tiles[MHand.TYPE_HAND]:
                            tiles[MHand.TYPE_HAND].remove(tile)
            
            tiles[MHand.TYPE_GANG].append(gang)
	    
	    ftlog.debug('MPlayer.canGang winNodes',self.winNodes)
            # 加入听口，如果都能和，不改变听口结果，继续杠牌；如果改变了听口，不能杠
            for node in self.winNodes:
                winTile = node['winTile']
                tiles[MHand.TYPE_HAND].append(winTile)
                # 判断是否影响听口，一律按照自摸情况预估
                result, _,_ = winRuleMgr.isHu(tiles, winTile, True, MWinRule.WIN_BY_MYSELF, magicTiles)
		ftlog.debug('MPlayer.canGang result:',result)
                if not result:
                    return False
                tiles[MHand.TYPE_HAND].remove(winTile)

        elif tingGangMode == MTableTile.MODE_TINGGANG_TINGKOU_LEFT:
            # 当前听牌，检查杠牌是否影响听牌，先去掉手牌中的杠牌
            if gang['style'] == MPlayerTileGang.AN_GANG:
                for tile in gang['pattern']:
                    tiles[MHand.TYPE_HAND].remove(tile)

            if gang['style'] == MPlayerTileGang.MING_GANG:
                if [tile,tile,tile] in tiles[MHand.TYPE_PENG]:
                    # 蓄杠，手牌仅清掉一张牌
                    tiles[MHand.TYPE_HAND].remove(tile)
                else:
                    for tile in gang['pattern']:
                        # 这里需要考虑3张牌在手上，最后一张明杠，清掉所有手上杠牌用掉的牌
                        if tile in tiles[MHand.TYPE_HAND]:
                            tiles[MHand.TYPE_HAND].remove(tile)
            
            tiles[MHand.TYPE_GANG].append(gang)
            # 加入听口，如果都能和，不改变听口结果，继续杠牌；如果改变了听口，不能杠
            for node in self.winNodes:
                winTile = node['winTile']
                tiles[MHand.TYPE_HAND].append(winTile)
                # 判断是否影响听口，一律按照自摸情况预估
                result, _,_ = winRuleMgr.isHu(tiles, winTile, True, MWinRule.WIN_BY_MYSELF, magicTiles)
                if result:
                    return True
                tiles[MHand.TYPE_HAND].remove(winTile)

        return True

    def canAlarm(self, tiles, tile, winRuleMgr=None, magicTiles=[]):
        """是否可以报警：报警必须有碰or杠
            返回值： if True return style  else False
        """
        alarmStyle = 0

        gangTiles = []
        pengTiles = tiles[MHand.TYPE_PENG]

        for gang in tiles[MHand.TYPE_GANG]:
            gangTiles.append(gang['pattern'])

        ftlog.info('Player pengTilesForAlarm:', self.pengTilesForAlarm)
        # for tempPengTile in self.pengTilesForAlarm:
        #     pengTiles.append(tempPengTile['pattern'])

        if len(pengTiles)== 0 and len(gangTiles) == 0:
            return alarmStyle

        #取出已有的报警类型，如果已经有了，不在判断
        allAlarm = []
        for alarm in self.alarmInfo:
            allAlarm.append(alarm.style)

        ftlog.info('Player allAlarm:', allAlarm)
        # 判断双八支 同色二杠 碰另一个色
        if MPlayerTileAlarm.DOUBLEEIGHT_ALARM not in allAlarm and len(pengTiles) >= 1 and len(gangTiles) >= 2:
            isDoubleEight = 0
            gangColors = -1 #如果大于－1，就是同色二杠成立
            tileColors = []
            for gangTile in gangTiles:
                tileColor = MTile.getColor(gangTile[0])
                if tileColor not in tileColors:
                    tileColors.append(tileColor)
                else:
                    gangColors = tileColor

            for pengTile in pengTiles:
                tileColor = MTile.getColor(pengTile[0])
                if gangColors >= 0 and tileColor != gangColors:
                    isDoubleEight = 1
                    break

            if isDoubleEight:
                alarmStyle = MPlayerTileAlarm.DOUBLEEIGHT_ALARM
                tileAlarm = MPlayerTileAlarm(tile, [], alarmStyle)
                self.__alarm_info.append(tileAlarm)

        # 判断双四核 同色二连对or中间隔对
        if MPlayerTileAlarm.DOUBLEFOUR_ALARM not in allAlarm and len(pengTiles) >= 2:
            isLianDui = 0
            tempTileColors = {}
            pengPattern = []
            for pengTile in pengTiles:
                tempColor = MTile.getColor(pengTile[0])
                ftlog.info('Player tempTileColors:', tempTileColors, "tempColor:", tempColor)
                if tempColor in tempTileColors.values():
                    if tempTileColors.has_key(str(pengTile[0]+1)) or tempTileColors.has_key(str(pengTile[0]-1)) or \
                            tempTileColors.has_key(str(pengTile[0] + 2)) or tempTileColors.has_key(str(pengTile[0] - 2)):
                        isLianDui = 1
                        tempTileColors[str(pengTile[0])] = tempColor
                        for key in tempTileColors:
                            if tempTileColors[key] == tempColor and int(key) not in pengPattern:
                                pengPattern.append(int(key))
                else:
                    tempTileColors[str(pengTile[0])] = tempColor
            ftlog.info('Player pengPattern:', pengPattern)
            if isLianDui:
                alarmStyle = MPlayerTileAlarm.DOUBLEFOUR_ALARM
                tileAlarm = MPlayerTileAlarm(tile, pengPattern, alarmStyle)
                self.__alarm_info.append(tileAlarm)

        #判断清或混
        if MPlayerTileAlarm.QINGORHUN_ALARM not in allAlarm and len(pengTiles)+len(gangTiles) >= 3:
            tileColors = []
            tempColor = -1
            for pengTile in pengTiles:
                tileColor = MTile.getColor(pengTile[0])
                tileColors.append(tileColor)

            for gangTile in gangTiles:
                tileColor = MTile.getColor(gangTile[0])
                tileColors.append(tileColor)

            #找出关键的颜色
            arrTiles = MTile.changeTilesToValueArr(tileColors)
            for color in range(len(arrTiles)):
                if arrTiles[color] >= 2:
                    tempColor = color

            pengs = []
            for pengTile in pengTiles:
                tileColor = MTile.getColor(pengTile[0])
                if tileColor == tempColor or MTile.TILE_FENG == tileColor:
                    pengs.append(pengTile)

            for gangTile in gangTiles:
                tileColor = MTile.getColor(gangTile[0])
                if tileColor == tempColor or MTile.TILE_FENG == tileColor:
                    pengs.append(gangTile)

            if len(pengs) >= 3:
                pengPattern = []
                for pengTile in self.__peng_tiles_for_alarm:
                    tileColor = MTile.getColor(pengTile['pattern'][0])
                    if tileColor == tempColor or MTile.TILE_FENG == tileColor:
                        pengPattern.append(pengTile)

                ftlog.info('Player tileColors:', tileColors, "pengPattern:", pengPattern)
                alarmStyle = MPlayerTileAlarm.QINGORHUN_ALARM
                tileAlarm = MPlayerTileAlarm(tile, pengPattern, alarmStyle)
                self.__alarm_info.append(tileAlarm)

        return alarmStyle

    def copyHandTiles(self):
        """拷贝手牌
        返回值： 数组
        """
        return copy.deepcopy(self.__hand_tiles)
    
    def copyChiArray(self):
        """拷贝吃牌，二位数组"""
        allChi = []
        for chiObj in self.__chi_tiles:
            allChi.append(chiObj.pattern)
        return copy.deepcopy(allChi)
        
    def copyPengArray(self):
        """拷贝所有的碰牌"""
        allPeng = []
        for pengObj in self.__peng_tiles:
            allPeng.append(pengObj.pattern)
        return allPeng
    
    def copyTingArray(self):
        """拷贝听牌数组"""
        return copy.deepcopy(self.tingResult)
    
    def copyGangArray(self):
        """拷贝杠牌"""
        allGangPattern = []
        for gangObj in self.__gang_tiles:
            gang = {}
            gang['pattern'] = gangObj.pattern
            gang['style'] = gangObj.style
            gang['actionID'] = gangObj.actionID
            if gangObj.styleScore:
                gang['styleScore'] = gangObj.styleScore
            allGangPattern.append(gang)
        return allGangPattern
    
    def copyHuArray(self):
        """拷贝和牌"""
        return copy.deepcopy(self.__hu_tiles)

    def copyHuModeArray(self):
        """拷贝和牌"""
        return copy.deepcopy(self.__hu_modes)
    
    def copyMaoTile(self):
        """拷贝锚牌"""
        allMaos = []
        for maoObj in self.maoTiles:
            mao = maoObj.copyData()
            allMaos.append(mao)
        ftlog.debug('MPlayer.copyMaoTile allMaos:', allMaos)
        return allMaos

    def getMaoTypes(self):
        """获取已有的锚/蛋类型"""
        maoType = 0
        for maoObj in self.maoTiles:
            maoType = maoType | maoObj.maoType
        return maoType

    def getPengMaoTypes(self):
        """获取碰、杠区有的锚/蛋类型"""
        maoType = 0
        for pengobj in self.pengTiles:
            if MTile.isFeng( pengobj.pattern[0]):
                maoType = maoType | MTDefine.MAO_DAN_DNXB
            if MTile.isArrow( pengobj.pattern[0]):
                maoType = maoType | MTDefine.MAO_DAN_ZFB

        for gangobj in self.gangTiles:
            if MTile.isFeng(gangobj.pattern[0]):
                maoType = maoType | MTDefine.MAO_DAN_DNXB
            if MTile.isArrow(gangobj.pattern[0]):
                maoType = maoType | MTDefine.MAO_DAN_ZFB

        return maoType
    
    def printTiles(self):
        """打印玩家手牌"""
        ftlog.debug('MPayer.printTiles name:', self.name, ' seatId:', self.curSeatId)
        ftlog.debug('HandTiles:', self.copyHandTiles())
        ftlog.debug('ChiTiles:', self.copyChiArray())
        ftlog.debug('PengTiles:', self.copyPengArray())
        ftlog.debug('gangTiles::', self.copyGangArray())
        ftlog.debug('WinTiles:', self.copyHuArray())
    
    def copyTiles(self):
        """拷贝玩家所有的牌
        返回值，二维数组
        索引  说明    类型
        0    手牌    数组
        1    吃牌    数组
        2    碰牌    数组
        3    明杠牌  数组
        4    暗杠牌  数组
        """
        re = [[] for _ in range(MHand.TYPE_COUNT)]
        # 手牌
        handTiles = self.copyHandTiles()
        re[MHand.TYPE_HAND] = (handTiles)
        
        # 吃牌
        re[MHand.TYPE_CHI] = self.copyChiArray()
        
        # 碰牌
        re[MHand.TYPE_PENG] = self.copyPengArray()

        # 明杠牌
        re[MHand.TYPE_GANG] = self.copyGangArray()
        
        # mao牌
        re[MHand.TYPE_MAO] = self.copyMaoTile()
        
        # 和牌
        re[MHand.TYPE_HU] = self.copyHuArray()

        # 最新手牌
        newestTiles = [self.__cur_tile]
        re[MHand.TYPE_CUR] = newestTiles

        re[MHand.TYPE_SHOW_FLOWERS] = self.flowers[:]

        return re
    
    """
    以下是玩家打牌的行为
    开始
    摸牌
    出牌
    明牌
    吃
    碰
    杠
    和
    """
    def actionBegin(self, handTiles):
        """开始
        参数
            handTiles - 初始手牌
        """
        self.__hand_tiles.extend(handTiles)
        self.__hand_tiles.sort()
        ftlog.info( 'Player ', self.name, ' Seat:', self.curSeatId, ' actionBegin:', self.__hand_tiles )
        
    def updateTile(self, tile, tableTileMgr):
        """更新吃牌/碰/杠牌中的宝牌"""
        magicTiles = tableTileMgr.getMagicTiles(False)
        if len(magicTiles) == 0:
            return False, None

        if tableTileMgr.canUseMagicTile(MTableState.TABLE_STATE_CHI):
            chiRe, chiData = self.updateChiTile(tile, magicTiles)
            if chiRe:
                return chiRe, chiData
            
        if tableTileMgr.canUseMagicTile(MTableState.TABLE_STATE_PENG):
            pengRe, pengData = self.updatePengTile(tile, magicTiles)
            if pengRe:
                return pengRe, pengData
            
        if tableTileMgr.canUseMagicTile(MTableState.TABLE_STATE_GANG):
            gangRe, gangData = self.updateMingGangTile(tile, magicTiles)
            if gangRe:
                return gangRe, gangData
            
        return False, None
    
    def updateChiTile(self, tile, magicTiles):
        """更新吃牌中的宝牌"""
        for chiObj in self.__chi_tiles:
            if tile in chiObj.pattern:
                continue
            
            bChanged = False
            oldPattern = copy.deepcopy(chiObj.pattern)
            newPattern = copy.deepcopy(oldPattern)
            oldTile = 0
            newTile = 0
            
            for index in range(3):
                if oldPattern[index] in magicTiles:
                    if index == 0:
                        if (oldPattern[index + 1] == (tile + 1)) or (oldPattern[index + 2] == (tile + 2)):
                            bChanged = True
                            oldTile = oldPattern[index]
                            newTile = tile
                            newPattern[index] = tile
                            break
                        
                    if index == 1:
                        if (oldPattern[index - 1] == (tile - 1)) or (oldPattern[index + 1] == (tile + 1)):
                            bChanged = True
                            oldTile = oldPattern[index]
                            newTile = tile
                            newPattern[index] = tile
                            break
                        
                    if index == 2:
                        if (oldPattern[index - 1] == (tile - 1)) or (oldPattern[index - 2] == (tile - 2)):
                            bChanged = True
                            oldTile = oldPattern[index]
                            newTile = tile
                            newPattern[index] = tile
                            break
            
            if bChanged:    
                chiObj.setPattern(newPattern)
                newData = {}
                newData['old'] = oldPattern
                newData['new'] = newPattern
                newData['type'] = 'chi'
                newData['oldTile'] = oldTile
                newData['newTile'] = newTile
                self.__hand_tiles.remove(tile)
                self.__hand_tiles.append(oldTile)
                
                return True, newData
        return False, None
            
    def updatePengTile(self, tile, magicTiles):
        """更新碰牌中的宝牌"""
        for pengObj in self.__peng_tiles:
            if tile not in pengObj.pattern:
                continue
            
            oldTile = 0
            newTile = 0
            
            newPattern = copy.deepcopy(pengObj.pattern)
            for index in range(len(newPattern)):
                if newPattern[index] in magicTiles:
                    oldTile = newPattern[index]
                    newTile = tile
                    newPattern[index] = tile
                    break
                
            ftlog.debug('MPlayer.updatePengTile newPattern:', newPattern)
            oldPattern = copy.deepcopy(pengObj.pattern)      
            pengObj.setPattern(newPattern)
            newData = {}
            newData['old'] = oldPattern
            newData['new'] = newPattern
            newData['type'] = 'peng'
            newData['newTile'] = newTile
            newData['oldTile'] = oldTile
            self.__hand_tiles.remove(tile)
            self.__hand_tiles.append(oldTile)
            return True, newData
                
        return False, None
    
    def updateMingGangTile(self, tile, magicTiles):
        """更新明杠牌中的宝牌"""
        for gangObj in self.__gang_tiles:
            if gangObj.isMingGang and (tile in gangObj.pattern):
                newPattern = copy.deepcopy(gangObj.pattern)
                oldPattern = copy.deepcopy(gangObj.pattern)
                
                oldTile = 0
                newTile = 0
                
                for index in range(4):
                    if oldPattern[index] in magicTiles:
                        newPattern[index] = tile
                        oldTile = oldPattern[index]
                        newTile = tile
                        break
                        
                gangObj.setPattern(newPattern)
                newData = {}
                
                old = {}
                old['pattern'] = oldPattern
                old['style'] = gangObj.style
                newData['old'] = old
                
                new = {}
                new['pattern'] = newPattern
                new['style'] = gangObj.style
                newData['new'] = new
                
                newData['type'] = 'gang'
                newData['oldTile'] = oldTile
                newData['newTile'] = newTile
                
                self.__hand_tiles.remove(tile)
                self.__hand_tiles.append(oldTile)
                return True, newData
                
        return False, None
        
    def actionAdd(self, tile):
        """摸牌
        加到最后，先不排序
        """ 
        ftlog.debug('actionAdd __cur_tile:',self.__cur_tile,' tile:',tile)                                                                                                     
        self.__cur_tile = tile
        self.__hand_tiles.append(tile)
        self.__hand_tiles.sort()
        ftlog.debug('Player:', self.name
                    , ' HandTiles:', self.__hand_tiles
                    , ' Seat:', self.curSeatId
                    , ' actionAdd:', tile)
        
    def canDropTile(self, tile, playMode):
        if tile not in self.handTiles:
            return False, 'TILE NOT IN HAND!!'
        
        for maoObj in self.maoTiles:
            if maoObj.maoType == MTDefine.MAO_DAN_ZFB:
                if tile >= MTile.TILE_HONG_ZHONG and tile <= MTile.TILE_BAI_BAN:
                    return False, '您已经下箭锚，该张手牌只能补锚，请重新选择出牌'

            if maoObj.maoType == MTDefine.MAO_DAN_DNXB:
                if tile >= MTile.TILE_DONG_FENG and tile <= MTile.TILE_BEI_FENG:
                    return False, '您已经下风锚，该张手牌只能补锚，请重新选择出牌'

            if maoObj.maoType == MTDefine.MAO_DAN_DNXBZFB:
                if tile >= MTile.TILE_DONG_FENG and tile <= MTile.TILE_BAI_BAN:
                    return False, '您已经下乱锚，该张手牌只能补锚，请重新选择出牌'

        return True, 'OK'

    def actionDrop(self, tile):
        """出牌
        """
        if tile not in self.handTiles:
            ftlog.error('Player：', self.name
                        , ' Seat:', self.curSeatId
                        , ' actiondrap dropTile:', tile
                        , ' handTile:', self.handTiles
                        , ' BUT TILE NOT IN HANDTILES!!!')
            return False

        self.dropNum += 1
        self.handTiles.remove(tile)
        # 手牌排序
        self.__limit_tiles = []
        self.handTiles.sort()
        ftlog.debug('Player:', self.name, ' Seat:', self.curSeatId, ' actionDrop:', tile )
        return True
    
    def actionMing(self):
        """明牌
        明牌后，别人可看到此人的手牌
        """
        ftlog.debug('MPlayer changeState to ming, userId:', self.userId
                    , ' seatId:', self.curSeatId)
        self.__state = self.PLAYER_STATE_MING
        ftlog.debug( 'Player:', self.name, ' Seat:', self.curSeatId, ' actionMing' )
    
    def actionChi(self, handTiles, chiTile, actionId, targetSeat=None):
        """吃
        参数：
            handTiles - 自己的手牌，跟chiTile组成吃牌组
            chiTile - 被吃的牌，跟handTiles组成吃牌组
        """
        ftlog.debug('actionChi handTiles:', handTiles, ' chiTile:', chiTile)
        for tile in handTiles:
            if tile not in self.__hand_tiles:
                ftlog.debug( 'chi error tile:', tile )
                return False
            self.__hand_tiles.remove(tile)
        
        chiTileObj = MPlayerTileChi(chiTile, handTiles, actionId)    
        self.__chi_tiles.append(chiTileObj)
	self.chiTilesWithTile.append(chiTile)
	self.afterChiTilesLimit(chiTileObj.tile,chiTileObj.pattern)
        self.__hand_tiles.sort()
        if targetSeat is not None:
            self.chipengSeats.append(targetSeat)
        self.resetGuoHuPoint()
        ftlog.debug( 'Player:', self.name, ' Seat:', self.curSeatId, ' actionChi:', chiTile )
        return True

    def afterChiTilesLimit(self,tile,pattern):
        if tile not in pattern:
            return

	if not len(self.__hand_tiles) > 2:
            return
	pattern.sort()	
        if tile == pattern[0]:
            self.__limit_tiles.append(tile)
            if (tile+3)/10 == tile/10:
                self.__limit_tiles.append(tile+3)
        elif tile == pattern[1]:
            self.__limit_tiles.append(tile)
        elif tile == pattern[2]:
            self.__limit_tiles.append(tile)
            if (tile-3)/10 == tile/10:
                self.__limit_tiles.append(tile-3)
	ftlog.debug('Player.afterChiTilesLimit:',tile,' pattern=',pattern)
	ftlog.debug('Player.afterChiTilesLimit:',self.curSeatId,' self.__limit_tiles=',self.__limit_tiles)
    
    def actionPeng(self, pengTile, pengPattern, actionId, lastSeatId=0):
        """碰别人
        """
        for _tile in pengPattern:
            self.__hand_tiles.remove(_tile)
        
        pengTileObj = MPlayerTilePeng(pengTile, pengPattern, actionId)
        self.__peng_tiles.append(pengTileObj)
        
        self.__hand_tiles.sort()
	self.__limit_tiles.append(pengTile)	
        alarmPeng = {"pattern":pengPattern,"seatId":lastSeatId}
        self.pengTilesForAlarm.append(alarmPeng)
        self.pengTilesFromSeat.append({'tile':pengTile,'playerSeat':lastSeatId})
        self.chipengSeats.append(lastSeatId)
        self.resetGuoHuPoint()
        ftlog.debug( 'Player:', self.name, ' Seat:', self.curSeatId, ' actionPeng:', pengTile, ' alarmPeng:', self.pengTilesForAlarm )
        return True
    
    def actionZhan(self, zhanTile, zhanPattern, actionId):
        """粘别人
        """
        for _tile in zhanPattern:
            self.__hand_tiles.remove(_tile)
            break
        
        self.__zhan_tiles = zhanPattern
        
        self.__hand_tiles.sort()
        ftlog.debug( 'Player:', self.name, ' Seat:', self.curSeatId, ' actionZhan:', zhanTile )
        return True

    def actionChaoTian(self,gangPattern,gangTile,actionId,style):


        if len(gangPattern)==4:
            tmpTile=gangPattern.pop()
        handTiles = self.copyHandTiles()
        for _tile in gangPattern:
            if _tile not in handTiles:
                ftlog.debug( 'gang error gangTile =', gangTile, "handtiles=", handTiles)
                return False
            else:
                handTiles.remove(_tile)
        self.__hand_tiles = handTiles
        gangPattern.append(tmpTile)
        gangTileObj = MPlayerTileGang(gangTile, gangPattern, actionId,style)
        self.__gang_tiles.append(gangTileObj)

        ftlog.debug( 'Player:', self.name, ' Seat:', self.curSeatId, ' actionGangByDropCard:', gangTile )

    def actionGangByDropCard(self, gangTile, gangPattern, actionId, targetSeat=None):
        """明杠，通过出牌杠牌，牌先加到手牌里，再加到杠牌里
        参数：
            gangTile - 被杠的牌，跟handTiles组成杠牌组
        """
        handTiles = self.copyHandTiles()
        for _tile in gangPattern:
            if _tile not in handTiles:
                ftlog.debug( 'gang error gangTile =', gangTile, "handtiles=", handTiles)
                return False
            else:
                handTiles.remove(_tile)
        
        self.__hand_tiles = handTiles
        gangTileObj = MPlayerTileGang(gangTile, gangPattern, actionId, True)
        self.__gang_tiles.append(gangTileObj)

        alarmPeng = {"pattern": gangPattern, "seatId": targetSeat}
        self.pengTilesForAlarm.append(alarmPeng)

        if targetSeat is not None:
            self.chipengSeats.append(targetSeat)
        self.resetGuoHuPoint()
        ftlog.debug( 'Player:', self.name, ' Seat:', self.curSeatId, ' actionGangByDropCard:', gangTile )
        return True        
        
    def actionGangByAddCard(self, gangTile, gangPattern, style, actionId, magicTiles):
        """暗杠/明杠都有可能
        1）杠牌在手牌里，暗杠
        2）杠牌在碰牌里，明杠
        参数：
            gangTile - 杠牌
        返回值：
        0 - 出错，不合法
        1 - 明杠
        2 - 暗杠
        """
        ftlog.debug( 'MPlayer.actionGangByAddCard, gangPattern = ', gangPattern, 'gangTile=', magicTiles)
        self.resetGuoHuPoint()
        if style == MPlayerTileGang.MING_GANG:
            pengPattern = [gangPattern[0], gangPattern[1], gangPattern[2]]
            pengObj = None
            if gangTile not in self.__hand_tiles:
                ftlog.debug( 'MPlayer.actionGangByAddCard gang error, gangTile not in handTiles' )
                return False
            
            realGangTile = None
            for _tile in self.__hand_tiles:
                if _tile in pengPattern:
                    realGangTile = _tile
                    break
                
            if not realGangTile and (len(magicTiles) > 0) and (gangTile in magicTiles):
                realGangTile = gangTile
                
            if not realGangTile:
                ftlog.debug( 'MPlayer.actionGangByAddCard an gang error, not gangTile in handTiles' )
                return False 
            
        
            for _pengObj in self.__peng_tiles:
                if _pengObj.pattern == pengPattern:
                    pengObj = _pengObj
                    break
            ftlog.debug( 'MPlayer.actionGangByAddCard, gangPattern = ', gangPattern, 'gangTile=', gangTile)
            # 带赖子的补杠
            isLaiziBuGang = False
            laizi = None
            if len(magicTiles) > 0:
                ftlog.debug( 'MPlayer.actionGangByAddCard1,')
                for magicTile in magicTiles:
                    ftlog.debug( 'MPlayer.actionGangByAddCard2,')
                    newGangPattern = copy.deepcopy(gangPattern)
                    ftlog.debug( 'MPlayer.actionGangByAddCard3,')
                    if magicTile in newGangPattern:
                        ftlog.debug( 'MPlayer.actionGangByAddCard, newGangPattern = ', newGangPattern, 'magicTile=', magicTile)
                        newGangPattern.remove(magicTile)
                        newPengPattern = newGangPattern
                        ftlog.debug( 'MPlayer.actionGangByAddCard, newPengPattern = ', newPengPattern, 'gangTile=', gangTile)
                        for _pengObj in self.__peng_tiles:
                            if _pengObj.pattern == newPengPattern:
                                pengObj = _pengObj
                                isLaiziBuGang = True
                                laizi = magicTile
                                break
                        
            if pengObj:
                self.__peng_tiles.remove(pengObj)
                if isLaiziBuGang and laizi:
                    self.__hand_tiles.remove(laizi)
                else:
                    self.__hand_tiles.remove(realGangTile)
                gangTileObj = MPlayerTileGang(gangTile, gangPattern, actionId, style)
                self.__gang_tiles.append(gangTileObj)
            return True
        else:
            handTiles = self.copyHandTiles()
            for _tile in gangPattern:
                if _tile in handTiles:
                    handTiles.remove(_tile)
                else:
                    ftlog.debug( 'MPlayer.actionGangByAddCard an gang error, not 4 gangTiles in handTiles' )
                    return False
                
            self.__hand_tiles = handTiles
            gangTileObj = MPlayerTileGang(gangTile, gangPattern, actionId, style)
            self.__gang_tiles.append(gangTileObj)
            return True

    def addGangScore(self, actionID, gangStyleScore):
        """将杠牌分数加到杠牌信息中"""
        ftlog.debug( 'MPlayer.addGangScore params actionID=',actionID,',gangStyleScore=',gangStyleScore,',copyGangArray=',self.copyGangArray() )
        for gang in self.__gang_tiles:
            if gang.actionID == actionID:
                # 根据actionID，记录当前用户的杠牌分数
                ftlog.debug( 'MPlayer.addGangScore added Score',  gangStyleScore)
                gang.setStyleScore(gangStyleScore)

    def actionTing(self, winNodes):
        """听
        """
        ftlog.info('MPlayer changeState to ting, userId:', self.userId
                    , ' seatId:', self.curSeatId)
        self.__state = self.PLAYER_STATE_TING
        self.setWinNodes(winNodes)
        ftlog.info('MPlayer:', self.name, ' Seat:', self.curSeatId, ' actionTing winNodes:', winNodes)

    def actionTingLiang(self, tableTileMgr, dropTile, actionId, kouTiles):
        """听牌同时亮牌
        """
        # 听牌同时亮牌，必须要先听牌
        if not self.isTing():
            return None

        self.__ting_liang_tiles = []
        self.__ting_liang_winTiles = []
        mode = tableTileMgr.getTingLiangMode()
        ftlog.info('actionTingLiang, mode:', mode, ' hand tiles:', self.__hand_tiles, ' drop tile:', dropTile)

        if mode == MTableTile.MODE_LIANG_NONE:
            # 当前不支持亮牌
            return None

        self.__kou_tiles = []
        if kouTiles:
            for kouTile in kouTiles:
                kouTilesPattern = [kouTile, kouTile, kouTile]
                self.__kou_tiles.append(kouTilesPattern)

            winNodesAfterKou = []
            for wn in self.__win_nodes:
                canDrop = True
                for kouTile in kouTiles:
                    if kouTile not in wn['canKouTiles']:
                        canDrop = False
                        break
                if canDrop:
                    winNodesAfterKou.append(wn)
            # 重新计算winNode
            self.__win_nodes = winNodesAfterKou

        for wn in self.__win_nodes:
            self.__ting_liang_winTiles.append(wn['winTile'])
            
        self.__ting_liang_actionId = actionId
        handTiles = copy.deepcopy(self.handTiles)

        
        if dropTile and dropTile in handTiles:
            handTiles.remove(dropTile)
        if mode == MTableTile.MODE_LIANG_HAND:
            # 亮全部手牌
            ftlog.info('actionTingLiang: in MTableTile.MODE_LIANG_HAND')
            # 此处一定要用deepcopy,否则会影响用户手牌
            self.__ting_liang_tiles = handTiles
        elif mode == MTableTile.MODE_LIANG_TING:
            # 亮全部听口的牌
            ftlog.info('actionTingLiang: in MTableTile.MODE_LIANG_TING')
            # 先找到最基本要亮的牌，就是winTile所在的所有pattern的牌的并集
            liangBasicTilesCount = [0 for _ in range(MTile.TILE_MAX_VALUE)]
            for wn in self.__win_nodes:
                liangBasicTilesCountTemp = [0 for _ in range(MTile.TILE_MAX_VALUE)]
                for p in wn['pattern']:
                    if wn['winTile'] in p:
                        # 只要要和牌出现在牌型中，这3张牌就是听口牌
                        for tile in p:
                            liangBasicTilesCountTemp[tile] += 1
                # 遍历过所有牌后，减去要胡的牌，剩下的是当前所有听口的牌
                liangBasicTilesCountTemp[wn['winTile']] -= 1
                # 汇总各种牌型中听口的牌
                for i in range(MTile.TILE_MAX_VALUE):
                    if liangBasicTilesCountTemp[i] > liangBasicTilesCount[i]:
                        liangBasicTilesCount[i] = liangBasicTilesCountTemp[i]
            # 把听口的牌整理出来
            tingLiangBasicTiles = []
            for i in range(MTile.TILE_MAX_VALUE):
                tingLiangBasicTiles.extend([i for _ in range(liangBasicTilesCount[i])])
            ftlog.info('actionTingLiang: tingLiangBasicTiles=', tingLiangBasicTiles)

            # 上面找到的最基本要亮的牌，可能拼不成一个真正要胡的牌型
            # 用户不能理解为什么胡这些牌，所以要把winNode中相关未亮的牌补全
            # 最后再求这些牌的并集
            liangTilesCount = [0 for _ in range(MTile.TILE_MAX_VALUE)]
            for wn in self.__win_nodes:
                liangTilesCountTemp = [0 for _ in range(MTile.TILE_MAX_VALUE)]
                for p in wn['pattern']:
                    # 只要那个pattern包含了基本要亮的牌，就要把整个pattern亮出来
                    # 这里可能会多亮一点牌，应该是取包含所有基本要亮的牌的最少的pattern
                    liangThisPattern = False
                    for tile in p:
                        if tile in tingLiangBasicTiles:
                            liangThisPattern = True
                            break
                    if liangThisPattern:
                        for tile in p:
                            liangTilesCountTemp[tile] += 1
                liangTilesCountTemp[wn['winTile']] -= 1
                # 汇总各种牌型中听口的牌
                for i in range(MTile.TILE_MAX_VALUE):
                    if liangTilesCountTemp[i] > liangTilesCount[i]:
                        liangTilesCount[i] = liangTilesCountTemp[i]
            # 把听口的牌整理出来
            for i in range(MTile.TILE_MAX_VALUE):
                self.__ting_liang_tiles.extend([i for _ in range(liangTilesCount[i])])

        ftlog.info('MPlayer.actionTingLiang playerName:', self.name
                   , ' Seat:', self.curSeatId
                   , ' actionTingLiang, mode:', mode
                   , ' tiles:', self.__ting_liang_tiles
                   , ' winTiles:', self.__ting_liang_winTiles
                   , ' kouTiles:', self.__kou_tiles)
        
    def actionHuFromOthers(self, tile):
        """吃和
        别分放炮
        """
        ftlog.debug('MPlayer changeState to actionHuFromOthers, userId:', self.userId
                    , ' seatId:', self.curSeatId)
        if self.__state == self.PLAYER_STATE_TING:
            self.__jinkanState = True
        self.__state = self.PLAYER_STATE_WON
        self.__hu_tiles.append(tile)
	self.__hu_modes.append(True)
        ftlog.debug( 'Player:', self.name, ' Seat:', self.curSeatId, ' actionHuFromOthers:', tile ,self.__hu_tiles)
        
    def actionHuByMyself(self, tile, addRemove = True):
        """自摸和
        """
        ftlog.debug('MPlayer changeState to actionHuByMyself, userId:', self.userId
                    , ' seatId:', self.curSeatId)
        if self.__state == self.PLAYER_STATE_TING:
            self.__jinkanState = True
        self.__state = self.PLAYER_STATE_WON
        # 取最后一张牌放到和牌里
        if tile and addRemove:
            self.__hu_tiles.append(tile)
            self.__hand_tiles.remove(tile)
	    self.__hu_modes.append(False)
        ftlog.debug( 'Player:', self.name, ' Seat:', self.curSeatId, ' actionHuByMyself:', tile,' self.__hand_tiles:',self.__hand_tiles,self.__hu_tiles)
    
    def actionHuByDrop(self, tile):
        """云南曲靖特殊玩法,自己出牌自己胡
        """
        ftlog.debug('MPlayer changeState to actionHuByDrop, userId:', self.userId
                    , ' seatId:', self.curSeatId)
        
        self.__state = self.PLAYER_STATE_WON
        # 取最后一张牌放到和牌里
        self.__hu_tiles.append(tile)
	self.__hu_modes.append(False)
        ftlog.debug( 'Player:', self.name, ' Seat:', self.curSeatId, ' actionHuByDrop:', tile )
        
    def actionFangMao(self, pattern, maoType, actionId):
        """
        放锚/蛋
            将锚/蛋的牌从手牌中移除，加到锚牌区
        """
        for tile in pattern:
            if tile not in self.handTiles:
                return False
            self.handTiles.remove(tile)
        maoObj = MPlayerTileMao(pattern, actionId, maoType)
        self.__mao_tiles.append(maoObj)
        return True
    
    def actionExtendMao(self, tile, maoType):
        if tile not in self.handTiles:
            return False, None
        
        for maoObj in self.maoTiles:
            if maoObj.maoType == maoType:
                maoObj.pattern.append(tile)
                self.handTiles.remove(tile)
                mao = {}
                mao['tile'] = tile
                mao['type'] = maoObj.maoType
                mao['pattern'] = maoObj.pattern
                return True, mao
        return False, None
            
    def resetWithScore(self):
        """带积分重置
        """
        self.reset()
        
if __name__ == "__main__":

    from majiang2.win_rule.win_rule_luosihu import MWinRuleLuosihu
    from majiang2.table_tile.table_tile_factory import MTableTileFactory

    luosihuWinRule = MWinRuleLuosihu()
    tableTileMgr = MTableTileFactory.getTableTileMgr(3, 'luosihu', 1)
    luosihuWinRule.setTableTileMgr(tableTileMgr)

    player = MPlayer('name', 0, 10000, 0)
    player.actionBegin([1,1,1,12,12,12,4,8,8,14,15,23,26])
    player.actionAdd(8)
    player.actionPeng(8, [8,8,8], 0, 0)
    # player.actionAdd(2)
    # player.actionPeng(2, [2, 2, 2], 0, 0)
    # player.actionAdd(3)
    # player.actionPeng(3, [3, 3, 3], 0, 0)
    ftlog.debug('Player canAlarm:', player.canAlarm([[1,1,26,28],[],[[22,22,22],[23,23,23],[24,24,24]],[]],3, None))
    # gang = {'pattern': [29, 29, 29, 29], 'style': 1, 'tile': 29}
    # tiles = [[29,29,27,28,29,26,27,28,23,24],[],[],[]]
    # tile = 29
    # player.actionTing([{'winTile': 22, 'winTileCount': 0, 'pattern': [[29, 29], [27, 28, 29], [26, 27, 28], [22, 23, 24]]}, {'winTile': 25, 'winTileCount': 4, 'pattern': [[29, 29], [27, 28, 29], [26, 27, 28], [23, 24, 25]]}])
    # assert False == player.canGang(gang, True, tiles, tile, luosihuWinRule, [])

    # player = MPlayer('name', 0, 10000, 0)
    # gang = {'pattern': [29, 29, 29, 29], 'style': 1, 'tile': 29}
    # tiles = [[26,27,28,23],[],[[29,29,29]],[]]
    # tile = 29
    # player.actionTing([{'winTile': 23, 'winTileCount': 0, 'pattern': [[26, 27, 28], [23, 23]]}])
    # assert True == player.canGang(gang, True, tiles, tile, luosihuWinRule, [])
    #
    # tiles = [[29,29,29,26,27,28,21],[],[],[]]
    # tile = 29
    # player.actionTing([{'winTile': 21, 'winTileCount': 0, 'pattern': [[29, 29, 29], [26, 27, 28], [21, 21]]}])
    # # 卡五星只看kouTiles
    # assert False == player.canGang(gang, True, tiles, tile, luosihuWinRule, [])
    #
    # player = MPlayer('name', 0, 10000, 0)
    # player.actionBegin([14,15,16,16,16,24,24,25,26,27,22])
    # dropTile = 22
    # actionId = 20
    # kouTiles = []
    # player.actionTing([{'winTile': 12, 'winTileCount': 1, 'pattern': [[12, 13, 14], [16, 17, 18], [29, 29]], 'canKouTiles': []}, \
    #                    {'winTile': 15, 'winTileCount': 0, 'pattern': [[13, 14, 15], [16, 17, 18], [29, 29]], 'canKouTiles': []}])
                       #{'winTile': 24, 'winTileCount': 0, 'pattern': [[16, 16], [14, 15, 16], [25, 26, 27], [24, 24, 24]], 'canKouTiles': []}])
    # from majiang2.table.table_config_define import MTDefine
    # tableTileMgr.setTableConfig({MTDefine.LIANG_PAI:2})
    # liangTiles = player.actionTingLiang(tableTileMgr, dropTile, actionId, kouTiles)
    # # 扣下去的牌前端会屏蔽
    # assert [14, 15, 16, 16, 16] == player.tingLiangTiles
    # assert [13, 16] == player.tingLiangWinTiles
    #
    # gangTile = 19
    # gangPattern = [19, 19, 19, 19]
    # actionId = 20
    # gangObj = MPlayerTileGang(gangTile, gangPattern, actionId, 1)
    # player.gangTiles.append(gangObj)
    # player.addGangScore(actionId, 4)
    # ftlog.debug( 'Player:', player.copyGangArray() )


    # pengObj = MPlayerTilePeng(MTile.TILE_FOUR_TIAO, [MTile.TILE_FOUR_TIAO, MTile.TILE_FOUR_TIAO, MTile.TILE_ONE_TIAO], 10)
    # player.pengTiles.append(pengObj)
#     chiObj2 = MPlayerTileChi(26, [26, 21, 28], 10)
#     player.chiTiles.append(chiObj2)

#    chiObj = MPlayerTileChi(MTile.TILE_FOUR_TIAO, [24, 25, 21], 10)
#    player.chiTiles.append(chiObj)

    #gangObj = MPlayerTileGang(24, [24, 21, 21, 24], 10, True)
    #player.gangTiles.append(gangObj)
    
    #player.actionBegin([24])
    
    #tileMgr = MTableTileFactory.getTableTileMgr(4, MPlayMode.YUNNAN)
    #print player.updateTile(24, tileMgr)
