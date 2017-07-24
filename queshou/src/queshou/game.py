# -*- coding=utf-8 -*-
'''
Created on 2015年9月25日

@author: liaoxx
'''
import time
from poker.entity.configure import gdata
from poker.entity.game.game import TYGame
from majiang2.robot.robot import MajiangRobotManager
from poker.entity.events.tyeventbus import globalEventBus
from poker.entity.events.tyevent import EventHeartBeat
from majiang2.entity.create_table import CreateTableData
from majiang2.entity.create_table_record import MJCreateTableRecord
from freetime.util import log as ftlog
from hall.entity.todotask import TodoTaskEnterGameNew, TodoTaskHelper
from freetime.entity.msg import MsgPack
from poker.protocol import router
from queshou.table.majiang_friend_table import QueshouMajiangFriendTable
from queshou.table.majiang_quick_table import QueshouMajiangQuickTable
from queshou.entity.configure.conf import GAMEID
from poker.entity.dao import gamedata

class TGQueshou(TYGame):

    def __init__(self, *args):
        super(TGQueshou, self).__init__()
        self._lastSendIntervalLedTime = int(time.time()) #上一次下发'每隔多久LED'LED的时间
        
    def initGameBefore(self):
        from queshou.entity import task_inspectors
        task_inspectors._registerClasses()

    def initGame(self):
        from majiang2.entity import majiang_account
        self._account = majiang_account
        serverType = gdata.serverType()

        if serverType == gdata.SRV_TYPE_ROBOT :
            self._robotmgr = MajiangRobotManager()
            globalEventBus.subscribe(EventHeartBeat, self._robotmgr.onHeartBeat)
            
        elif (serverType == gdata.SRV_TYPE_TABLE) or (serverType == gdata.SRV_TYPE_ROOM):
            CreateTableData.initialize(gdata.serverId())                # 初始化创建牌桌数据模块
            MJCreateTableRecord.initialize()                            # 初始化自建桌战绩模块
        elif serverType == gdata.SRV_TYPE_CENTER:
            pass

    def gameId(self):
        '''
        取得当前游戏的GAMEID, int值
        '''
        return GAMEID

    def newTable(self, room, tableId):
        '''
        此方法由系统进行调用
        更具给出的房间的基本定义信息, 创建一个TYTable的实例
        其必须是 poker.entity.game.table.TYTable的子类
        room 桌子所属的房间的TYRoom实例
        tableId 新桌子实例的ID
        '''
        playMode = room.roomConf.get("playMode", "queshou")
        isCreateTable = room.roomConf.get("iscreate", 0)
        if ftlog.is_debug():
            ftlog.debug('TGhaerbin.newTable playMode:', playMode, ' isCreateTable:', isCreateTable)
        
        # 根据playMode和isCreateTable决定实例化那张桌子
        if isCreateTable:    
            table = QueshouMajiangFriendTable(tableId, room)
        else:
            table = QueshouMajiangQuickTable(tableId, room)
        return table
    
    def getInitDataKeys(self):
        '''
        取得游戏数据初始化的字段列表
        '''
        return self._account.getInitDataKeys()

    def getInitDataValues(self):
        '''
        取得游戏数据初始化的字段缺省值列表
        '''
        return self._account.getInitDataValues()

    def getGameInfo(self, userId, clientId):
        '''
        取得当前用户的游戏账户信息dict
        '''
        return self._account.getGameInfo(userId, clientId, GAMEID)

    def getDaShiFen(self, userId, clientId):
        '''
        取得当前用户的游戏账户的大师分信息
        '''
        return self._account.getDaShiFen(userId, clientId, GAMEID)

    def createGameData(self, userId, clientId):
        '''
        初始化该游戏的所有的相关游戏数据
        包括: 主游戏数据gamedata, 道具item, 勋章medal等
        返回主数据的键值和值列表
        '''
        return self._account.createGameData(userId, clientId, GAMEID)

    def loginGame(self, userId, gameId, clientId, iscreate, isdayfirst):
        '''
        用户登录一个游戏, 游戏自己做一些其他的业务或数据处理
        例如: 1. IOS大厅不发启动资金的补丁, 
             2. 麻将的记录首次登录时间
             3. 游戏插件道具合并至大厅道具
        '''
        return self._account.loginGame(userId, gameId, clientId, iscreate, isdayfirst)
    
    def getRobotManager(self):
        '''
        取得游戏的机器人管理器
        一定是 : TYRobotManager 的实例
        '''
        return self._robotmgr
    
    def checkFriendTable(self, ftId):
        '''
        检测自建桌ID是否继续使用，如果不使用，将回收次ftId
        0 - 有效
        1 - 无效
        
        返回值：
        False - 无用
        True - 有用
        '''
        tableId0, roomId0 = CreateTableData.getTableIdByCreateTableNo(ftId)
        if not tableId0 or not roomId0:
            # 房间无用，大厅可释放房间了
            return False
        
        return True
    
    def enterFriendTable(self, userId, gameId, clientId, ftId):
        """进入自建桌，插件实现具体功能"""
        if ftlog.is_debug():
            ftlog.debug('MAJIANG enterFriendTable userId:', userId
                        , ' gameId:', gameId
                        , ' clientId:', clientId
                        , ' ftId:', ftId)
            
        tableId0, roomId0 = CreateTableData.getTableIdByCreateTableNo(ftId)
        if ftlog.is_debug():
            ftlog.debug('MAJIANG enterFriendTable ftId:', ftId
                        , ' roomId:', roomId0
                        , ' tableId:', tableId0)
        
        if not tableId0 or not roomId0:
            from majiang2.entity.util import sendPopTipMsg
            sendPopTipMsg(userId, '您要进入的朋友场房间不存在，请核对房间号')
            return
        
        config = {
            "type":"game",
            "pluginParams": {
                "gameType": 11,
                "ftId": ftId
            }
        }
        
        todotask = TodoTaskEnterGameNew(GAMEID, config)
        mo = MsgPack()
        mo.setCmd('todo_tasks')
        mo.setResult('gameId', gameId)
        mo.setResult('pluginId', GAMEID)
        mo.setResult('userId', userId)
        mo.setResult('tasks', TodoTaskHelper.encodeTodoTasks(todotask))
        router.sendToUser(mo, userId)
        
    def getPlayGameInfoByKey(self, userId, clientId, keyName):
        if keyName == TYGame.PLAY_COUNT:
            countStr = gamedata.getGameAttr(userId, GAMEID, 'play_game_count')
            if not countStr:
                return 0
            return int(countStr)
        
        elif keyName == TYGame.WIN_COUNT:
            winStr = gamedata.getGameAttr(userId, GAMEID, 'win_game_count')
            if not winStr:
                return 0
            return int(winStr)
        
        return None
    
TGQueshou = TGQueshou()

def getInstance():
    return TGQueshou
