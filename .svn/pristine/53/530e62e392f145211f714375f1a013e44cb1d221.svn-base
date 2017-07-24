# -*- coding=utf-8 -*-
'''
Created on 2015年12月29日

@author: liaoxx
'''
from freetime.entity.msg import MsgPack
from freetime.util import log as ftlog
from poker.entity.configure import gdata
from poker.entity.robot.robotuser import RobotUser 
 
class RobotUser(RobotUser):
 
 
    def __init__(self, clientId, snsId, name):
        super(RobotUser, self).__init__(clientId, snsId, name)

    def _stop(self):
        pass
 
    def _start(self):
        playMode = gdata.roomIdDefineMap()[self.roomId].configure['playMode']
        self.playMode = playMode

    def _newTileManager(self):
        self.tileManager = None
 
    def onMsgTableBegin(self):
        roomTypeName = gdata.roomIdDefineMap()[self.roomId].configure['typeName']
        if roomTypeName == "majiang_bigmatch":             
            moSigninMatch = MsgPack()
            moSigninMatch.setCmdAction('room', 'signin')
            moSigninMatch.setParam('userId', self.userId)
            moSigninMatch.setParam('gameId', self.gameId)
            moSigninMatch.setParam('clientId', self.clientId)
            moSigninMatch.setParam('roomId', self.roomId)
            self.writeMsg(moSigninMatch)
            self.isMatch = True
        else :
            ftlog.debug('send quick Start !!!')
            self.adjustChip()
            mo = MsgPack()
            mo.setCmdAction('game', 'quick_start')
            mo.setParam('userId', self.userId)
            mo.setParam('gameId', self.gameId)
            mo.setParam('clientId', self.clientId)
            mo.setParam('roomId', self.roomId)
            mo.setParam('tableId', self.tableId)
            self.writeMsg(mo)
            self.isMatch = False
        return
    
    def _initTiles(self, tiles):
        if (self.playMode == "guobiao" or self.playMode == "guobiao2ren" 
            or self.playMode == "harbin" or self.playMode == "nanchang"):
            self.tileManager.init_tiles(tiles)
        else:
            for tile in tiles:
                self.tileManager.AddTile(tile)
                
    def _addTile(self, tile):
        if (self.playMode == "guobiao" or self.playMode == "guobiao2ren" 
            or self.playMode == "harbin" or self.playMode == "nanchang"):
            self.tileManager.add(tile)
        else:
            self.tileManager.AddTile(tile)
            
    def _delTile(self, tile):
        if (self.playMode == "guobiao" or self.playMode == "guobiao2ren" 
            or self.playMode == "harbin" or self.playMode == "nanchang"):
            self.tileManager.delete(tile)
        else:
            self.tileManager.DropTile(tile)
            
    def _playAsTrustee(self):
        if (self.playMode == "guobiao" or self.playMode == "guobiao2ren" 
            or self.playMode == "harbin" or self.playMode == "nanchang"):
            return self.tileManager.play_as_trustee()
        else:
            return self.tileManager.PlayAsTrustee()        
    
    def _dealSendTile(self, msg):
        ftlog.debug("standuptiles:", self._getStandupTiles(), self.snsId)
        tile = msg.getResult("tile")
        result = msg.getKey('result')
        mo = MsgPack()
       
        if "win_action" in result and result.get("win_action") == 1:
            mo.setCmdAction('table_call', 'win')
        elif "ting_action" in result and len(result.get("ting_action")) >= 1:
            self._addTile(tile)
            ting_action = result.get("ting_action")
            tingTile = ting_action[0][0]
            self._delTile(tingTile)
            mo.setCmdAction('table_call', 'play')
            mo.setParam('tile', tingTile)
            mo.setParam('ting', 1) 
        elif "gang_action" in result:
            mo.setCmdAction('table_call', 'gang')  
            mo.setParam('tile', result.get("gang_action")[0])
        else:
            self._addTile(tile)
            mo.setCmdAction('table_call', 'play')
            playTile = self._playAsTrustee()
            self._delTile(playTile)
            mo.setParam('tile', playTile)
            
        mo.setParam('userId', self.userId)
        mo.setParam('gameId', self.gameId)
        mo.setParam('clientId', self.clientId)
        mo.setParam('roomId', self.roomId)
        mo.setParam('tableId', self.tableId)         
        mo.setParam('seatId', self.seatId)
        mo.setParam('action_id', result.get("action_id"))
            
        self.writeMsg(mo)
        return  
    
    """
    sichuan:
    0-胡牌；1-杠；2-碰。返回执行的一个动作，3-过。
    harbin:
    #[win, grabTing, gang, peng, chi]
    #return 0: win, 1:grabTing, 2: gang, 3: peng,4: pass     >=5: chi,  5+0 zuo 5+1 zhong 5+2 you
    
    guobiao:
    /// @param actions  [win, gang, peng, chi]  True/False
    /// @return 0:win, 1:gang, 2:peng, 3:pass, >=4 :shun   style: -4
    """
    def _dealPlay(self, msg):
        tile = msg.getResult("tile")
        result = msg.getKey('result')
        actions = []
        if "win_action" in result:
            actions.append("win")
        if "peng_action" in result:
            actions.append("peng")
        if "gang_action" in result:
            actions.append("gang")
        if "chi_action" in result:
            actions.append("chi")
        if "grabTing_action" in result:
            actions.append("grabTing")
       
        if len(actions) > 0:
            self._reactAsTrustee(actions, tile, msg)
            
    def _reactAsTrustee(self, actions, tile, msg):
        message = MsgPack()
        if (self.playMode == "sichuan" or self.playMode == "sichuan_dq" 
                    or self.playMode == "sichuan_xlch"):     
            actionList = []
            if "win" in actions:
                actionList.append(0)   
            if "gang" in actions:
                actionList.append(1)
            if "peng" in actions:
                actionList.append(2)
            action, tile = self.tileManager.DealAsTrustee(tile, actionList)
            if action == 0:
                message.setCmdAction('table_call', 'win')
            elif action == 1:
                message.setCmdAction('table_call', 'gang')
            elif action == 2:
                message.setCmdAction('table_call', 'peng')                
            elif action == 3:
                message.setCmdAction('table_call', 'pass')
            message.setParam('tile', tile)
        elif (self.playMode == "guobiao" or self.playMode == "guobiao2ren" or self.playMode == "nanchang"):
            actionList = []
            if "win" in actions:
                actionList.append(True) 
            else:
                actionList.append(False)
            if "gang" in actions:
                actionList.append(True) 
            else:
                actionList.append(False) 
            if "peng" in actions:
                actionList.append(True) 
            else:
                actionList.append(False) 
            if "chi" in actions:
                actionList.append(True) 
            else:
                actionList.append(False)  
            reply_action = self.tileManager.react_as_trustee(tile, actionList)
            if reply_action == 0:
                message.setCmdAction('table_call', 'win')
            elif reply_action == 1:
                message.setCmdAction('table_call', 'gang')
            elif reply_action == 2:
                message.setCmdAction('table_call', 'peng')
            elif reply_action == 3:
                message.setCmdAction('table_call', 'pass')
            else:
                message.setCmdAction('table_call', 'chi')
                message.setParam('style', reply_action - 4)
            message.setParam('tile', tile)
        elif (self.playMode == "harbin"):
            actionList = []
            if "win" in actions:
                actionList.append(True) 
            else:
                actionList.append(False)
            if "grabTing" in actions:
                actionList.append(True) 
            else:
                actionList.append(False)
            if "gang" in actions:
                actionList.append(True) 
            else:
                actionList.append(False) 
            if "peng" in actions:
                actionList.append(True) 
            else:
                actionList.append(False) 
            if "chi" in actions:
                actionList.append(True) 
            else:
                actionList.append(False)  
            reply_action = self.tileManager.react_as_trustee(tile, actionList)
            if reply_action == 0:
                message.setCmdAction('table_call', 'win')
            elif reply_action == 1:
                message.setCmdAction('table_call', 'grabTing')
                grabInfo = msg.getResult("grabTing_action")
                if "chi_action" in grabInfo:
                    message.setParam('chi', tile)
                    message.setParam('style', grabInfo["chi_action"][0])
                else:
                    message.setParam('peng', tile)
                    
            elif reply_action == 2:
                message.setCmdAction('table_call', 'gang')
            elif reply_action == 3:
                message.setCmdAction('table_call', 'peng')
            elif reply_action == 4:
                message.setCmdAction('table_call', 'pass')
            else:
                message.setCmdAction('table_call', 'chi')
                message.setParam('style', reply_action - 5)
                        
        message.setParam('userId', self.userId)
        message.setParam('gameId', self.gameId)
        message.setParam('clientId', self.clientId)
        message.setParam('roomId', self.roomId)
        message.setParam('tableId', self.tableId)         
        message.setParam('seatId', self.seatId)
        message.setParam('action_id', msg.getResult("action_id"))
        self.writeMsg(message)
        return  
    
    def _dealGrabTing(self, msg):
        chiTile = msg.getResult("chi")
        pengTile = msg.getResult("peng")
        if chiTile:
            chiStyle = msg.getResult("style")
            self.tileManager.set_chi(chiTile, chiStyle)
        else:
            self._setPeng(pengTile)
            
        ting_infos = msg.getResult("ting_action")
        playTile = ting_infos[0][0]
        self._delTile(playTile)
        message = MsgPack() 
        message.setCmdAction('table_call', 'play')
        message.setParam("tile", playTile)
        message.setParam('ting', 1)
        message.setParam('userId', self.userId)
        message.setParam('gameId', self.gameId)
        message.setParam('clientId', self.clientId)
        message.setParam('roomId', self.roomId)
        message.setParam('tableId', self.tableId)         
        message.setParam('seatId', self.seatId)
        message.setParam('action_id', msg.getResult("action_id"))
        self.writeMsg(message)
        return  
        
            
    def _setPeng(self, tile):
        if (self.playMode == "sichuan" or self.playMode == "sichuan_dq" 
                    or self.playMode == "sichuan_xlch"):               
            self.tileManager.SetPeng(tile)
        else:
            self.tileManager.set_peng(tile)
        
            
    def _dealChiPeng(self, msg):
        tile = msg.getResult("tile")
        style = msg.getResult("style")
        cmd = msg.getCmd()
        if cmd == "chi":
            self.tileManager.set_chi(tile,style)
        else:
            self._setPeng(tile)
        result = msg.getKey('result') 
        message = MsgPack() 
        if "ting_action" in result:
            tingAction = result.get("ting_action")
            message.setCmdAction('table_call', 'play')
            playTile = tingAction[0][0]
            message.setParam("tile", playTile)
            message.setParam('ting', 1)
        else:
            message.setCmdAction('table_call', 'play')
            playTile = self._playAsTrustee()
            message.setParam("tile", playTile) 
        self._delTile(playTile)
        message.setParam('userId', self.userId)
        message.setParam('gameId', self.gameId)
        message.setParam('clientId', self.clientId)
        message.setParam('roomId', self.roomId)
        message.setParam('tableId', self.tableId)         
        message.setParam('seatId', self.seatId)
        message.setParam('action_id', msg.getResult("action_id"))
        self.writeMsg(message)
        return            
            
    def _dealGang(self, msg):
        tile = msg.getResult("tile")
        style = msg.getResult("style")
        if (self.playMode == "sichuan" or self.playMode == "sichuan_dq" 
                    or self.playMode == "sichuan_xlch"):               
            self.tileManager.SetGang(tile, style)
        else:
            self.tileManager.set_gang(tile, style)
        return  
    
    def _dealWin(self, msg):
        tile = msg.getResult("tile")
        message = MsgPack()
        message.setCmd("table_call")
        message.setParam("action", "win")
        message.setParam("tile", tile)  
        message.setParam('userId', self.userId)
        message.setParam('gameId', self.gameId)
        message.setParam('clientId', self.clientId)
        message.setParam('roomId', self.roomId)
        message.setParam('tableId', self.tableId)         
        message.setParam('seatId', self.seatId)
        message.setParam('action_id', msg.getResult("action_id"))
        self.writeMsg(message)
        
    def _sendLeave(self):
        message = MsgPack()
        message.setCmd("table_call")
        message.setParam("action", "leave")
        message.setParam('userId', self.userId)
        message.setParam('gameId', self.gameId)
        message.setParam('clientId', self.clientId)
        message.setParam('roomId', self.roomId)
        message.setParam('tableId', self.tableId)         
        message.setParam('seatId', self.seatId)
        self.writeMsg(message)
        
        
    def _dealTing(self,msg):
        message = MsgPack()
        message.setCmd("table_call")
        message.setParam("action", "ting")
        message.setParam('userId', self.userId)
        message.setParam('gameId', self.gameId)
        message.setParam('clientId', self.clientId)
        message.setParam('roomId', self.roomId)
        message.setParam('tableId', self.tableId)         
        message.setParam('seatId', self.seatId)
        message.setParam('ting_info', [])
        message.setParam('server_reply', 1)
        message.setParam('action_id', msg.getResult("action_id"))
        self.writeMsg(message)
        
    def _getStandupTiles(self):
        if (self.playMode == "sichuan" or self.playMode == "sichuan_dq" 
                    or self.playMode == "sichuan_xlch"):               
            tiles = self.tileManager.GetStandupTiles()
        else:
            tiles = self.tileManager.get_all_standup_tiles()
        return tiles 
        
    def _sendChange3Tiles(self, msg):
        change3Tiles = self.tileManager.GetThreeTilesChange()
        for tile in change3Tiles:
            self._delTile(tile)
        message = MsgPack()
        message.setCmd("table_call")
        message.setParam("action", "change_3tiles")
        message.setParam('userId', self.userId)
        message.setParam('gameId', self.gameId)
        message.setParam('clientId', self.clientId)
        message.setParam('roomId', self.roomId)
        message.setParam('tableId', self.tableId)         
        message.setParam('seatId', self.seatId)
        message.setParam('action_id', msg.getResult("action_id"))
        message.setParam('threeTiles', change3Tiles)
        self.writeMsg(message)
        
    def _dealSend3Tiles(self, msg):
        new3Tiles = msg.getResult("threeTiles")
        for tile in new3Tiles:
            self._addTile(tile)
        absence = msg.getResult("absence")
        message = MsgPack()
        message.setCmd("table_call")
        message.setParam("action", "decide_absence")
        message.setParam('userId', self.userId)
        message.setParam('gameId', self.gameId)
        message.setParam('clientId', self.clientId)
        message.setParam('roomId', self.roomId)
        message.setParam('tableId', self.tableId)         
        message.setParam('seatId', self.seatId)
        message.setParam('action_id', msg.getResult("action_id"))
        message.setParam('absence', absence)
        self.writeMsg(message)
        self.tileManager.setAbsence(absence)

    def onMsgTablePlay(self, msg):
        cmd = msg.getCmd()         
        if cmd == 'table_info' :
            self.roomId = msg.getResult('roomId')
            self.tableId = msg.getResult('tableId')
            self.seatId = msg.getResult('seatId')
            self.tableInfoResult = msg.getKey('result')
            
        if cmd == "init_tiles":
            self._newTileManager()
            tiles = msg.getResult("tiles")
            self._initTiles(tiles)
            ftlog.debug("standuptiles:", self._getStandupTiles(), self.snsId)
            if self.playMode == "sichuan_dq":
                self._sendChange3Tiles(msg)
            
            
        if cmd == "send_tile":
            seatId = msg.getResult('seatId')
            actionId = msg.getResult("action_id")
            if seatId == self.seatId and actionId:
                self._dealSendTile(msg)
                
        if cmd == "send_3tiles":
            self._dealSend3Tiles(msg)     
                     
        if cmd == "play":
            seatId = msg.getResult('seatId')
            ftlog.debug("play,seatId",seatId, 'my seatId', self.seatId)
            if seatId != self.seatId:
                ftlog.debug("deal play:", self.seatId)
                self._dealPlay(msg)
                
        if cmd == "ting":
            self._dealTing(msg)
                
        if cmd == "chi" or cmd == "peng":
            seatId = msg.getResult('seatId')
            ftlog.debug("chipeng,seatId",seatId, 'my seatId', self.seatId)
            if seatId == self.seatId:
                ftlog.debug("deal chipeng:", self.seatId)
                self._dealChiPeng(msg)
                
        if cmd == "gang":
            seatId = msg.getResult('seatId')
            if seatId == self.seatId:
                self._dealGang(msg)
                
        if cmd == "grab_gang":
            seatId = msg.getResult('seatId')
            if seatId == self.seatId:
                self._dealWin(msg)
                
        if cmd == "grabTing":
            seatId = msg.getResult('seatId')
            if seatId == self.seatId:
                self._dealGrabTing(msg)



        if cmd == 'award_certificate' :
                self.stop()
            
        if cmd == 'win'  or cmd == 'third_win':
            if (not self.isMatch) and (self.playMode != "sichuan_xlch") :
                winner_seat_id = msg.getResult('winner_seat_id')
                if winner_seat_id == self.seatId:
                    self._sendLeave()
                    
        if  cmd == 'display_budget':
            if not self.isMatch:
                self._sendLeave()
                
        if  cmd == 'leave':
            seatId = msg.getResult('seatId')
            if seatId == self.seatId:
                ftlog.debug("robot leave", self.userId)
                self.stop()
             
        return
    
    
    def writeMsg(self, msg):
        ftlog.debug("****************write msg:", msg)
        if self.protocol :
            self.protocol.writeMsg(msg)    