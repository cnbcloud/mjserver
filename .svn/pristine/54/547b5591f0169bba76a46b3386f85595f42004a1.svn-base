# -*- coding=utf-8 -*-
from poker.entity.biz.task.task import TYTaskInspector,\
    TYTaskInspectorRegister
from majiang2.entity.events.events import UserTablePlayEvent
from queshou.entity.configure.conf import GAMEID
from freetime.util import log as ftlog

class GameTaskInspectorPlay(TYTaskInspector):
    TYPE_ID = str(GAMEID) + '.play'
    EVENT_GAMEID_MAP = {UserTablePlayEvent:(GAMEID,)}
    def __init__(self):
        super(GameTaskInspectorPlay, self).__init__(self.EVENT_GAMEID_MAP)
        
    def _processEventImpl(self, task, event):
        ftlog.debug('GameTaskInspectorPlay udpate task progress:', task.progress
                , ' roomId:', event.roomId
                , ' tableId:', event.tableId
                , ' userId:', event.userId
                , ' gameId:', event.gameId
                , ' timestamp:', event.timestamp)
        
        if isinstance(event, UserTablePlayEvent) and (event.gameId == GAMEID):
            return task.setProgress(task.progress + 1, event.timestamp)
        return False, 0
    
    def on_task_created(self, task):
        ftlog.debug('GameTaskInspectorPlay.on_task_created...')

def _registerClasses():
    ftlog.info('majiang2_task._registerClasses')
    TYTaskInspectorRegister.registerClass(GameTaskInspectorPlay.TYPE_ID, GameTaskInspectorPlay)