# -*- coding=utf-8
'''
Created on 2016年9月23日

@author: zhaol
'''
from majiang2.tile.tile import MTile
from freetime.util import log as ftlog
from majiang2.player.hand.hand import MHand
import copy

class MWin(object):
    """公共的判断和牌的AI
    """
    
    def __init__(self):
        super(MWin, self).__init__()
        
    @classmethod
    def isLuanFengyise(cls, tiles, colorCount):
        """
         风一色
        """
        ftlog.debug('MWin.isLuanFengyise tiles:', tiles
                    , ' colorCount:', colorCount)
        if colorCount > 1:
            return False, []
        
        for tile in tiles:
            if (not MTile.isFeng(tile)) and (not MTile.isArrow(tile)):
                return False, []
            
        ftlog.debug('MWin.isLuanFengyise ok, pattern:', tiles)
        return True, [tiles]
      
    @classmethod  
    def isQiDui(cls, tiles, baoTiles = []):
        '''
        判断是否是七对
        现在加入宝牌处理判断
        
        特别注意，baoTiles不是癞子牌，是宝牌，穷和玩法特有的宝牌，上听后生效。
        上听后摸到一张就和牌
        baoTiles可以是癞子牌，但传进来的必须是手牌中的赖子数组，如手牌中有2个7是赖子 baoTiles=[7,7]
        '''
        
        #ftlog.debug('MWin.isQiDui tiles:', tiles, ' baoTiles:', baoTiles)
        tileArr = MTile.changeTilesToValueArr(tiles)
        #ftlog.debug('MWin.isQiDui tileArr:', tileArr)
        
        for magicTile in baoTiles:
            tileArr[magicTile] -= 1
                
        allMagicTiles = copy.deepcopy(baoTiles)
        resultArr = []
        duiCount = 0
        for tileIndex in range(0, len(tileArr)):
            if tileArr[tileIndex] == 0:
                continue
            
            #单张情况
            elif tileArr[tileIndex] == 1:
                if len(allMagicTiles) >= 1:
                    duiCount += 1
                    resultArr.append([tileIndex, allMagicTiles.pop(0)])
            #三张情况        
            elif tileArr[tileIndex] == 3:
                if len(allMagicTiles) >= 1:
                    duiCount += 2
                    resultArr.append([tileIndex, tileIndex])
                    resultArr.append([tileIndex, allMagicTiles.pop(0)])
            #一对
            elif tileArr[tileIndex] == 2:
                resultArr.append([tileIndex, tileIndex])
                duiCount += 1
            #两对    
            elif tileArr[tileIndex] == 4:
                resultArr.append([tileIndex, tileIndex])
                resultArr.append([tileIndex, tileIndex])
                duiCount += 2
                
        for index in range(len(allMagicTiles)):
            if ((index + 1) % 2) == 0:
                resultArr.append([allMagicTiles[index - 1], allMagicTiles[index]])
                duiCount += 1
        
        ftlog.info('MWin.isQiDui, tiles:', tiles
                   , ' baoTiles:', baoTiles
                   , ' duiCount:', duiCount
                   , ' resultArr',resultArr)
             
        if (duiCount == 7) and (len(tiles) == 14):
            return True, resultArr
        elif (duiCount == 6) and (len(tiles) == 12):
            return True, resultArr
        else:
            return False, []


    @classmethod
    def isQuanJiang(cls, tiles):
        '''
        判断是否全将
        '''
        jiang258 = [2,5,8,12,15,18,22,25,28]

        handTiles = tiles[MHand.TYPE_HAND]
        chiTiles  = tiles[MHand.TYPE_CHI]
        pengTiles = tiles[MHand.TYPE_PENG]#[[4, 4, 4]]
        gangTiles = tiles[MHand.TYPE_GANG] #'gang': [{'pattern': [31, 31, 31, 31], 'style': True, 'actionID': 11}]


        for tile in handTiles:
            if not tile in jiang258:
                return False,[]
        if len(chiTiles) > 0:
                return False,[]
        for tilePatten in pengTiles:
            if not tilePatten[0] in jiang258:
                return False,[]
        for tile in gangTiles:
            if not tile['pattern'][0] in jiang258:
                return False,[]

        return True, [handTiles]

    @classmethod
    def isDadiaoche(self,tiles):
        """
        大吊车：胡牌时自己手上只有一张牌，且胡的是二五八
        """
        handTile = tiles[MHand.TYPE_HAND]
        huTile = tiles[MHand.TYPE_HU][0]
        handTile.extend(tiles[MHand.TYPE_HU])
        if len(handTile) == 2 and huTile < MTile.TILE_DONG_FENG and ( MTile.getValue(huTile) == 2 or MTile.getValue(huTile) == 5 or MTile.getValue(huTile) == 8):
            return True,[handTile]

        return False,[]

    @classmethod
    def isFlowerHu(self, tiles):
        """
        花胡：摸到花牌8张全
        """
        handTile = tiles[MHand.TYPE_HAND]
        flowerTile = tiles[MHand.TYPE_SHOW_FLOWERS]

        flower_count = 0
        for tile in handTile:
            if MTile.isFlower(tile):
                flower_count += 1
        if flower_count + len(flowerTile) == 8:
            return True, [handTile]

        return False, []

    @classmethod
    def isMagicHu(self,tiles,magicTile,tile):
        """
        三金胡：摸到3张赖子
        """
        handTiles = tiles[MHand.TYPE_HAND]
        #三金倒
        magicTileCount = 0
        for oneTile in handTiles:
	    if oneTile == magicTile:
                magicTileCount = magicTileCount + 1
	ftlog.debug("isMagicHu ===", handTiles,magicTileCount)
        if magicTileCount ==3:
            return True,[handTiles] 
        return False, []

    @classmethod
    def is13BuKao(cls, handTiles):
        '''
        判断是否十三不靠
        '''

        #有五张不同的风牌或箭牌
        fengTiles =[]
        for index in range(0,len(handTiles)):
            if (MTile.isFeng(handTiles[index]) or MTile.isArrow(handTiles[index])):
                if (handTiles[index] not in fengTiles):
                    fengTiles.append(handTiles[index])
                else:
                    return False, []

        if len(fengTiles) > 0:
            for tile in fengTiles:
                handTiles.remove(tile)
        #剩余9张牌
        if not (len(fengTiles) == 5 and len(handTiles) == 9):
            return False,[]
        #排序
        handTiles.sort()

        ftlog.debug("handTiles ===", handTiles)

        #根据花色分组
        groups =[[] for _ in xrange(3)]
        for tile in handTiles:
            if ((tile % 10) == 0) or (tile >= 30):
                continue
                
            index = tile / 10
            groups[index].append(tile)

        ftlog.debug("groups ===", groups)

        # 每组3张牌
        types = [1,2,3]
        for grp in groups:
            if len(grp) != 3:
                return False,[]
            
            v = grp[0]%10
            if not (grp[1]%10 == (v+3) and grp[2]%10 == (v+6)):
                return False,[]
            
            if v in types:
                types.remove(v)
            else:
                return False, []

        ftlog.debug("handTile ===",handTiles)

        handTiles.extend(fengTiles)

        return True, [handTiles]

    @classmethod
    def is13BuKaoWithOutLimit(cls, handTiles, hanMagics=[]):
        '''
        判断是否十三不靠 只要手牌没有靠着的就行 没有其他限制
        hanMagics是手牌中的赖子数组，如手牌中有2个7是赖子 baoTiles=[7,7]
        '''
        newHandTiles = copy.deepcopy(handTiles)
        # 有五张不同的风牌或箭牌
        fengTiles = []
        for index in range(0, len(newHandTiles)):
            if (MTile.isFeng(newHandTiles[index]) or MTile.isArrow(newHandTiles[index])):
                if (newHandTiles[index] not in fengTiles):
                    fengTiles.append(newHandTiles[index])
                else:
                    return False, []

        if len(fengTiles) > 0:
            for tile in fengTiles:
                newHandTiles.remove(tile)

        # 排序
        newHandTiles.sort()
        for magic in hanMagics:
            if magic in newHandTiles:
                newHandTiles.remove(magic)

        # 根据花色分组
        groups = [[] for _ in xrange(3)]
        for tile in newHandTiles:
            if ((tile % 10) == 0) or (tile >= 30):
                continue

            index = tile / 10
            groups[index].append(tile)

        # 每组3张牌
        buKaoCount = 0
        for grp in groups:
            if len(grp) == 0:
                continue

            v = grp[0] % 10
            if len(grp) == 2 and ((grp[1] % 10 == (v + 3) or grp[1] % 10 == (v + 6))):
                buKaoCount += len(grp)
            elif len(grp) == 3 and ((grp[1] % 10 == (v + 3) and grp[2] % 10 == (v + 6))):
                buKaoCount += len(grp)
            elif len(grp) == 1:
                buKaoCount += len(grp)

        ftlog.debug("buKaoCount ===", buKaoCount)
        ftlog.debug("handMagics ===", len(hanMagics))
        ftlog.debug("fengTiles ===", len(fengTiles))
        if buKaoCount + len(hanMagics) + len(fengTiles) != 14:
            return False, []

        return True, [handTiles]

    @classmethod
    def isHuWishSpecialJiang(cls, tiles, jiangPattern, magics = []):
        """
        指定将牌类型判断是否胡牌
            暂时不考虑将牌
        """
        # 先移除将牌。无指定将牌，判和失败
        tileArr = MTile.changeTilesToValueArr(tiles)
        jiangTile = jiangPattern[0]
        if tileArr[jiangTile] < 2:
            return False, []
        # 移除将牌
        tileArr[jiangTile] -= 2
        
        # 计算剩下的结果
        resultArr = []
        resultArr.append(jiangPattern)
        tileTypes = [MTile.TILE_WAN, MTile.TILE_TONG, MTile.TILE_TIAO, MTile.TILE_FENG]
        winResult = False
        for tileType in tileTypes:
            winResult, _, _tArr, _rArr, _mArr = cls.isHuWithMagic(tileArr, resultArr, magics, True, tileType,False)
            if not winResult:
                return False, []
            else:
                tileArr = copy.deepcopy(_tArr)
                resultArr = copy.deepcopy(_rArr)
        
        return winResult, resultArr
       
    @classmethod
    def isHu(cls, tiles, magicTiles = [], allowZFB = False):
        """胡牌判断，只判断手牌，杠牌，吃牌，碰牌不在内
           杠牌、吃牌、碰牌已成型，不用另外计算
           1）肯定包含将牌
           2）剩下的牌里不会有暗杠牌
           3）杠牌/吃牌/碰牌是已经成型的牌，按成型的样式计算积分，不再重新计算
        返回值：
            True - 和了
            False - 没和
            
        特别说明：
            这个API是判断是否胡牌，并未遍历所有的胡牌解
            依据返回的pattern去判断番型是有问题的。
            具体的番型要用具体的番型API去判断。
        """
        tileArr = MTile.changeTilesToValueArr(tiles)
        magicArr = []
        for magicTile in magicTiles:
            magicArr.extend([magicTile for _ in range(tileArr[magicTile])])
            tileArr[magicTile] = 0
            
        resultArr = []
        tileTypes = [MTile.TILE_WAN, MTile.TILE_TONG, MTile.TILE_TIAO, MTile.TILE_FENG]
        hasJiang = False
        winResult = False
        for tileType in tileTypes:
            winResult, hasJiang, _tArr, _rArr, _mArr = cls.isHuWithMagic(tileArr, resultArr, magicArr, hasJiang, tileType,allowZFB)
            if not winResult:
                return False, []
            else:
                tileArr = copy.deepcopy(_tArr)
                resultArr = copy.deepcopy(_rArr)
                magicArr = copy.deepcopy(_mArr)
        if winResult and not hasJiang and len(magicArr) >= 2:
            hasJiang = True
        return hasJiang and winResult, resultArr

    
    @classmethod
    def isShisanyao(cls, tiles, magicTiles=[]):
        """
         十三幺判断
        """
        yao13Arr = [1, 9, 11, 19, 21, 29, 31, 32, 33, 34, 35, 36, 37]
        yaoCount = [0 for _ in range(len(yao13Arr))]

        for tile in tiles:
            if tile not in yao13Arr:
                return False,[]
            else:
                for index in range(len(yao13Arr)):
                    if tile == yao13Arr[index]:
                        yaoCount[index] += 1

        for count in yaoCount:
            if count == 0 or count > 2:
                return False,[]

        return True, [tiles]

    @classmethod
    def isHuWithMagic(cls, tileArr, resultArr, magicArr, hasJiang, tileType, allowZFB):
        # 不能一次性把所有癞子都给过去，要一个一个的给，使用最少的癞子打成胡牌效果。
        # 用掉太多癞子，会导致漏和
        _hasJiang = hasJiang
        _tileArr = copy.deepcopy(tileArr)
        _resultArr = copy.deepcopy(resultArr)
        for magicLength in range(len(magicArr) + 1):
            newMagicArr = magicArr[0:magicLength]
            _newMagicArr = copy.deepcopy(newMagicArr)
            _resultType, _hasJiang = cls.isBu(_tileArr, _resultArr, newMagicArr, tileType, _hasJiang, allowZFB)
            #ftlog.debug('tileType:', tileType, ' resultType:', resultType, ' hasJiang:', hasJiang)
            if not _resultType:
                continue
            else: 
                magicArr = magicArr[len(_newMagicArr):]
                magicArr.extend(newMagicArr)
                return _resultType, _hasJiang, _tileArr, _resultArr, magicArr
            
        return False, hasJiang, None, None, None
    
    @classmethod
    def isBu(cls, tileArr, resultArr, magicArr, tileType, hasJiang, allowZFB):
        """判断某个花色是否是三朴，缺的牌从癞子中获取，如果没有癞子牌了，也形不成三朴，和牌失败"""
        if 0 == cls.getCardNumByType(tileArr, tileType):
            # 这个花色没有牌
            return True, hasJiang
        
        #ftlog.debug('check card:', MTile.traverseTile(tileType))
        for tileIndex in MTile.traverseTile(tileType):
            if tileArr[tileIndex] == 0:
                continue
            
            if tileArr[tileIndex] >= 3:
                # 刻，没有占用癞子
                tileArr[tileIndex] -= 3
                resultTmp, hasJiang = cls.isBu(tileArr, resultArr, magicArr, tileType, hasJiang, allowZFB)
                if resultTmp:
                    resultArr.append([tileIndex, tileIndex, tileIndex])
                    return True, hasJiang
                # 还原手牌，继续判断
                tileArr[tileIndex] += 3
                
            if (tileArr[tileIndex] == 2) and (len(magicArr) >= 1):
                # 对子，尝试加一张癞子组成刻
                tileArr[tileIndex] -= 2
                mTile = magicArr.pop(-1)
