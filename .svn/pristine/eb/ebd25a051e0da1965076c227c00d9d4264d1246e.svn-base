# -*- coding=utf-8
'''
Created on 2016年9月23日

@author: zhaol
'''
from majiang2.table_state.state import MTableState
from majiang2.table_state_processor.processor import MProcessor
from freetime.util import log as ftlog
from majiang2.table_state_processor.extend_info import MTableStateExtendInfo
from majiang2.table.table_config_define import MTDefine

"""
抢杠和的操作处理
情况：
一个人回头杠，可能有人和牌
本处理类只处理抢杠胡牌的情况，要处理的状态只有抢杠和一个，AI策略处理起来比较简单。
"""
class MQiangGangHuProcessor(MProcessor):
    def __init__(self, count):
        super(MQiangGangHuProcessor, self).__init__()
        self.__processors = [{"state": MTableState.TABLE_STATE_NEXT ,"extendInfo": None, "response": 0} for _ in range(count)]
        # 玩家数量
        self.__count = count
        # 开杠的那张牌
        self.__tile = 0
        # 杠牌的用户的座位号
        self.__cur_seat_id = 0
        # 杠牌用户当时的状态
        self.__gang_state = 0
        # 杠牌时pattern
        self.__gang_pattern = None
        # 杠牌时特殊的牌
        self.__special_tile = None
        # 杠牌的类型
        self.__style = 0
        # 抢杠胡的人的座位数组,在全部放弃后清空
        self.__qiang_gang_seats = []

    @property
    def count(self):
        return self.__count

    def setCount(self, count):
        self.__count = count

    @property
    def processors(self):
        return self.__processors

    @property
    def qiangGangSeats(self):
        return self.__qiang_gang_seats   
        
    @property
    def style(self):    
        return self.__style
    
    @property
    def tile(self):
        return self.__tile
    
    @property
    def curSeatId(self):
        """获取当前座位号"""
        return self.__cur_seat_id
    
    @property
    def gangState(self):
        return self.__gang_state
    
    @property
    def gangPattern(self):
        return self.__gang_pattern
    
    @property
    def specialTile(self):
        return self.__special_tile
    
    def getSeatsBySchedule(self):
        """根据座位号，获取吃牌的座位号列表"""
        seats = []
        for index in range(1, self.__count):
            seats.append((self.curSeatId + index) % self.__count)
        ftlog.debug("getSeatsBySchedule self.curSeatId  = "
                        , self.curSeatId
                        , "self.count="
                        , self.__count
                        , "seats = "
                        , seats)
        return seats
    
    def getAutoDecideSeatsBySchedule(self, trustTee):
        """根据座位号，获取托管的座位号列表"""
        seats = []
        for index in range(self.__count - 1):
            nextSeat = (self.curSeatId + index + 1) % self.__count
            if self.isUserAutoDecided(nextSeat, trustTee, self.getStateBySeatId(nextSeat), self.getResponseBySeatId(nextSeat) == 0):
                seats.append(nextSeat)
            # if self.players[nextSeat].autoDecide or self.players[nextSeat].isTing() or (self.timeOut < 0):
            #     seats.append(nextSeat)
        return seats

    def getResponseBySeatId(self, seatId):
        """根据seatId获取响应状态"""
        return self.__processors[seatId]['response']

    def getStateBySeatId(self, seatId):
        """根据seatId获取出牌状态
        """
        return self.__processors[seatId]['state']
    
    def getState(self):
        """获取本轮出牌状态
        """
        state = 0
        for seat in range(self.__count):
            state = state | self.__processors[seat]['state']
            
        ftlog.debug( 'MQiangGangHuProcessor.getState return:', state )
        return state
            
    def reset(self):
        """重置数据"""
        self.__processors = [{"state": 0, "extendInfo": None, "response": 0} for _ in range(self.__count)]
        self.__tile = 0
        self.__cur_seat_id = 0
        self.__qiang_gang_seats = []
        ftlog.debug('MQiangGangHuProcessor.reset now processors:', self.__processors)
        
    def resetSeatId(self, seatId):
        """重置某个座位，用户放弃"""
        self.__processors[seatId] = {"state": 0, "extendInfo": None, "response": 0}
        ftlog.debug('MQiangGangHuProcessor.resetSeatId now processors:', self.__processors)
        return True
        
    def initTile(self, tile, curSeat, gangState, gangPattern, style, specialTile = None):
        """初始化本轮手牌，用做校验
        """
        ftlog.debug( 'MQiangGangHuProcessor.initTile will gang tile:', tile 
                     ,'curSeat:', curSeat, 'gangState:', gangState,
                     'gangPattern:', gangPattern, 'specialTile', specialTile)
        self.__tile = tile
        self.__cur_seat_id = curSeat
        self.__gang_state = gangState
        self.__gang_pattern = gangPattern
        self.__special_tile = specialTile
        self.__style = style
        
    def getExtendResultBySeatId(self,seatId):
        extendInfo = self.__processors[seatId]['extendInfo']
        return extendInfo
                    
    def initProcessor(self, actionID, seatId, state, extendInfo = None, timeOut = 9):
        """
        初始化处理器
        参数
            seatId - 座位号
            state - 状态集合，当前座位号可以做出的全部选择
        """
        ftlog.debug('MQiangGangHuProcessor.initProcessor seatId:', seatId, ' state:', state, ' extentdInfo:', extendInfo)
        self.setActionID(actionID)
        self.__processors[seatId]['state'] = state
        self.__processors[seatId]['extendInfo'] = extendInfo
        # 用户未做出选择
        self.__processors[seatId]['response'] = 1
        if seatId not in self.__qiang_gang_seats:
            self.__qiang_gang_seats.append(seatId)
        self.setTimeOut(timeOut)
        ftlog.debug('MQiangGangHuProcessor.initProcessor end:', self.__processors)

    def updateDuoHu(self, actionId, seatIds, state):
        """更新多胡"""
        ftlog.debug('MQiangGangHuProcessor.updateDuoHu actionId:', actionId
                    , ' seatIds:', seatIds
                    , ' state:', state)

        if len(seatIds) <= 1:
            ftlog.debug('MQiangGangHuProcessor.updateDuoHu, only one player win, should not be here...')
            return False

        if actionId != self.actionID:
            ftlog.debug('MQiangGangHuProcessor.updateDuoHu wrong actionId, do not process actionId:', actionId
                        , ' actionIdInProcessor:', self.actionID)
            return False

        if not self.allResponsed():
            ftlog.debug('MQiangGangHuProcessor.updateDuoHu not all user responsed, do not process...')
            return False

        for seat in range(self.count):
            if seat in seatIds:
                continue

            if self.getStateBySeatId(seat) >= MTableState.TABLE_STATE_QIANGGANG:
                ftlog.debug('MQiangGangHuProcessor.updateDuoHu seatIds:', seatIds
                            , ' but seat:', seat
                            , ' also can win, not right...')
                return False

        return True

    def updateProcessor(self, actionID, seatId, state, tile, pattern = None):
        """
        用户做出了选择，state为0，表示放弃
        用户的选择集合明确
        """
        if actionID != self.actionID:
            # 不是本轮处理的牌
            ftlog.debug( 'timeout dropcard processor update' )
            return False
        
        ftlog.debug('MQiangGangHuProcessor.updateProcessor actionID:', actionID
            , ' seatId:', seatId
            , ' state:', state
            , ' tile:', tile)
        
       # if self.__processors[seatId]['response'] == 0:
            # 已经做过选择,再发送过来就不处理了
           # ftlog.debug( 'MQiangGangHuProcessor.updateProcessor response = 0, already responsed' )
           # return False
        self.__processors[seatId]['state'] = state
        # 用户已做出选择
        self.__processors[seatId]['response'] = 0
        ftlog.debug('MQiangGangHuProcessor.updateProcessor end:', self.__processors)

        return self.isBiggestPriority(state, seatId)
    
    # def isBiggestPriority(self, state, seatId):
    #     """
    #     是否是最高优先级
    #     """
    #     seats = self.getSeatsBySchedule()
    #     curIndex = seats.index(seatId)
    #     if curIndex == 0:
    #         return True
    #
    #     for index in range(curIndex):
    #         if self.__processors[seats[index]] == MTableState.TABLE_STATE_QIANGGANG:
    #             return False
    #
    #     # 最高优先级
    #     return True

    def isBiggestPriority(self, state, seatId):
        """
        是否是最高优先级
        """
        seats = self.getSeatsBySchedule()
        ftlog.debug('MQiangGangHuProcessor.isBiggestPriority state:', state
                    , ' seatId:', seatId
                    , ' seats:', seats)

        curIndex = seats.index(seatId)
        for index in range(len(seats)):
            seat = seats[index]
            if seat == seatId:
                continue

            comAction = self.__processors[seat]['state']
            if index < curIndex:
                # 如果index的优先级大于curIndex的，则非最大优先级
                if self.isBigger(comAction, state):
                    ftlog.debug('MQiangGangHuProcessor.isBiggestPriority biggest1 curIndex :', curIndex
                                , ' state:', state
                                , ' index:', index
                                , ' state:', state)
                    return False
            else:
                # 如果curIndex的优先级小于index的，
                if not self.isBigger(state, comAction):
                    ftlog.debug('MQiangGangHuProcessor.isBiggestPriority biggest2 curIndex :', curIndex
                                , ' state:', state
                                , ' index:', index
                                , ' state:', state)
                    return False

            if comAction & MTableState.TABLE_STATE_QIANGGANG and state & MTableState.TABLE_STATE_QIANGGANG and self.tableTileMgr.canDuoHu():
                return False

        ftlog.debug('MQiangGangHuProcessor.isBiggestPriority biggest at last...')
        return True

    def isBigger(self, p1, p2):
        """两个人的优先级比较，判断seat1的优先级是否比seat2大
        参数：
        seat1 座位1
        p1 座位1的行为

        seat2 座位2
        p2 座位2的行为

        seat2是seat1顺时针循环得到的玩家
        """
        ftlog.debug('MQiangGangHuProcessor.isBigger p1:', p1
                    , ' p2:', p2
                    , ' canDuoHu:', self.tableTileMgr.canDuoHu())
        if (p1 & MTableState.TABLE_STATE_GRABTING) and (p2 & MTableState.TABLE_STATE_GRABTING):
            return True

        # 两家同时胡牌 上家也和那么优先级大于下家
        if (p1 & MTableState.TABLE_STATE_QIANGGANG) and (p2 & MTableState.TABLE_STATE_QIANGGANG):
            if self.tableTileMgr.canDuoHu():
                return False
            else:
                return True

        if p1 == p2:
            return True

        return p1 > p2

    def hasAutoDecideAction(self, curSeat, trustTeeSet):
        """
        是否有自动托管的行为
        逆时针找到第一个抢杠和的人
        """
        seats = self.getAutoDecideSeatsBySchedule(trustTeeSet)

        if not self.tableTileMgr.canDuoHu():
            for seat in seats:
                if self.__processors[seat]['state'] == MTableState.TABLE_STATE_QIANGGANG:
                    return [seat]

            return []
        else:
            return [seat for seat in seats if self.__processors[seat]['state'] == MTableState.TABLE_STATE_QIANGGANG]
    
    def allResponsed(self):
        """本轮出牌，所有人都已经响应
        """
        response = 0
        for seat in range(self.__count):
            response += self.__processors[seat]['response']
        return 0 == response
    
    def clearQiangGangSeats(self):
        """抢杠胡的人的座位数组"""
        self.__qiang_gang_seats = []


