# -*- coding=utf-8
'''
Created on 2016年9月23日

@author: zhaol
'''
from majiang2.table_state_processor.processor import MProcessor
from freetime.util import log as ftlog
from majiang2.table_state_processor.extend_info import MTableStateExtendInfo
from majiang2.table.table_config_define import MTDefine
from majiang2.table_state.state import MTableState

"""
抢锚胡的操作处理
情况：
一个人补锚，可能有人胡牌
本处理类只处理抢锚胡牌的情况，要处理的状态只有抢锚胡一个，AI策略处理起来比较简单。

抢锚碰/杠只会有一个人
本处理类，只处理抢锚时引起的碰/杠

能碰/杠的只有一个人
"""
class MQiangExmaoHuProcessor(MProcessor):
    def __init__(self, count):
        super(MQiangExmaoHuProcessor, self).__init__()
        self.__processors = [{"state": MTableState.TABLE_STATE_NEXT ,"extendInfo": None, "response": 0} for _ in range(count)]
        # 玩家数量
        self.__count = count
        # 补锚的那张牌
        self.__tile = 0
        # 补锚的用户的座位号
        self.__cur_seat_id = 0
        # 补锚的类型
        self.__style = 0
        # 补锚用户当时的状态
        self.__exmao_state = 0
    
    def reset(self):
        """重置数据"""
        self.__tile = 0
        self.__cur_seat_id = 0
        self.__style = 0
        self.__exmao_state = 0
        self.__time_out = 0
        self.__processors = [{"state": 0, "extendInfo": None, "response": 0} for _ in range(self.__count)]
    
    @property
    def processors(self):
        return self.__processors    
        
    @property
    def style(self):    
        return self.__style
    
    def setStyle(self, style):
        self.__style = style
    
    @property
    def tile(self):
        return self.__tile
    
    def setTile(self, tile):
        self.__tile = tile
    
    @property
    def curSeatId(self):
        """获取当前座位号"""
        return self.__cur_seat_id
    
    def setCurSeatId(self, curSeatId):
        self.__cur_seat_id = curSeatId
    
    @property
    def maoState(self):
        return self.__exmao_state
    
    def setMaoState(self, maoState):
        self.__exmao_state = maoState
    
    def getState(self):
        """获取本轮出牌状态
        """
        state = 0
        for seat in range(self.__count):
            state = state | self.__processors[seat]['state']
            
        return state
    
    def resetSeatId(self, seatId):
        """重置某个座位，用户放弃"""
        self.__processors[seatId] = {"state": 0, "extendInfo": None, "response": 0}
        return True
    
    def getResponseBySeatId(self, seatId):
        """根据seatId获取响应状态"""
        return self.__processors[seatId]['response']

    def getStateBySeatId(self, seatId):
        """根据seatId获取出牌状态
        """
        return self.__processors[seatId]['state']
    
    def getAutoDecideSeatsBySchedule(self, trustTee):
        """根据座位号，获取托管的座位号列表"""
        seats = []
        for index in range(self.__count - 1):
            nextSeat = (self.curSeatId + index + 1) % self.__count
            if self.isUserAutoDecided(nextSeat, trustTee, self.getStateBySeatId(nextSeat), self.getResponseBySeatId(nextSeat) == 0):
                seats.append(nextSeat)
            # if self.players[nextSeat].autoDecide or self.players[nextSeat].isTing() or (self.timeOut < 0):
            #     seats.append(nextSeat)
        if self.maoState != 0:
            seats.append(self.curSeatId)
            
        return seats
    
    def hasAutoDecideAction(self, curSeat, trustTeeSet):
        """是否有托管可以处理的行为"""
        if self.maoState == 0:
            return []

        retrunSeats=[]        
        seats = self.getAutoDecideSeatsBySchedule(trustTeeSet)
        for seat in seats:
            if self.__processors[seat]['state'] == MTableState.TABLE_STATE_QIANG_EXMAO_HU:
                retrunSeats.append(seat)
                
        retrunSeats.append(self.curSeatId)
            
        return retrunSeats
      
    def initProcessor(self, actionID, seatId, maoType, huSeatId, state, extendInfo, extendTile, timeOut = 9):
        """
        初始化处理器
        参数
            seatId - 座位号
            state - 状态集合，当前座位号可以做出的全部选择
        """
        ftlog.debug('MQiangExmaoHuProcessor.initProcessor seatId:', seatId
                    , ' maoType:', maoType
                    , ' state:', state
                    , ' huSeatId:', huSeatId
                    , ' extentdInfo:', extendInfo
                    , ' timeOut:', timeOut)
        self.setActionID(actionID)
        self.setCurSeatId(seatId)
        self.setStyle(maoType)
        self.setMaoState(MTableState.TABLE_STATE_FANGMAO)
        self.setTimeOut(timeOut)
        self.setTile(extendTile)
        
        self.__processors[huSeatId]['state'] = state
        self.__processors[huSeatId]['extendInfo'] = extendInfo
        self.__processors[huSeatId]['response'] = 1 # 用户未做出选择
        
    
    def updateProcessor(self, actionID, actionSeatId, state, tile, pattern = None):
        """
        用户做出了选择，state为0，表示放弃
        用户的选择集合明确
        """
        if actionID != self.actionID:
            # 不是本轮处理的牌
            ftlog.debug('not this round actionId...' )
            return False
        
        
        self.__processors[actionSeatId]['state'] = state
        self.__processors[actionSeatId]['response'] = 0  #用户已做出选择
        ftlog.debug('MQiangExmaoHuProcessor.updateProcessor end:', self.__processors)

        return self.isBiggestPriority(state, actionSeatId)
    
    
    def isBiggestPriority(self, state, actionSeatId):
        """
        是否是最高优先级
        """
        #逆时针获取补锚之后玩家顺序        
        seatIds = []
        for index in range(1, self.__count):
            tempseatid = (self.curSeatId + index) % self.__count
            if self.__processors[tempseatid]['state'] == MTableState.TABLE_STATE_QIANG_EXMAO_HU:
                seatIds.append(tempseatid)
        
        ftlog.debug('MQiangExmaoHuProcessor.isBiggestPriority seatIds:', seatIds,'state',state,'actionSeatId',actionSeatId)
        
        if state == MTableState.TABLE_STATE_QIANG_EXMAO_HU:
            #如果用户cancle过，self.__processors[seat]['state'] 会被设置为0
            huCurIndex = seatIds.index(actionSeatId)
            ftlog.debug('MQiangExmaoHuProcessor.isBiggestPriority TABLE_STATE_QIANG_EXMAO_HU huCurIndex:', huCurIndex)
            for seatindex in range(huCurIndex):
                realSeat = seatIds[seatindex]
                if self.__processors[realSeat]['state'] == MTableState.TABLE_STATE_QIANG_EXMAO_HU:
                    return False
            return True
        elif state == MTableState.TABLE_STATE_FANGMAO:
            if self.getState()==0:
                return True
            else:
                return False
            
    def canHuNow(self,actionSeatId):   
        seatIds = []
        for index in range(1, self.__count):
            tempseatid = (self.curSeatId + index) % self.__count
            if self.__processors[tempseatid]['state'] == MTableState.TABLE_STATE_QIANG_EXMAO_HU \
                and self.__processors[tempseatid]['response']==0:
                seatIds.append(tempseatid)
        
        if actionSeatId in seatIds:
            huCurIndex = seatIds.index(actionSeatId)
            for seatindex in range(huCurIndex):
                realSeat = seatIds[seatindex]
                if self.__processors[realSeat]['state'] == MTableState.TABLE_STATE_QIANG_EXMAO_HU:
                    return False
            return True
        
        return False   
        
   
    
