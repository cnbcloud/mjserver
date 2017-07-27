# -*- coding=utf-8 -*-
'''
Created on 2015年9月30日
麻将好友桌的牌桌，负责好友桌号的管理和好友桌赛制的调度。
@author: 赵良
'''
from majiang2.ai.play_mode import MPlayMode
from majiang2.table.majiang_quick_table import MajiangQuickTable
from freetime.util import log as ftlog
from majiang2.entity import majiang_conf
from poker.entity.game.tables.table_player import TYPlayer
from majiang2.table.friend_table_define import MFTDefine
from majiang2.table.table_config_define import MTDefine
from majiang2.entity import util
from hall.entity import hall_friend_table
from majiang2.servers.util.rpc import user_remote
from majiang2.entity.create_table import CreateTableData
from poker.entity.configure import gdata
from freetime.core.lock import locked

class MajiangFriendTable(MajiangQuickTable):
    # 解散同意
    DISSOLVE_AGREE = 1
    # 解散拒绝
    DISSOLVE_REFUSE = 0
    
    """
    好友桌的牌桌管理类，继承自MajiangQuickTable
    与MajiangQuickTable相比，有几个地方不同。
    1）角色区分房主非房主
    2）准备阶段，房主退出，房间解散，归还全部房卡
    3）牌局开始后，退出走投票机制
    4）自建桌有局数设置，所有的局数打完，散桌。没打完时，继续准备开始下一局
    """
    def __init__(self, tableId, room):
        super(MajiangFriendTable, self).__init__(tableId, room)
        self.__init_params = None
        self.__ftId = None
        self.__table_owner = 0
        self.__vote_info = [None for _ in range(self.maxSeatN)]
        self.__vote_host = MTDefine.INVALID_SEAT
        self.__vote_time_out = 0
        self.__params_desc = None
        self.__params_option_name = None
        self.__params_play_desc = None
        self.__table_owner_seatId = MTDefine.INVALID_SEAT
        self.__ready_time_out_timer = False
        # 用户操作超时
        self.__cur_seat = 0
        # 当前的无用户操作时间
        self.__cur_no_option_time_out = -1
        # 上报比赛开始
        self.__report_game_begin = False
        # 是否试炼场
        self.__is_practice = False
        
    @property
    def paramsOptionName(self):
        return self.__params_option_name
    
    def setParamsOptionName(self, name):
        self.__params_option_name = name
        
    @property
    def isPractice(self):
        return self.__is_practice
    
    def setPractice(self, isPractice):
        self.__is_practice = isPractice
     
    @property   
    def reportGameBegin(self):
        return self.__report_game_begin
    
    def setReportGameBegin(self, reportGameBegin):
        self.__report_game_begin = reportGameBegin
        
    @property
    def readyTimeOutTimer(self):
        return self.__ready_time_out_timer
        
    @property
    def paramsDesc(self):
        return self.__params_desc
    
    @property
    def paramsPlayDesc(self):
        return self.__params_play_desc
        
    @property
    def tableOwner(self):
        return self.__table_owner
        
    @property
    def tableOwnerSeatId(self):
        return self.__table_owner_seatId
    
    @property
    def curSeat(self):
        return self.__cur_seat
    
    @property
    def curNoOptionTimeOut(self):
        """当前的无用户操作时间"""
        return self.__cur_no_option_time_out
        
    @property
    def initParams(self):
        return self.__init_params
    
    @property
    def ftId(self):
        return self.__ftId
    
    @property
    def voteInfo(self):
        return self.__vote_info
    
    @property
    def voteHost(self):
        return self.__vote_host
    
    @property
    def voteTimeOut(self):
        return self.__vote_time_out

    '''
    自定义排序玩家勾选参数顺序
    '''
    def customSort(self, initParams):
        customSortList = ['shareFangka','cardCount','maiMa','maxFan','dingPiao']
        customSortDict = {}
        for key in customSortList:
            if initParams.has_key(key):
                customSortDict[key] = initParams.get(key)
        for key in initParams:
            if customSortDict.has_key(key) == False:
                customSortDict[key] = initParams.get(key)
        return customSortDict 

    def sendMsgTableInfo(self, msg, userId, seatId, isReconnect, isHost = False):
        """用户坐下后给用户发送table_info"""
        if msg and msg.getParam('itemParams', None):
            initParams = msg.getParam('itemParams', None) #玩家选定参数
            if MPlayMode().isSubPlayMode(self.playMode,MPlayMode.LUOSIHU):
                self.__init_params = self.customSort(initParams)
            else:
                self.__init_params = initParams
            self.__params_desc, self.__params_play_desc = self.get_select_create_config_items()
            self.__params_option_name = self.get_select_create_config_options()
            self.__is_practice = msg.getParam('hasRobot', 0)
            ftlog.info('MajiangFriendTable.sendMsgTableInfo userId:', userId
                , ' seatId:', seatId
                , ' message:', msg
                , ' itemParams:', self.__init_params
                , ' isPractice', self.isPractice
                , ' paramsDesc:', self.paramsDesc
                , ' paramsPlayDesc:', self.paramsPlayDesc
                , ' paramsOptionName',self.paramsOptionName
            )
            
            ftId = msg.getParam('ftId', None)
            if ftId:
                self.processCreateTableSetting()
                self.__ftId = ftId
                # 保存自建桌对应关系
                CreateTableData.addCreateTableNo(self.tableId, self.roomId, gdata.serverId(), self.ftId)
                        
                self.__table_owner = userId
                self.__table_owner_seatId = seatId
                self.logic_table.tableConfig[MFTDefine.FTID] = self.ftId
                self.logic_table.tableConfig[MFTDefine.FTOWNER] = userId
                self.logic_table.tableConfig[MFTDefine.ITEMPARAMS] = self.initParams
                self.logic_table.tableConfig[MFTDefine.CREATE_TABLE_DESCS] = self.paramsDesc
                self.logic_table.tableConfig[MFTDefine.CREATE_TABLE_OPTION_NAMES] = self.paramsOptionName
                self.logic_table.tableConfig[MFTDefine.CREATE_TABLE_PLAY_DESCS] = self.paramsPlayDesc
                # 返回房主建房成功消息，准备状态
                self.logic_table.playerReady(self.getSeatIdByUserId(userId), True)
                self.logic_table.msgProcessor.create_table_succ_response(userId
                        , self.getSeatIdByUserId(userId)
                        , 'ready'
                        , 1
                        , self.logic_table.getBroadCastUIDs())
                
                # 房主启动准备定时器，超时解散牌桌
                message = self.logic_table.msgProcessor.getMsgReadyTimeOut()
                readyTimeOut = self.getTableConfig(MFTDefine.READY_TIMEOUT, 3600)
                ftlog.debug('MajiangFriendTable.sendMsgTableInfo begin to check ready timeout, message:', message
                        , ' readyTimeOut:', readyTimeOut
                        , ' tableOwnerSeatId:', self.tableOwnerSeatId)
                self.tableTimer.setupTimer(self.tableOwnerSeatId, readyTimeOut, message)
                self.__ready_time_out_timer = True
        # 发送table_info
        super(MajiangFriendTable, self).sendMsgTableInfo(msg, userId, seatId, isReconnect, userId == self.__table_owner)
        # 如果正在投票解散，给用户补发投票解散的消息
        if self.logic_table.isFriendTablePlaying() and self.voteHost != MTDefine.INVALID_SEAT:
            # 补发投票解散信息
            self.logic_table.msgProcessor.create_table_dissolve_vote(self.players[self.voteHost].userId
                    , self.voteHost
                    , self.maxSeatN
                    , self.get_leave_vote_info()
                    , self.get_leave_vote_info_detail()
                    , self.logic_table.player[self.voteHost].name
                    , self.__vote_time_out
                    , self.logic_table.getBroadCastUIDs())   
    
    def get_select_create_config_items(self):
        """
        获取自建桌创建的选项描述
            显示完整的配置需前端上传所有的配置
            
            返回值1，paramsDesc - 分享时的建桌参数，包含人数和局数
            返回值2，paramsPlayDesc - 在牌桌上显示的建桌参数，不包含人数和局数
            
        """
        paramsDesc = []
        paramsPlayDesc = []
        
        create_table_config = majiang_conf.getCreateTableTotalConfig(self.gameId)
        playmode_config = {}
        if create_table_config:
            playmode_config = create_table_config.get(self.playMode,{})
            
        playerTypeId = self.initParams.get(MFTDefine.PLAYER_TYPE, 1)
        playerTypeConfig = majiang_conf.getCreateTableConfig(self.gameId, self.playMode, MFTDefine.PLAYER_TYPE, playerTypeId)
        cardCardKey = playerTypeConfig.get(MFTDefine.CARD_COUNT, MFTDefine.CARD_COUNT)
        #modified by robin

	playerCount = playerTypeConfig.get('count', 4)
	#self.maxSeatN=playerCount
	#modified    
        #通过id直接获取自建桌配置的key数组
        for key, value in self.__init_params.iteritems():
            if (key not in playmode_config) or ((MFTDefine.CARD_COUNT in key) and (key != cardCardKey)):
                continue
            
            items = playmode_config[key]
            for item in items:
                ftlog.debug('get_select_create_config_items item:', item, ' value:', value)
                if item['id'] == value:
                    if (key == cardCardKey) or (key == 'playerType'):
                        paramsDesc.append(item['desc'])
                    else:
                        paramsDesc.append(item['desc'])
			paramsPlayDesc.append(item['desc'])
                    
        ftlog.debug('get_select_create_config_items paramsDesc:', paramsDesc
                    , ' paramsPlayDesc:', paramsPlayDesc)
        return paramsDesc, paramsPlayDesc

    def get_select_create_config_options(self):
        """获取自建桌创建的选项
        """
        ret = []
        items = []
        create_table_config = majiang_conf.getCreateTableTotalConfig(self.gameId)
        playmode_config = {}
        if create_table_config:
            playmode_config = create_table_config.get(self.playMode,{})
            ftlog.debug('playmode_config descs:', playmode_config ,'playMode:', self.playMode)
            
        playerTypeId = self.initParams.get(MFTDefine.PLAYER_TYPE, 1)
        playerTypeConfig = majiang_conf.getCreateTableConfig(self.gameId, self.playMode, MFTDefine.PLAYER_TYPE, playerTypeId)
        cardCardKey = playerTypeConfig.get(MFTDefine.CARD_COUNT, MFTDefine.CARD_COUNT)
            
        #通过id直接获取自建桌配置的key数组
        ftlog.debug('__init_params descs:', self.__init_params)
        for key, value in self.__init_params.iteritems():
            if (key not in playmode_config) or ((MFTDefine.CARD_COUNT in key) and (key != cardCardKey)):
                continue
            
            ftlog.debug('get_select_create_config_names descs:', playmode_config ,'   key:', key)
            items = playmode_config['paramType']
            #ret.append(items[key])
	    
            if key != 'fangka_pay':
                if value:
                    ret.append(items[key])
            else:
                ret.append(items[key])
	    
        ftlog.debug('get_select_create_config_names descs:', ret)
        return ret

    
    def processCreateTableSetting(self):
        """解析处理自建桌参数"""
        # 配置0 人数
        playerTypeId = self.initParams.get(MFTDefine.PLAYER_TYPE, 1)
        playerTypeConfig = majiang_conf.getCreateTableConfig(self.gameId, self.playMode, MFTDefine.PLAYER_TYPE, playerTypeId)
        cardCardKey = playerTypeConfig.get(MFTDefine.CARD_COUNT, MFTDefine.CARD_COUNT)
        ftlog.debug('MajiangFriendTable.processCreateTableSetting playerTypeConfig:', playerTypeConfig
                    , ' cardCountKey:', cardCardKey)
        
        # 配置1 轮数
        cardCountId = self.initParams.get(cardCardKey, -1)
        cardCountConfig = majiang_conf.getCreateTableConfig(self.gameId, self.playMode, cardCardKey, cardCountId)
        if self.isPractice:
            cardCountConfig = cardCountConfig.get('hasRobot', cardCountConfig)
        ftlog.info('MajiangFriendTable.processCreateTableSetting cardCountConfig:', cardCountConfig)

        if cardCountConfig:
            cType = cardCountConfig.get('type', MFTDefine.CARD_COUNT_ROUND)
            if cType == MFTDefine.CARD_COUNT_ROUND:
                round_count = cardCountConfig.get('value', 1)
                card_count = cardCountConfig.get('fangka_count', 1)
                self.logic_table.tableConfig[MFTDefine.ROUND_COUNT] = round_count
                self.logic_table.tableConfig[MFTDefine.CUR_ROUND_COUNT] = 0
                self.logic_table.tableConfig[MFTDefine.QUAN_COUNT] = 0
                self.logic_table.tableConfig[MFTDefine.CUR_QUAN_COUNT] = 0
                self.logic_table.tableConfig[MFTDefine.CARD_COUNT] = card_count
                self.logic_table.tableConfig[MFTDefine.LEFT_CARD_COUNT] = card_count
                self.logic_table.tableConfig[MFTDefine.BASE_COUNT] = 0
                self.logic_table.tableConfig[MFTDefine.CUR_BASE_COUNT] = 0
                ftlog.debug('MajiangFriendTable.processCreateTableSetting roundCount:', round_count, 'cardCount', card_count)
            elif cType == MFTDefine.CARD_COUNT_CIRCLE:
                quan_count = cardCountConfig.get('value', 1)
                card_count = cardCountConfig.get('fangka_count', 1)
                self.logic_table.tableConfig[MFTDefine.ROUND_COUNT] = 999999
                self.logic_table.tableConfig[MFTDefine.CUR_ROUND_COUNT] = 0
                self.logic_table.tableConfig[MFTDefine.QUAN_COUNT] = quan_count
                self.logic_table.tableConfig[MFTDefine.CUR_QUAN_COUNT] = 0
                self.logic_table.tableConfig[MFTDefine.CARD_COUNT] = card_count
                self.logic_table.tableConfig[MFTDefine.LEFT_CARD_COUNT] = card_count
                self.logic_table.tableConfig[MFTDefine.BASE_COUNT] = 0
                self.logic_table.tableConfig[MFTDefine.CUR_BASE_COUNT] = 0
                ftlog.debug('MajiangFriendTable.processCreateTableSetting quanCount:', quan_count, 'quanCount', card_count)
            elif cType == MFTDefine.CARD_COUNT_BASE:
                base_count = cardCountConfig.get('value', 1)
                card_count = cardCountConfig.get('fangka_count', 1)
                self.logic_table.tableConfig[MFTDefine.BASE_COUNT] = base_count
                self.logic_table.tableConfig[MFTDefine.CUR_BASE_COUNT] = 0
                self.logic_table.tableConfig[MFTDefine.ROUND_COUNT] = 999999
                self.logic_table.tableConfig[MFTDefine.CUR_ROUND_COUNT] = 0
                self.logic_table.tableConfig[MFTDefine.QUAN_COUNT] = 0
                self.logic_table.tableConfig[MFTDefine.CUR_QUAN_COUNT] = 0
                self.logic_table.tableConfig[MFTDefine.CARD_COUNT] = card_count
                self.logic_table.tableConfig[MFTDefine.LEFT_CARD_COUNT] = card_count
                ftlog.debug('MajiangFriendTable.processCreateTableSetting base_count:', base_count, 'quanCount', card_count)

        # 初始化经过了0局, 后扣房卡方式里已扣除0张房卡
        self.logic_table.tableConfig[MFTDefine.PASSED_ROUND_COUNT] = 0
        self.logic_table.tableConfig[MFTDefine.CONSUMED_FANGKA_COUNT] = 0

        # 配置1-2 daKou
        daKouId = self.initParams.get('daKou', 0)
        daKouConfig = majiang_conf.getCreateTableConfig(self.gameId, self.playMode, 'daKou', daKouId)
        if daKouConfig:
            self.logic_table.tableConfig[MTDefine.DA_KOU] = daKouConfig.get(MTDefine.DA_KOU, 0)
            ftlog.debug('MajiangFriendTable.processCreateTableSetting daKou:', self.logic_table.tableConfig[MTDefine.DA_KOU])
              
        # 配置 底分
        winBaseId = self.initParams.get('winBase', 0)
        winBaseConfig = majiang_conf.getCreateTableConfig(self.gameId, self.playMode, 'winBase', winBaseId)
        if winBaseConfig:
            difen = winBaseConfig.get(MTDefine.WIN_BASE, 1)
            self.logic_table.tableConfig[MTDefine.WIN_BASE] = difen
            ftlog.debug('MajiangFriendTable.processCreateTableSetting winBase:', self.logic_table.tableConfig[MTDefine.WIN_BASE])

        # 配置 杠分
        gangBaseId = self.initParams.get('gangBase', 0)
        gangBaseConfig = majiang_conf.getCreateTableConfig(self.gameId, self.playMode, 'gangBase', gangBaseId)
        if gangBaseConfig:
            difen = gangBaseConfig.get(MTDefine.GANG_BASE, 1)
            self.logic_table.tableConfig[MTDefine.GANG_BASE] = difen
            ftlog.debug('MajiangFriendTable.processCreateTableSetting gangBase:', self.logic_table.tableConfig[MTDefine.GANG_BASE])
            
        # 配置
        maxScoreId = self.initParams.get('maxLossScore', 0)
        maxScoreConfig = majiang_conf.getCreateTableConfig(self.gameId, self.playMode, 'maxLossScore', maxScoreId)
        if maxScoreConfig:
            temps = maxScoreConfig.get(MTDefine.MAX_LOSS_SCORE, 256)
            self.logic_table.tableConfig[MTDefine.MAX_LOSS_SCORE] = temps
            ftlog.debug('MajiangFriendTable.processCreateTableSetting maxScore:', self.logic_table.tableConfig[MTDefine.MAX_LOSS_SCORE])
            
        # 配置2 纯夹
        chunJiaId = self.initParams.get('chunJia', 0)
        chunJiaConfig = majiang_conf.getCreateTableConfig(self.gameId, self.playMode, 'chunJia', chunJiaId)
        if chunJiaConfig:
            self.logic_table.tableConfig[MTDefine.MIN_MULTI] = chunJiaConfig.get(MTDefine.MIN_MULTI, 0)
            ftlog.debug('MajiangFriendTable.processCreateTableSetting chunJia:', self.logic_table.tableConfig[MTDefine.MIN_MULTI])
        
        # 配置3 红中宝
        hzbId = self.initParams.get('hongZhongBao', 0)
        hzbConfig = majiang_conf.getCreateTableConfig(self.gameId, self.playMode, 'hongZhongBao', hzbId)
        if hzbConfig:
            self.logic_table.tableConfig[MTDefine.HONG_ZHONG_BAO] = hzbConfig.get(MTDefine.HONG_ZHONG_BAO, 0)
            ftlog.debug('MajiangFriendTable.processCreateTableSetting hongZhongBao:', self.logic_table.tableConfig[MTDefine.HONG_ZHONG_BAO])
            
        # 配置4 三七边
        sqbId = self.initParams.get('sanQiBian', 0)
        sqbConfig = majiang_conf.getCreateTableConfig(self.gameId, self.playMode, 'sanQiBian', sqbId)
        if sqbConfig:
            self.logic_table.tableConfig[MTDefine.BIAN_MULTI] = sqbConfig.get(MTDefine.BIAN_MULTI, 0)
            ftlog.debug('MajiangFriendTable.processCreateTableSetting sanQiBian:', self.logic_table.tableConfig[MTDefine.BIAN_MULTI])
        
        # 配置5 刮大风
        fengId = self.initParams.get('guaDaFeng', 0)
        fengConfig = majiang_conf.getCreateTableConfig(self.gameId, self.playMode, 'guaDaFeng', fengId)
        if fengConfig:
            self.logic_table.tableConfig[MTDefine.GUA_DA_FENG] = fengConfig.get(MTDefine.GUA_DA_FENG, 0)
            ftlog.debug('MajiangFriendTable.processCreateTableSetting guaDaFeng:', self.logic_table.tableConfig[MTDefine.GUA_DA_FENG])

        # 配置6 频道
        pinDaoId = self.initParams.get('pinDao', 0)
        pinDaoConfig = majiang_conf.getCreateTableConfig(self.gameId, self.playMode, 'pinDao', pinDaoId)
        if pinDaoConfig:
            self.logic_table.tableConfig[MTDefine.PIN_DAO] = pinDaoConfig.get(MTDefine.PIN_DAO, 0)
            ftlog.debug('MajiangFriendTable.processCreateTableSetting pinDao:', self.logic_table.tableConfig[MTDefine.PIN_DAO])

        # 配置7 跑恰摸八
        paoqiamobaId = self.initParams.get('paoqiamoba', 0)
        paoqiamobaConfig = majiang_conf.getCreateTableConfig(self.gameId, self.playMode, 'paoqiamoba', paoqiamobaId)
        if paoqiamobaConfig:
            self.logic_table.tableConfig[MTDefine.PAOQIAMOBA] = paoqiamobaConfig.get(MTDefine.PAOQIAMOBA, 0)
            ftlog.debug('MajiangFriendTable.processCreateTableSetting paoqiamoba:', self.logic_table.tableConfig[MTDefine.PAOQIAMOBA])

        # 配置8 定漂
        dingPiaoId = self.initParams.get('dingPiao', 0)
        dingPiaoConfig = majiang_conf.getCreateTableConfig(self.gameId, self.playMode, 'dingPiao', dingPiaoId)
        if dingPiaoConfig:
            self.logic_table.tableConfig[MTDefine.DING_PIAO] = dingPiaoConfig.get(MTDefine.DING_PIAO, 0)
            self.logic_table.tableStater.enableSpecialStateByTableConfig(self.logic_table.tableConfig)
            ftlog.debug('MajiangFriendTable.processCreateTableSetting dingPiao:', self.logic_table.tableConfig[MTDefine.DING_PIAO])

        # 配置9 买马
        maiMaId = self.initParams.get('maiMa', 0)
        maiMaConfig = majiang_conf.getCreateTableConfig(self.gameId, self.playMode, 'maiMa', maiMaId)
        if maiMaConfig:
            self.logic_table.tableConfig[MTDefine.MAI_MA] = maiMaConfig.get(MTDefine.MAI_MA, 0)
            ftlog.debug('MajiangFriendTable.processCreateTableSetting maiMa:', self.logic_table.tableConfig[MTDefine.MAI_MA])

        # 配置10 数坎
        shuKanId = self.initParams.get('shuKan', 0)
        shuKanConfig = majiang_conf.getCreateTableConfig(self.gameId, self.playMode, 'shuKan', shuKanId)
        if shuKanConfig:
            self.logic_table.tableConfig[MTDefine.SHU_KAN] = shuKanConfig.get(MTDefine.SHU_KAN, 0)
            ftlog.debug('MajiangFriendTable.processCreateTableSetting shuKan:', self.logic_table.tableConfig[MTDefine.SHU_KAN])

        # 配置11 听牌时亮牌规则
        liangPaiId = self.initParams.get('liangPai', 0)
        liangPaiConfig = majiang_conf.getCreateTableConfig(self.gameId, self.playMode, 'liangPai', liangPaiId)
        if liangPaiConfig:
            self.logic_table.tableConfig[MTDefine.LIANG_PAI] = liangPaiConfig.get(MTDefine.LIANG_PAI, 0)
            ftlog.debug('MajiangFriendTable.processCreateTableSetting liangPai:', self.logic_table.tableConfig[MTDefine.LIANG_PAI])

        # 配置12 最大番数
        maxFanId = self.initParams.get('maxFan', 0)
        maxFanConfig = majiang_conf.getCreateTableConfig(self.gameId, self.playMode, 'maxFan', maxFanId)
        if maxFanConfig:
            self.logic_table.tableConfig[MTDefine.MAX_FAN] = maxFanConfig.get(MTDefine.MAX_FAN, 0)
            ftlog.debug('MajiangFriendTable.processCreateTableSetting maxFan:', self.logic_table.tableConfig[MTDefine.MAX_FAN])

        # 配置13 卡五星番数
        luosihuFanId = self.initParams.get('luosihuFan', 0)
        luosihuFanConfig = majiang_conf.getCreateTableConfig(self.gameId, self.playMode, 'luosihuFan', luosihuFanId)
        if luosihuFanConfig:
            self.logic_table.tableConfig[MTDefine.LUOSIHU_FAN] = luosihuFanConfig.get(MTDefine.LUOSIHU_FAN, 0)
            ftlog.debug('MajiangFriendTable.processCreateTableSetting luosihuFan:', self.logic_table.tableConfig[MTDefine.LUOSIHU_FAN])

        # 配置14 碰碰胡番数
        pengpenghuFanId = self.initParams.get('pengpenghuFan', 0)
        pengpenghuFanConfig = majiang_conf.getCreateTableConfig(self.gameId, self.playMode, 'pengpenghuFan', pengpenghuFanId)
        if pengpenghuFanConfig:
            self.logic_table.tableConfig[MTDefine.PENGPENGHU_FAN] = pengpenghuFanConfig.get(MTDefine.PENGPENGHU_FAN, 0)
            ftlog.debug('MajiangFriendTable.processCreateTableSetting pengpenghuFan:', self.logic_table.tableConfig[MTDefine.PENGPENGHU_FAN])

        # 配置15 杠上花番数
        gangshanghuaFanId = self.initParams.get('gangshanghuaFan', 0)
        gangshanghuaFanConfig = majiang_conf.getCreateTableConfig(self.gameId, self.playMode, 'gangshanghuaFan', gangshanghuaFanId)
        if gangshanghuaFanConfig:
            self.logic_table.tableConfig[MTDefine.GANGSHANGHUA_FAN] = gangshanghuaFanConfig.get(MTDefine.GANGSHANGHUA_FAN, 0)
            ftlog.debug('MajiangFriendTable.processCreateTableSetting gangshanghuaFan:', self.logic_table.tableConfig[MTDefine.GANGSHANGHUA_FAN])
            
        # 配置16 闭门算番(鸡西)
        biMenFanId = self.initParams.get('biMenFan', 0)
        biMenFanConfig = majiang_conf.getCreateTableConfig(self.gameId, self.playMode, 'biMenFan', biMenFanId)
        if biMenFanConfig:
            self.logic_table.tableConfig[MTDefine.BI_MEN_FAN] = biMenFanConfig.get(MTDefine.BI_MEN_FAN, 0)
            ftlog.debug('MajiangFriendTable.processCreateTableSetting biMenFan:', self.logic_table.tableConfig[MTDefine.BI_MEN_FAN])
        
        #配置 天胡（白城可选玩法）
        tianHuId = self.initParams.get('tian_hu', 0)
        tianHuConfig = majiang_conf.getCreateTableConfig(self.gameId, self.playMode, 'tian_hu', tianHuId)
        if tianHuConfig:
            self.logic_table.tableConfig[MTDefine.TIAN_HU] = tianHuConfig.get(MTDefine.TIAN_HU, 0)
            self.logic_table.tableConfig[MTDefine.DI_HU] = tianHuConfig.get(MTDefine.TIAN_HU, 0)
            ftlog.debug('MajiangFriendTable.processCreateTableSetting tianHu:', self.logic_table.tableConfig[MTDefine.TIAN_HU],' dihu:',self.logic_table.tableConfig[MTDefine.DI_HU])

        #配置 责任制（白城可选玩法）
        inchargeId = self.initParams.get('incharge', 0)
        inchargeConfig = majiang_conf.getCreateTableConfig(self.gameId, self.playMode, 'incharge', inchargeId)
        if inchargeConfig:
            self.logic_table.tableConfig[MTDefine.BAOZHUANG_BAOGANG] = inchargeConfig.get(MTDefine.BAOZHUANG_BAOGANG, 0)
            ftlog.debug('MajiangFriendTable.processCreateTableSetting BAOZHUANG_BAOGANG:', self.logic_table.tableConfig[MTDefine.BAOZHUANG_BAOGANG])

        #配置 liangtoujia（白城可选玩法）
        liangtoujiaId = self.initParams.get('liangtoujia', 0)
        liangtoujiaConfig = majiang_conf.getCreateTableConfig(self.gameId, self.playMode, 'liangtoujia', liangtoujiaId)
        if liangtoujiaConfig:
            self.logic_table.tableConfig[MTDefine.LIANGTOU_JIA] = liangtoujiaConfig.get(MTDefine.LIANGTOU_JIA, 0)
            ftlog.debug('MajiangFriendTable.processCreateTableSetting liangtoujia:', self.logic_table.tableConfig[MTDefine.LIANGTOU_JIA])

        # 配置17 抽奖牌数量(鸡西)
        awordTileCountId = self.initParams.get('awordTileCount', 0)
        awordTileCountConfig = majiang_conf.getCreateTableConfig(self.gameId, self.playMode, 'awordTileCount', awordTileCountId)
        if awordTileCountConfig:
            self.logic_table.tableConfig[MTDefine.AWARD_TILE_COUNT] = awordTileCountConfig.get(MTDefine.AWARD_TILE_COUNT, 1)
            ftlog.debug('MajiangFriendTable.processCreateTableSetting awordTileCount:', self.logic_table.tableConfig[MTDefine.AWARD_TILE_COUNT])
            
        # 配置18 宝牌隐藏(鸡西 默认暗宝)
        magicHideId = self.initParams.get('magicHide', 0)
        magicHideConfig = majiang_conf.getCreateTableConfig(self.gameId, self.playMode, 'magicHide', magicHideId)
        if magicHideConfig:
            self.logic_table.tableConfig[MTDefine.MAGIC_HIDE] = magicHideConfig.get(MTDefine.MAGIC_HIDE, 1)
            ftlog.debug('MajiangFriendTable.processCreateTableSetting magicHide:', self.logic_table.tableConfig[MTDefine.MAGIC_HIDE])
            
        # 配置19 对宝(哈尔滨补充 规则和鸡西通宝一样)
        duiBaoId = self.initParams.get('duiBao', 0)
        duiBaoConfig = majiang_conf.getCreateTableConfig(self.gameId, self.playMode, 'duiBao', duiBaoId)
        if duiBaoConfig:
            self.logic_table.tableConfig[MTDefine.DUI_BAO] = duiBaoConfig.get(MTDefine.DUI_BAO, 0)
            ftlog.debug('MajiangFriendTable.processCreateTableSetting duiBao:', self.logic_table.tableConfig[MTDefine.DUI_BAO])
            
        # 配置20 单吊算夹(哈尔滨补充)
        danDiaoJiaId = self.initParams.get('danDiaoJia', 0)
        danDiaoJiaConfig = majiang_conf.getCreateTableConfig(self.gameId, self.playMode, 'danDiaoJia', danDiaoJiaId)
        if danDiaoJiaConfig:
            self.logic_table.tableConfig[MTDefine.DAN_DIAO_JIA] = danDiaoJiaConfig.get(MTDefine.DAN_DIAO_JIA, 0)
            ftlog.debug('MajiangFriendTable.processCreateTableSetting danDiaoJia:', self.logic_table.tableConfig[MTDefine.DAN_DIAO_JIA])
            
        # 配置21 平度麻将的是否允许吃
        allowChiId = self.initParams.get(MFTDefine.ALLOW_CHI, MFTDefine.ALLOW_CHI_NO)
        allowChiConfig = majiang_conf.getCreateTableConfig(self.gameId, self.playMode, MFTDefine.ALLOW_CHI, allowChiId)
        if allowChiConfig:
            self.logic_table.tableConfig[MTDefine.CHIPENG_SETTING] = allowChiConfig.get(MTDefine.CHIPENG_SETTING, MTDefine.NOT_ALLOW_CHI)
            ftlog.debug('MajiangFriendTable.processCreateTableSetting chiPengSetting1:', self.logic_table.tableConfig[MTDefine.CHIPENG_SETTING])

        # 配置 盘锦麻将的是否允许gang
        allowgangId = self.initParams.get('allowGang', 0)
        allowgangConfig = majiang_conf.getCreateTableConfig(self.gameId, self.playMode, 'allowGang', allowgangId)
        if allowgangConfig:
            self.logic_table.tableConfig[MTDefine.GANG_SETTING] = allowgangConfig.get(MTDefine.GANG_SETTING, 0)
            ftlog.debug('MajiangFriendTable.processCreateTableSetting GANG_SETTING:', self.logic_table.tableConfig[MTDefine.GANG_SETTING])

        # 配置 盘锦麻将
        jihuId = self.initParams.get('jiHu', 0)
        jihuConfig = majiang_conf.getCreateTableConfig(self.gameId, self.playMode, 'jiHu', jihuId)
        if jihuConfig:
            self.logic_table.tableConfig[MTDefine.JI_HU] = jihuConfig.get(MTDefine.JI_HU, 0)

        # 配置 盘锦麻将
        qiongHuId = self.initParams.get('qiongHu', 0)
        qiongHuConfig = majiang_conf.getCreateTableConfig(self.gameId, self.playMode, 'qiongHu', qiongHuId)
        if qiongHuConfig:
            self.logic_table.tableConfig[MTDefine.QIONG_HU] = qiongHuConfig.get(MTDefine.QIONG_HU, 0)

        # 配置 盘锦麻将
        jueHuId = self.initParams.get('jueHu', 0)
        jueHuConfig = majiang_conf.getCreateTableConfig(self.gameId, self.playMode, 'jueHu', jueHuId)
        if jueHuConfig:
            self.logic_table.tableConfig[MTDefine.JUE_HU] = jueHuConfig.get(MTDefine.JUE_HU, 0)

        # 配置 盘锦麻将
        huiPaiId = self.initParams.get('huiPai', 0)
        huiPaiConfig = majiang_conf.getCreateTableConfig(self.gameId, self.playMode, 'huiPai', huiPaiId)
        if huiPaiConfig:
            self.logic_table.tableConfig[MTDefine.HUI_PAI] = huiPaiConfig.get(MTDefine.HUI_PAI, 0)

        # 配置22，卡五星的吃碰设置
        # 这样做不好，会直接把协议暴漏给外面，需要按照上面的方式修改
        chiPengSetting = self.initParams.get(MTDefine.CHIPENG_SETTING, 0)
        if chiPengSetting != 0:
            self.logic_table.tableConfig[MTDefine.CHIPENG_SETTING] = chiPengSetting
            ftlog.debug('MajiangFriendTable.processCreateTableSetting chiPengSetting2:', chiPengSetting)
            
        # 配置23 输赢倍数
        # 这样做不好，会直接把协议暴漏给外面，需要按照上面的方式修改
        multiNum = self.initParams.get(MTDefine.MULTIPLE, MTDefine.MULTIPLE_MIN)
        if multiNum >= MTDefine.MULTIPLE_MIN and multiNum <= MTDefine.MULTIPLE_MAX:
            self.logic_table.tableConfig[MTDefine.MULTIPLE] = multiNum
            
        # 配置24 必漂分值
        mustPiao = self.initParams.get(MFTDefine.MUST_PIAO, 0)
        mustPiaoConfig = majiang_conf.getCreateTableConfig(self.gameId, self.playMode, MFTDefine.MUST_PIAO, mustPiao)
        if mustPiaoConfig:
            self.logic_table.tableConfig[MTDefine.BIPIAO_POINT] = mustPiaoConfig.get('value', 0)
            
        # 配置25 锚／蛋时间设置
        maodantime = self.initParams.get(MTDefine.MAO_DAN_FANG_TIME, 0)
        maodantimeConfig = majiang_conf.getCreateTableConfig(self.gameId, self.playMode, MTDefine.MAO_DAN_FANG_TIME, maodantime)
        if maodantimeConfig:
            self.logic_table.tableConfig[MTDefine.MAO_DAN_FANG_TIME] = maodantimeConfig.get(MTDefine.MAO_DAN_FANG_TIME, 0)

        # 配置26 锚／蛋设置
        maodan = self.initParams.get(MTDefine.MAO_DAN_SETTING, 0)
        maodanConfig = majiang_conf.getCreateTableConfig(self.gameId, self.playMode, MTDefine.MAO_DAN_SETTING, maodan)
        if maodanConfig:
            self.logic_table.tableConfig[MTDefine.MAO_DAN_SETTING] = maodanConfig.get(MTDefine.MAO_DAN_SETTING, 0)
            
        # 配置27 必须自摸
        zimo = self.initParams.get(MFTDefine.MUST_ZIMO, 0)
        zimoConfig = majiang_conf.getCreateTableConfig(self.gameId, self.playMode, MFTDefine.MUST_ZIMO, zimo)
        if zimoConfig:
            self.logic_table.tableConfig[MTDefine.WIN_BY_ZIMO] = zimoConfig.get('value', 0)
            ftlog.debug('MajiangFriendTable.processCreateTableSetting zimo:', zimo
                        , ' zimoConfig:', zimoConfig
                        , ' zimoConfig in table:', self.logic_table.tableConfig[MTDefine.WIN_BY_ZIMO])
            
        # 配置28，去掉风牌箭牌
        noFengTiles = self.initParams.get(MFTDefine.NO_FENG_TILES, 0)
        noFengConfig = majiang_conf.getCreateTableConfig(self.gameId, self.playMode, MFTDefine.NO_FENG_TILES, noFengTiles)
        if noFengConfig:
            self.logic_table.tableConfig[MTDefine.REMOVE_FENG_ARROW_TILES] = noFengConfig.get('value', 0)
            ftlog.debug('MajiangFriendTable.processCreateTableSetting noFengTiles:', noFengTiles
                        , ' noFengConfig:', noFengConfig
                        , ' noFengConfigInTable:', self.logic_table.tableConfig[MTDefine.REMOVE_FENG_ARROW_TILES])
            
        # 配置29 庄翻倍
        bankerDouble = self.initParams.get(MFTDefine.BANKER_DOUBLE, 0)
        bankerDoubleConfig = majiang_conf.getCreateTableConfig(self.gameId, self.playMode, MFTDefine.BANKER_DOUBLE, bankerDouble)
        if bankerDoubleConfig:
            self.logic_table.tableConfig[MTDefine.BANKER_DOUBLE] = bankerDoubleConfig.get('value', 1)
            ftlog.debug('MajiangFriendTable.processCreateTableSetting bankerDouble:', bankerDouble
                        , ' bankerDoubleConfig:', bankerDoubleConfig
                        , ' bankerDoubleConfigInTable:', self.logic_table.tableConfig[MTDefine.BANKER_DOUBLE])
            
        # 配置30 门清翻倍
        clearDouble = self.initParams.get(MFTDefine.CLEAR_DOUBLE, 0)
        clearDoubleConfig = majiang_conf.getCreateTableConfig(self.gameId, self.playMode, MFTDefine.CLEAR_DOUBLE, clearDouble)
        if clearDoubleConfig:
            self.logic_table.tableConfig[MTDefine.MEN_CLEAR_DOUBLE] = clearDoubleConfig.get('value', 1)
            self.logic_table.tableConfig[MTDefine.DUANYAOJIU] = clearDoubleConfig.get('value', 1)
            ftlog.debug('MajiangFriendTable.processCreateTableSetting clearDouble:', clearDouble
                        , ' clearDoubleConfig:', clearDoubleConfig
                        , ' clearDoubleConfigInTable:', self.logic_table.tableConfig[MTDefine.MEN_CLEAR_DOUBLE]
                        , ' self.logic_table.tableConfig[MTDefine.DUANYAOJIU]',self.logic_table.tableConfig[MTDefine.DUANYAOJIU])

        # 配置31 二五八掌
        zhang258 = self.initParams.get(MFTDefine.ZHANG_258, 0)
        zhang258Config = majiang_conf.getCreateTableConfig(self.gameId, self.playMode, MFTDefine.ZHANG_258,zhang258)
        if zhang258Config:
            self.logic_table.tableConfig[MTDefine.ONLY_JIANG_258] = zhang258Config.get('value', 0)
            ftlog.debug('MajiangFriendTable.processCreateTableSetting zhang258:', zhang258
                        , ' zhang258Config:', zhang258Config
                        , ' zhang258ConfigInTable:', self.logic_table.tableConfig[MTDefine.ONLY_JIANG_258])


        # 配置32 是否乱锚 威海
        luanMao = self.initParams.get(MFTDefine.LUAN_MAO, 0)
        luanMaoConfig = majiang_conf.getCreateTableConfig(self.gameId, self.playMode, MFTDefine.LUAN_MAO, luanMao)
        if self.playMode == 'weihai':
            if luanMaoConfig: #乱锚
                self.logic_table.tableConfig[MTDefine.MAO_DAN_SETTING] = luanMaoConfig.get(MTDefine.MAO_DAN_SETTING, MTDefine.MAO_DAN_DNXB + MTDefine.MAO_DAN_ZFB)
                ftlog.debug('MajiangFriendTable.processCreateTableSetting luanMao:', luanMao
                            , ' luanMaoConfig:', luanMaoConfig
                            , ' luanMaoConfigInTable:', self.logic_table.tableConfig[MTDefine.MAO_DAN_SETTING])
            else: #不乱锚
                self.logic_table.tableConfig[MTDefine.MAO_DAN_SETTING] = luanMaoConfig.get(MTDefine.MAO_DAN_SETTING, MTDefine.MAO_DAN_DNXBZFB)
                ftlog.debug('MajiangFriendTable.processCreateTableSetting luanMao reset:', luanMao
                            , ' luanMaoConfig:', luanMaoConfig
                            , ' luanMaoConfigInTable:', self.logic_table.tableConfig[MTDefine.MAO_DAN_SETTING])

        # 配置33 必杠模式
        bigang = self.initParams.get('bigang', 0)
        bigangConfig = majiang_conf.getCreateTableConfig(self.gameId, self.playMode, 'bigang', bigang)
        if bigangConfig:
            self.logic_table.tableConfig[MTDefine.BI_GANG] = bigangConfig.get(MTDefine.BI_GANG, 0)
            ftlog.debug('MajiangFriendTable.processCreateTableSetting bigang:', self.logic_table.tableConfig[MTDefine.BI_GANG])

        # 配置33 玩家牌码
        multiple = self.initParams.get(MTDefine.MULTIPLE, MTDefine.MULTIPLE_MIN)
        multipleConfig = majiang_conf.getCreateTableConfig(self.gameId, self.playMode, MTDefine.MULTIPLE, multiple)
        if multipleConfig:
            initScore = multipleConfig.get(MFTDefine.INIT_SCORE, 0)
            if initScore:
                self.logic_table.tableConfig[MFTDefine.INIT_SCORE] = initScore
            ftlog.debug('MajiangFriendTable.processCreateTableSetting multipleConfig:', multipleConfig
                        , ' initScore:', initScore)

        # 配置34 只许自摸
        needZimo = self.initParams.get('needzimo', 0)
        needZimoConfig = majiang_conf.getCreateTableConfig(self.gameId, self.playMode, 'needzimo', needZimo)
        if needZimoConfig:
            self.logic_table.tableConfig[MTDefine.WIN_BY_ZIMO] = needZimoConfig.get(MTDefine.WIN_BY_ZIMO, 0)
            ftlog.debug('MajiangFriendTable.processCreateTableSetting needZimo:', self.logic_table.tableConfig[MTDefine.WIN_BY_ZIMO])

        # 配置35 喜相逢分数
        xiXiangFeng = self.initParams.get('xixiangfeng', 0)
        xiXiangFengConfig = majiang_conf.getCreateTableConfig(self.gameId, self.playMode, 'xixiangfeng', xiXiangFeng)
        if xiXiangFengConfig:
            self.logic_table.tableConfig[MTDefine.XIXIANGFENG] = xiXiangFengConfig.get(MTDefine.XIXIANGFENG, 50)
            ftlog.debug('MajiangFriendTable.processCreateTableSetting xiXiangFeng', self.logic_table.tableConfig[MTDefine.XIXIANGFENG])

        # 配置36 是否均摊房卡
        shareFangka= self.initParams.get('shareFangka', 0)
        shareFangkaConfig = majiang_conf.getCreateTableConfig(self.gameId, self.playMode, 'shareFangka', shareFangka)
        if shareFangkaConfig:
            self.logic_table.tableConfig[MTDefine.SHARE_FANGKA] = shareFangkaConfig.get(MTDefine.SHARE_FANGKA, 0)
            ftlog.debug('MajiangFriendTable.processCreateTableSetting shareFangkaConfig:', self.logic_table.tableConfig[MTDefine.SHARE_FANGKA])
            
        # 配置37 是否允许听
        canTingId = self.initParams.get(MFTDefine.CAN_TING, MTDefine.TING_UNDEFINE)
        canTingConfig = majiang_conf.getCreateTableConfig(self.gameId, self.playMode, MFTDefine.CAN_TING, canTingId)
        if canTingConfig:
            self.logic_table.tableConfig[MTDefine.TING_SETTING] = canTingConfig.get('value', MTDefine.TING_NO)
            ftlog.debug('MajiangFriendTable.processCreateTableSetting tingSetting:', self.logic_table.tableConfig[MTDefine.TING_SETTING])
            
        # 配置38，是否允许漂
        canPiaoId = self.initParams.get(MFTDefine.CAN_PIAO, MTDefine.PIAO_UNDEFINE)
        canPiaoConfig = majiang_conf.getCreateTableConfig(self.gameId, self.playMode, MFTDefine.CAN_PIAO, canPiaoId)
        if canPiaoConfig:
            self.logic_table.tableConfig[MTDefine.PIAO_SETTING] = canPiaoConfig.get('value', MTDefine.PIAO_NO)
            ftlog.debug('MajiangFriendTable.processCreateTableSetting piaoSetting:', self.logic_table.tableConfig[MTDefine.PIAO_SETTING])
          
        # 配置39，是否允许加倍  
        canDoubleId = self.initParams.get(MFTDefine.CAN_DOUBLE, MTDefine.DOUBLE_UNDEFINE)
        canDoubleConfig = majiang_conf.getCreateTableConfig(self.gameId, self.playMode, MFTDefine.CAN_DOUBLE, canDoubleId)
        if canDoubleConfig:
            self.logic_table.tableConfig[MTDefine.DOUBLE_SETTING] = canDoubleConfig.get('value', MTDefine.DOUBLE_NO)
            ftlog.debug('MajiangFriendTable.processCreateTableSetting doubleSetting:', self.logic_table.tableConfig[MTDefine.DOUBLE_SETTING])

        # 配置40，胡牌方式
        winSetId = self.initParams.get("winsetting", 0)
        winSetConfig = majiang_conf.getCreateTableConfig(self.gameId, self.playMode, "winsetting", winSetId)
        if winSetConfig:
            self.logic_table.tableConfig[MTDefine.WIN_SETTING] = winSetConfig.get('type', MTDefine.WIN_TYPE1)
            ftlog.debug('MajiangFriendTable.processCreateTableSetting winSetting:',
                        self.logic_table.tableConfig[MTDefine.WIN_SETTING])

        # 配置41，初始积分
        initScore = self.initParams.get("initScore", 0)
        initScoreConfig = majiang_conf.getCreateTableConfig(self.gameId, self.playMode, "initScore", initScore)
        if initScoreConfig:
            self.logic_table.tableConfig[MFTDefine.INIT_SCORE] = initScoreConfig.get('value', 0)
            ftlog.debug('MajiangFriendTable.processCreateTableSetting initScoreConfig:',
                        self.logic_table.tableConfig[MFTDefine.INIT_SCORE])

        # 配置42，对亮对翻
        duiLiangDuiFan = self.initParams.get("duiliangduifan", 0)
        duiLiangDuiFanConfig = majiang_conf.getCreateTableConfig(self.gameId, self.playMode, "duiliangduifan", duiLiangDuiFan)
        if duiLiangDuiFanConfig:
            self.logic_table.tableConfig[MTDefine.DUILIANGDUIFAN] = duiLiangDuiFanConfig.get(MTDefine.DUILIANGDUIFAN,0)
            ftlog.debug('MajiangFriendTable.processCreateTableSetting duiliangduifan:',
                        self.logic_table.tableConfig[MTDefine.DUILIANGDUIFAN])
        # 配置43 换三张
        change3tilesId = self.initParams.get('change3Tiles', 0)
        change3tilesConfig = majiang_conf.getCreateTableConfig(self.gameId, self.playMode, 'change3Tiles', change3tilesId)
        if change3tilesConfig:
            self.logic_table.tableConfig[MTDefine.CHANGE3TILES] = change3tilesConfig.get(MTDefine.CHANGE3TILES, 0)
            ftlog.debug('MajiangFriendTable.processCreateTableSetting change3Tiles:', self.logic_table.tableConfig[MTDefine.CHANGE3TILES])
       
        # 配置43 将对
        jiangduiId = self.initParams.get('jiangdui', 0)
        jiangduiConfig = majiang_conf.getCreateTableConfig(self.gameId, self.playMode, 'jiangdui', jiangduiId)
        if jiangduiConfig:
            self.logic_table.tableConfig[MTDefine.JIANGDUI] = jiangduiConfig.get(MTDefine.JIANGDUI, 0)
            ftlog.debug('MajiangFriendTable.processCreateTableSetting jiangdui:', self.logic_table.tableConfig[MTDefine.JIANGDUI])

        # 配置43 中发白
        zhongfabaiId = self.initParams.get('nozfb', 0)
        zhongfabaiConfig = majiang_conf.getCreateTableConfig(self.gameId, self.playMode, 'nozfb', zhongfabaiId)
        if zhongfabaiConfig:
            self.logic_table.tableConfig[MTDefine.CHOOSE_ZFB] = zhongfabaiConfig.get(MTDefine.CHOOSE_ZFB, 0)
            ftlog.debug('MajiangFriendTable.processCreateTableSetting CHOOSE_ZFB:', self.logic_table.tableConfig[MTDefine.CHOOSE_ZFB])

        # 配置43 中发白
        gangwithtingId = self.initParams.get('gangWithTing', 0)
        gangwithtingConfig = majiang_conf.getCreateTableConfig(self.gameId, self.playMode, 'gangWithTing', gangwithtingId)
        if gangwithtingConfig:
            self.logic_table.tableConfig[MTDefine.GANGWITHTING] = gangwithtingConfig.get(MTDefine.GANGWITHTING, 0)
            ftlog.debug('MajiangFriendTable.processCreateTableSetting GANGWITHTING:', self.logic_table.tableConfig[MTDefine.GANGWITHTING]) 

        # 配置44 两杠满番
	
        lianggangmanfanId = self.initParams.get('lianggangmanfan', 0)
        lianggangConfig = majiang_conf.getCreateTableConfig(self.gameId, self.playMode, 'lianggangmanfan', lianggangmanfanId)
        if lianggangConfig:
            self.logic_table.tableConfig[MTDefine.LIANGGANGMANFAN] = lianggangConfig.get(MTDefine.LIANGGANGMANFAN, 0)
            ftlog.debug('MajiangFriendTable.processCreateTableSetting LIANGGANGMANFAN:', self.logic_table.tableConfig[MTDefine.LIANGGANGMANFAN])

        # 配置45 自摸加分
        zimojiafenId = self.initParams.get('zimojiafen', 0)
        zimojiafenConfig = majiang_conf.getCreateTableConfig(self.gameId, self.playMode, 'zimojiafen', zimojiafenId)
        if zimojiafenConfig:
            self.logic_table.tableConfig[MTDefine.ZIMOJIAFEN] = zimojiafenConfig.get(MTDefine.ZIMOJIAFEN, 0)
            ftlog.debug('MajiangFriendTable.processCreateTableSetting ZIMOJIAFEN:', self.logic_table.tableConfig[MTDefine.ZIMOJIAFEN])
                
        # 配置46 自摸加倍
        zimoDoubleId = self.initParams.get('zimoDouble', 0)
        zimoDoubleConfig = majiang_conf.getCreateTableConfig(self.gameId, self.playMode, 'zimoDouble', zimoDoubleId)
        if zimoDoubleConfig:
            self.logic_table.tableConfig[MTDefine.ZIMODOUBLE] = zimoDoubleConfig.get(MTDefine.ZIMODOUBLE, 0)
            ftlog.debug('MajiangFriendTable.processCreateTableSetting ZIMODOUBLE:', self.logic_table.tableConfig[MTDefine.ZIMODOUBLE])

        # 配置47 清一色加倍
        qingyiseDoubleId = self.initParams.get('qingyiseDouble', 0)
        qingyiseDoubleConfig = majiang_conf.getCreateTableConfig(self.gameId, self.playMode, 'qingyiseDouble', qingyiseDoubleId)
        if qingyiseDoubleConfig:
            self.logic_table.tableConfig[MTDefine.QINGYISEDOUBLE] = qingyiseDoubleConfig.get(MTDefine.QINGYISEDOUBLE, 0)
            ftlog.debug('MajiangFriendTable.processCreateTableSetting QINGYISEDOUBLE:', self.logic_table.tableConfig[MTDefine.QINGYISEDOUBLE])

        # 配置48 七对加倍
        qiduiDoubleId = self.initParams.get('qiduiDouble', 0)
        qiduiDoubleConfig = majiang_conf.getCreateTableConfig(self.gameId, self.playMode, 'qiduiDouble', qiduiDoubleId)
        if qiduiDoubleConfig:
            self.logic_table.tableConfig[MTDefine.QIDUIDOUBLE] = qiduiDoubleConfig.get(MTDefine.QIDUIDOUBLE, 0)
            ftlog.debug('MajiangFriendTable.processCreateTableSetting QIDUIDOUBLE:', self.logic_table.tableConfig[MTDefine.QIDUIDOUBLE])            
        
        #配置49 杠上炮
        gangshangpaoFanId = self.initParams.get('gangshangpaoFan', 0)
        gangshangpaoFanConfig = majiang_conf.getCreateTableConfig(self.gameId, self.playMode, 'gangshangpaoFan', gangshangpaoFanId)
        if gangshangpaoFanConfig:
            self.logic_table.tableConfig[MTDefine.GANGSHANGPAO] = gangshangpaoFanConfig.get(MTDefine.GANGSHANGPAO, 0)
            ftlog.debug('MajiangFriendTable.processCreateTableSetting GANGSHANGPAO:', self.logic_table.tableConfig[MTDefine.GANGSHANGPAO])  
            ftlog.debug('MajiangFriendTable.gangshangpaoFanId:',gangshangpaoFanId,' gangshangpaoFanConfig:',gangshangpaoFanConfig)  


        # 配置50 金钩钓加倍
        jingoudiaoDoubleId = self.initParams.get('jingoudiaoDouble', 0)
        jingoudiaoDoubleConfig = majiang_conf.getCreateTableConfig(self.gameId, self.playMode, 'jingoudiaoDouble', jingoudiaoDoubleId)
        if jingoudiaoDoubleConfig:
            self.logic_table.tableConfig[MTDefine.JINGOUDIAODOUBLE] = jingoudiaoDoubleConfig.get(MTDefine.JINGOUDIAODOUBLE, 0)
            ftlog.debug('MajiangFriendTable.processCreateTableSetting JINGOUDIAODOUBLE:', self.logic_table.tableConfig[MTDefine.JINGOUDIAODOUBLE])

        #配置54 房卡支付方式
        Fangka_Pay= self.initParams.get('fangka_pay', 0)
        FangkaPayConfig = majiang_conf.getCreateTableConfig(self.gameId, self.playMode, 'fangka_pay', Fangka_Pay)
        if FangkaPayConfig:
            self.logic_table.tableConfig[MTDefine.FANGKA_PAY] = FangkaPayConfig.get('value', 0)
            ftlog.debug('MajiangFriendTable.processCreateTableSetting Fangka Pay Config:', self.logic_table.tableConfig[MTDefine.FANGKA_PAY])

        # 配置55 呼叫转移
        hujiaozhuanyiId = self.initParams.get('hujiaozhuanyi', 0)
        hujiaozhuanyiConfig = majiang_conf.getCreateTableConfig(self.gameId, self.playMode, 'hujiaozhuanyi', hujiaozhuanyiId)
        if hujiaozhuanyiConfig:
            self.logic_table.tableConfig[MTDefine.HUJIAOZHUANYI] = hujiaozhuanyiConfig.get(MTDefine.HUJIAOZHUANYI, 0)
            ftlog.debug('MajiangFriendTable.processCreateTableSetting HUJIAOZHUANYI:', self.logic_table.tableConfig[MTDefine.HUJIAOZHUANYI])

        # 配置56 杠上杠
        gangshanggangId = self.initParams.get('gangshanggang', 0)
        gangshanggangConfig = majiang_conf.getCreateTableConfig(self.gameId, self.playMode, 'gangshanggang', gangshanggangId)
        if gangshanggangConfig:
            self.logic_table.tableConfig[MTDefine.GANGSHANGGANG] = gangshanggangConfig.get(MTDefine.GANGSHANGGANG, 0)
            ftlog.debug('MajiangFriendTable.processCreateTableSetting GANGSHANGGANG:', self.logic_table.tableConfig[MTDefine.GANGSHANGGANG])

        # 配置57 放胡
        fanghuId = self.initParams.get('fangHu', 1)
        fanghuConfig = majiang_conf.getCreateTableConfig(self.gameId, self.playMode, 'fangHu', fanghuId)
        if fanghuConfig:
            self.logic_table.tableConfig[MTDefine.FANGHU] = fanghuConfig.get('value', 1)
            ftlog.debug('MajiangFriendTable.processCreateTableSetting FANGHU:', self.logic_table.tableConfig[MTDefine.FANGHU])

        # 配置58 混一色
        qinghunyiseId = self.initParams.get('qinghunyise', 0)
        qinghunyiseConfig = majiang_conf.getCreateTableConfig(self.gameId, self.playMode, 'qinghunyise', qinghunyiseId)
        if qinghunyiseConfig:
            self.logic_table.tableConfig[MTDefine.QINGHUNYISE] = qinghunyiseConfig.get(MTDefine.QINGHUNYISE, 0)
            ftlog.debug('MajiangFriendTable.processCreateTableSetting QINGHUNYISE:', self.logic_table.tableConfig[MTDefine.QINGHUNYISE])

        # 配置59 金雀开口不平胡
        jinquekaikouId = self.initParams.get('jinquekaikou', 0)
        jinquekaikouConfig = majiang_conf.getCreateTableConfig(self.gameId, self.playMode, 'jinquekaikou', jinquekaikouId)
        if jinquekaikouConfig:
            self.logic_table.tableConfig[MTDefine.JINQUEKAIKOU] = jinquekaikouConfig.get(MTDefine.JINQUEKAIKOU, 0)
            ftlog.debug('MajiangFriendTable.processCreateTableSetting JINQUEKAIKOU:', self.logic_table.tableConfig[MTDefine.JINQUEKAIKOU])

        # 配置60 单钓剩金不平胡
        dandiaoshengjinId = self.initParams.get('dandiaoshengjin', 0)
        dandiaoshengjinConfig = majiang_conf.getCreateTableConfig(self.gameId, self.playMode, 'dandiaoshengjin', dandiaoshengjinId)
        if dandiaoshengjinConfig:
            self.logic_table.tableConfig[MTDefine.DANDIAOSHENGJIN] = dandiaoshengjinConfig.get(MTDefine.DANDIAOSHENGJIN, 0)
            ftlog.debug('MajiangFriendTable.processCreateTableSetting DANDIAOSHENGJIN:', self.logic_table.tableConfig[MTDefine.DANDIAOSHENGJIN]) 

        # 配置61 连庄加局
        lianzhuangId = self.initParams.get('lianzhuangjiaju', 0)
        lianzhuangConfig = majiang_conf.getCreateTableConfig(self.gameId, self.playMode, 'lianzhuangjiaju', lianzhuangId)
        if lianzhuangConfig:
            self.logic_table.tableConfig[MTDefine.LIANZHUANGJIAJU] = lianzhuangConfig.get(MTDefine.LIANZHUANGJIAJU, 0)
            ftlog.debug('MajiangFriendTable.processCreateTableSetting LIANZHUANGJIABEI:', self.logic_table.tableConfig[MTDefine.LIANZHUANGJIAJU]) 

        # 把用户设定的逻辑桌配置传递给 WinRule
        self.logic_table.winRuleMgr.setTableConfig(self.logic_table.tableConfig)

    def nextRoundOrReady(self, msg, userId, seatId, action, clientId):
        '''
        table_call next_round
        '''
        self.logic_table.sendMsgTableInfo(seatId)
        beginGame = self.logic_table.playerReady(seatId, True)
        self.logic_table.msgProcessor.create_table_succ_response(userId, seatId, 'ready', 1 if (userId == self.__table_owner) else 0, self.logic_table.getBroadCastUIDs())
        for player in self.logic_table.player:
            if not player:
                continue
            
            if (not TYPlayer.isHuman(player.userId)) and (not player.isReady()):
                beginGame = self.logic_table.playerReady(player.curSeatId, True)
        
        if beginGame:
            #纪录上一局的日志 给GM使用
            #addOneResult(tableNo, seats, deltaScore, totalScore, curRound, totalRound, gameId, roomId, tableId)
            if self.logic_table.tableConfig[MFTDefine.CUR_ROUND_COUNT] > 1 and len(self.logic_table.tableResult.results) > 0:
                roundResult = self.logic_table.tableResult.results[-1]
                deltaScore = roundResult.score
                totalScore = self.logic_table.tableResult.score
                curRound = self.logic_table.tableConfig[MFTDefine.CUR_ROUND_COUNT] - 1
                totalRound = self.logic_table.tableConfig[MFTDefine.ROUND_COUNT]
                seats = self.logic_table.getSeats()
                ftlog.debug('MajiangFriendTable.doTableCall nextRound stat tableNo', self.ftId, 'seats', seats, 'deltaScore:', 
                            deltaScore, 'totalScore:', totalScore, 'gameId:', self.gameId, 'roomId:', self.roomId, 'tableId', self.tableId)
                hall_friend_table.addOneResult(self.ftId, seats, deltaScore, totalScore, curRound, totalRound, self.gameId, self.roomId, self.tableId)
            
            if not self.reportGameBegin:
                #纪录开局日志 gameBegin(tableNo, seats, gameId, roomId, tableId)
                self.setReportGameBegin(True)
                seats = self.logic_table.getSeats()
                ftlog.debug('MajiangFriendTable._doTableCall log game begin tableNo:', self.__ftId, 'seats:', seats, 'gameId:', self.gameId, 'roomId:', self.roomId, 'tableId', self.tableId)
                hall_friend_table.gameBegin(self.__ftId, seats, self.gameId, self.gameId, self.tableId)
                
        else:
            ftlog.debug('MajiangFriendTable.doTableCall nextRound stat log error not begin')
            
    def resumeFangKa(self, uids):
        if (self.logic_table.tableConfig[MFTDefine.LEFT_CARD_COUNT] > 0) and \
                    (not self.getRoomConfig(MTDefine.HAS_ROBOT, 0)) and \
                    (not self.getRoomConfig(MFTDefine.LATE_CONSUME_FANGKA, 0)):
            itemId = self.room.roomConf.get('create_item', None)
            if itemId:
                consume_fangka_count = self.logic_table.tableConfig[MFTDefine.LEFT_CARD_COUNT]
                if self.logic_table.tableConfig.get(MTDefine.SHARE_FANGKA,0):
                    consume_fangka_count = self.logic_table.tableConfig[MFTDefine.CARD_COUNT]/self.logic_table.playerCount
                    for player in self.players:
                        if not player or player.userId not in uids:
                            continue
                        
                        ftlog.info('MajiangFriendTable.resumeFangKa userId:', player.userId
                                                , ' gameId:', self.gameId
                                                , ' itemId:', itemId
                                                , ' itemCount:', consume_fangka_count
                                                , " table owner:",self.__table_owner
                                                , " roomId:", self.roomId
                                                , " bigRoomId", self.bigRoomId)
                        
                        user_remote.resumeItemFromTable(player.userId
                                        , self.gameId
                                        , itemId
                                        , consume_fangka_count
                                        , self.roomId
                                        , self.tableId
                                        , self.bigRoomId)
                else:
                    if self.tableOwner not in uids:
                        return
                    
                    user_remote.resumeItemFromTable(self.tableOwner
                                        , self.gameId
                                        , itemId
                                        , consume_fangka_count
                                        , self.roomId
                                        , self.tableId
                                        , self.bigRoomId)
            
    def createTableUserLeave(self, msg, userId, seatId, action, clientId):
        '''
        table_call action create_table_user_leave
        '''
        if (self.logic_table.tableConfig[MFTDefine.CUR_ROUND_COUNT] > 0):
            util.sendPopTipMsg(userId, "游戏已开始，不能解散")
            return
        
        # 房主解散，由前端主动发送，存在隐患，后续修改。房主建房后，掉线，房主的房间状态将不对，TODO
        if userId == self.tableOwner:
            ftlog.debug('MajiangFriendTable.create_table_user_leave owner leave...')
            # 解散时，给大家提示
            for player in self.logic_table.player:
                if not player:
                    continue
                # 通知
                util.sendPopTipMsg(player.userId, "房主解散房间")
                
            # 归还剩余房卡道具
            ftlog.debug('MajiangFriendTable.doTableCall leftCardCount:', self.logic_table.tableConfig[MFTDefine.LEFT_CARD_COUNT]
                    , ' tableOwner:', self.__table_owner)
            uids = self.logic_table.getBroadCastUIDs()
            self.resumeFangKa(uids)
            # 解散牌桌
            self.clearTable(True)
        else:
            self.resumeFangKa([userId])
            util.sendPopTipMsg(userId, "您已退出房间")
            self.kickOffUser(userId, seatId, True)
     
    def createTableDissolution(self, msg, userId, seatId, action, clientId):  
        '''
        table_call action  create_table_dissolution
        '''
        if self.logic_table.tableConfig.get(MFTDefine.CUR_BASE_COUNT, 0)==0 and self.logic_table.tableConfig[MFTDefine.CUR_ROUND_COUNT] == 0:
            ftlog.debug('MajiangFriendTable._doTableCall create_table_dissolution game not start, can not dissolved...')
            return
        
        # 投票解散牌桌
        if self.voteHost != MTDefine.INVALID_SEAT:
            ftlog.debug('MajiangFriendTable._doTableCall create_table_dissolution ', self.voteHost, ' already dissolved...')
            return
        
        self.__vote_host = seatId
        self.__vote_info[seatId] = {'userId': userId, 'seatId': seatId, 'vote': self.DISSOLVE_AGREE}
        self.__vote_time_out = self.getTableConfig('dissolve_vote_time_out', 60)
        ftlog.debug('MajiangFriendTable.create_table_dissolution voteInfo:', self.voteInfo)
        
        # 广播解散投票消息
        self.logic_table.msgProcessor.create_table_dissolve_vote(userId
                    , seatId
                    , self.maxSeatN
                    , self.get_leave_vote_info()
                    , self.get_leave_vote_info_detail()
                    , self.logic_table.player[seatId].name
                    , self.__vote_time_out
                    , self.logic_table.getBroadCastUIDs())
        
    def userLeaveVote(self, msg, userId, seatId, action, clientId):
        '''
        table_call cation user_leave_vote
        '''
        ftlog.debug('MajiangFriendTable._doTableCall voteInfo:', self.voteInfo)
        if self.voteHost == MTDefine.INVALID_SEAT:
            ftlog.debug('MajiangFriendTable._doTableCall user_leave_vote, voteHost is invalid, no need process this message...')
            return
        
        vote = msg.getParam('vote', self.DISSOLVE_REFUSE)
        self.__vote_info[seatId] = {'userId': userId, 'seatId': seatId, 'vote': vote}
        self.logic_table.msgProcessor.create_table_dissolve_vote(userId
                    , seatId
                    , self.maxSeatN
                    , self.get_leave_vote_info()
                    , self.get_leave_vote_info_detail()
                    , self.logic_table.player[self.voteHost].name
                    , self.__vote_time_out
                    , self.logic_table.getBroadCastUIDs())
        # 计算投票结果
        self.dissolveDecision()
        
    def createFriendInvite(self, msg, userId, seatId, action, clientId):
        '''
        table_call action create_friend_invite
        '''
        if self.gameId == 715:
            # 临时硬编码，对卡五星分享的内容做特殊定制
            contentArr = []
            for i in range(len(self.paramsOptionName)):
                if self.paramsOptionName[i] != "人数":
                    contentArr.append(self.__params_desc[i])
            contentStr = ', '.join(contentArr)
        else:
            contentStr = ','.join(self.__params_desc)
        util.sendTableInviteShareTodoTask(userId
                , self.gameId
                , self.ftId
                , self.playMode
                , self.logic_table.tableConfig[MFTDefine.CARD_COUNT]
                , contentStr)
         
    
    def _doTableCall(self, msg, userId, seatId, action, clientId):
        """
        继承父类，处理table_call消息
        单独处理自建桌的分享/解散
        """
        if not self.CheckSeatId(seatId, userId):
            ftlog.warn("MajiangFriendTable.doTableCall, delay msg action:", action
                    , ' seatId:', seatId
                    , ' messange:', msg)
            return
            
        if action == 'next_round':
            if self.logic_table.isStart():
                return
            self.nextRoundOrReady(msg, userId, seatId, action, clientId)
                
        elif action == 'ready':
            if self.logic_table.isStart():
                return
            self.nextRoundOrReady(msg, userId, seatId, action, clientId)
            
        elif action == 'create_table_user_leave':
            self.createTableUserLeave(msg, userId, seatId, action, clientId)
            
        elif action == 'create_table_dissolution':
            self.createTableDissolution(msg, userId, seatId, action, clientId)
            
        elif action == 'user_leave_vote':
            self.userLeaveVote(msg, userId, seatId, action, clientId)
                
        elif action == 'create_friend_invite': #微信邀请todotask下发
            self.createFriendInvite(msg, userId, seatId, action, clientId)
            
        elif action == 'friend_table_ready_time_out':# 准备超时，回收牌桌
            # 退还房卡
            uids = self.logic_table.getBroadCastUIDs()
            self.resumeFangKa(uids)
            self.clearTable(True)
            
        else:
            super(MajiangFriendTable, self)._doTableCall(msg, userId, seatId, action, clientId)
            
    """
    def kickOffUser(self, userId, seatId, sendLeave = False):
        # 拉出牌桌
        #游戏开始之后的退出，客户端不需要再收到退出消息 客户端的退出由其自身控制
        #游戏未开始时房主解散了房间才需要向客户端发消息
        if sendLeave:
            uids = self.logic_table.getBroadCastUIDs()
            self.logic_table.msgProcessor.create_table_dissolve(userId, seatId, 'dissolve', uids)
        super(MajiangFriendTable, self).kickOffUser(userId, seatId)
    """
            
    def _doStandUp(self, msg, userId, seatId, reason, clientId):
        '''
        自建桌这里的逻辑退出，不自动站起/退出
        '''
        pass
    
    @locked
    def handle_auto_decide_action(self):
        """牌桌定时器"""
        if self.__ready_time_out_timer and self.logic_table.isFriendTablePlaying():
            self.__ready_time_out_timer = False
            self.tableTimer.cancelTimer(self.tableOwnerSeatId)
        
        if self.voteHost != MTDefine.INVALID_SEAT:
            ftlog.debug('MajiangFriendTable.handle_auto_decide_action voteTimeOut--')
            self.__vote_time_out -= MTDefine.TABLE_TIMER
            ftlog.debug('voteTimeOut--111111111',self.__vote_time_out)
            for player in self.logic_table.player:
                if not player:
                    continue
                if not self.voteInfo[player.curSeatId] and player.isRobot():
                    self.__vote_info[player.curSeatId] = {'userId': player.userId, 'seatId': player.curSeatId, 'vote': self.DISSOLVE_AGREE}
                    self.logic_table.msgProcessor.create_table_dissolve_vote(player.userId
                        , player.curSeatId
                        , self.maxSeatN
                        , self.get_leave_vote_info()
                        , self.get_leave_vote_info_detail()
                        , self.logic_table.player[self.voteHost].name
                        , self.__vote_time_out
                        , self.logic_table.getBroadCastUIDs())
                    self.dissolveDecision()
                    break

            if self.voteTimeOut <= 0:
                self.processVoteDissolveTimeOut()
                
        if self.logic_table.isGameOver():
            """游戏结束，通知玩家离开，站起，重置牌桌"""
            ftlog.debug('MajiangFriendTable.handle_auto_decide_action gameOver... tableId:', self.tableId
                    , ' totalRoundCount:', self.logic_table.tableConfig[MFTDefine.ROUND_COUNT]
                    , ' now RoundCount:', self.logic_table.tableConfig[MFTDefine.CUR_ROUND_COUNT])
            
            #如果，表示按局数最终结算，否则按圈数结算
                    
            ftlog.debug('useQuan', 1, 
                        'CUR_ROUND_COUNT',self.logic_table.tableConfig[MFTDefine.CUR_ROUND_COUNT],
                        'ROUND_COUNT',self.logic_table.tableConfig[MFTDefine.ROUND_COUNT],
                        'CUR_QUAN_COUNT',self.logic_table.tableConfig[MFTDefine.CUR_QUAN_COUNT],
                        'QUAN_COUNT',self.logic_table.tableConfig[MFTDefine.QUAN_COUNT])
            
            if self.logic_table.isCountByRound():
                if self.logic_table.tableConfig[MFTDefine.CUR_ROUND_COUNT] == self.logic_table.tableConfig[MFTDefine.ROUND_COUNT]:
                    # TODO 自建桌最终结算
                    self.checkLateConsumeFangKa(isConsumeAllLeft=True)
                    self.logic_table.sendCreateExtendBudgetsInfo(0)
                    ftlog.debug('MajiangFriendTable.handle_auto_decide_action cur Table hasRobot:', self.getRoomConfig(MTDefine.HAS_ROBOT, 0))
                    if not self.getRoomConfig(MTDefine.HAS_ROBOT, 0):
                        self.saveRecordAfterTable()
                    self.clearTable(False)
                    return
            elif self.logic_table.isCountByQuan():
                if self.logic_table.tableConfig[MFTDefine.CUR_QUAN_COUNT] == self.logic_table.tableConfig[MFTDefine.QUAN_COUNT]:
                    # TODO 自建桌最终结算
                    ftlog.debug(':quanjiesuan')
                    self.checkLateConsumeFangKa(isConsumeAllLeft=True)
                    self.logic_table.sendCreateExtendBudgetsInfo(0)
                    if not self.getRoomConfig(MTDefine.HAS_ROBOT, 0):
                        self.saveRecordAfterTable()                   
                    self.clearTable(False)
                    return
            elif self.logic_table.isOverByBase():
                # TODO 自建桌最终结算 按玩家底分算 低分<=0 over
                ftlog.debug(':isOverByCardScore')
                self.checkLateConsumeFangKa(isConsumeAllLeft=True)
                self.logic_table.sendCreateExtendBudgetsInfo(0)
                if not self.getRoomConfig(MTDefine.HAS_ROBOT, 0):
                    self.saveRecordAfterTable()
                self.clearTable(False)
                return

            # 后扣房卡检查
            self.logic_table.tableConfig[MFTDefine.PASSED_ROUND_COUNT] += 1
            self.checkLateConsumeFangKa(isConsumeAllLeft=False)

            self.logic_table.nextRound()
            self.resetNoOptionTimeOut()
            return
        ftlog.debug('AutoDecide._checkGeo_internal called xxx') 
        self.actionHander.updateTimeOut(-MTDefine.TABLE_TIMER)
	self.logic_table.geoMixin.checkGeo_internal()
        self.actionHander.doAutoAction()
        self.checkNoOptionTimeOut()

    def checkLateConsumeFangKa(self, isConsumeAllLeft=False):
        """后扣房卡检查
        isConsumeAll: 表示是否扣掉所有的剩余待扣房卡数，否则只在奇数局结束时扣一张
        """
        if not self.logic_table.tableConfig.get(MFTDefine.LATE_CONSUME_FANGKA, 0):
            return

        ftId = self.logic_table.tableConfig[MFTDefine.FTID]
        passedRoundCount = self.logic_table.tableConfig[MFTDefine.PASSED_ROUND_COUNT]
        try:
            totalNeedCardCount = self.logic_table.tableConfig[MFTDefine.CARD_COUNT]
            if totalNeedCardCount <= 0:
                return

            if self.logic_table.tableConfig[MFTDefine.CONSUMED_FANGKA_COUNT] >= totalNeedCardCount:
                return

            count = 0
            if isConsumeAllLeft:  # 扣掉所有的剩余待扣房卡数
                count = totalNeedCardCount - self.logic_table.tableConfig[MFTDefine.CONSUMED_FANGKA_COUNT]
            else:
                if self.logic_table.tableConfig[MFTDefine.PASSED_ROUND_COUNT] % 2 == 1:  # 奇数局时才做房卡扣除
                    count = 1
            if count == 0:
                return

            ftlog.info('lateConsumeFangka<<|tableId,ftId,passedRoundCount,fangka:', self.tableId, ftId, passedRoundCount, count)
            self.logic_table.tableConfig[MFTDefine.CONSUMED_FANGKA_COUNT] += count
            fangkaId = self.logic_table.tableConfig.get(MFTDefine.CREATE_ITEM, None)
            user_remote.consumeItem(self.logic_table.tableConfig[MFTDefine.FTOWNER],
                                            self.gameId,
                                            fangkaId,
                                            count,
                                            self.roomId,
                                            self.bigRoomId)
        except Exception, e:
            ftlog.info('checkLateConsumeFangKa<<|tableId,ftId,passedRoundCount,err:', self.tableId, ftId, passedRoundCount, e.message)

    def resetNoOptionTimeOut(self):
        """充值无操作超时参数"""
        if self.__cur_no_option_time_out != -1:
            self.__cur_no_option_time_out = -1
            self.__cur_seat = 0
        
    def checkNoOptionTimeOut(self):
        """检查无操作超时"""
        if not self.getRoomConfig(MTDefine.HAS_ROBOT, 0):
            """非练习场不检查"""
            return
        
        curCount = self.logic_table.tableConfig.get(MFTDefine.CUR_ROUND_COUNT, 0)
        if curCount == 0:
            """牌桌不是玩牌状态，不检查"""
            return
        
        ftlog.debug('MajiangFriendTable.checkNoOptionTimeOut timeOut:', self.curNoOptionTimeOut
                , ' curSeat:', self.curSeat
                , ' ftOwner:', self.tableOwner
                , ' tableId:', self.tableId)
        nowSeat = self.logic_table.curSeat
        if (self.curNoOptionTimeOut == -1) or (self.curSeat != nowSeat):
            self.__cur_no_option_time_out = self.logic_table.getTableConfig(MFTDefine.CLEAR_TABLE_NO_OPTION_TIMEOUT, 3600)
            self.__cur_seat = nowSeat
        elif self.curNoOptionTimeOut > 0:
            self.__cur_no_option_time_out -= 1
            if self.curNoOptionTimeOut <= 0:
                self.resetNoOptionTimeOut()
                self.clearTable(True)
        
    def processVoteDissolveTimeOut(self):
        """超时自动处理解散投票"""
        ftlog.debug('MajiangFriendTable.processVoteDissolveTimeOut...')
        for player in self.logic_table.player:
            if not player:
                continue
            
            if not self.voteInfo[player.curSeatId]:
                self.__vote_info[player.curSeatId] = {'userId': player.userId, 'seatId': player.curSeatId, 'vote': self.DISSOLVE_AGREE}
        self.dissolveDecision()
        
    def resetVoteInfo(self):
        self.__vote_host = MTDefine.INVALID_SEAT
        self.__vote_info = [None for _ in range(self.maxSeatN)]
        self.__vote_time_out = 0
    
    def dissolveDecision(self):
        """计算投票结果"""
        ftlog.debug('MajiangFriendTable.dissolveDecision voteInfo:', self.voteInfo)
        
        agree = 0
        refuse = 0
        for info in self.voteInfo:
            if not info:
                continue
            
            if info['vote'] == self.DISSOLVE_AGREE:
                agree += 1
            if info['vote'] == self.DISSOLVE_REFUSE:
                refuse += 1
        
        ftlog.debug('MajiangFriendTable.dissolveDecision agree and refuse:',agree,refuse)
        bClear = False
	
        if (agree + refuse) == self.maxSeatN:
            self.resetVoteInfo()
            if agree > refuse:
                bClear = True
            else:
                for player in self.logic_table.player:
                    if not player:
                        continue
                    util.sendPopTipMsg(player.userId, "经投票，牌桌继续...")
                    self.logic_table.msgProcessor.create_table_dissolve_close_vote(player.userId, player.curSeatId)
        else:
            voteConfig = self.getTableConfig(MFTDefine.LEAVE_VOTE_NUM, {})
            ftlog.debug('MajiangFriendTable.dissolveDecision voteConfig:', voteConfig)
            strCount = str(self.logic_table.playerCount) 
            #'4':3  '3':2
            count = voteConfig.get(strCount, 0)
            if count and agree >= count:
                bClear = True
        # 新增投票规则
        # 如果设置REFUSE_LEAVE_VOTE_NUM 当投拒绝票数>=设定数则本局继续,default as 1 refuse
        refuseVoteConfig = self.getTableConfig(MFTDefine.REFUSE_LEAVE_VOTE_NUM, {})
        ftlog.debug('MajiangFriendTable.dissolveDecision refusevoteConfig:', refuseVoteConfig)
        if refuseVoteConfig:
           strCount = str(self.logic_table.playerCount)
           refuseCount = refuseVoteConfig.get(strCount, 1)
           ftlog.debug('MajiangFriendTable.dissolveDecision refuse:', refuseCount, refuse)
           if refuse >= refuseCount:
            for player in self.logic_table.player:
                if not player:
                    continue
                util.sendPopTipMsg(player.userId, "经投票，牌桌继续...")
                self.logic_table.msgProcessor.create_table_dissolve_close_vote(player.userId, player.curSeatId)
            self.resetVoteInfo()
            return
        
           if self.maxSeatN == agree:
            bClear = True
           else:
            # 等待投票结果或者超时
            return
        
        if bClear:
            self.logic_table.setVoteHost(self.voteHost)
            self.resetVoteInfo()
            # 解散牌桌时发送大结算
            self.logic_table.setVoteFinal(True)
            self.logic_table.sendCreateExtendBudgetsInfo(0)
            
            ftlog.debug('MajiangFriendTable.dissolveDecision cur Table hasRobot:', self.getRoomConfig(MTDefine.HAS_ROBOT, 0))
            if not self.getRoomConfig(MTDefine.HAS_ROBOT, 0):
                self.saveRecordAfterTable()
            
            # 归还剩余房卡道具
            if self.logic_table.tableConfig.get(MTDefine.RESUME_ITEM_AFTER_BEGIN, 1):
                uids = self.logic_table.getBroadCastUIDs()
                self.resumeFangKa(uids)
            # 通知玩家离开
            for player in self.logic_table.player:
                if not player:
                    continue
                
                util.sendPopTipMsg(player.userId, "经投票，牌桌已解散")
                self.logic_table.msgProcessor.create_table_dissolve_close_vote(player.userId, player.curSeatId, True)
                
            # 牌桌解散
            self.clearTable(False)
 
    def get_leave_vote_info(self):
        """获取投票简要信息"""
        agree = 0
        disagree = 0
        for info in self.voteInfo:
            if not info:
                continue
            
            if info['vote'] == self.DISSOLVE_AGREE:
                agree += 1
            elif info['vote'] == self.DISSOLVE_REFUSE:
                disagree += 1
        return {'disagree': disagree, 'agree':agree}
    
    def get_leave_vote_info_detail(self):
        '''20160909新需求添加，增加用户头像,用户名等信息'''
        retList = []
        for info in self.voteInfo:
            if not info:
                continue
            
            retData = {}
            seatId = info['seatId']
            retData['name'], retData['purl'] = self.logic_table.player[seatId].name, self.logic_table.player[seatId].purl
            retData['vote'] = info['vote']
            retData['userId'] = info['userId']
            retList.append(retData) 
        return retList
    
    def clearTable(self, sendLeave):
        self.setReportGameBegin(False)
        #纪录最后一局日志和结束日志 
        seats = self.logic_table.getSeats()
        if self.logic_table.tableConfig[MFTDefine.CUR_ROUND_COUNT] == self.logic_table.tableConfig[MFTDefine.ROUND_COUNT]:
            if len(self.logic_table.tableResult.results) > 0:
                roundResult = self.logic_table.tableResult.results[-1]
                deltaScore = roundResult.score
                totalScore = self.logic_table.tableResult.score
                curRound = self.logic_table.tableConfig[MFTDefine.CUR_ROUND_COUNT]
                totalRound = self.logic_table.tableConfig[MFTDefine.ROUND_COUNT]
                ftlog.debug('MajiangFriendTable.cleraTable stat tableNo', self.ftId, 'seats', seats, 'deltaScore:', 
                            deltaScore, 'totalScore:', totalScore, 'gameId:', self.gameId, 'roomId:', self.roomId, 'tableId', self.tableId)
                hall_friend_table.addOneResult(self.ftId, seats, deltaScore, totalScore, curRound, totalRound, self.gameId, self.roomId, self.tableId)
            else:
                ftlog.debug('MajiangFriendTable.cleraTable CUR_ROUND_COUNT', 
                            self.logic_table.tableConfig[MFTDefine.CUR_ROUND_COUNT],
                            'ROUND_COUNT',
                            self.logic_table.tableConfig[MFTDefine.ROUND_COUNT])
        
        #def gameEnd(tableNo, seats, totalScore, totalRound, gameId, roomId, tableId)
        if self.logic_table.tableConfig[MFTDefine.CUR_ROUND_COUNT] > 0:
            totalScore = self.logic_table.tableResult.score
            if not totalScore:
                totalScore = [0 for _ in range(self.logic_table.playerCount)]
            totalRound = self.logic_table.tableConfig[MFTDefine.ROUND_COUNT]
            ftlog.debug('MajiangFriendTable.cleraTable stat gameEnd tableNo:', self.ftId, 'seats:', seats,
                        'totalScore:', totalScore, 'totalRound:', totalRound, 
                        'gameId:', self.gameId, 'roomId:', self.roomId, 
                        'tableId:', self.tableId)
            hall_friend_table.gameEnd(self.ftId, seats, totalScore, totalRound, self.gameId, self.roomId, self.tableId)
        
        """清理桌子"""
        super(MajiangFriendTable, self).clearTable(sendLeave)
        # 释放大厅房间ID
        hall_friend_table.releaseFriendTable(self.gameId, self.ftId)
        CreateTableData.removeCreateTableNo(gdata.serverId(), self.ftId)
        
    def getTableScore(self):
        '''
        取得当前桌子的快速开始的评分
        越是最适合进入的桌子, 评分越高, 座位已满评分为0
        '''
        if self.maxSeatN <= 0 :
            ftlog.info('MajiangFriendTable.getTableScore return 1')
            return 1
        
        # 自建桌逻辑特殊，有人坐下后，后续就不安排人坐下了
        if self.realPlayerNum > 0:
            ftlog.info('MajiangFriendTable.getTableScore friendTable has User, return 0')
            return 0
        
        return (self.realPlayerNum + 1) * 100 / self.maxSeatN
