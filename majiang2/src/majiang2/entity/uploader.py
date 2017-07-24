# -*- coding:utf-8 -*-
'''
Created on 2016年10月19日

@author: zhaojiangang
'''
import hashlib
import os
import random

from freetime.aio import http
import freetime.util.log as ftlog
from freetime.core.tasklet import FTTasklet
from qiniu import Auth, put_file, etag, urlsafe_base64_encode
import qiniu.config
import zlib

def calcPath(videoId):
    filePath = '%s.json' % (videoId)
    m = hashlib.md5()
    names = []
    for _ in xrange(3):
        m.update(filePath)
        name = str(int(m.hexdigest()[-3:], 16) % 1024)
        filePath = name + '/' + filePath
        names.append(name)
    return filePath

class FormItem(object):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    @property
    def isFile(self):
        return False

class FormItemData(FormItem):
    def __init__(self, name, value):
        super(FormItemData, self).__init__(name, value)

    @property
    def isFile(self):
        return False

class FormItemFile(FormItem):
    def __init__(self, name, value, filename):
        super(FormItemFile, self).__init__(name, value)
        self.filename = filename

    @property
    def isFile(self):
        return True

def genBoundary():
    getRandomChar = lambda:chr(random.choice(range(97,123)))
    randomChars = [getRandomChar() for _ in range(20)]
    return ''.join(randomChars)

def encodeFormItems(boundary, items):
    boundary = '--' + boundary
    lines = []
    for item in items:
        lines.append(boundary)
        header = 'Content-Disposition: form-data; name="%s"' % (item.name.encode('utf-8'))
        if item.isFile:
            header += '; filename="%s"' % (item.filename.encode('utf-8'))
            lines.append(header)
            lines.append('Content-Type: application/octet-stream')
            lines.append('')
            lines.append(item.value)
        else:
            lines.append(header)
            lines.append('')
            lines.append(item.value.encode('utf-8'))

    lines.append(boundary + '--')
    return '\r\n'.join(lines)
    #return zlib.compress('\r\n'.join(lines))

def olduploadVideo(uploadUrl, token, uploadPath, videoData):
    filename = os.path.basename(uploadPath)
    formItems = []
    formItems.append(FormItemData('token', token))
    formItems.append(FormItemData('key', uploadPath))
    formItems.append(FormItemFile('file', videoData, filename))
    #formItems.append(FormItemFile('fileBinaryData', videoData, filename))

    boundary = genBoundary()
    uploadData = encodeFormItems(boundary, formItems)
    headers={
        'Content-Type':['multipart/form-data; charset=utf-8; boundary=%s' % (boundary)]
    }
    try:
        code, body = http.runHttp(method='POST', url=uploadUrl, header=headers,
                                  body=uploadData,
                                  connect_timeout=5,
                                  timeout=5)
        if ftlog.is_debug():
            ftlog.debug('uploader.uploadVideo uploadUrl=', uploadUrl,
                        'uploadPath=', uploadPath,
                        'token=', token,
                        'ret=', (code, body))

        if code == 200:
            return 0, body

        ftlog.info('uploader.uploadVideo Res uploadUrl=', uploadUrl,
                    'uploadPath=', uploadPath,
                    'token=', token,
                    'ret=', code)
        return -1, '上传失败'
    except:
        return -2, '上传失败'

def uploadVideo(uploadUrl, token, uploadPath, videoData):
    ftlog.debug('All is OK for uploadVideo',uploadPath)
    accessKey = '6Q0h4Myad3nc5kYkloB3jlCnsMIOIHM0qhhFCtjU'
    secretKey = 'UcjNWFN5v3QjJl4XLTCJWoczV08zb_iI0UBEHGg8'
    ec, info = uploadPlaybackRecord(accessKey, secretKey, uploadPath,videoData)
    return ec,info
def uploadPlaybackRecord(accessKey, secretKey, uploadPath, recordData):
    q = Auth(accessKey, secretKey)
    key = os.path.basename(uploadPath)
    bucket_name = 'qipai-playback'
    token = q.upload_token(bucket_name, key, 3600)
    #要上传文件的本地路径
    ret, info = qiniu.put_data(token, key, recordData)
    if ret is not None:
        ftlog.debug('All is OK')
    else:
        ftlog.debug('--------upload error----------')
        ftlog.debug(info) # error message in info

    try:
        #ftlog.debug(ret)
        #{u'hash': u'Fk0g1Aqn62dw17eVTIklKD7Ry_Mb', u'key': u'luosihu-xuezhan-439740-1-16-1494579556'}
        retKey = ret['key'].encode('utf-8')
        assert retKey == key
        return 0, '上传成功'
    except:
        return -1, '上传失败'
    

if __name__ == '__main__':
    '''
    uploadUrl = 'http://up.wcsapi.biz.matocloud.com:8090/file/upload/'
    token = '87c953283acaba7e75340fccad71c97b047569c2:MjEwN2QyMzI2NzAwNDNjYTMzYmQyYjFiYzJiMWRmODg5NDU0YmEyNQ==:eyJzY29wZSI6InR5aGFsbCIsImRlYWRsaW5lIjoiMTQ4NTUyMjU3MDAwMCIsIm92ZXJ3cml0ZSI6MCwiZnNpemVMaW1pdCI6MCwiaW5zdGFudCI6MCwic2VwYXJhdGUiOjB9'
    
    from freetime.core.reactor import mainloop
    def runUpload():
        ec, info = uploadVideo(uploadUrl, token, 'util1.py', zlib.compress('util.py'))
        print 'runupload ec=', ec, 'info=', info
    argd = {'handler':runUpload}
    FTTasklet.create([], argd)
    mainloop()
    '''
    from freetime.core.reactor import mainloop
    def runUpload():
    	accessKey = '6Q0h4Myad3nc5kYkloB3jlCnsMIOIHM0qhhFCtjU'
    	secretKey = 'UcjNWFN5v3QjJl4XLTCJWoczV08zb_iI0UBEHGg8'
    	recordname='luosihu-xuezhan-439740-1-16-1494579556'
    	#file=open(recordname,'r')
    	#str=file.read()
    	str='11111112222222222222223333'
    	ec, info = uploadPlaybackRecord(accessKey, secretKey, recordname, str)
    	print 'runupload ec=', ec, 'info=', info
    argd = {'handler':runUpload}
    FTTasklet.create([], argd)
    mainloop()	