def testDuoWinsProcessor():
    """
    测试一炮多响时，多个和牌的状态更新
    状态：
        0号位出牌，1号位2号位两个人可和牌，能一炮多响

    操作：
        2号位先和牌
        1号位再和牌

    预期：
        2号位胡牌结果先不确认
        1号位胡牌的和牌结果确认
        1/2号位同时胡牌
    """
    from majiang2.player.player import MPlayer
    from majiang2.table_tile.table_tile_factory import MTableTileFactory
    from majiang2.ai.play_mode import MPlayMode
    from majiang2.table.run_mode import MRunMode

    dp = MQiangGangHuProcessor(4)
    player3 = MPlayer('3', 1, 10003, 0)
    player3.setSeatId(3)
    player2 = MPlayer('2', 1, 10002, 0)
    player2.setSeatId(2)
    player1 = MPlayer('1', 1, 10001, 0)
    player1.setSeatId(1)
    player0 = MPlayer('0', 1, 10000, 0)
    player0.setSeatId(0)

    dp.players.append(player0)
    dp.players.append(player1)
    dp.players.append(player2)
    dp.players.append(player3)

    tableTileMgr = MTableTileFactory.getTableTileMgr(4, MPlayMode.LUOSIHU, MRunMode.CONSOLE)
    dp.setTableTileMgr(tableTileMgr)

    exInfoWin1 = MTableStateExtendInfo()
    winInfo1 = {'tile': 9, 'qiangGang': 1, 'gangSeatId': 0}
    exInfoWin1.appendInfo(MTableState.TABLE_STATE_QIANGGANG, winInfo1)
    dp.initProcessor(19, 1, MTableState.TABLE_STATE_QIANGGANG, exInfoWin1, 9)

    exInfoWin2 = MTableStateExtendInfo()
    winInfo2 = {'tile': 9, 'qiangGang': 1, 'gangSeatId': 0}
    exInfoWin2.appendInfo(MTableState.TABLE_STATE_QIANGGANG, winInfo2)
    dp.initProcessor(19, 2, MTableState.TABLE_STATE_QIANGGANG, exInfoWin2, 9)

    result2 = dp.updateProcessor(19, 2, MTableState.TABLE_STATE_QIANGGANG, 9, None)
    print 'result2:', result2
    print dp.processors

    autoSeatId = dp.hasAutoDecideAction(0, -1)
    print 'autoSeatId2:', autoSeatId

    result1 = dp.updateProcessor(19, 1, MTableState.TABLE_STATE_QIANGGANG, 9, None)
    print 'result1:', result1

    autoSeatId = dp.hasAutoDecideAction(0, -1)
    print 'autoSeatId1:', autoSeatId

    wins = [1, 2]
    result3 = dp.updateDuoHu(19, wins, MTableState.TABLE_STATE_QIANGGANG)
    print 'result3:', result3

    print dp.processors