#                 ftlog.debug('[11M]magicArr pop:', mTile, ' after pop:', magicArr)
                resultTmp, hasJiang = cls.isBu(tileArr, resultArr, magicArr, tileType, hasJiang,allowZFB)
                if resultTmp:
                    resultArr.append([tileIndex, tileIndex, mTile])
                    return True, hasJiang
                    
                # 还原手牌，继续判断
                tileArr[tileIndex] += 2
                magicArr.append(mTile)
#                 ftlog.debug('[11M]magicArr push:', mTile, ' after push:', magicArr)
                
            if (tileArr[tileIndex] == 1) and (len(magicArr) >= 2):
                # 单张，尝试加两张癞子组成刻
                tileArr[tileIndex] -= 1
                mTile1 = magicArr.pop(-1)
                mTile2 = magicArr.pop(-1)
#                 ftlog.debug('[1MM] magicArr pop1:', mTile1, ' pop2:', mTile2, ' after pop:', magicArr)
                resultTmp, hasJiang = cls.isBu(tileArr, resultArr, magicArr, tileType, hasJiang,allowZFB)
                if resultTmp:
                    resultArr.append([tileIndex, mTile1, mTile2])
                    return True, hasJiang
                # 还原手牌，继续判断
                tileArr[tileIndex] += 1
                magicArr.append(mTile1)
                magicArr.append(mTile2)
