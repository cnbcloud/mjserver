# -*- coding=utf-8
'''
Created on 2016年9月23日

@author: zhaol
'''
from poker.entity.dao import userchip
from poker.entity.biz import bireport
from freetime.util import log as ftlog
from poker.entity.game.tables.table_player import TYPlayer

class MTableExpression(object):
    
    def __init__(self):
        super(MTableExpression, self).__init__()
        
    @classmethod
    def get_interactive_expression_config(self, base_chip):
        """获取互动表情的配置"""
        chip_limit = int(base_chip * 1.1)
        cost_1 = int(base_chip * 0.5)
        cost_2 = int(base_chip)

        ret = {
            # 炸弹
            '0': {'chip_limit': chip_limit
                , 'cost': cost_2
                , 'charm': int(cost_2/10)
                , 'ta_charm': -int(cost_2/10)
            },
            # 钻戒
            '1': {'chip_limit': chip_limit
                , 'cost': cost_2
                , 'charm': int(cost_2/5)
                , 'ta_charm': int(cost_2/5)
            },
            # 鸡蛋
            '2': {'chip_limit': chip_limit
                , 'cost': cost_1
                , 'charm': int(cost_1/10)
                , 'ta_charm': -int(cost_1/10)
            },
            # 鲜花
            '3': {'chip_limit': chip_limit
                , 'cost': cost_1
                , 'charm': int(cost_1/5)
                , 'ta_charm': int(cost_1/5)
            },
        }

        return ret
    
    @classmethod
    def process_interactive_expression(cls, userId, gameId, seatId, chat_msg, target_player_uid, base_chip):
        """处理消费金币的表情"""
        config = cls.get_interactive_expression_config(base_chip)
        emoId = str(chat_msg.get('emoId', -1))
        if emoId not in config:
            ftlog.warn('chat msg illegal', chat_msg, config)
            return False

        info = config[emoId]
        # 底分限制
        chip = userchip.getChip(userId)
        if chip < info['chip_limit'] + info['cost']:
            ftlog.warn('insufficient', chip, info['chip_limit'], info['cost'])
            return False
        
        if TYPlayer.isHuman(userId):
            from majiang2.entity.util import Util
            clientId = Util.getClientId(userId)
            trueDelta, _ = userchip.incrChip(userId
                    , gameId
                    , -info['cost']
                    , 0
                    , "EMOTICON_CONSUME"
                    , chat_msg['emoId']
                    , clientId
            )
            
            if trueDelta != -info['cost']:   # 失败
                ftlog.warn('coin not enougth: ', chip, info['chip_limit'], info['cost'])
                return False
            bireport.gcoin('out.interactive_expression', gameId, info['cost'])
            
            # 处理魅力值
#             charm = incrCharm(userId, info['charm'])
#             hallranking.rankingSystem.setUserByInputType(gameId
#                     , TYRankingInputTypes.CHARM
#                     , userId
#                     , charm)
        
#         if TYPlayer.isHuman(target_player_uid):
#             charm = incrCharm(target_player_uid, info['ta_charm'])
#             hallranking.rankingSystem.setUserByInputType(gameId
#                     , TYRankingInputTypes.CHARM
#                     , target_player_uid
#                     , charm)
        
        return True