if __name__ == "__main__":
    # dp = MQiangGangHuProcessor(4)
    # exInfo = MTableStateExtendInfo()
    # #exInfo.setExtend( {'peng': [[18, 18, 18]], 'pengTing': [{'tile': 18, 'ting': [{'winNo       des': [{'winTile': 17, 'pattern': [[17, 18, 19], [11, 11]], 'winTileCount': 3}], 'dropTile': 28}], 'pattern': [18, 18, 18]}], 'gang': [{'tile': 18, 'pattern': [18, 18, 18, 18], 'style': 1}], 'gangTing': [{'ti       le': 18, 'ting': [{'winNodes': [{'winTile': 26, 'pattern': [[26, 27, 28], [11, 11]], 'winTileCount': 2}, {'winTile': 29, 'pattern': [[27, 28, 29], [11, 11]], 'winTileCount': 2}], 'dropTile': 19}], 'style': 1,        'pattern': [18, 18, 18, 18]}]})
    # exInfo.setExtend( {'peng': [[18, 18, 18]], 'pengTing': [{'tile': 18, 'ting': [{'winNodes': [{'winTile': 17, 'pattern': [[17, 18, 19], [11, 11]], 'winTileCount': 3}], 'dropTile': 28}], 'pattern': [18, 18, 18]}]})
    # dp.initProcessor(10, 0, 28, exInfo, 9)

    testDuoWinsProcessor()
