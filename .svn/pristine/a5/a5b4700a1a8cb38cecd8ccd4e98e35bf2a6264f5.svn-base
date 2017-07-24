#coding:utf-8
import json
from poker.entity.dao import daobase
from majiang2.entity import util
from freetime.util import log as ftlog

class CreateTableData(object):
    """创建牌桌相关数据管理类 模块中redis script初始化在GT进程
    """
    _load_lua_script = False
    
    ADD_CREATE_TABLE_NO_SCRIPT_NAME = 'HAERBIN_ADD_CREATE_TABLE_NO_SCRIPT'
    _add_create_table_no_script = """
    local createTableKey = tostring(KEYS[1])
    local createTableNo = tostring(KEYS[2])
    local serverId = tostring(KEYS[3])
    local tableNoMapKey = tostring(KEYS[4])
    local tableId = tonumber(KEYS[5])
    local tableNoMapValue = tostring(KEYS[6])
    local allNos = redis.call("HVALS", createTableKey)
    if #allNos > 0 then
        for k,v in pairs(allNos) do
            local noArr = cjson.decode(v)
            for no_k,no_v in pairs(noArr) do
                if no_v == createTableNo then
                    return false
                end
            end
        end
    end
    local serverIdAllNoStr = redis.call('HGET',createTableKey,serverId)
    local noArr = {}
    if serverIdAllNoStr then
        noArr = cjson.decode(serverIdAllNoStr)
    end
    noArr[#noArr+1] = createTableNo
    redis.call('HSET', createTableKey, serverId, cjson.encode(noArr))
    redis.call('HSET', tableNoMapKey, createTableNo, tableNoMapValue)
    return true
    """
    REMOVE_CREATE_TABLE_SCRIPT_NAME = 'HAERBIN_REMOVE_CREATE_TABLE_SCRIPT'
    _remove_create_table_script = """
    local createTableKey = tostring(KEYS[1])
    local createTableNo = tostring(KEYS[2])
    local serverId = tostring(KEYS[3])
    local tableNoMapKey = tostring(KEYS[4])
    local serverIdNos = redis.call("HGET", createTableKey, serverId)
    
    if serverIdNos then
        local serverIdNoArr = cjson.decode(serverIdNos)
        if #serverIdNoArr > 0 then
            for no_k,no_v in pairs(serverIdNoArr) do
                if no_v == createTableNo then
                    table.remove(serverIdNoArr, no_k)
                    redis.call('HSET', createTableKey, serverId, cjson.encode(serverIdNoArr))
                    redis.call('HDEL', tableNoMapKey, createTableNo)
                    break
                end
            end
        end
    end
    """
    CLEAR_CREATE_TABLE_SCRIPT_NAME = 'HAERBIN_CLEAR_CREATE_TABLE_SCRIPT'
    _clear_create_table_script = """
    local createTableKey = tostring(KEYS[1])
    local serverId = tostring(KEYS[2])
    local tableNoMapKey = tostring(KEYS[3])
    local serverIdNos = redis.call("HGET", createTableKey, serverId)
    
    if serverIdNos then
        local serverIdNoArr = cjson.decode(serverIdNos)
        if #serverIdNoArr > 0 then
            for no_k,no_v in pairs(serverIdNoArr) do
                redis.call('HDEL', tableNoMapKey, no_v)
            end
        end
    end
    redis.call('HDEL', createTableKey, serverId)
    """
    @classmethod
    def initialize(cls, serverId):
        """初始化，加载lua脚本,清除serverId对应的数据
        """
        ftlog.debug('CreateTableData.initialize serverId:', serverId
            , ' load_lua_script:', cls._load_lua_script)
        
        if not cls._load_lua_script:
            cls._load_lua_script = True
            daobase.loadLuaScripts(cls.ADD_CREATE_TABLE_NO_SCRIPT_NAME, cls._add_create_table_no_script)
            daobase.loadLuaScripts(cls.REMOVE_CREATE_TABLE_SCRIPT_NAME, cls._remove_create_table_script)
            daobase.loadLuaScripts(cls.CLEAR_CREATE_TABLE_SCRIPT_NAME, cls._clear_create_table_script)
        cls._clearCreateTableData(serverId)
        
    @classmethod
    def _clearCreateTableData(cls, serverId):
        """清除重启进程对应的创建牌桌数据 只在GT服调用
        """
        ftlog.debug('CreateTableData.clearCreateTableData serverId:', serverId)
        daobase.executeMixLua(cls.CLEAR_CREATE_TABLE_SCRIPT_NAME
                , 3
                , cls._getCreateTableNoKey()
                , serverId
                , cls._getTableNoMapTableIdKey()
        )
    
    @classmethod
    def _getCreateTableNoKey(cls):
        """返回存储所有serverId:[no1,no2...]映射的redis key
        """
        return "mj:create_table"
    
    @classmethod
    def _getTableNoMapTableIdKey(cls):
        """返回存储所有tableNo:tableId映射的redis key
        """
        return "mj:create_table_no:hash"
    
    
    @classmethod
    def addCreateTableNo(cls, tableId, roomId, serverId, tableNoKey):
        """添加自建桌验证码数据 只在GT服调用
        """
        ftlog.debug('CreateTableData.addCreateTableNo tableId:', tableId
            , ' roomId:', roomId
            , ' serverId:', serverId
            , ' tableNoKey:', tableNoKey)
        
        tableNoMapValue = json.dumps([tableId,roomId])
        result = daobase.executeMixLua(cls.ADD_CREATE_TABLE_NO_SCRIPT_NAME
                , 6
                , cls._getCreateTableNoKey()
                , tableNoKey
                , serverId
                , cls._getTableNoMapTableIdKey()
                , tableId
                , tableNoMapValue
        )
        
        ftlog.info("===addCreateTableNo===",serverId, tableNoKey, result)
        return result
    
    @classmethod
    def removeCreateTableNo(cls, serverId, tableNoKey):
        """删除redis中自建桌验证码数据 只在GT服调用
        """
        daobase.executeMixLua(cls.REMOVE_CREATE_TABLE_SCRIPT_NAME, 4, 
                                       cls._getCreateTableNoKey(), 
                                       tableNoKey, 
                                       serverId,
                                       cls._getTableNoMapTableIdKey(),
                                       )
        ftlog.info('<<< serverId=',serverId,'tableNoKey',tableNoKey,caller=cls)
        
    @classmethod
    def getAllCreateTableNoList(cls):
        """获取所有的自建桌验证码列表
        """
        datas = daobase.executeMixCmd('HVALS', cls._getCreateTableNoKey())
        retArr = []
        if not isinstance(datas, list) or len(datas)<=0:
            return retArr
        try:
            for tableNoListStr in datas:
                tableNoList = json.loads(tableNoListStr)
                retArr.extend(tableNoList)
        except:
            ftlog.error('<<< datas=', datas, caller=cls)
            return retArr
        ftlog.debug('<<< retArr', caller=cls)
        return retArr
    
    @classmethod
    def getTableIdByCreateTableNo(cls, createTableNo):
        """通过自建桌验证码查找返回tableId
        """
        tableRoomIdStr = daobase.executeMixCmd('HGET', cls._getTableNoMapTableIdKey(), createTableNo)
        if tableRoomIdStr:
            ftlog.debug('getTableIdByCreateTableNo ftId:', createTableNo, ' tableInfo:', tableRoomIdStr)
            
            try:
                tableIdRoomIdList = json.loads(tableRoomIdStr)
            except:
                ftlog.error('<<< tableRoomIdStr=', tableRoomIdStr, caller=cls)
                return 0,0
            if len(tableIdRoomIdList) == 2:
                return tableIdRoomIdList[0],tableIdRoomIdList[1]
            
        return 0,0
    
    @classmethod
    @util.safemethod
    def getAllCreatedTableIdList(cls):
        """返回所有已创建的tableId列表
        """
        datas = daobase.executeMixCmd('HVALS', cls._getTableNoMapTableIdKey())
        retArr = []
        if not isinstance(datas, list) or len(datas)<=0:
            return retArr
        try:
            for tableNoMapListStr in datas:
                tableIdRoomIdList = json.loads(tableNoMapListStr)
                if len(tableIdRoomIdList)==2:
                    retArr.append(tableIdRoomIdList[0])
                else:
                    return retArr
        except:
            ftlog.error('<<< datas=', datas, caller=cls)
            return retArr
        ftlog.debug('<<< CreatedTableIdLis=',retArr, caller=cls)
        return retArr
