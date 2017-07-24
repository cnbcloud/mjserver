# -*- coding=utf-8 -*-
'''
Created on 2016年10月26日

@author: zengxx
'''

import json
import zipfile
import stackless
import os
from freetime.util import log as ftlog
from freetime.core.timer import FTTimer
from majiang2.entity import majiang_conf

SCANRATE = 1

class MJCreateTableRecordMsg(object):
    """牌局回放单局数据
    """

    # # 牌局回放需要记录的协议的cmd
    # PLAY_BACK_CMDS = [
    #     "cancel_suggestion",
    #     "online_reward",
    #     "set_trustee",
    #     "remove_trustee",
    #     "send_tile",
    #     "play",
    #     "seen_tile",
    #     "peng",
    #     "gang",
    #     "bu",
    #     "chi",
    #     "win",
    #     "third_win",
    #     "display_gang",
    #     "grab_gang",
    #     "display_budget",
    #     "display_guiyang_budget",
    #     "player_chick_type",
    #     "player_claim_ting",
    #     "ting",
    #     "decideAbsence",
    #     "absence_broadcast",
    #     "grabTing",
    #     "updateHandTiles",
    #     "send_tile_list",
    #     "play_list",
    #     "show_laizi_tiles",
    #     "fan_jing",
    #     "display_jing_budget",
    #     "table_info",
    #     "table_info_recovery",
    #     "sit",
    #     "init_tiles"
    # ]

    def __init__(self):
        self.msgs = []
        self.fileName = ''

    def reset(self):
        self.msgs = []
        self.fileName = ''

    def saveMsg(self, msg, uidList):
        '''
        每当麻将向客户端发送协议时，都调用本函数
        记录并且存储牌桌相关的协议
        '''
        if not isinstance(uidList, list):
            uidList = [uidList]
            
        gameId = msg.getResult('gameId')

        msg_obj = json.loads(msg.pack())
        if 'result' in msg_obj:
            # 这条协议下发玩家列表
            msg_obj['result']['record_uid_list'] = uidList
            # 所有回放数据都加上标记
            msg_obj['result']['isTableRecord'] = True

            # table_info的话，生成本局协议保存的文件名
            if (msg.getCmd() == "table_info") and ('create_table_extend_info' in msg_obj['result']):
                self.fileName = majiang_conf.get_table_record_msg_fileName(gameId
                        , msg_obj['result']['create_table_extend_info']['tableRecordKey']
                        , msg_obj['result']['create_table_extend_info']['create_now_cardcount'])

        self.msgs.append(msg_obj)

    def saveRecord(self, needUpload=True):
        """保存当前局的纪录
        """
        key = ""
        if needUpload == True and self.fileName:
            absoluteFileName = self.fileName.split("/")[-1]
            # 生成txt文件
            fw_obj = open(absoluteFileName, 'w')
            fw_obj.write(json.dumps(self.msgs))
            fw_obj.close()
            # 压缩为zip
            self.txt2zip(absoluteFileName, '%s.%s' % (absoluteFileName, 'zip'))
            # 上传zip数据
            fr_obj = open('%s.%s' % (absoluteFileName, 'zip'), 'r')
            data = fr_obj.read()
            fr_obj.close()

            key = '%s.%s' % (self.fileName, 'zip')
            FTTimer(SCANRATE, self.upload, key, data, 1)
            # 删除文件
            if os.path.exists(absoluteFileName):
                os.remove(absoluteFileName)
            if os.path.exists('%s.%s' % (absoluteFileName, 'zip')):
                os.remove('%s.%s' % (absoluteFileName, 'zip'))

            # ftlog.debug("MJCreateTableRecordMsg:saveRecord========", key, data)

        self.reset()
        return key

    def upload(self):
        """
        如果上传失败，每隔2*n的时间重试一次，重试4次
        """
        key = stackless.getcurrent()._fttask.run_argl[0]
        data = stackless.getcurrent()._fttask.run_argl[1]
        times = stackless.getcurrent()._fttask.run_argl[2]

        ret, _ = majiang_conf.uploadVideo(key, data)
        if ret == 0:
            ftlog.debug("MJCreateTableRecordMsg: upload the record success!!!")
        if ret != 0 and times <= 16:
            times = times*2
            FTTimer(SCANRATE*times, self.upload, key, data, times)

    def txt2zip(self, tfile, zfileName='default.zip'):
        zout = zipfile.ZipFile(zfileName, 'w', zipfile.ZIP_DEFLATED)
        zout.write(tfile)
        zout.close()
        
