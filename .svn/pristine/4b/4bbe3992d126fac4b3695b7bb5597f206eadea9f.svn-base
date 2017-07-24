# -*- coding:utf-8 -*-

import freetime.util.log as ftlog
from freetime.entity.msg import MsgPack
from hall.entity import hallstore
from hall.entity.todotask import TodoTaskShowInfo, TodoTaskHelper, TodoTaskQuickStart, TodoTaskOrderShow, TodoTaskTriggerEvent
from hall.entity.todotask import TodoTaskPayOrder, TodoTaskEnterGameNew
from poker.protocol import router
from poker.entity.dao import onlinedata, sessiondata
from poker.util import strutil
from poker.entity.game.tables.table_player import TYPlayer

def sendTodoTaskInviteFriends(userId, gameId, invite_uids, play_mode, roomId, tableId, info_str, purl):
    """ 邀请好友来牌桌
    @param        name        发送邀请的用户名
    @param        invite_uids 被邀请的玩家uid列表
    @param        table       牌桌对象
    """
    ftlog.debug('userId =', userId, 'roomId =', roomId, 'tableId =', tableId,
                'invite_uids =', invite_uids, 'info_str =', info_str)
    if not TYPlayer.isHuman(userId):
        ftlog.debug('robot is not supported!')
        return

    for uid in invite_uids:
        last_gameId = onlinedata.getLastGameId(uid)
        if last_gameId == gameId:     # 如果玩家在麻将里
            sendFriendInviteTodotask(uid, userId, gameId, play_mode, roomId, tableId, info_str, purl)
        elif last_gameId == 9999:                       # 如果玩家在大厅主界面
            sendFriendInviteEnterGameTodotask(uid, gameId, play_mode, roomId, tableId, info_str)
        else:                                           # 在其它游戏里，直接忽略
            ftlog.debug('last_gameId is not 7 or 9999', 'last_gameId =', last_gameId)
            return
        from majiang2.entity import util
        util.sendPrivateMessage(uid, info_str)

def makeLeadLedTodoTask(params):
    """ LED的todotask按钮
    """
    trigger_event = TodoTaskTriggerEvent()
    trigger_event.updateParams(params)
    return [trigger_event.toDict()]


def sendFriendInviteEnterGameTodotask(userId, gameId, play_mode, roomId, tableId, info_str):
    """ 构造从大厅主界面进桌子的todotask
    """
    enter_param = {
                 'type':         'quickstart',
                 'pluginParams': {
                     'play_mode':       play_mode,
                     'roomId':          roomId,
                     'tableId':         tableId,
                     'gameType':        9   # TODO: 写死了9，因为目前只有贵宾桌使用到了这个功能
                 }
            }
    todotask = TodoTaskEnterGameNew(gameId, enter_param)
    show_info_ = TodoTaskShowInfo(info_str, True)
    show_info_.setSubCmd(todotask)
    msg = TodoTaskHelper.makeTodoTaskMsg(gameId, userId, show_info_)
    router.sendToUser(msg, userId)


def sendFriendInviteTodotask(userId, invite_uid, gameId, play_mode, roomId, tableId, info_str, purl):
    """ 推送牌桌好友邀请的todotask
    * 版本 3.732 之后，改为麻将自己的todotask
    """
    todotask = TodoTaskQuickStart(gameId, roomId, tableId)
    todotask.setParam('play_mode', play_mode)
    client_ver = sessiondata.getClientIdVer(userId)

    if client_ver < 3.732:
        show_info_ = TodoTaskShowInfo(info_str, True)
        show_info_.setSubCmd(todotask)
        msg = TodoTaskHelper.makeTodoTaskMsg(gameId, userId, show_info_)
        router.sendToUser(msg, userId)
    else:
        task = {
                'action':       'pop_wnd_invite',
                'params':       {
                                 'tasks':       [todotask.toDict()],
                                 'invite_uid':   invite_uid,
                                 'purl':         purl,
                                 'info_str':     info_str
                                 }
                }
        mo = MsgPack()
        mo.setCmd('majiang_todotasks')
        mo.setResult('gameId', gameId)
        mo.setResult('userId', userId)
        mo.setResult('tasks', [task])
        router.sendToUser(mo, userId)