if __name__ == "__main__":
    dp = MQiangExmaoHuProcessor(4)
    exInfo = MTableStateExtendInfo()
    #exInfo.setExtend( {'peng': [[18, 18, 18]], 'pengTing': [{'tile': 18, 'ting': [{'winNo       des': [{'winTile': 17, 'pattern': [[17, 18, 19], [11, 11]], 'winTileCount': 3}], 'dropTile': 28}], 'pattern': [18, 18, 18]}], 'gang': [{'tile': 18, 'pattern': [18, 18, 18, 18], 'style': 1}], 'gangTing': [{'ti       le': 18, 'ting': [{'winNodes': [{'winTile': 26, 'pattern': [[26, 27, 28], [11, 11]], 'winTileCount': 2}, {'winTile': 29, 'pattern': [[27, 28, 29], [11, 11]], 'winTileCount': 2}], 'dropTile': 19}], 'style': 1,        'pattern': [18, 18, 18, 18]}]})
    exInfo.setExtend( {'peng': [[18, 18, 18]], 'pengTing': [{'tile': 18, 'ting': [{'winNodes': [{'winTile': 17, 'pattern': [[17, 18, 19], [11, 11]], 'winTileCount': 3}], 'dropTile': 28}], 'pattern': [18, 18, 18]}]})
    dp.initProcessor(10, 0, 28, exInfo, 9)