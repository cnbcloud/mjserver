# -*- coding=utf-8 -*-
'''
Created on 2015年9月30日
麻将好友桌的牌桌，负责好友桌号的管理和好友桌赛制的调度。
@author: 赵良
'''
from majiang2.table.majiang_friend_table import MajiangFriendTable
from queshou.table.majiang_table_observer import QueshouTableObserver

class QueshouMajiangFriendTable(MajiangFriendTable):

    def __init__(self, tableId, room):
        super(QueshouMajiangFriendTable, self).__init__(tableId, room)
        observer = QueshouTableObserver(self.gameId, self.roomId, self.tableId)
        self.setTableObserver(observer)
