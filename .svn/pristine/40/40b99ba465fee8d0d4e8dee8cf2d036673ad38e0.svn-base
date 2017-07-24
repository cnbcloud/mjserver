# -*- coding=utf-8
'''
Created on 2017年6月6日

@author: youjun
'''
from majiang2.table_state.state import MTableState
from majiang2.table.table_config_define import MTDefine
from freetime.util import log as ftlog
class MTableStateQueshou(MTableState):
    
    def __init__(self):
        super(MTableStateQueshou, self).__init__()
        # 福州玩法
        self.setState(MTableState.TABLE_STATE_DROP)
	# 吃
	self.setState(MTableState.TABLE_STATE_CHI)
        # 碰
        self.setState(MTableState.TABLE_STATE_PENG)
        # 杠
        self.setState(MTableState.TABLE_STATE_GANG)
        # 听
        self.setState(MTableState.TABLE_STATE_TING)
	# 补花
	self.setState(MTableState.TABLE_STATE_BUFLOWER)
        # 开金
        self.setState(MTableState.TABLE_STATE_KAIJIN)
        # 抢杠和
        self.setState(MTableState.TABLE_STATE_QIANGGANG)
        # 和
        self.setState(MTableState.TABLE_STATE_HU)
	# 和牌后游戏结束
	self.setState(MTableState.TABLE_STATE_GAME_OVER)
    def getStandUpSchedule(self, state = MTableState.TABLE_STATE_NONE):
        """获取每一小局的发牌流程
        """
        return MTableState.TABLE_STATE_NEXT
