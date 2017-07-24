# -*- coding=utf-8
'''
Created on 2016年9月23日
牌桌麻将牌的管理器
包括：
1）发牌
2）牌桌上的出牌
3）宝牌

发牌说明：
发牌涉及到好牌点
@author: zhaol
'''
from majiang2.table_tile.test.table_tile_test import MTableTileTest
from poker.entity.dao import daobase
from freetime.util import log as ftlog
import json

class MTableTileTestLongNet(MTableTileTest):
    
    def __init__(self, playerCount, playMode):
        super(MTableTileTestLongNet, self).__init__(playerCount, playMode)
        
    def initTiles(self):
        """初始化手牌，用于摆牌测试"""
        key = 'put_card:' + self.playMode
        ftlog.debug('MTableTileTestLongNet key:', key)
        
        tile_info = daobase.executeMixCmd('get', key)
        ftlog.debug('MTableTileTestLongNet.initTiles tile_info:', tile_info)
        if not tile_info:
            ftlog.debug('MTableTileTestLongNet.initTiles failed...')
            return False
        
        tileObj = json.loads(tile_info)
        handTiles = []
        ftlog.debug('MTableTileTestLongNet.playerCount:', self.playerCount)
        for index in range(1, self.playerCount+1):
            indexTiles = tileObj.get('seat'+str(index), [])
            ftlog.debug('MTableTileTestLongNet.initTiles seat'+str(index)+':', indexTiles, ' length:', len(indexTiles))
            #数据校验
            if len(indexTiles) > 16:
                return False
            handTiles.append(indexTiles)
        pool = tileObj.get('pool', [])
        ftlog.debug('MTableTileTestLongNet.initTiles pool:', pool, ' length:', len(pool))
        
        self.setHandTiles(handTiles)
        self.setTiles(pool)
        
        return True
