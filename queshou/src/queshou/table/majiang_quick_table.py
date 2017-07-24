# -*- coding=utf-8 -*-
'''
Created on 2015年9月30日
麻将陌生人桌的牌桌
@author: zhaol
'''
from majiang2.table.majiang_quick_table import MajiangQuickTable
from queshou.table.majiang_table_observer import QueshouTableObserver

class QueshouMajiangQuickTable(MajiangQuickTable):
    """
    1）负责框架桌子资源的管理，对接赛制/自建桌
    2）负责处理用户的上行消息处理
    3）麻将的具体逻辑，在逻辑类中处理
    4）负责联网玩法用户准备情况的管理，条件合适的时候开始游戏
    5）MajiangTable就是核心玩法里联网的action_handler
    """
    def __init__(self, tableId, room):
        super(QueshouMajiangQuickTable, self).__init__(tableId, room)
        observer = QueshouTableObserver(self.gameId, self.roomId, self.tableId)
        self.setTableObserver(observer)