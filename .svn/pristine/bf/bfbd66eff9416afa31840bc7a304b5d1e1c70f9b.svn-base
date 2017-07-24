# -*- coding=utf-8 -*-
'''
Created on 2015年10月11日

@author: liaoxx
'''
import json, time
from poker.util.timestamp import getWeekStartTimestamp
from poker.entity.dao import gamedata, userdata
import freetime.util.log as ftlog
from poker.entity.dao import userchip


class MajiangData():

    # 各个字段的含义描述
    # lastlogin: 上次登陆时间，从2012/5/1以来的第N天
    # nslogin: 连续登陆天数
    # chip: 用户金币数，初始为1600
    # exp: 用户经验值
    # level: 用户等级
    # play_game_count: 参与的牌局总数
    # win_game_count: 赢的牌局总数（最后结算如果金币数个数大于0，就为赢)
    # draw_game_count: 平局的牌局数
    # lose_game_count: 输的牌局总数
    # bang_count: 点炮次数
    # best_pattern: 最佳番型, 使用json串记录{'description':'','degree':x}
    # highest_lose_chip: 一盘内最大的输金币数
    # highest_win_chip: 一盘内最大的赢金币数
    # big_pattern_history: 大牌历史记录，比如几次天胡,龙七对
    #                      [{'pattern_name':'', 'order':x, 'count':x}]
    # highest_chip_record: 记录曾经达到的最大金币数
    # online_records: 记录在某个房间内的已经打完的局数，会给予用户进行在线时长奖励
    # day_win_game_count: 每日胡牌次数
    # day_win_sequence_count: 每日连胡次数，每天清零一次
    # day_max_win_sequence_count: 每日最大连胡次数
    # max_degree_week_duration: 记录一周内的最大胡牌番数，每周一清空
    # max_degree_week_duration_ts: 最大胡牌番数的记时时间戳
    # master_point: 历史雀神分
    # week_master_point: 周雀神分
    # week_master_point_ts: 周雀神分计时时间戳
    # charm: 魅力值
    # day_play_game_count: 每日游戏次数，每天清零一次
    # ... ...
    # ... ...
    # 后续如果要添加新的字段，直接在后面追加，为了兼容，不要删除任何字段
    config = [
        ['lastlogin', 0],
        ['nslogin', 0],
        ['exp', 0],
        ['level', 1],
        ['play_game_count', 0],
        ['win_game_count', 0],
        ['draw_game_count', 0],
        ['lose_game_count', 0],
        ['bang_count', 0],
        ['highest_lose_chip', 0],
        ['highest_win_chip', 0],
        ['highest_chip_record', 0],
        ['day_win_game_count', 0],
        ['day_win_sequence_count', 0],
        ['day_max_win_sequence_count', 0],
        ['big_pattern_history', '{}'],
        ['best_pattern', '{}'],
        ['online_records', '{}'],
        ['win_sequence_count', 0],
        ['max_win_sequence_count', 0],
        ['guobiao_best_pattern', '{}'],
        ['guobiao_online_records', '{}'],
        ['master_point', 0],
        ['week_master_point', 0],
        ['week_master_point_ts', 0],
        ['day_play_game_count', 0],
        ['new_win_sequence_count',0],#与win_sequence_count的区别在于这个new_win_sequence_count会在回到房间列表时清零(也表示各玩法单独统计)
        ['invite_state', 0], #邀请状态
    ]

    @classmethod
    def getGameDataKeys(cls, bFilterInvite = False):
        keys = []
        for item in cls.config:
            if bFilterInvite and item[0] == 'invite_state':
                continue
            keys.append(item[0])
        return keys

    @classmethod
    def getGameDataValues(cls,bFilterInvite = False):
        values = []
        for item in cls.config:
            if bFilterInvite and item[0] == 'invite_state':
                continue
            values.append(item[1])
        return values

    @classmethod
    def get_kvs(cls, tasklet, uid, gid):
        '''
        attrs = ['lastlogin', 'nslogin', 'play_game_count', 'win_game_count', 'draw_game_count',
                 'lose_game_count', 'bang_count', 'highest_lose_chip', 'highest_win_chip',
                 'highest_chip_record', 'day_win_game_count', 'day_win_sequence_count',
                 'day_max_win_sequence_count', 'big_pattern_history', 'best_pattern',
                 'online_records', 'guobiao_play_game_count', 'guobiao_win_game_count', 'guobiao_draw_game_count',
                 'guobiao_lose_game_count', 'guobiao_bang_count', 'guobiao_highest_lose_chip',
                 'guobiao_highest_win_chip', 'guobiao_highest_chip_record', 'win_sequence_count', 'max_win_sequence_count',
                 'guobiao_best_pattern', 'guobiao_online_records', 'max_degree_week_duration', 'max_degree_week_duration_ts',
                 'master_point', 'week_master_point', 'week_master_point_ts', 'day_play_game_count']
        '''
        attrs = ['win_sequence_count',  'max_win_sequence_count', 'guobiao_best_pattern']
        values = gamedata.getGameAttrs(uid, gid, attrs)
        for i, value in enumerate(values):
            if value is None:
                ftlog.debug(attrs[i], 'is None')
                values[i] = cls.get_default_value(attrs[i])[1]
            else:
                values[i] = cls.parse_content_from_redis(attrs[i], value)
        kvs = dict(zip(attrs, values))
        cls.check_attrs_timestamp(tasklet, uid, gid, kvs)

        kvs['chip'] = userchip.getChip(uid)
        kvs['exp'] = userdata.getExp(uid)
        kvs['charm'] = userdata.getCharm(uid)
        if not kvs['chip']:
            kvs['chip'] = 0
        if not kvs['exp']:
            kvs['exp'] = 0
        if not kvs['charm']:
            kvs['charm'] = 0
        return kvs

    @classmethod
    def check_attrs_timestamp(cls, tasklet, uid, gid, kvs):
        """检查相关属性是否过期"""
        update_attrs = []
        # 本周最大番数
        week_start_ts = getWeekStartTimestamp()
        if 'max_degree_week_duration' in kvs:
            refresh_ts = kvs['max_degree_week_duration']
            if refresh_ts < week_start_ts:
                kvs['max_degree_week_duration_ts'] = int(time.time())
                kvs['max_degree_week_duration'] = 0
                update_attrs.append('max_degree_week_duration_ts')
                update_attrs.append('max_degree_week_duration')

        # 本周雀神分
        if 'week_master_point' in kvs:
            refresh_ts = kvs['week_master_point_ts']
            if refresh_ts < week_start_ts:
                kvs['week_master_point_ts'] = int(time.time())
                kvs['week_master_point'] = 0
                update_attrs.append('week_master_point_ts')
                update_attrs.append('week_master_point')

        # 更新
        if update_attrs:
            update_values = []
            for attr in update_attrs:
                value = cls.serialize_string_to_redis(attr, kvs[attr])
                update_values.append(value)
            gamedata.setGameAttrs(uid, gid, update_attrs, update_values)

    @classmethod
    def get_sichuan_attrs(cls):
        """
        Player对象需要获取gamedata，等用户结束一局时，需要更新gamedata
        """
        attrs = ['sc_exp', 'guobiao_exp']
        for item in cls.config:
            # 默认只取四川麻将的值
            if item[0].startswith('guobiao'):
                continue
            attrs.append(item[0])

        attrs.remove('exp')
        return attrs

    @classmethod
    def get_guobiao_attrs(cls):
        '''
        keys = ['chip', 'day_win_game_count', 'day_win_sequence_count', 'day_play_game_count',
                'win_sequence_count', 'max_win_sequence_count',
                'max_degree_week_duration',
                'max_degree_week_duration_ts', 'exp', 'sc_exp',
                'master_point', 'week_master_point', 'week_master_point_ts', 'charm']
        '''
        keys = ['play_game_count', 'win_game_count', 'draw_game_count','lose_game_count',
                'day_win_game_count', 'day_win_sequence_count', 'day_play_game_count',
                'win_sequence_count', 'max_win_sequence_count',
                'max_degree_week_duration',
                'max_degree_week_duration_ts',
                'master_point', 'week_master_point', 'week_master_point_ts','new_win_sequence_count', 'invite_state']
        for item in cls.config:
            if item[0].startswith('guobiao'):
                keys.append(item[0])
        return keys

    @classmethod
    def get_nanchang_attrs(cls):
        '''
        keys = ['chip', 'day_win_game_count', 'day_win_sequence_count', 'day_play_game_count',
                'win_sequence_count', 'max_win_sequence_count',
                'max_degree_week_duration',
                'max_degree_week_duration_ts', 'exp', 'sc_exp',
                'master_point', 'week_master_point', 'week_master_point_ts', 'charm']
        '''
        keys = ['play_game_count', 'win_game_count', 'draw_game_count','lose_game_count',
                'day_win_game_count', 'day_win_sequence_count', 'day_play_game_count',
                'win_sequence_count', 'max_win_sequence_count',
                'max_degree_week_duration',
                'max_degree_week_duration_ts',
                'master_point', 'week_master_point', 'week_master_point_ts','new_win_sequence_count']
        for item in cls.config:
            if item[0].startswith('nanchang'):
                keys.append(item[0])
        return keys
    
    @classmethod
    def get_ji_an_attrs(cls):
        '''
        '''
        keys = []
        for item in cls.config:
            if item[0].startswith('nanchang') or item[0].startswith('guobiao') or item[0].startswith('ganzhou'):
                continue
            keys.append(item[0])
        return keys
    
    @classmethod
    def get_ganzhou_attrs(cls):
        '''
        '''
        keys = []
        for item in cls.config:
            if item[0].startswith('nanchang') or item[0].startswith('guobiao') or item[0].startswith('ji_an'):
                continue
            keys.append(item[0])
        return keys

    @classmethod
    def get_default_value(cls, key):
        """
        获取某个key对应的初始化值, 返回(True/False, value)
        """
        for item in cls.config:
            if item[0] == key:
                if key == 'big_pattern_history':
                    value = {u'天胡': 0, u'地胡': 0, u'清龙七对': 0,
                             u'龙七对': 0, u'七对': 0, u'清七对': 0,
                             u'将对': 0, u'清对': 0, u'对对胡': 0,
                             u'清幺九': 0, u'全幺九': 0, u'清一色': 0}
                    return True, value
                elif key in ['best_pattern', 'guobiao_best_pattern', 'nanchang_best_pattern']:
                    value = {'degree':0, 'description':''}
                    return True, value
                elif key in ['online_records', 'guobiao_online_records', 'nanchang_online_records']:
                    return True, {}
                elif key in ['sc_exp']:
                    return True, None
                else:
                    return True, item[1]
        return False, None

    @classmethod
    def parse_content_from_redis(cls, key, value):
        """
        每个key对应的value，在redis中对应一个int/string，如果要存储复杂
        结构，需要给value使用特殊编码，比如protobuf, json等，目前先使用
        json存储，后续再看其它方案吧
        """
        if key in ['best_pattern', 'big_pattern_history', 'online_records',
                   'guobiao_best_pattern', 'guobiao_online_records',
                   'nanchang_best_pattern', 'nanchang_online_records']:
            return json.loads(value)
        else:
            return value

    @classmethod
    def serialize_string_to_redis(cls, key, value):
        """
        序列化key对应的value到redis中
        """
        if key in ['best_pattern', 'big_pattern_history', 'online_records',
                   'guobiao_best_pattern','guobiao_online_records',
                   'nanchang_best_pattern', 'nanchang_online_records']:
            return json.dumps(value)
        else:
            return value