def sendBuyDiamondTodoTask(userId, gameId, clientId, pay_order):
    """ 幸运大抽奖，钻石购买
    @param         pay_order        挑选商品模板
    """
    if not TYPlayer.isHuman(userId):
        return
    
    product, _ = hallstore.findProductByPayOrder(gameId, userId, clientId, pay_order)
    if not product:
        ftlog.error('userId =', userId, 'clientId =', clientId, 'pay_order =', pay_order,
                    'can not find suitable product!')
        return
    try:
        product = product.clone()
    except:
        product = strutil.cloneData(product)
    desc = u'您的钻石不够哦~\n现在' + unicode(product.price) +u'元立得' + unicode(product.priceDiamond) +u'钻石！'
    product.content.desc = str(product.priceDiamond) + '钻石'
    client_ver = sessiondata.getClientIdVer(userId)
    if client_ver < 3.74:   # 客户端bug，小于3.74的版本转换一下
        product.priceDiamond = product.price
    todotasks = TodoTaskOrderShow.makeByProduct(desc, '', product)
    TodoTaskHelper.sendTodoTask(gameId, userId, todotasks)

def sendMasterGiftTodoTask(userId, gameId, clientId, pic, pay_order, roomId):
    """ 推送高手礼包弹窗
    @param         pay_order        挑选商品模板
    """
    if not TYPlayer.isHuman(userId):
        return
    product, _ = hallstore.findProductByPayOrder(gameId, userId, clientId, pay_order)
    if not product:
        ftlog.error('userId =', userId, 'clientId =', clientId, 'pay_order =', pay_order,
                    'can not find suitable product!')
        return
    todotask = TodoTaskPayOrder(product)
    task = {
            'action':   'cache_wnd_gaoshou',
            'params':   {
                         'pic':     pic,
                         'tasks':   [todotask.toDict()]
                         }
            }
    mo = MsgPack()
    mo.setCmd('majiang_todotasks')
    mo.setResult('gameId', gameId)
    mo.setResult('userId', userId)
    mo.setResult('tasks', [task])
    router.sendToUser(mo, userId)

def sendMarketEstimateTodoTask(userid, gameId, url, des, cache = False, direct = True):
    """ 推送麻将五星好评Cache
    发送五星好评的数据,客户端缓存,什么时候激活五星好评由客户端实现
    @param         des        五星好评内容
    """
    if not TYPlayer.isHuman(userid):
        return False, None
    ftlog.debug('sendMarketEstimateTodoTask:', userid, url, des, cache, direct)
    from majiang2.entity.todotasks_builder.todotasks_builder import MahjongTodoTaskBuilder

    task = MahjongTodoTaskBuilder.dict_market_estimate(userid, url, des, cache)
    if not task:
        return False, None

    if True == direct:
        mo = MsgPack()
        mo.setCmd('majiang_todotasks')
        mo.setResult('gameId', gameId)
        mo.setResult('userId', userid)
        mo.setResult('tasks', [task])
        router.sendToUser(mo, userid)
        return True, None
    else:
        return True, task

