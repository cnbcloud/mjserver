# -*- coding=utf-8
'''
Created on 2016年9月23日

@author: zhaol
'''
from majiang2.tile.tile import MTile
from freetime.util import log as ftlog
from majiang2.table.table_config_define import MTDefine

class MMao(object):
    """是否可以杠
    
    例子：
    [[2, 3, 4], [3, 4, 5], [4, 5, 6]]
    """
    
    def __init__(self):
        super(MMao, self).__init__()
        
    @classmethod
    def checkMao(cls, pattern, maoType, maoDanSetting):
        ftlog.debug('MMao.checkMao pattern:', pattern
                    , ' maoType:', maoType
                    , ' maoDanSetting:', maoDanSetting)
        
        values = []
        if maoType & MTDefine.MAO_DAN_DNXBZFB: #乱锚
            if not maoDanSetting & MTDefine.MAO_DAN_DNXBZFB:
                return False
            
            for tile in pattern:
                if MTile.isArrow(tile) or MTile.isFeng(tile):
                    values.append(tile) #取消对相同牌的检查
                else:
                    return False
        elif maoType & MTDefine.MAO_DAN_DNXB:
            if not maoDanSetting & MTDefine.MAO_DAN_DNXB:
                return False
            
            for tile in pattern:
                if MTile.isFeng(tile):
                    if tile not in values:
                        values.append(tile)
                    continue
                else:
                    return False
        elif maoType & MTDefine.MAO_DAN_ZFB:
            if not maoDanSetting & MTDefine.MAO_DAN_ZFB:
                return False
            
            for tile in pattern:
                if MTile.isArrow(tile):
                    if tile not in values:
                        values.append(tile)
                    continue
                else:
                    return False
                
        elif maoType & MTDefine.MAO_DAN_YAO:
            if not maoDanSetting & MTDefine.MAO_DAN_YAO:
                return False
            
            for tile in pattern:
                if MTile.getValue(tile) == 1:
                    if tile not in values:
                        values.append(tile)
                    continue
                else:
                    return False
        
        elif maoType & MTDefine.MAO_DAN_JIU:
            if not maoDanSetting & MTDefine.MAO_DAN_JIU:
                return False
            
            for tile in pattern:
                if MTile.getValue(tile) == 9:
                    if tile not in values:
                        values.append(tile)
                    continue
                else:
                    return False
                
        ftlog.debug('MMao.checkMao pattern:', pattern
                    , ' maoType:', maoType)        
        return len(values) >= 3
        
    @classmethod
    def hasMao(cls, tiles, maoDanSetting, alreadyHave = 0):
        ftlog.debug('MMao.hasMao tiles:', tiles
                    , ' maoDanSetting:', maoDanSetting
                    , ' alreadyHave:', alreadyHave)
        maos = []
        
        if (maoDanSetting & MTDefine.MAO_DAN_DNXBZFB) and (not (alreadyHave & MTDefine.MAO_DAN_DNXBZFB)):
            pattern = []
            values = []
            for tile in tiles:
                if MTile.isFeng(tile) or MTile.isArrow(tile):
                    pattern.append(tile)
                    if tile not in values:
                        values.append(tile)
                        
            if len(values) >= 3:
                luanMao = {}
                luanMao['type'] = MTDefine.MAO_DAN_DNXBZFB
                luanMao['pattern'] = values
                luanMao['name'] = MTDefine.MAO_DAN_DNXBZFB_NAME
                maos.append(luanMao)
                
        if (maoDanSetting & MTDefine.MAO_DAN_DNXB) and \
            (not (alreadyHave & MTDefine.MAO_DAN_DNXB) and \
            (not (maoDanSetting & MTDefine.MAO_DAN_DNXBZFB))):
            pattern = []
            values = []
            for tile in tiles:
                if MTile.isFeng(tile):
                    pattern.append(tile)
                    if tile not in values:
                        values.append(tile)
                        
            if len(values) >= 3:
                fengMao = {}
                fengMao['type'] = MTDefine.MAO_DAN_DNXB
                fengMao['pattern'] = values
                fengMao['name'] = MTDefine.MAO_DAN_DNXB_NAME
                maos.append(fengMao)
                
        if (maoDanSetting & MTDefine.MAO_DAN_ZFB) and \
            (not (alreadyHave & MTDefine.MAO_DAN_ZFB)) and \
            (not (maoDanSetting & MTDefine.MAO_DAN_DNXBZFB)):
            pattern = []
            values = []
            for tile in tiles:
                if MTile.isArrow(tile):
                    pattern.append(tile)
                    if tile not in values:
                        values.append(tile)
                        
            if len(values) >= 3:
                arrowMao = {}
                arrowMao['type'] = MTDefine.MAO_DAN_ZFB
                arrowMao['pattern'] = values
                arrowMao['name'] = MTDefine.MAO_DAN_ZFB_NAME
                maos.append(arrowMao)
                
        if (maoDanSetting & MTDefine.MAO_DAN_YAO) and (not (alreadyHave & MTDefine.MAO_DAN_YAO)):
            pattern = []
            values = []
            for tile in tiles:
                if MTile.getValue(tile) == 1:
                    pattern.append(tile)
                    if tile not in values:
                        values.append(tile)
            if len(values) >= 3:
                yaoMao = {}
                yaoMao['type'] = MTDefine.MAO_DAN_YAO
                yaoMao['pattern'] = values
                yaoMao['name'] = MTDefine.MAO_DAN_YAO_NAME
                maos.append(yaoMao)
                
        if (maoDanSetting & MTDefine.MAO_DAN_JIU) and (not (alreadyHave & MTDefine.MAO_DAN_JIU)):
            pattern = []
            values = []
            for tile in tiles:
                if MTile.getValue(tile) == 9:
                    pattern.append(tile)
                    if tile not in values:
                        values.append(tile)
                        
            if len(values) >= 3:
                jiuMao = {}
                jiuMao['type'] = MTDefine.MAO_DAN_JIU
                jiuMao['pattern'] = values
                jiuMao['name'] = MTDefine.MAO_DAN_JIU_NAME
                maos.append(jiuMao)
        
        ftlog.debug('MMao.hasMao tiles:', tiles
                    , ' maoDanSetting:', maoDanSetting
                    , ' maos:', maos)    
        return maos
    
    @classmethod
    def hasExtendMao(cls, tiles, alreadyHave = 0):
        extendMaos = []
        if alreadyHave & MTDefine.MAO_DAN_DNXBZFB:
            es = []
            for tile in tiles:
                if MTile.isFeng(tile) or MTile.isArrow(tile):
                    es.append(tile)
            if len(es) > 0:
                faNode = {}
                faNode['type'] = MTDefine.MAO_DAN_DNXBZFB
                faNode['extends'] = es
                faNode['name'] = MTDefine.MAO_DAN_DNXBZFB_NAME
                extendMaos.append(faNode)
                
        if alreadyHave & MTDefine.MAO_DAN_DNXB:
            es = []
            for tile in tiles:
                if MTile.isFeng(tile):
                    es.append(tile)
            if len(es) > 0:
                faNode = {}
                faNode['type'] = MTDefine.MAO_DAN_DNXB
                faNode['extends'] = es
                faNode['name'] = MTDefine.MAO_DAN_DNXB_NAME
                extendMaos.append(faNode)
                
        if alreadyHave & MTDefine.MAO_DAN_ZFB:
            es = []
            for tile in tiles:
                if MTile.isArrow(tile):
                    es.append(tile)
            if len(es) > 0:
                faNode = {}
                faNode['type'] = MTDefine.MAO_DAN_ZFB
                faNode['extends'] = es
                faNode['name'] = MTDefine.MAO_DAN_ZFB_NAME
                extendMaos.append(faNode)
                
        if alreadyHave & MTDefine.MAO_DAN_YAO:
            es = []
            for tile in tiles:
                if MTile.getValue(tile) == 1:
                    es.append(tile)
            if len(es) > 0:
                faNode = {}
                faNode['type'] = MTDefine.MAO_DAN_YAO
                faNode['extends'] = es
                faNode['name'] = MTDefine.MAO_DAN_YAO_NAME
                extendMaos.append(faNode)
                
        if alreadyHave & MTDefine.MAO_DAN_JIU:
            es = []
            for tile in tiles:
                if MTile.getValue(tile) == 9:
                    es.append(tile)
            if len(es) > 0:
                faNode = {}
                faNode['type'] = MTDefine.MAO_DAN_JIU
                faNode['extends'] = es
                faNode['name'] = MTDefine.MAO_DAN_JIU_NAME
                extendMaos.append(faNode)
                
        return extendMaos

    @classmethod
    def checkPengMao(cls,tile,maoDanSetting,maoTiles):

        ftlog.debug('MMao.checkChiMao tile:', tile, 'maoDanSetting: ', maoDanSetting,'maoTiles: ',maoTiles)
        if maoDanSetting & MTDefine.MAO_DAN_DNXBZFB: #乱锚情况下
            if len(maoTiles) > 0:#已经放过锚
                if MTile.isArrow(tile) or MTile.isFeng(tile):#
                    return False
        else:
            if len(maoTiles) > 0:#已经放过锚
                for mao in maoTiles:
                    ftlog.debug('MMao.checkChiMao type:', mao['type'])
                    if MTile.isArrow(tile) and mao['type'] == 1:#已放箭牌
                        return False
                    if MTile.isFeng(tile) and mao['type'] == 2:#已放风牌
                        return False

        return True



    
def hasMaoDemo():
    tiles = [2,2,2,3,3,3,4,4,4,22,31,32,33,34]
    result = MMao.hasMao(tiles, 6, 0)
    ftlog.debug( result )
    
def checkMaoDemo():
    result = MMao.checkMao([33,35,36], 4, 4)
    print 'result:', result
    
if __name__ == "__main__":
    # hasMaoDemo()
    checkMaoDemo()