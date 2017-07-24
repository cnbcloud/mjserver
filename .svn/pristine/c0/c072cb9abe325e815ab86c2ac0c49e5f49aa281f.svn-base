# -*- coding=utf-8
'''
Created on 2016年9月23日
上行行为处理

@author: zhaol
'''
from majiang2.action_handler.action_handler import ActionHandler
from freetime.util import log as ftlog

class ActionHandlerConsole(ActionHandler):
    
    def __init__(self):
        super(ActionHandlerConsole, self).__init__()
        
    def processAction(self, cmd):
        """处理玩家行为
        在本类里为终端输入
        """
        ftlog.debug('cmd:', cmd)
        details = cmd.split(' ')
#         print details[0]
#         print details[1]
#         print details[2]
        cpSeat = int(details[0])
        cpAction = int(details[1])
        
        ftlog.debug('cpAction', cpAction)
        ftlog.debug('ACTION_DROP', ActionHandler.ACTION_DROP)
        
        if not self.table:
            ftlog.debug('table error')
        
        if cpAction == ActionHandler.ACTION_DROP:
            dropTile = int(details[2])
            ftlog.debug('dropTile', dropTile)
            self.table.dropTile(cpSeat, dropTile)
        elif cpAction == ActionHandler.ACTION_CHI:
            chiTile = int(details[2])
#             ftlog.debug('chiTile', chiTile )
            
            # 输入格式，形如：11，12，13
            chiTiles = details[3]
#             ftlog.debug('chiTiles', chiTiles)
            chiTilesArr = chiTiles.split(',')
#             ftlog.debug('chiPattern', chiTilesArr)
            
            chiPattern = []
            chiPattern.append(int(chiTilesArr[0]))
            chiPattern.append(int(chiTilesArr[1]))
            chiPattern.append(int(chiTilesArr[2]))
            
#             ftlog.debug( 'chiPattern 0', chiPattern[0] )
#             ftlog.debug( 'chiPattern 1', chiPattern[1] )
#             ftlog.debug( 'chiPattern 2', chiPattern[2] )
            
            self.table.chiTile(cpSeat, chiTile, chiPattern)
        elif cpAction == ActionHandler.ACTION_PENG:
            pengTile = int(details[2])
            ftlog.debug( 'pengTile', pengTile )
            # 输入格式，形如：11，11，11
            pengPattern = [pengTile, pengTile, pengTile]
            pengTiles = details[3]
            if pengTiles:
                pengTilesArr = pengTiles.split(',')
                pengPattern = [int(pengTilesArr[0]), int(pengTilesArr[1]), int(pengTilesArr[2])]

            self.table.pengTile(cpSeat, pengTile, pengPattern)
            
        elif cpAction == ActionHandler.ACTION_GANG:
            gangTile = int(details[2])
            ftlog.debug( 'gangTile', gangTile )
            # 输入格式，形如：11，11，11
            gangTiles = details[3]
            gangTilesArr = gangTiles.split(',')
            gangPattern = [int(gangTilesArr[0]), int(gangTilesArr[1]), int(gangTilesArr[2]), int(gangTilesArr[3])]
                
            isMingGang = (int(details[4]) == 1)
            self.table.gangTile(cpSeat, gangTile, gangPattern, isMingGang)
            
        elif cpAction == ActionHandler.ACTION_HU:
            winTile = int(details[2])
            ftlog.debug( 'winTile', winTile )
            self.table.gameWin(cpSeat, winTile)
            
        elif cpAction == ActionHandler.ACTION_TING:
            dropTile = int(details[2])
            ftlog.debug( 'dropTile ', dropTile, ' to ting!' )
            self.table.tingAfterDropCard(cpSeat, dropTile)
            
        elif cpAction == ActionHandler.ACTION_MAO:
            maoTiles = details[2]
            maoTilesArr = maoTiles.split(',')
            maoPattern = []
            for strTile in maoTilesArr:
                maoPattern.append(int(strTile))
                
            maoType = int(details[3])
            mao = {}
            mao['pattern'] = maoPattern
            mao['type'] = maoType
            self.table.fangMao(cpSeat, mao)
            
        elif cpAction == 0:
            tile = int(details[2])
            ftlog.debug( 'tile', tile )
            self.table.playerCancel(cpSeat)
        
if __name__ == "__main__":
    # 吃 seatId 2 tile pattern
    cmd = '0 2 11 11,12,13'
    # 碰
#     cmd = '0 3 11'
    # 杠
#     cmd = '0 4 11'
    # 和
#     cmd = '0 5 11'
    
    handler = ActionHandlerConsole()
    handler.processAction(cmd, None)