#                 ftlog.debug('[1MM] magicArr push1:', mTile1, ' push2:', mTile2, ' after push:', magicArr)
                
            if not hasJiang and \
                tileArr[tileIndex] > 0 and \
                (tileArr[tileIndex] + len(magicArr) >= 2):
                tileArr[tileIndex] -= 1
                isMagicJiang = False
                jiangTile = tileIndex
                if tileArr[tileIndex] > 0:
                    tileArr[tileIndex] -= 1
                else:
                    isMagicJiang = True
                    jiangTile = magicArr.pop(-1)
#                     ftlog.debug('[1M] magicArr pop:', jiangTile, ' after pop:', magicArr)
                
                oldJiang = hasJiang
                resultTmp, hasJiang = cls.isBu(tileArr, resultArr, magicArr, tileType, True,allowZFB)
                if resultTmp:
                    resultArr.append([tileIndex, jiangTile])
                    hasJiang = True
                    return True, hasJiang
                else:
                    # 还原将牌标记
                    hasJiang = oldJiang
                     
                # 还原手牌
                tileArr[tileIndex] += 1
                if isMagicJiang:
                    magicArr.append(jiangTile)
#                     ftlog.debug('[1M] magicArr append:', jiangTile, ' after append:', magicArr)
                else:
                    tileArr[tileIndex] += 1
            
            #是否允许中发白作为顺牌，暂时没有考虑赖子的情况，后续可以修改添加
            if not allowZFB:    
                if tileIndex >= MTile.TILE_DONG_FENG:
                    # 风箭牌不能组成顺
                    return False, hasJiang
            else:
                if tileIndex == MTile.TILE_HONG_ZHONG:
                    if tileArr[tileIndex] > 0 and tileArr[tileIndex+1] > 0 and tileArr[tileIndex+2] > 0:
                        pattern = [tileIndex, tileIndex+1, tileIndex+2]
                        tileArr[tileIndex] -= 1
                        tileArr[tileIndex+1] -= 1
                        tileArr[tileIndex+2] -= 1
                                  
                        resultTmp, hasJiang = cls.isBu(tileArr, resultArr, magicArr, tileType, hasJiang,allowZFB)
                        if resultTmp:
                            resultArr.append(pattern)
                            return True, hasJiang
                elif tileIndex >= MTile.TILE_DONG_FENG:
                    return False, hasJiang

            # 提取顺牌组合
            if tileArr[tileIndex] > 0 and tileType != MTile.TILE_FENG:
                # 测试顺子 0 1 2
                if MTile.getValue(tileIndex) <= 7:
                    tile0 = tileIndex
                    needMagic = 0
                    is1Magic = False
                    is2Magic = False
                    if tileArr[tileIndex + 1] == 0:
                        needMagic += 1
                        is1Magic = True
                    if tileArr[tileIndex + 2] == 0:
                        needMagic += 1
                        is2Magic = True
                     
                    if needMagic <= len(magicArr):    
                        pattern = [tile0, None, None]
                        tileArr[tileIndex] -= 1
                        
                        if is1Magic:
                            pattern[1] = (magicArr.pop(-1))
                        else:
                            pattern[1] = (tileIndex + 1)
                            tileArr[tileIndex + 1] -= 1
                            
                        if is2Magic:
                            pattern[2] = (magicArr.pop(-1))
                        else:
                            pattern[2] = (tileIndex + 2)
                            tileArr[tileIndex + 2] -= 1
                            
