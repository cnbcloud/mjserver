#! -*- coding:utf-8 -*-
# Author:   yawen
# Created:  2017/3/25


from majiang2.table_state_processor.processor import MProcessor
from freetime.util import log as ftlog
from majiang2.table_state.state import MTableState
import time


class KaijinProcessor(MProcessor):
    """开金
    """

    def __init__(self, count, playMode):
        super(KaijinProcessor, self).__init__()
        # 标记
        self.__state = MTableState.TABLE_STATE_NEXT
        self.__uids = None
        self.__banker = 0
	self.__magicTiles = []
    def reset(self):
        self.__state = MTableState.TABLE_STATE_NEXT
	self.__uids = None
        self.__banker = 0
	self.__magicTiles = []

    @property
    def state(self):
        return self.__state
    
    def setState(self, state):
        self.__state = state

    def initProcessor(self, state, banker, msgProcessor, uids):
        self.__state = state
        self.setMsgProcessor(msgProcessor)
 
	self.__banker = banker
        self.__uids = uids 
	return True
  
    def beginKaijin(self):
        magicTile = 0
	ftlog.debug('KaijinProcessor.beginKaijin called',) 
        if len(self.tableTileMgr.tiles) > 0:
	    # 开金
	    ftlog.debug('self.tableTileMgr.tiles=',self.tableTileMgr.tiles)
            magicTile = self.tableTileMgr.tiles.pop(0)
	    self.__magicTiles.append(magicTile)
	    #if len(self.__magicTiles) >0:
            time.sleep(2)
	    ftlog.debug('magicTile=',magicTile)
            if self.tableTileMgr.isFlower(magicTile):
                self.players[self.__banker].addFlowers(magicTile)
                self.tableTileMgr.setFlowerTileInfo(magicTile,self.__banker)
                self.players[self.__banker].addFlowerScores(1)
                self.tableTileMgr.addFlowerScores(1, self.__banker)
		self.msgProcessor.table_call_kaijin_broadcast(magicTile,self.__uids,True,self.__banker)
                return False            
            else:                
                self.tableTileMgr.addSpecialTile(magicTile)
		self.tableTileMgr.setMagicTile(magicTile)
    		self.tableTileMgr.setMagicTileInfo(magicTile)
	        self.endKaijin(magicTile)
		ftlog.debug('KaijinProcessor.Kaijin magicTile=',magicTile) 
		return True

	return False
    '''
    def sleepToContinue(self):
        time.sleep(0.3)
        self.beginKaijin()
    '''
    def endKaijin(self,magicTile):
        self.msgProcessor.table_call_kaijin_broadcast(magicTile,self.__uids,False,self.__banker)
        self.setState(MTableState.TABLE_STATE_NEXT)
        self.reset()

    def getState(self):
        """获取状态 1 掷骰子 0 完毕
        """
        return self.state