def sendChangeFortuneTodoTask(userid, gameId, roomid, insert, cache = False, direct = True):
    """ 推送麻将转运礼包Cache added by nick.kai.lee
    发送转运礼包的数据,客户端是否缓存由cache决定,cache为True时不是立即激活,
    什么时候激活转运礼包由客户端实现

    Args:
        userid: 玩家userid
        roomid: 房间id
        insert: 插入的task dict类型
        cache: action命名是否是缓存形式,默认不缓存
        direct: 是否直接发送,False则return dict
    """
    if not TYPlayer.isHuman(userid):
        return False, None
    ftlog.debug('sendChangeFortuneTodoTask:', userid, roomid, insert, cache, direct)
    from majiang2.entity.todotasks_builder.todotasks_builder import MahjongTodoTaskBuilder

    task = MahjongTodoTaskBuilder.dict_change_fortune(userid, gameId, roomid, cache)
    if not task:
        return False, None

    if isinstance(insert, dict):
        task['params']['buttons'][1]['tasks'].append(insert)

    ftlog.debug('sendChangeFortuneTodoTask:', task)

    if True == direct:
        mo = MsgPack()
        mo.setCmd('majiang_todotasks')
        mo.setResult('gameId', gameId)
        mo.setResult('userId', userid)
        mo.setResult('tasks', [task])
        router.sendToUser(mo, userid)
        return True, None
    else:
        return True, task

def sendAlmsTodoTask(userid, gameId, cache = False, direct = True):
    """ 推送麻将救济金Cache  added by nick.kai.lee
    发送麻将救济金数据,客户端是否缓存由cache决定,cache为True时不是立即激活,
    什么时候激活转运礼包由客户端实现

    Args:
        userid: 玩家userid
        cache: action命名是否是缓存形式,默认不缓存
        direct: 是否直接发送,False则return dict
    """
    if not TYPlayer.isHuman(userid):
        return False, None

    ftlog.debug('sendAlmsTodoTask:', userid, cache, direct)
    from majiang2.entity.todotasks_builder.todotasks_builder import MahjongTodoTaskBuilder
    from hall.entity import hallbenefits
    _, userBenefits = hallbenefits.benefitsSystem.sendBenefits(gameId, userid)
    benefitsStrs = []
    benefitsStrs.append('送您%s金币翻本吧！' % (userBenefits.sendChip))
    privilegeName = userBenefits.privilege.name if userBenefits.privilege else ''
    if userBenefits.extSendChip > 0:
        benefitsStrs.append('您是%s再加赠%s金币' % (privilegeName, userBenefits.extSendChip))
    benefitsStrs.append('（%s每天%s次，今天第%s次）' % (privilegeName, userBenefits.totalMaxTimes, userBenefits.times))
    if userBenefits.privilege and userBenefits.privilege.desc:
        benefitsStrs.append('\n%s' % (userBenefits.privilege.desc))

    task = MahjongTodoTaskBuilder.dict_general_box(userid, '\n'.join(benefitsStrs), cache)
    if not task:
        return False, None

    # task['params']['buttons'][0]['tasks'].append({})

    ftlog.debug('sendAlmsTodoTask:', task)
    if False == direct:
        return True, task

    mo = MsgPack()
    mo.setCmd('majiang_todotasks')
    mo.setResult('gameId', gameId)
    mo.setResult('userId', userid)
    mo.setResult('tasks', [task])
    router.sendToUser(mo, userid)
    return True, None

