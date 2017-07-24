#coding:utf-8
"""
    客户端获取自建桌信息
"""

from freetime.util import log as ftlog
from poker.entity.configure import gdata
from majiang2.entity.create_table import CreateTableData
from majiang2.table.friend_table_define import MFTDefine

class CreateTable(object):
    """ 自建桌
    """
    @classmethod
    def get_create_table_by_roomid(cls, roomid):
        """ table的RPC方法调用，UT进程请求执行，获取此房间符合条件的桌子并返回给UT进程
        """
        results = {}
        room = gdata.rooms()[roomid]
        room_conf = room.roomDefine.configure
        ftlog.debug('room_conf =', room_conf, caller=cls)
        if not room_conf.get(MFTDefine.IS_CREATE, 0):
            return  results
        
        from majiang2.servers.table.rpc import table_rpc
        table = table_rpc.getTableByRoomId(roomid)
        return table

    @classmethod
    def get_create_table_from_table_list(cls, table_list):
        """ 根据room得到合适的table返回
        """
        for i in xrange(len(table_list)):
            count, table = table_list[i]
            if count == 0: #桌子上没人
                ftlog.debug('===========get_create_table_by_room==',table.tableId,caller=cls)
                if table.tableId not in CreateTableData.getAllCreatedTableIdList():
                    #桌子没被创建
                    return table.tableId
        ftlog.debug('===========rpc success==',caller=cls)
        return 0