#                         if is1Magic and is2Magic:
#                             ftlog.debug('[1MM] magicArr pop1:', pattern[1], ' pop2:', pattern[2], ' after pop:', magicArr)
#                         elif is1Magic:
#                             ftlog.debug('[1M3] magicArr pop1:', pattern[1], ' after pop:', magicArr)
#                         elif is2Magic:
#                             ftlog.debug('[12M] magicArr pop2:', pattern[2], ' after pop:', magicArr)
                            
                        resultTmp, hasJiang = cls.isBu(tileArr, resultArr, magicArr, tileType, hasJiang,allowZFB)
                        if resultTmp:
                            resultArr.append(pattern)
                            return True, hasJiang
                        
                        # 还原手牌
                        tileArr[tileIndex] += 1
                        if is1Magic:
                            magicArr.append(pattern[1])
                        else:
                            tileArr[tileIndex + 1] += 1
                        
                        if is2Magic:
                            magicArr.append(pattern[2])
                        else:
                            tileArr[tileIndex + 2] += 1
                        
#                         if is1Magic and is2Magic:
#                             ftlog.debug('[1MM] magicArr append1:', pattern[1], ' append2:', pattern[2], ' after append:', magicArr)
#                         elif is1Magic:
#                             ftlog.debug('[1M3] magicArr append1:', pattern[1], ' after append:', magicArr)
#                         elif is2Magic:
#                             ftlog.debug('[12M] magicArr append2:', pattern[2], ' after append:', magicArr)
                    
                # 测试顺子 -1 0 1
                if MTile.getValue(tileIndex) <= 8 and MTile.getValue(tileIndex) >= 2:
                    tile1 = tileIndex
                    needMagic = 0
                    is0Magic = False
                    is2Magic = False
                    if tileArr[tileIndex - 1] == 0:
                        needMagic += 1
                        is0Magic = True
                    if tileArr[tileIndex + 1] == 0:
                        needMagic += 1
                        is2Magic = True
                        
                    if needMagic <= len(magicArr):    
                        pattern = [None, tile1, None]
                        tileArr[tileIndex] -= 1
                        
                        if is0Magic:
                            pattern[0] = (magicArr.pop(-1))
                        else:
                            pattern[0] = (tileIndex - 1)
                            tileArr[tileIndex - 1] -= 1
                            
                        if is2Magic:
                            pattern[2] = (magicArr.pop(-1))
                        else:
			    #猜测有问题，导致pattern 长度为4 包含None
                            #pattern.append(tileIndex + 1)
                            pattern[2] = (tileIndex + 1)
			    tileArr[tileIndex + 1] -= 1
                            
