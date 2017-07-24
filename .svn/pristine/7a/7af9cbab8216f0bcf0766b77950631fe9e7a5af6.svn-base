# -*- coding:utf-8 -*-


from freetime.util import log as ftlog
from poker.entity.dao import gamedata
from majiang2.entity import majiang_conf as configure
from majiang2.entity.majiang_data import MajiangData

def getInitDataKeys(bFilterInvite = False):
    """ gamedata的key
    """
    return MajiangData.getGameDataKeys(bFilterInvite)

def getInitDataValues(bFilterInvite = False):
    """ gamedata的value
    """
    return MajiangData.getGameDataValues(bFilterInvite)


def getGameInfo(userId, clientId, gameId):
    """ 获取玩家的游戏数据
    """
    ukeys = getInitDataKeys()
    uvals = gamedata.getGameAttrs(userId, gameId, ukeys)
    uvals = list(uvals)
    values = getInitDataValues()
    for x in xrange(len(uvals)):
        if uvals[x] == None:
            uvals[x] = values[x]
    gdata = dict(zip(ukeys, uvals))
    return gdata


def createGameData(userId, clientId, gameId):
    """ 创建玩家的游戏数据
    """
    ftlog.debug('userId =', userId, 'clientId =', clientId)
    inviteState = gamedata.getGameAttr(userId, gameId, 'invite_state')
    bFilterInvite = False
    if inviteState > 0:
        bFilterInvite = True
    gdkeys = getInitDataKeys(bFilterInvite)
    ftlog.debug('createGameData  userId =', userId, 'gdkeys =', gdkeys)
    gvals = getInitDataValues(bFilterInvite)
    gamedata.setGameAttrs(userId, gameId, gdkeys, gvals)
    return gdkeys, gvals


def loginGame(userId, gameId, clientId, iscreate, isdayfirst):
    """ 用户登录一个游戏, 游戏自己做一些其他的业务或数据处理
    """
    ftlog.debug('userId =', userId, 'gameId =', gameId, 'clientId =', clientId,
                'iscreate =', iscreate, 'isdayfirst =', isdayfirst)
    if isdayfirst:
        gamedata.setGameAttr(userId, gameId, "day_play_game_count", 0)

def getDaShiFen(userId, clientId, gameId):
    """ 获取玩家大师分信息
    """
    master_point = gamedata.getGameAttr(userId, gameId, 'master_point')
    if not master_point:
        master_point = 0
    master_point_level = 0
    config = configure.get_medal_ui_config(gameId)
    title_pic, level_pic = '', ''
    if config:
        title_pic = config['title']
        level_pic = config['level'] % master_point_level
    return {
            'name':             '麻将',
            'skillscore':       master_point,
            'level':            master_point_level,
            'pic':              level_pic,
            'title':            title_pic,
            'des':              '麻将房间中每次胜利都可获得雀神分，高倍数、高级房间、会员获得的更快！',
            'score':            master_point,
            'grade':            1,
            'premaxscore':      0,
            'curmaxscore':      0,
            }

