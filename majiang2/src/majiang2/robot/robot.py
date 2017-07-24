# -*- coding=utf-8 -*-
'''
Created on 2015年12月29日

@author: liaoxx
'''
from majiang2.robot.robotuser import RobotUser
from freetime.util import log as ftlog
from poker.entity.configure import gdata
from poker.entity.robot.robot import TYRobotManager
from majiang2.resource import resource
 
class MajiangRobotManager(TYRobotManager):
 
 
    def __init__(self):
        super(MajiangRobotManager, self).__init__()
        baseSnsId = 'robot:' + gdata.serverId()
        users = []
        for index in range(resource.getRobotCount()):
            robot = resource.getRobot(index)
            name = robot['name']
            snsId = baseSnsId + '_' + str(index)
            users.append(RobotUser(None, snsId, name)) 
        self.freeRobotUsers = users
        ftlog.debug('robot user count ->', len(users))