#                         if is0Magic and is2Magic:
#                             ftlog.debug('[M1M] magicArr pop0:', pattern[0], ' pop2:', pattern[2], ' after pop:', magicArr)
#                         elif is0Magic:
#                             ftlog.debug('[M23] magicArr pop1:', pattern[0], ' after pop:', magicArr)
#                         elif is2Magic:
#                             ftlog.debug('[12M] magicArr pop2:', pattern[2], ' after pop:', magicArr)
                            
                        resultTmp, hasJiang = cls.isBu(tileArr, resultArr, magicArr, tileType, hasJiang,allowZFB)
                        if resultTmp:
                            resultArr.append(pattern)
                            return True, hasJiang
                        
                        # 还原手牌
                        tileArr[tileIndex] += 1
                        if is0Magic:
                            magicArr.append(pattern[0])
                        else:
                            tileArr[tileIndex - 1] += 1
                        
                        if is2Magic:
                            magicArr.append(pattern[2])
                        else:
                            tileArr[tileIndex + 1] += 1
                            
#                         if is0Magic and is2Magic:
#                             ftlog.debug('[M1M] magicArr append0:', pattern[0], ' append2:', pattern[2], ' after append:', magicArr)
#                         elif is0Magic:
#                             ftlog.debug('[M23] magicArr append0:', pattern[0], ' after append:', magicArr)
#                         elif is2Magic:
#                             ftlog.debug('[12M] magicArr append2:', pattern[2], ' after append:', magicArr)  
                
                # 测试顺子 -2 -1 0
                if MTile.getValue(tileIndex) >= 3:
                    tile2 = tileIndex
                    needMagic = 0
                    is0Magic = False
                    is1Magic = False
                    if tileArr[tileIndex - 2] == 0:
                        needMagic += 1
                        is0Magic = True
                    if tileArr[tileIndex - 1] == 0:
                        needMagic += 1
                        is1Magic = True
                     
                    if needMagic <= len(magicArr):    
                        pattern = [None, None, tile2]
                        tileArr[tileIndex] -= 1
                        
                        if is0Magic:
                            pattern[0] = (magicArr.pop(-1))
                        else:
                            pattern[0] = (tileIndex - 2)
                            tileArr[tileIndex - 2] -= 1
                            
                        if is1Magic:
                            pattern[1] = (magicArr.pop(-1))
                        else:
                            pattern[1] = (tileIndex - 1)
                            tileArr[tileIndex - 1] -= 1
                            
