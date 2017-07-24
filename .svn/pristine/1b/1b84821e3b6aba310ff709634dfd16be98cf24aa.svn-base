# -*- coding=utf-8
'''
Created on 2016年9月23日
上行行为处理

@author: zhaol
'''
from majiang2.table_state.state import MTableState
from majiang2.ai.tile_value import MTileValue
from freetime.util import log as ftlog
from majiang2.table.table_config_define import MTDefine

class ActionHandler(object):
    # 出
    ACTION_DROP = 1
    # 吃
    ACTION_CHI = 2
    # 碰
    ACTION_PENG = 3
    # 杠
    ACTION_GANG = 4
    # 听
    ACTION_TING = 5
    # 和
    ACTION_HU = 6
    # 锚/蛋
    ACTION_MAO = 7
    
    def __init__(self):
        super(ActionHandler, self).__init__()
        self.__table = None
        
    @property
    def table(self):
        return self.__table
    
    def setTable(self, table):
        """设置牌桌"""
        self.__table = table
        
    def processAction(self, cmd):
        pass
    
    def updateTimeOut(self, delta):
        if self.table.addCardProcessor.getState() > 0:
            self.table.addCardProcessor.updateTimeOut(delta)
            
        if self.table.dropCardProcessor.getState() > 0:
            self.table.dropCardProcessor.updateTimeOut(delta)
            
        if self.table.piaoProcessor.getState() > 0:
            self.table.piaoProcessor.updateTimeOut(delta)
            
        if self.table.doubleProcessor.getState() > 0:
            self.table.doubleProcessor.updateTimeOut(delta)

        if self.table.zhisaiziProcessor.getState() > 0:
            self.table.zhisaiziProcessor.updateTimeOut(delta)
    
    def doAutoAction(self):
        """自动行为，关注当前牌局是否正在开始"""

        ftlog.debug('')
        ftlog.debug('[ActionHandler] =====Timer Start Check AutoAction =====')
        ftlog.debug('ActionHandler.doAutoAction self.table.flowerProcessor.getState()=',self.table.flowerProcessor.getState())
	ftlog.debug('ActionHandler.doAutoAction self.table.curState()=',self.table.curState())
	ftlog.debug('ActionHandler.doAutoAction self.table.kaijinProcessor.getState()=',self.table.kaijinProcessor.getState())
	ftlog.debug('ActionHandler.doAutoAction self.table.qiangjinProcessor.getState()=',self.table.qiangjinProcessor.getState())
        if not self.table.isPlaying():
            return

        if self.table.curState() == MTableState.TABLE_STATE_NEXT:
            ftlog.debug( 'ActionHandler.gameNext...' )
            self.table.gameNext()
            return True
        
        if self.table.zhisaiziProcessor.updateProcessor(MTableState.TABLE_STATE_NEXT):
            self.table.autoDecideCrapShoot()
            return True

        if self.table.flowerProcessor.getState() == MTableState.TABLE_STATE_BUFLOWER:
            self.table.autoBuFlower()
            return True

        if self.table.kaijinProcessor.getState() ==  MTableState.TABLE_STATE_KAIJIN:
            self.table.autoKaijin()
            return True

        seats = self.table.piaoProcessor.getAutoDecideSeatsBySchedule()
        for seat in seats:
            self.table.autoDecidePiao(seat)
        if len(seats) > 0:
            return True
        
        seats = self.table.doubleProcessor.getAutoDecideSeatsBySchedule()
        for seat in seats:
            self.table.autoDecideDouble(seat)
        if len(seats) > 0:
            return True

        if MTDefine.INVALID_SEAT != self.table.addCardProcessor.hasAutoDecideAction(self.table.curSeat, self.table.tableConfig[MTDefine.TRUSTTEE_TIMEOUT]):
            ftlog.debug( 'ActionHandler.addCardProcessor.hasAutoDecideAction curSeat: ', self.table.curSeat
                         , ' trustTeeSet:', self.table.tableConfig[MTDefine.TRUSTTEE_TIMEOUT] )
            self.autoProcessAddCard()
            return True
            
        seatIds = self.table.dropCardProcessor.hasAutoDecideAction(self.table.curSeat, self.table.tableConfig[MTDefine.TRUSTTEE_TIMEOUT])
        if len(seatIds) > 0:
            ftlog.debug( 'ActionHandler.dropCardProcessor.hasAutoDecideAction seatIds:', seatIds )
            self.autoProcessDropCard(seatIds)
            return True
        
        seatId = self.table.louHuProcesssor.hasAutoDecideAction(self.table.curSeat, self.table.tableConfig[MTDefine.TRUSTTEE_TIMEOUT])
        if seatId != MTDefine.INVALID_SEAT and \
            (not self.table.dropCardProcessor.getState() & MTableState.TABLE_STATE_HU):
            ftlog.debug('ActionHandler.louHuProcesssor.hasAutoDecideAction seatId:', seatId)
            self.autoProcessLouHu(seatId)
            return True
        
        seatId = self.table.daFengProcessor.hasAutoDecideAction(self.table.curSeat, self.table.tableConfig[MTDefine.TRUSTTEE_TIMEOUT])
        if seatId != MTDefine.INVALID_SEAT:
            self.autoProcessDaFeng(seatId)
            return True
        
        seatIds = self.table.qiangGangHuProcessor.hasAutoDecideAction(self.table.curSeat, self.table.tableConfig[MTDefine.TRUSTTEE_TIMEOUT])
        if len(seatIds) > 0:
            ftlog.debug('ActionHandler.qiangGangHuProcessor.hasAutoDecideAction seatId:', seatIds)
            self.autoProcessQiangGangHu(seatIds)
            return True
        
        seatId = self.table.qiangExmaoPengProcessor.hasAutoDecideAction(self.table.curSeat, self.table.tableConfig[MTDefine.TRUSTTEE_TIMEOUT])
        if seatId != MTDefine.INVALID_SEAT:
            ftlog.debug('ActionHandler.qiangExmaoPengProcessor.hasAutoDecideAction seatId:', seatId)
            self.autoProcessQiangExmaoPeng(seatId)
            return True
        
        seatIds = self.table.qiangExmaoHuProcessor.hasAutoDecideAction(self.table.curSeat, self.table.tableConfig[MTDefine.TRUSTTEE_TIMEOUT])
        if len(seatIds) > 0:
            ftlog.debug('ActionHandler.qiangExmaoHuProcessor.hasAutoDecideAction seatId:', seatIds[0])
            self.autoProcessQiangExmaoHu(seatIds)
            return True
        
        seatId = self.table.tingBeforeAddCardProcessor.hasAutoDecideAction(self.table.curSeat, self.table.tableConfig[MTDefine.TRUSTTEE_TIMEOUT])
        if seatId != MTDefine.INVALID_SEAT:
            ftlog.debug('ActionHandler.tingBeforeAddCardProcessor.hasAutoDecideAction seatId:', seatId)
            self.autoProcessTingBeforeAddTile(seatId)
            return True

        seatId = self.table.tianTingProcessor.hasAutoDecideAction(self.table.curSeat, self.table.tableConfig[ MTDefine.TRUSTTEE_TIMEOUT])
        if seatId != MTDefine.INVALID_SEAT:
            ftlog.debug('ActionHandler.tingBeforeAddCardProcessor.hasAutoDecideAction seatId:', seatId)
            self.autoProcessTianTing(seatId)
            return True
        
        return False
    
    def autoProcessTingBeforeAddTile(self, seatId):
        if (self.table.getTableConfig(MTDefine.ROBOT_LEVEL, MTDefine.ROBOT_SMART) == MTDefine.ROBOT_FOOLISH) and \
            self.table.player[seatId].isRobot():
            # 傻瓜级别AI，不抢杠和
            self.table.playerCancel(seatId)
            return
        self.table.tingBeforeAddCard(seatId, self.table.actionID)

    def autoProcessTianTing(self, seatId):
        if (self.table.getTableConfig(MTDefine.ROBOT_LEVEL, MTDefine.ROBOT_SMART) == MTDefine.ROBOT_FOOLISH) and \
            self.table.player[seatId].isRobot():
            # 傻瓜级别AI，不抢杠和
            self.table.playerCancel(seatId)
            return
        self.table.tianTing(seatId, self.table.actionID)
    
    def autoProcessQiangExmaoPeng(self, seatId):
        if (self.table.getTableConfig(MTDefine.ROBOT_LEVEL, MTDefine.ROBOT_SMART) == MTDefine.ROBOT_FOOLISH) and \
            self.table.player[seatId].isRobot():
            # 傻瓜级别AI，不抢杠和
            self.table.playerCancel(seatId)
            return

        state = self.table.qiangExmaoPengProcessor.getState()
        if state & MTableState.TABLE_STATE_GANG:
            extend = self.table.qiangExmaoPengProcessor.exmaoExtend
            gang = extend.getChoosedInfo(MTableState.TABLE_STATE_GANG)
            self.table.gangTile(seatId, gang['pattern'][0], gang['pattern'], MTableState.TABLE_STATE_GANG)
        elif state & MTableState.TABLE_STATE_PENG:
            extend = self.table.qiangExmaoPengProcessor.exmaoExtend
            peng = extend.getChoosedInfo(MTableState.TABLE_STATE_PENG)
            self.table.pengTile(seatId, peng[0], peng, MTableState.TABLE_STATE_PENG)
            
    def autoProcessQiangExmaoHu(self, seatIds):
        for seatId in seatIds:
            if (self.table.getTableConfig(MTDefine.ROBOT_LEVEL, MTDefine.ROBOT_SMART) == MTDefine.ROBOT_FOOLISH) and \
                self.table.player[seatId].isRobot():
                # 傻瓜级别AI，不抢杠和
                self.table.playerCancel(seatId)

        if self.table.qiangExmaoHuProcessor.getState() != 0:
            for seatId in seatIds:
                if self.table.qiangExmaoHuProcessor.canHuNow(seatId):
                    self.table.gameWin(seatId,self.table.qiangExmaoHuProcessor.tile)
                

    def autoProcessQiangGangHu(self, seatIds):
        """自动处理抢杠和"""
        humanSeatIds = []
        for seatId in seatIds:
            if (self.table.getTableConfig(MTDefine.ROBOT_LEVEL, MTDefine.ROBOT_SMART) == MTDefine.ROBOT_FOOLISH) and \
                self.table.player[seatId].isRobot():
                # 傻瓜级别AI，不抢杠和
                self.table.playerCancel(seatId)
                continue
            humanSeatIds.append(seatId)

        if len(humanSeatIds) > 0:
            extend = self.table.qiangGangHuProcessor.getExtendResultBySeatId(humanSeatIds[0])
            choose = extend.getChoosedInfo(MTableState.TABLE_STATE_QIANGGANG)
    #         winInfo['tile'] = tile
    #         winInfo['qiangGang'] = 1
    #         winInfo['gangSeatId'] = self.curSeat
            self.table.grabHuGang(humanSeatIds[0],choose['tile'], humanSeatIds)


    def autoProcessDropCard(self, seatIds):
        """托管出牌操作
        简单点儿：
        1）能和就和
        2）能杠就杠
        3）能碰就碰
        4）能吃就吃
        """
        seatId = seatIds[0]
        if (self.table.getTableConfig(MTDefine.ROBOT_LEVEL, MTDefine.ROBOT_SMART) == MTDefine.ROBOT_FOOLISH) and \
            self.table.player[seatId].isRobot():
            # 傻瓜级别， 不吃不碰不杠不和
            self.table.playerCancel(seatId)
            return
        
        seatState = self.table.dropCardProcessor.getStateBySeatId(seatId)
        nowTile = self.table.dropCardProcessor.tile
        if seatState > 0:
            if (seatState & MTableState.TABLE_STATE_HU):
		if len(seatIds) > 1:
                    for winSeatId in seatIds:
                        self.table.gameWin(winSeatId, nowTile, seatIds)
                else:
		     self.table.gameWin(seatId, nowTile, seatIds)
                return
                
            extend = self.table.dropCardProcessor.getExtendResultBySeatId(seatId)
            choose = extend.getChoosedInfo(seatState)
            ftlog.debug('autoProcessDropCard gang choose:', choose)
            
            if seatState & MTableState.TABLE_STATE_GANG:
                special_tile = self.getPiguTile()
                # AI自动选择杠听
                if seatState & MTableState.TABLE_STATE_GRABTING:
                    self.table.gangTile(seatId
                        , nowTile
                        , choose['pattern']
                        , choose['style']
                        , MTableState.TABLE_STATE_GANG | MTableState.TABLE_STATE_GRABTING
                        , special_tile)
                else:
                    self.table.gangTile(seatId
                        , nowTile
                        , choose['pattern']
                        , choose['style']
                        , MTableState.TABLE_STATE_GANG
                        , special_tile)
                return
                
            if seatState & MTableState.TABLE_STATE_PENG:
                # AI自动选择碰听
                ftlog.debug('seatId:', seatId, ' nowTile:', nowTile, ' extend:', extend)
                if seatState & MTableState.TABLE_STATE_GRABTING:
                    self.table.pengTile(seatId, nowTile, choose['pattern'], MTableState.TABLE_STATE_PENG | MTableState.TABLE_STATE_GRABTING)
                else:
                    self.table.pengTile(seatId, nowTile, choose, MTableState.TABLE_STATE_PENG)
                return
                
            if seatState & MTableState.TABLE_STATE_CHI:
                # 这里的准确逻辑是，如果吃的牌在吃听里，继续转听。如果吃的牌不在听牌里，按普通的吃处理
                if seatState & MTableState.TABLE_STATE_GRABTING:
                    self.table.chiTile(seatId
                            , nowTile
                            , choose['pattern']
                            , MTableState.TABLE_STATE_CHI | MTableState.TABLE_STATE_GRABTING)
                else:
                    self.table.chiTile(seatId, nowTile, choose, MTableState.TABLE_STATE_CHI)
                return
                
            # 未处理的状态，自动取消
            self.table.playerCancel(seatId)   
            
    def autoProcessLouHu(self, seatId):
        if self.table.louHuProcesssor.actionID != self.table.actionID:
            return
        
        player = self.table.player[seatId]
        if (self.table.getTableConfig(MTDefine.ROBOT_LEVEL, MTDefine.ROBOT_SMART) == MTDefine.ROBOT_FOOLISH) and \
            player.isRobot():
            self.table.playerCancel(seatId)
            return
        
        self.table.gameWin(seatId, self.table.louHuProcesssor.tile)
        
    def autoProcessDaFeng(self, seatId):
        if self.table.daFengProcessor.actionID != self.table.actionID:
            return
        
        player = self.table.player[seatId]
        if (self.table.getTableConfig(MTDefine.ROBOT_LEVEL, MTDefine.ROBOT_SMART) == MTDefine.ROBOT_FOOLISH) and \
            player.isRobot():
            self.table.playerCancel(seatId)
            return
        
        self.table.gameWin(seatId, self.table.daFengProcessor.tile)
                
    def autoProcessAddCard(self):
        player = self.table.addCardProcessor.getPlayer()
        nowTile = self.table.addCardProcessor.getTile()

        if (self.table.getTableConfig(MTDefine.ROBOT_LEVEL, MTDefine.ROBOT_SMART) == MTDefine.ROBOT_FOOLISH) and \
            player.isRobot():
            # AI是傻瓜级别，抓什么打什么
            self.table.dropTile(player.curSeatId, nowTile)
            return
        
        if self.table.addCardProcessor.getState() & MTableState.TABLE_STATE_HU:
            self.table.gameWin(player.curSeatId, nowTile)
            return
        
        exInfo = self.table.addCardProcessor.extendInfo
        if self.table.addCardProcessor.getState() & MTableState.TABLE_STATE_TING:
            _pattern, newState = exInfo.getFirstPattern(MTableState.TABLE_STATE_TING)
            tingInfo = exInfo.getChoosedInfo(newState)
            ftlog.debug('MajiangTable.autoProcessAddCard tingInfo:', tingInfo)
            if 'ting' in tingInfo:
                tingInfo = tingInfo['ting'][0]
            ftlog.debug('MajiangTable.autoProcessAddCard tingInfo:', tingInfo)
            # 选择打掉的牌，用剩下的牌听，自动选择可胡牌数最多的解，默认不扣任何牌
            self.table.tingAfterDropCard(player.curSeatId, tingInfo['dropTile'], [], self.table.addCardProcessor.extendInfo)
            return
        
        if self.table.addCardProcessor.getState() & MTableState.TABLE_STATE_GANG:
            _pattern, newState = exInfo.getFirstPattern(MTableState.TABLE_STATE_GANG)
            ftlog.debug('MajiangTable.autoProcessAddCard getFirstGangPattern pattern:', _pattern
                , ' newState:', newState)
            
            exInfo.updateState(newState, _pattern)
            gangInfo = exInfo.getChoosedInfo(newState)

            ftlog.debug( 'MajiangTable.autoProcessAddCard gangInfo:', gangInfo )
            style = gangInfo['style']
            pattern = gangInfo['pattern']
            special_tile = self.getPiguTile()
            self.table.gangTile(player.curSeatId, nowTile, pattern, style, MTableState.TABLE_STATE_GANG, special_tile)
            return

        ftlog.debug( player.copyTiles() )
        ftlog.debug( player.isTing() )
        minTile, minValue = MTileValue.getBestDropTile(player.copyTiles()
            , self.table.tableTileMgr.getTiles()
            , self.table.playMode
            , nowTile
            , player.isTing()
            , self.table.tableTileMgr.getMagicTiles(player.isTing())
            , self.table.tingRule
      	    ,player.isWon())
	# modify by youjun 05.04 
        ftlog.debug('autoProcessAddCard.getBestDropTile minTile:', minTile, ' minValue:', minValue)
        
        # 最后，出价值最小的牌
        self.table.dropTile(player.curSeatId, minTile)

    def getPiguTile(self):
        """获取翻屁股"""
        if self.table.checkTableState(MTableState.TABLE_STATE_FANPIGU):
            pigus = self.table.tableTileMgr.getPigus()
            if pigus and len(pigus) > 0:
                return pigus[0]
        return None
