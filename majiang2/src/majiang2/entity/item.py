#coding:utf-8
import freetime.util.log as ftlog
from freetime.entity.msg import MsgPack
import poker.util.timestamp as pktimestamp
from poker.protocol import router
from hall.entity import hallitem, datachangenotify

class MajiangItem(object):
    """道具
    """ 
    CREATE_TABLE_CARDS_KIND_ID = 4346
    
    
    @classmethod
    def encodeItemAction(cls, gameId, userBag, item, action, timestamp):
        ret = {
            'action':action.name,
            'name':action.displayName,
        }
        inputParams = action.getInputParams(gameId, userBag, item, timestamp)
        if inputParams:
            ret['params'] = inputParams
        return ret
    
    @classmethod
    def encodeItemActionList(cls, gameId, userBag, item, timestamp):
        ret = []
        actions = userBag.getExecutableActions(item, timestamp)
        for action in actions:
            ret.append(cls.encodeItemAction(gameId, userBag, item, action, timestamp))
        return ret
    
    @classmethod
    def encodeUserItem(cls, gameId, userBag, item, timestamp):
        ret = {
            'id':item.itemId,
            'kindId':item.kindId,
            'name':item.itemKind.displayName,
            'units':item.itemKind.units.displayName,
            'desc':item.itemKind.desc,
            'pic':item.itemKind.pic,
            'count':max(1, item.remaining),
            'actions':cls.encodeItemActionList(gameId, userBag, item, timestamp)
        }
        if item.expiresTime >= 0:
            ret['expires'] = item.expiresTime
        return ret
    
    @classmethod
    def encodeUserItemList(cls, gameId, userBag, timestamp):
        ret = []
        itemList = userBag.getAllItem()
        for item in itemList:
            if item.itemKind.visibleInBag and item.visibleInBag(timestamp):
                ret.append(cls.encodeUserItem(gameId, userBag, item, timestamp))
        return ret
    
    @classmethod
    def queryUserItemTabsV3_7(cls, gameId, userId, userBag=None):
        if userBag is None:
            userBag = hallitem.itemSystem.loadUserAssets(userId).getUserBag()
        timestamp = pktimestamp.getCurrentTimestamp()
        ret = cls.encodeUserItemList(gameId, userBag, timestamp)
        return ret
    
    @classmethod
    def sendItemListResponse(cls, gameId, userId, tabs):
        mo = MsgPack()
        mo.setCmd('user')
        mo.setResult('action', 'majiang_item')
        mo.setResult('gameId', gameId)
        mo.setResult('userId', userId)
        mo.setResult('items', cls.queryUserItemTabsV3_7(gameId, userId))
        router.sendToUser(mo, userId)
    
    @classmethod
    def getUserItemCountByKindId(cls, userId, itemId):
        timestamp = pktimestamp.getCurrentTimestamp()
        assetKindId ='item:%s' % itemId
        count = hallitem.itemSystem.loadUserAssets(userId).balance(9999, assetKindId, timestamp)
        return count
    
    @classmethod
    def consumeItemByKindId(cls, userId, gameId, kindId, count, eventId, roomId=0):
        """道具消费
        """
        itemKind = hallitem.itemSystem.findItemKind(kindId)
        if not itemKind:
            return False
        userBag = hallitem.itemSystem.loadUserAssets(userId).getUserBag()
        timestamp = pktimestamp.getCurrentTimestamp()
        consumeCount = userBag.consumeUnitsCountByKind(gameId
                , itemKind
                , count
                , timestamp
                , eventId
                , roomId)
        datachangenotify.sendDataChangeNotify(gameId, userId, 'item')
        if consumeCount < count:
            return False
        
        return True
    
    @classmethod
    def addUserItemByKindId(cls, userId, gameId, kindId, count, eventId, roomId=0):
        timestamp = pktimestamp.getCurrentTimestamp()
        itemKind = hallitem.itemSystem.findItemKind(kindId)
        if not itemKind:
            ftlog.error('returnBackItem userId:', userId,'kindId:',kindId,'count:',count )
            return False
        
        userBag = hallitem.itemSystem.loadUserAssets(userId).getUserBag()
        items = userBag.addItemUnitsByKind(gameId
                , itemKind
                , count
                , timestamp
                , userId
                , eventId
                , roomId)
        
        datachangenotify.sendDataChangeNotify(gameId, userId, 'item')
        ftlog.debug('addUserItemByKindId userId:', userId, ' gameId:', gameId, 'kindId', kindId, 'count', count, 'items', items)
        return True
    