#                         if is0Magic and is1Magic:
#                             ftlog.debug('[MM3] magicArr pop0:', pattern[0], ' pop1:', pattern[1], ' after pop:', magicArr)
#                         elif is0Magic:
#                             ftlog.debug('[M23] magicArr pop0:', pattern[0], ' after pop:', magicArr)
#                         elif is1Magic:
#                             ftlog.debug('[1M3] magicArr pop1:', pattern[1], ' after pop:', magicArr)
                            
                        resultTmp, hasJiang = cls.isBu(tileArr, resultArr, magicArr, tileType, hasJiang,allowZFB)
                        if resultTmp:
                            resultArr.append(pattern)
                            return True, hasJiang
                    
                        # 还原手牌
                        tileArr[tileIndex] += 1
                        if is0Magic:
                            magicArr.append(pattern[0])
                        else:
                            tileArr[tileIndex - 2] += 1
                        
                        if is1Magic:
                            magicArr.append(pattern[1])
                        else:
                            tileArr[tileIndex - 1] += 1
                            
#                         if is0Magic and is1Magic:
#                             ftlog.debug('[MM3] magicArr append0:', pattern[0], ' append1:', pattern[1], ' after append:', magicArr)
#                         elif is0Magic:
#                             ftlog.debug('[M23] magicArr append0:', pattern[0], ' after append:', magicArr)
#                         elif is1Magic:
#                             ftlog.debug('[1M3] magicArr append1:', pattern[1], ' after append:', magicArr)
        
        # 无和牌可能
        return False, hasJiang
        
    @classmethod
    def _isHu(cls, tileArr, hasJiang, resultArr):
        """判断是否和牌
        参数
            tileArr： 整理好的手牌
            hasJiang： 是否有将牌
            resultArr： 结果牌
        """
        # 带判断数组中没有剩余牌了，和了
        _num = cls.getCardNum(tileArr)
        
        if 0 == _num:
            # 一定有将牌
            return hasJiang
        
        for tile in range(40):
            # 3张组合，刻
            if tileArr[tile] >= 3:
                # 去掉这三张牌
                tileArr[tile] -= 3
                # 判断剩下的牌
                if cls._isHu(tileArr, hasJiang, resultArr):
                    # 存储结果
                    pattern = [tile, tile, tile]
                    resultArr.append(pattern)
                    return True
                # 还原，继续判断
                tileArr[tile] += 3
                
            # 2张组合，对
            if tileArr[tile] >= 2 and not hasJiang:
                hasJiang = True
                tileArr[tile] -= 2
                if cls._isHu(tileArr, hasJiang, resultArr):
                    # 保存结果
                    pattern = [tile, tile]
                    resultArr.append(pattern)
                    return True
                # 还原
                hasJiang = False
                tileArr[tile] += 2
             
            # 风牌不会组成顺，不和
            if tile > 30 and hasJiang:
                """已经有将牌，只考虑顺"""
                return False
            
            # 提取顺牌组合
            if (tile % 10 ) <= 7 \
                and tileArr[tile] > 0 \
                and tileArr[tile + 1] > 0 \
                and tileArr[tile + 2] > 0:
                tileArr[tile] -= 1
                tileArr[tile + 1] -= 1
                tileArr[tile + 2] -= 1
                
                if cls._isHu(tileArr, hasJiang, resultArr):
                    # 保存结果
                    pattern = [tile, tile+1, tile+2]
                    resultArr.append(pattern)
                    return True
                # 还原
                tileArr[tile] += 1
                tileArr[tile + 1] += 1
                tileArr[tile + 2] += 1
        
        # 无法和牌
        return  False
    
    @classmethod
    def getCardNumByType(cls, tileArr, tileType):
        num = 0    
        for tile in MTile.traverseTile(tileType):
            num += tileArr[tile]
        return num
    
    @classmethod
    def getCardNum(cls, tileArr):
        num = 0
        for tile in tileArr:
            num += tile
        return num
    
