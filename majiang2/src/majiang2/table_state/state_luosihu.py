# -*- coding=utf-8
'''
Created on 2016年9月23日

@author: zhaol
'''
from majiang2.table_state.state import MTableState
from majiang2.table.table_config_define import MTDefine
from freetime.util import log as ftlog
class MTableStateLuosihu(MTableState):
    
    def __init__(self):
        super(MTableStateLuosihu, self).__init__()
        # 卡五星玩法
        self.setState(MTableState.TABLE_STATE_DROP)
        # 碰
        self.setState(MTableState.TABLE_STATE_PENG)
        # 杠
        self.setState(MTableState.TABLE_STATE_GANG)
        # 听
        self.setState(MTableState.TABLE_STATE_TING)
        # 抢杠和
        self.setState(MTableState.TABLE_STATE_QIANGGANG)
        # 和
        self.setState(MTableState.TABLE_STATE_HU)
	# 和牌后游戏结束
	self.setState(MTableState.TABLE_STATE_GAME_OVER)
    def enableSpecialStateByTableConfig(self, tableConfig):
        # 缺
        dingque = tableConfig[MTDefine.DING_QUE]
        if dingque:
            self.setState(MTableState.TABLE_STATE_ABSENCE)
        else:
            self.clearState(MTableState.TABLE_STATE_ABSENCE)
    def getStandUpSchedule(self, state = MTableState.TABLE_STATE_NONE):
        """获取每一小局的发牌流程
        先加漂，再发牌
        """
        #modify by youjun 04.25
        # 定缺
        if self.playMode == "luosihu-xuezhan":
            self.setState(MTableState.TABLE_STATE_ABSENCE)
            self.setState(MTableState.TABLE_STATE_XUELIU)
	    self.clearState(MTableState.TABLE_STATE_GAME_OVER)
	elif self.playMode == "luosihu-luosihu":
	    # 和牌后血流成河
            self.setState(MTableState.TABLE_STATE_XUELIU) 
	    self.clearState(MTableState.TABLE_STATE_GAME_OVER)
        elif self.playMode == "luosihu-ctxuezhan":
            self.setState(MTableState.TABLE_STATE_ABSENCE)
	    self.setState(MTableState.TABLE_STATE_XUEZHAN)
            self.clearState(MTableState.TABLE_STATE_GAME_OVER) 
        #modify end  
        return MTableState.TABLE_STATE_NEXT
