# -*- coding=utf-8
'''
Created on 2016年9月23日

@author: zhaol
'''
from majiang2.table_state_processor.processor import MProcessor
from freetime.util import log as ftlog
from majiang2.table_state_processor.extend_info import MTableStateExtendInfo
from majiang2.table.table_config_define import MTDefine

"""
抢锚碰的操作处理
情况：
一个人补锚，可能有人碰牌
本处理类只处理抢杠胡牌的情况，要处理的状态只有抢杠和一个，AI策略处理起来比较简单。

抢锚碰/杠只会有一个人
本处理类，只处理抢锚时引起的碰/杠
抢锚胡交给抢杠胡processor处理

能碰/杠的只有一个人
"""
class MQiangExmaoPengProcessor(MProcessor):
    def __init__(self, count):
        super(MQiangExmaoPengProcessor, self).__init__()
        # 补锚的那张牌
        self.__tile = 0
        # 补锚的用户的座位号
        self.__cur_seat_id = 0
        # 补锚的类型
        self.__style = 0
        # 抢锚的人的座位数组,在全部放弃后清空
        self.__exmao_seat_id = 0
        # 补锚用户当时的状态
        self.__exmao_state = 0
        # 补锚人的extend
        self.__exmao_extend = None
    
    def reset(self):
        """重置数据"""
        self.__tile = 0
        self.__cur_seat_id = 0
        self.__style = 0
        self.__exmao_seat_id = 0
        self.__exmao_state = 0
        self.__exmao_extend = None
        self.__time_out = 0
    
    @property    
    def exmaoExtend(self):
        return self.__exmao_extend
    
    def setExmaoExtend(self, exmaoExtend):
        self.__exmao_extend = exmaoExtend
    
    @property
    def exmaoSeatId(self):
        return self.__exmao_seat_id
    
    def setExmaoSeatId(self, exMaoSeatId):
        self.__exmao_seat_id = exMaoSeatId
        
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
        return self.maoState
    
    def hasAutoDecideAction(self, curSeat, trustTeeSet):
        """是否有托管可以处理的行为"""

        if self.players[self.exmaoSeatId].isRobot():
            return self.exmaoSeatId

        return MTDefine.INVALID_SEAT
      
    def initProcessor(self, actionID, seatId, maoType, maoSeatId, state, extendInfo, extendTile, timeOut = 9):
        """
        初始化处理器
        参数
            seatId - 座位号
            state - 状态集合，当前座位号可以做出的全部选择
        """
        ftlog.debug('MQiangExmaoPengProcessor.initProcessor seatId:', seatId
                    , ' maoType:', maoType
                    , ' state:', state
                    , ' maoSeatId:', maoSeatId
                    , ' extentdInfo:', extendInfo
                    , ' timeOut:', timeOut)
        self.setActionID(actionID)
        self.setCurSeatId(seatId)
        self.setStyle(maoType)
        self.setExmaoSeatId(maoSeatId)
        self.setMaoState(state)
        self.setExmaoExtend(extendInfo)
        self.setTimeOut(timeOut)
        self.setTile(extendTile)
        
    def resetSeatId(self, seatId):
        if self.exmaoSeatId == seatId:
            self.setMaoState(0)
    
    def updateProcessor(self, actionID, seatId, state, tile, pattern = None):
        """
        用户做出了选择，state为0，表示放弃
        用户的选择集合明确
        """
        if actionID != self.actionID:
            # 不是本轮处理的牌
            ftlog.debug('not this round actionId...' )
            return False
        
        if seatId != self.exmaoSeatId:
            ftlog.debug('Not this round qiangPeng/Gang user... right seatId:', self.exmaoSeatId
                        , ' wrong seatId:', seatId)
            return False
        
        if not (state & self.maoState):
            ftlog.debug('Right user, but wrong action. state:', self.maoState
                        , ' now action:', state)
            return False
        
        self.setMaoState(0)
        return True
    
if __name__ == "__main__":
    dp = MQiangExmaoPengProcessor(4)
    exInfo = MTableStateExtendInfo()
    #exInfo.setExtend( {'peng': [[18, 18, 18]], 'pengTing': [{'tile': 18, 'ting': [{'winNo       des': [{'winTile': 17, 'pattern': [[17, 18, 19], [11, 11]], 'winTileCount': 3}], 'dropTile': 28}], 'pattern': [18, 18, 18]}], 'gang': [{'tile': 18, 'pattern': [18, 18, 18, 18], 'style': 1}], 'gangTing': [{'ti       le': 18, 'ting': [{'winNodes': [{'winTile': 26, 'pattern': [[26, 27, 28], [11, 11]], 'winTileCount': 2}, {'winTile': 29, 'pattern': [[27, 28, 29], [11, 11]], 'winTileCount': 2}], 'dropTile': 19}], 'style': 1,        'pattern': [18, 18, 18, 18]}]})
    exInfo.setExtend( {'peng': [[18, 18, 18]], 'pengTing': [{'tile': 18, 'ting': [{'winNodes': [{'winTile': 17, 'pattern': [[17, 18, 19], [11, 11]], 'winTileCount': 3}], 'dropTile': 28}], 'pattern': [18, 18, 18]}]})
    dp.initProcessor(10, 0, 28, exInfo, 9)