def test1():
    tiles = [3, 3]
    return  MWin.isHu(tiles, [21])

def test2():
    tiles = [5,6,6,13,14,15,21,21]
    return MWin.isHu(tiles, [21])
    
def testqidui():
    tiles = [5,5,6,6,7,7,8,8,13,13,15,15,21,22]
    return MWin.isQiDui(tiles,22,False, [22])

def testqidui1():
    tiles = [5,5,6,6,7,7,8,8,13,13,15,15,21,22]
    return MWin.isQiDui(tiles, 22,False, [21,23])

def testqidui2():
    tiles = [5,5,6,6,7,7,8,8,13,13,14,15,21,22]
    return MWin.isQiDui(tiles, 22,False, [14,15])

def testqidui3():
    tiles = [5,5,6,6,7,7,8,8,13,13,14,15,21,22]
    return MWin.isQiDui(tiles, 22,False, [14,15,21,22])

def testqidui4():
    tiles = [5,5,6,6,7,7,8,8,13,13,14,15,21,22]
    return MWin.isQiDui(tiles, 22,False, [14,24,25,26])

def testqidui5():
    tiles = [5,5,6,6,7,7,8,8,13,13]
    return MWin.isQiDui(tiles, 13,False, [13,13,8,8])

def testQiDui6():
    tiles = [12, 12, 14, 14, 17, 17, 17, 22, 22, 23, 29, 29]
    return MWin.isQiDui(tiles, [17])

