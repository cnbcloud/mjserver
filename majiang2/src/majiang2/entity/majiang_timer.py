# -*- coding=utf-8 -*-
'''
Created on 2015年10月8日

@author: liaoxx
'''
import stackless
from poker.entity.game.tables.table_timer import TYTableTimer
from freetime.core.timer import FTTimer
from freetime.entity.msg import MsgPack

class TableTimer(TYTableTimer):
    def setup(self, interval, action, msgPackParams, cancelLastTimer=True):
        '''
        启动计时器
        interval 倒计时的时间, 单位: 秒
        action table_call命令下(params中)的action值
        msgPackParams 传递的其他的参数数据集合dict, 可以在doTableCall中的msg中使用msg.getParam(key)来取得其中的参数
        '''
        if self._fttimer and cancelLastTimer:
            self._fttimer.cancel()
        self._interval = interval
        userId = msgPackParams.get('userId', 0)
        clientId = msgPackParams.get('clientId', None)
        assert(isinstance(userId, int))
        assert(isinstance(action, (unicode, str)))
        if clientId != None :
            assert(isinstance(clientId, (unicode, str)))
        msg = MsgPack()
        msg.updateParam(msgPackParams)
        msg.setCmdAction('table_call', action)
        msg.setParam('gameId', self._table.gameId)
        msg.setParam('roomId', self._table.roomId)
        msg.setParam('tableId', self._table.tableId)
        msg.setParam('userId', userId)
        msg.setParam('clientId', clientId)
        self._fttimer = FTTimer(interval, self._onTimeOut, msg, pack = msg)
    

class MajiangTableTimer(object):
    """
    麻将牌桌的定时器
    有几个座位，就有几个定时器
    定时器跟座位号一一对应
    """
    
    def __init__(self, timerCount, table):
        """
        参数
        1）timerCount 定时器个数
        2）TYTable实例
        """
        self._timer = []
        for _ in range(timerCount):
            self._timer.append(TableTimer(table))

    def setupTimer(self, timerid, interval, msg, gdata = None):
        timer = self._timer[timerid]
        action = msg.getParam("action")
        msgPackParams = msg._ht.get("params",{})
        timer.setup(interval, action, msgPackParams)

    def getTimeOut(self, timerid):
        timer = self._timer[timerid]
        return timer.getTimeOut()

    def getTimerInterval(self, timerid):
        timer = self._timer[timerid]
        if timer._fttimer:
            return timer.getInterval()
        else:
            return 0
    
    def resetTimer(self, timerid, interval):
        timer = self._timer[timerid]
        if timer._fttimer:
            timer.reset(interval)
    
    def cancelTimer(self, timerid):
        timer = self._timer[timerid]
        timer.cancel()

    def cancelTimerAll(self):
        for i in xrange(len(self._timer)):
            timer = self._timer[i]
            timer.cancel() 

class RoomTimer(object): 
    def __init__(self, room):
        self._fttimer = None  # 计时器对象
        self._interval = 0  # 倒计时时间,单位: 秒
        self._room = room

    def _onTimeOut(self):
        msg = stackless.getcurrent()._fttask.run_argl[0]
        self._room.on_match_event(msg)

    def setup(self, interval, msg, cancelLastTimer=True):
        if self._fttimer and cancelLastTimer:
            self._fttimer.cancel()
        self._interval = interval
        self._fttimer = FTTimer(interval, self._onTimeOut, msg)

    def cancel(self):
        '''
        取消当前的计时器
        '''
        if self._fttimer :
            self._fttimer.cancel()
            self._fttimer = None
            self._interval = 0  
            
    def reset(self, interval):
        '''
        重置当前的计时器
        '''
        
        if self._fttimer:
            self._fttimer.reset(interval)
            self._interval = interval
    
    def getInterval(self):
        '''
        取得当前计时器的倒计时时间
        '''
        if self._fttimer:
            return self._interval
        else:
            return 0
    
    
    def getTimeOut(self):
        '''
        取得当前计时器的剩余的倒计时时间, 若没有开始倒计时, 那么返回0
        '''
        if self._fttimer :
            self._fttimer.getTimeOut()
        return 0.0
           
class MajiangRoomTimer(object):            
    def __init__(self, timerCount, room):
        self._timer = []
        for _ in range(timerCount):
            self._timer.append(RoomTimer(room))

    def setupTimer(self, timerid, interval, msg):
        timer = self._timer[timerid]
        timer.setup(interval, msg)

    def getTimeOut(self, timerid):
        timer = self._timer[timerid]
        return timer.getTimeOut()


    def getTimerInterval(self, timerid):
        timer = self._timer[timerid]
        return timer.getInterval()
    
    def resetTimer(self, timerid, interval):
        timer = self._timer[timerid]
        timer.reset(interval)
    
    def cancelTimer(self, timerid):
        timer = self._timer[timerid]
        timer.cancel()

    def cancelTimerAll(self):
        for i in xrange(len(self._timer)):
            timer = self._timer[i]
            timer.cancel()         