# -*- coding=utf-8 -*-
'''
Created on 2016年03月08日
mahjong todotasks builder
@author: nick.kai.lee
'''
from poker.entity.dao import sessiondata
from poker.entity.biz.exceptions import  TYBizConfException

class MahjongTodoTaskBuilder(object):

    def __init__(self):
        super(object, self).__init__()

    @classmethod
    def dict_pay_order(cls, userid, product):
        """ 根据商品信息生成payOrder的字典
        action: pop_pay_order
        Args:
            userid: 玩家userid
            product: 商品信息
        """
        from hall.entity.todotask import TodoTaskPayOrder
        payorder = TodoTaskPayOrder(product)
        payorder = payorder.toDict()
        if not isinstance(payorder, dict):
            raise TYBizConfException(payorder, 'MahjongTodoTaskBuilder.dict_pay_order must be dict!')
        else:
            return payorder

    @classmethod
    def dict_change_fortune(cls, userid, gameId, roomid, cache = False):
        """ 根据商品信息生成payOrder的字典
        action: pop_fortune&cache_fortune
        Args:
            userid: 玩家userid
            roomid: 房间id
            cache: action命名是否是缓存形式
        """
        clientid = sessiondata.getClientId(userid)
        from hall.entity import hallproductselector, hallitem
        product, _ = hallproductselector.selectZhuanyunProduct(gameId, userid, clientid, roomid)
        if not product:
            return None

        payorder = cls.dict_pay_order(userid, product)

        chip = product.getMinFixedAssetCount(hallitem.ASSET_CHIP_KIND_ID)
        content1 = u'运气不好，来个转运礼包！'
        content2 = u'全国只有1%的人有机会呦！'
        rmblabel = u'￥'+str(product.price)
        chiplabel = chip

        action = "pop_fortune" if True != cache else "cache_fortune"
        return {
            'action': action,
            'params': {
                'content1': content1,
                'content2': content2,
                'rmb': rmblabel,
                'coin': chiplabel,
                'buttons': [
                        {
                            'content': u"立即购买",
                            'tasks': [
                                payorder
                            ]

                        },
                        {
                            'content': u'取消',
                            'tasks': [

                            ]
                        }
                    ]
                }
        }

    @classmethod
    def dict_general_box(cls, userid, content, cache = False):
        """ 根据商品信息生成payOrder的字典
        action: pop_general_box&cache_general_box
        Args:
            userid: 玩家userid
            cache: action命名是否是缓存形式
        """
        action = "pop_general_box" if True != cache else "cache_general_box"
        return {
            'action': action,
            'params': {
                'content': content,
                'buttons': [
                        {
                            'content': u'确定',
                            'tasks': [

                            ]
                        }
                    ]
                }
        }

    @classmethod
    def dict_market_estimate(cls, userid, url, des, cache = False):
        """ 根据商品信息生成五星好评的字典
        action: pop_market_estimate_wnd&cache_market_estimate_wnd
        Args:
            userid: 玩家userid
            cache: action命名是否是缓存形式
        """
        from hall.entity.todotask import TodoTaskFiveStarRating, TodoTaskGotoHelp
        rating = TodoTaskFiveStarRating(url)
        gotoHelp = TodoTaskGotoHelp()
        action = "pop_market_estimate_wnd" if True != cache else "cache_market_estimate_wnd"
        return {
            'action': action,
            'params': {
                'des': des,
                'tasks': [rating.toDict(), gotoHelp.toDict()]
            }
        }

    @classmethod
    def dict_reg_push_alarm(cls, userid, content = "", delaytime = 1, right = [True, True, True, True, True, True], buttonlabel = "", buttontask = {},  displaytime = 1 ):
        """ 生成闹钟push的字典
        action: run_reg_push_alarm
        Args:
            userid: 玩家userid
            content: 闹钟push内容
            delaytime: 闹钟延迟多少秒提示
            right: 权限
            buttonlabel: 按钮上的文字
            buttontask: 按钮响应的todotask
            displaytime: push显示时间
        """

        return {
            'action': "run_reg_push_alarm",
            'params': {
                'content': content,
                'delaytime': delaytime,
                'right': right,
                'buttonlabel': buttonlabel,
                'buttontask': buttontask,
                'displaytime': displaytime,
            }
        }

    @classmethod
    def dict_free_chip(cls, userid, cache = False):
        """ 免费金币
        action: pop_free_chip&cache_free_chip
        Args:
            userid: 玩家userid
            cache: action命名是否是缓存形式
        """
        import poker.util.timestamp as pktimestamp
        from hall.entity import hallbenefits
        timestamp = pktimestamp.getCurrentTimestamp()
        userBenefits = hallbenefits.benefitsSystem.loadUserBenefits(9999, userid, timestamp)
        times = userBenefits.times
        maxtimes = userBenefits.maxTimes
        action = "pop_free_chip" if True != cache else "cache_free_chip"
        return {
            'action': action,
            'params': {
                'times': times,  # 发了几次救济金
                'maxTimes': maxtimes # 总共几次救济金
            }
        }