def testshisanyao():
    tiles = [1, 9, 11, 19, 19,21, 29, 31, 32, 33, 34, 35, 36, 37]
    return MWin.isShisanyao(tiles)

def test13bukao():
    tiles = [[4, 7, 12, 15, 18, 23, 26, 29, 31, 32, 33, 33, 34, 35],[],[],[],[]]
    return MWin.is13BuKao(tiles[MHand.TYPE_HAND])

def testQuanjiang():
    tiles = [[2, 2, 5, 2, 5,8, 22, 12, 5, 25, 28, 18, 18, 18],[],[],[],[]]
    return MWin.isQuanJiang(tiles)

def testDadiaoche():
    tiles = [[2],[],[],[],[],[2]]
    return MWin.isDadiaoche(tiles)

def testFlowerHu():
    tiles = [[2,3,23,12,43,41,23,44,32,35,26,28,19],[],[],[],[],[],[],[42,45,46,47,48]]
    return MWin.isFlowerHu(tiles)

def testZFB():
    tiles = [1,1,1,2,2,2,3,3,3,4,4,35,36,37]
    return MWin.isHu(tiles)

def testMagci():
    tiles = [12,12,13,14,14,25,25,25,26,27,28,28,28,1]
    magics = [1]
    return MWin.isHu(tiles, magics)

if __name__ == "__main__":
    #result, pattern = test1()
    #ftlog.debug('result:', result, ' pattern:', pattern)
# 
#     result, pattern = testqidui1()
#     ftlog.debug('result:', result)
#     
#     result, pattern = testqidui2()
#     ftlog.debug('result:', result)
#     
#     result, pattern = testqidui3()
#     ftlog.debug('result:', result)
#     
#     result, pattern = testqidui4()
#     ftlog.debug('result:', result)
#     
#     result, pattern = testqidui5()
#     ftlog.debug('result:', result)
#     result, pattern = testQiDui6()
#     ftlog.debug('result:', result
#                 , ' pattern:', pattern)
#     result, pattern = testFlowerHu()
#     ftlog.debug('result:', result , pattern )
    
    result, pattern = test13bukao()
    ftlog.debug('result:', result , pattern )
