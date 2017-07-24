# -*- coding:utf-8 -*-

from freetime.util import log as ftlog
from hall.servers.common.base_http_checker import BaseHttpMsgChecker
from poker.protocol import router, runhttp
from poker.protocol.decorator import markHttpHandler, markHttpMethod
from freetime.entity.msg import MsgPack
from majiang2.entity.quick_start import MajiangCreateTable
from poker.entity.configure import gdata
from poker.entity.dao import daobase
import re, json

@markHttpHandler
class MJ2Admin(BaseHttpMsgChecker):

    def __init__(self):
        super(MJ2Admin, self).__init__()
        
    def _passThis(self):
        """ 判断这个请求是否需要被屏蔽
        """
        # 不能在线上和仿真服使用
        if gdata.mode() not in [3, 4]:
            return False
        return True

    @markHttpMethod(httppath='/majiang2/admin/put_tiles')
    def putTiles(self):
        if not self._passThis():
            return {'info': 'can not use this tool !', 'code': 1}

        play_mode = runhttp.getParamStr('play_mode')
        seat1 = runhttp.getParamStr('seat1', '')
        seat2 = runhttp.getParamStr('seat2', '')
        seat3 = runhttp.getParamStr('seat3', '')
        seat4 = runhttp.getParamStr('seat4', '')
        jing  = runhttp.getParamStr('jing', '')
        laizi = runhttp.getParamStr('laizi', '')
        pool  = runhttp.getParamStr('pool')
        ftlog.debug('play_mode =', play_mode, 'seat1 =', seat1, 'seat2 =', seat2, 'seat3 =', seat3,
                    'seat4 =', seat4, 'jing=', jing,'laizi=',laizi, 'pool =', pool, caller=self)

        tile_info = {
                     'seat1':       self._splitTiles(seat1),
                     'seat2':       self._splitTiles(seat2),
                     'seat3':       self._splitTiles(seat3),
                     'seat4':       self._splitTiles(seat4),
                     'jing':        self._splitTiles(jing),
                     'pool':        self._splitTiles(pool),
                     'laizi':       self._splitTiles(laizi)
                     }
        key = 'put_card:' + play_mode
        daobase.executeMixCmd('set', key, json.dumps(tile_info))
        return {'info': 'ok', 'code': 0}
    
    def _splitTiles(self, tiles_str):
        """ 解析牌
        """
        tiles = []
        tiles_list = re.split(',|;| |\\t', tiles_str)
        for tile in tiles_list:
            try:
                t = int(tile)
                if t > 48:
                    continue
                tiles.append(t)
            except:
                pass
        return tiles
    
    @markHttpMethod(httppath='/majiang2/admin/cancel_put_tiles')
    def cancelPutTiles(self):
        """ 撤销摆牌
        """
        if not self._passThis():
            return {'info': 'fuck you!', 'code': 1}
        
        play_mode = runhttp.getParamStr('play_mode')
        key = 'put_card:' + play_mode
        daobase.executeMixCmd('del', key)
        return {'info': 'ok', 'code': 0}
    