def sendLocalPushTodoTask(userid, gameId, hour, minute, second, direct = True):
    """ 推送 本地推送push  added by nick.kai.lee
    向客户端推送闹钟push的注册,比如每次客户端登录时都会推送一次"本地推送的功能"

    Args:
        userid: 玩家userid
        cache: action命名是否是缓存形式,默认不缓存
        direct: 是否直接发送,False则return dict
    """
    if not TYPlayer.isHuman(userid):
        return False, None

    ftlog.debug('sendLocalPushTodoTask:', userid)
    from majiang2.entity.todotasks_builder.todotasks_builder import MahjongTodoTaskBuilder

    from datetime import datetime
    now = datetime.now()
    #alarm3个元素,days,seconds,microseconds, seconds遇到过去的时间会自动获得明天这个时间点的时间差
    alarm = datetime(datetime.now().year, datetime.now().month, datetime.now().day, hour, minute, second)

    # 推送内容
    import random
    content = random.choice([
        "还记得上次在拜雀神中抽取的大奖么？机会又来了!",
        "修复老年痴呆，拯救弱智儿童，途游麻将提高智商值得你拥有！",
        "主人，您的任务奖励还没领取呢，去看看吧！",
        "优惠降临！充值送豪礼，下班来放松玩玩吧！",
        "幸运大抽奖可以免费领取金币了，快来领取吧！",
        "您有一份礼包未签收，快去活动中心看看吧！",
        "点我速领500金币~",
        "工作一天了，让麻将小莲帮你放松放松~",
        "亲，每隔10分钟1场免费定时赛，100奖券随便拿！",
        "您可以领取每日奖励了，它将会很快过期，快回到途游麻将领取吧！",
        "雀神爷爷说马上就要发红包了，你准备好了么？",
        "您获取的奖券兑换话费了嘛？",
        "大哥，您的贵宾桌我们已经为您准备好了！静候您的光临！",
        "您的好友邀请您一起对战途游麻将！"
	])

    task = MahjongTodoTaskBuilder.dict_reg_push_alarm(userid, content, (alarm-now).seconds, [True, False, True, False, True, False], "", {}, 3 )

    if not task:
        return False, None

    ftlog.debug('sendLocalPushTodoTask:', task)
    if False == direct:
        return True, task

    mo = MsgPack()
    mo.setCmd('majiang_todotasks')
    mo.setResult('gameId', gameId)
    mo.setResult('userId', userid)
    mo.setResult('tasks', [task])
    router.sendToUser(mo, userid)
    return True, None

def sendFreeChipTodoTask(userid, gameId, cache = False, direct = True):
    """ 推送 免费金币  added by nick.kai.lee

    Args:
        userid: 玩家userid
        cache: action命名是否是缓存形式,默认不缓存
        direct: 是否直接发送,False则return dict
    """
    if not TYPlayer.isHuman(userid):
        return False, None

    ftlog.debug('sendFreeChipTodoTask:', userid)
    from majiang2.entity.todotasks_builder.todotasks_builder import MahjongTodoTaskBuilder


    task = MahjongTodoTaskBuilder.dict_free_chip(userid, cache)

    if not task:
        return False, None

    ftlog.debug('sendFreeChipTodoTask:', task)
    if False == direct:
        return True, task

    mo = MsgPack()
    mo.setCmd('majiang_todotasks')
    mo.setResult('gameId', gameId)
    mo.setResult('userId', userid)
    mo.setResult('tasks', [task])
    router.sendToUser(mo, userid)
    return True, None

def sendBigMatchWaitTodoTask(userid, gameId, cache = False, direct=True):
    """比赛结算界面返回按钮返回时  
    """
    from majiang2.entity.todotasks_builder.todotasks_builder import MahjongTodoTaskBuilder
    msg = "比赛正在配桌中，请您耐心等待"
    task = MahjongTodoTaskBuilder.dict_general_box(userid, msg, cache)
    mo = MsgPack()
    mo.setCmd('majiang_todotasks')
    mo.setResult('gameId', gameId)
    mo.setResult('userId', userid)
    mo.setResult('tasks', [task])
    router.sendToUser(mo, userid)
    return True, None

def sendBigMatchBackToListTodoTask(userid, gameId, cache = False, direct=True):
    """比赛结算界面返回按钮返回时  
    """
    from majiang2.entity.todotasks_builder.todotasks_builder import MahjongTodoTaskBuilder
    msg = "比赛已结束，点击离开按钮返回比赛列表"
    task = MahjongTodoTaskBuilder.dict_general_box(userid, msg, cache)
    retTask = strutil.cloneData(task)
    buttonLeaveTask =  {
                            "content":"离开",
                            "tasks":[
                                {
                                    "action":"trigger_notify",
                                    "params":{
                                        "eventName":"UPDATE_MATCH_BACK_TO_LIST"
                                    }
                                }
                            ]
                        }
    retTask['params']['buttons'] = [buttonLeaveTask]
    mo = MsgPack()
    mo.setCmd('majiang_todotasks')
    mo.setResult('gameId', gameId)
    mo.setResult('userId', userid)
    mo.setResult('tasks', [retTask])
    router.sendToUser(mo, userid)
    return True, None
