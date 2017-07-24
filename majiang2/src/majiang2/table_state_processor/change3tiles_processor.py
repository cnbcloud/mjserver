#! -*- coding:utf-8 -*-
# Author:   you
# Created:  2017/4/21

from freetime.util import log as ftlog

from majiang2.table_state_processor.processor import MProcessor
from majiang2.ai.play_mode import MPlayMode
from majiang2.tile.tile import MTile
import random
#class MAbsenceProcessor(MProcessor):
class MChange3tilesProcessor(MProcessor):
    """换三张处理
       在庄家14张牌，闲家13张牌时，庄家不打牌，进入换三张阶段，在所有玩家都换三张之后，才能继续定缺,打牌
    """

    SCHEDULE_CHANGE3TILES_NONE = 0   # 默认处于非换三张阶段
    SCHEDULE_CHANGE3TILES_BEGIN = 1  # 开始进入换三张阶段
    SCHEDULE_CHANGE3TILES_DING = 2   # 询问玩家选择哪三张

    TILES_CHANGE_INIT = [-1,-1,-1]  # 初始换三张状态
    #self.__drop_tiles = [[] for _ in range(self.playCount)]
    
    # 每个玩家摸到的牌
    #self.__add_tiles = [[] for _ in range(self.playCount)]

    def __init__(self, count, playMode):
        super(MChange3tilesProcessor, self).__init__()
        # 玩家数量
        self.__player_count = count
        # 玩法
        self.__player_mode = playMode
        # 调度情况
        self.__schedule = self.SCHEDULE_CHANGE3TILES_NONE
        # 缺门情况
        self.__change3Tiles = [self.TILES_CHANGE_INIT] * self.playerCount
	self.__banker_mgr = None
        self.__directionId = 0


    def reset(self):
        self.__schedule = self.SCHEDULE_CHANGE3TILES_NONE
        self.__change3Tiles = [self.TILES_CHANGE_INIT] * self.playerCount
        self.__directionId = 0

    @property
    def directionId(self):
        return self.__directionId

    @property
    def playerCount(self):
        return self.__player_count

    def setPlayerCount(self, pCount):
        self.__player_count = pCount

    #modify by youjun 04.27
    @property
    def bankerMgr(self):
        """庄"""
        return self.__banker_mgr

    def setBankerMgr(self,bankerMgr):
        self.__banker_mgr = bankerMgr

    @property
    def playMode(self):
        """获取本局玩法"""
        return self.__player_mode

    def setPlayMode(self, playMode):
        self.__player_mode = playMode

    @property
    def schedule(self):
        return self.__schedule

    def setSchedule(self, schedule):
        self.__schedule = schedule

    @property
    def change3Tiles(self):  # absenceColor(self):
        return self.__change3Tiles

    def setChange3Tiles(self, value):
        self.__change3Tiles = value

    def getState(self):
        return 0 if self.schedule == self.SCHEDULE_CHANGE3TILES_NONE else 1

    def beginChange3Tiles(self):
        """开始换三张，前端收到这个消息之后提示让玩家换三张操作
        """
        self.setSchedule(self.SCHEDULE_CHANGE3TILES_BEGIN)

    def onBankerAddedFirstTile(self):
        """庄家摸完了牌，开始询问玩家进行换三张
        """
        self.setSchedule(self.SCHEDULE_CHANGE3TILES_DING)
        for seatId in range(self.playerCount):
            ftlog.debug('change3tiles_processor onBankerAddedFirstTile:',len(self.players),' seatId:',seatId,' playerCount:',self.playerCount)
            self.msgProcessor.table_call_ask_change3tiles(self.players[seatId].userId, seatId)
            # 取出手牌
            tiles = self.players[seatId].copyHandTiles()
            ftlog.debug('player seatId',seatId,' tiles:',tiles)

    def chooseChange3tiles(self, seatId, tiles):
        """玩家选择换哪三张
        """
        # 玩家已经选择过了，不能再次选择
        if self.change3Tiles[seatId] != self.TILES_CHANGE_INIT:
            return

        # 只能缺万筒条中的一个颜色
        #if color not in (MTile.TILE_WAN, MTile.TILE_TONG, MTile.TILE_TIAO):
        #    return

        self.change3Tiles[seatId] = tiles
        #self.change3Tiles[seatId].append(tiles)

        ftlog.debug('chooseChange3tiles seatId:', seatId, ' tiles:', tiles)

        if self.isAllSelected():
            # 所有人都已选择换三张，结束换三张状态
            self.chooseMethodForChange3tiles()
            self.setSchedule(self.SCHEDULE_CHANGE3TILES_NONE)
            ftlog.debug('chooseChange3tiles AllSelected')
        else:
             for i in range(self.playerCount):
                self.msgProcessor.table_call_player_change3tiles_end(self.players[i].userId, seatId)     
    def chooseMethodForChange3tiles(self):
        #随机选择换三张方式:0-逆时针 1-顺时针 

        for seatId in range(self.playerCount):
            for tileId in range(len(self.change3Tiles[seatId])):
                change3tile = self.change3Tiles[seatId][tileId]
                if change3tile not in self.players[seatId].handTiles:
                    ftlog.error('chooseMethodForChange3tiles', self.players[seatId].name
                            , ' SeatId:', seatId
                            , ' change3tile:', change3tile
                            , ' handTile:', self.players[seatId].handTiles
                            , ' BUT change3tile NOT IN HANDTILES!!!')
                    return False
                self.players[seatId].handTiles.remove(change3tile)

                
        self.__directionId = random.randint(0, 2)

        if self.directionId == 0:     
            #逆时针   
            self.chooseAnticlockwiseChange3tiles()                             
        elif self.directionId == 1:
            #顺时针
            self.chooseClockwiseChange3tiles()          
	elif self.directionId == 2:
            #对家
            if self.playerCount == 4:
                self.chooseFaceChange3tiles()
            else:
                #玩家小于4则选择逆时针
                self.__directionId = 0
                self.chooseAnticlockwiseChange3tiles()
    def chooseClockwiseChange3tiles(self):
        #顺时针
        for seatId in range(self.playerCount):
            # 取出手牌
            #tiles = self.players[seatId].copyHandTiles()
            ftlog.debug('chooseClockwiseChange3tiles seatId',seatId,' handTiles:',self.players[seatId].handTiles)
            change3tilesId = (seatId + 1 + self.playerCount) % self.playerCount
            for tileId in range(len(self.change3Tiles[change3tilesId])):
                self.players[seatId].handTiles.append(self.change3Tiles[change3tilesId][tileId])
            self.players[seatId].handTiles.sort()
            ftlog.debug('chooseClockwiseChange3tiles change3tiles end handTiles:' ,self.players[seatId].handTiles)
            #banker = self.players[self.bankerMgr.queryBanker()]
            #if banker == self.players[seatId] :
	    #    self.players[seatId].handTiles.remove(self.players[seatId].curTile)
            #    ftlog.debug('chooseClockwiseChange3tiles banker seatId',seatId)
	    change3tilesInfo=[]
            # 向玩家广播换三张完毕, 换三张的情况
            self.msgProcessor.table_call_send_3tiles(self.players[seatId].userId, seatId, self.change3Tiles[change3tilesId],self.players[seatId].handTiles,self.directionId)


    def chooseAnticlockwiseChange3tiles(self):
        #逆时针
        for seatId in range(self.playerCount):
            # 取出手牌
            #tiles = self.players[seatId].copyHandTiles()
            ftlog.debug('chooseAnticlockwiseChange3tiles seatId',seatId,' handTiles:',self.players[seatId].handTiles)
            change3tilesId = (seatId - 1 + self.playerCount) % self.playerCount
            for tileId in range(len(self.change3Tiles[change3tilesId])):
                self.players[seatId].handTiles.append(self.change3Tiles[change3tilesId][tileId])
            self.players[seatId].handTiles.sort()
            ftlog.debug('chooseAnticlockwiseChange3tiles change3tiles end handTiles:' ,self.players[seatId].handTiles)
            #banker = self.players[self.bankerMgr.queryBanker()]
            #if banker == self.players[seatId] :
	    #    self.players[seatId].handTiles.remove(self.players[seatId].curTile)
            #    ftlog.debug('chooseClockwiseChange3tiles banker seatId',seatId)
	    change3tilesInfo=[]
            # 向玩家广播换三张完毕, 换三张的情况
            self.msgProcessor.table_call_send_3tiles(self.players[seatId].userId, seatId, self.change3Tiles[change3tilesId],self.players[seatId].handTiles,self.directionId)

    def chooseFaceChange3tiles(self):
        #对家
        for seatId in range(self.playerCount):
            # 取出手牌
            ftlog.debug('chooseFaceChange3tiles seatId',seatId,' handTiles:',self.players[seatId].handTiles)
            change3tilesId = (seatId + 2 + self.playerCount) % self.playerCount
            for tileId in range(len(self.change3Tiles[change3tilesId])):
                self.players[seatId].handTiles.append(self.change3Tiles[change3tilesId][tileId])
            self.players[seatId].handTiles.sort()
            ftlog.debug('chooseFaceChange3tiles change3tiles end handTiles:' ,self.players[seatId].handTiles)

            change3tilesInfo=[]
            # 向玩家广播换三张完毕, 换三张的情况
            self.msgProcessor.table_call_send_3tiles(self.players[seatId].userId, seatId, self.change3Tiles[change3tilesId],self.players[seatId].handTiles,self.directionId)


    def isAllSelected(self):
        """是否所有人都已换三张
        """
        for tiles in self.change3Tiles:
            if tiles == self.TILES_CHANGE_INIT:
                return False
        return True

    def handlePlayerReconnect(self, userId, seatId):
        """处理玩家的断线重连
        """
	ftlog.debug('handlePlayerReconnect change3TilesProcessor self.schedule:',self.schedule,self.change3Tiles[seatId])
        if not self.msgProcessor:
            return

        if self.schedule == self.SCHEDULE_CHANGE3TILES_DING:  # 正在换三张的阶段
            # 玩家还没换三张，通知其换三张
            if self.change3Tiles[seatId] == self.TILES_CHANGE_INIT:
                self.msgProcessor.table_call_ask_change3tiles(userId, seatId)

    if __name__ == "__main__":
        change3tilesPro = MChange3tilesProcessor(4)
        change3tilesPro.reset()
        change3tilesPro()
        change3tilesPro.onBankerAddedFirstTile()
        change3tilesPro.chooseChange3tiles(0,[1,2,3])
        change3tilesPro.chooseChange3tiles(0,[1,2,3])
        change3tilesPro.chooseChange3tiles(0,[1,2,3])
        change3tilesPro.chooseChange3tiles(0,[1,2,3])
        ftlog.debug('tile',change3tilesPro.change3Tiles[0][0],' ',change3tilesPro.change3Tiles[0][1],' ',change3tilesPro.change3Tiles[0][2])

