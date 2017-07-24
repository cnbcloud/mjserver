# -*- coding:utf-8 -*-


from poker.protocol.rpccore import markRpcCall
from poker.entity.configure import gdata
from freetime.util import log as ftlog

@markRpcCall(groupName="roomId", lockName="", syncCall=1)
def getTableByRoomId(roomId):
    """ 
    * UT调用，需要处理完之后返回消息给UT
    """
    from majiang2.entity.create_table_list import CreateTable
    room = gdata.rooms().get(roomId, None)
    if not room:
        ftlog.info('getTableByRoomId, room is null:', roomId)
        return 0
    table_list = [] 
    for table in room.maptable.values():
        table_list.append([table.realPlayerNum, table])
        table_list = sorted(table_list, reverse=True)
    ftlog.debug('===getTableByRoomId===table_list=', table_list)
    return CreateTable.get_create_table_from_table_list(table_list)

