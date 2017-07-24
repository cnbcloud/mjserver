# coding=UTF-8
'''
Created on 2015年6月26日

@author: zqh
'''
from hashlib import md5
import json
import time
import urllib
import urllib2


def md5digest(md5str):
    '''
    计算一个字符串的MD5值, 返回32位小写的MD5值
    '''
    m = md5()
    m.update(md5str)  
    md5code = m.hexdigest()
    return md5code.lower()


def dohttpquery(posturl, datadict):
    Headers = {'Content-type': 'application/x-www-form-urlencoded'}
    postData = urllib.urlencode(datadict)
    request = urllib2.Request(url=posturl, data=postData, headers=Headers)
    response = urllib2.urlopen(request)
    if response != None :
        retstr = response.read()
        return retstr
    return None


def syncDataFromGdss(apiName):
    ct = int(time.time())
    sign = md5digest('qp-gm-shediao-api-' + str(ct) + '-qp-gm-shediao-api')
    posturl = 'http://qp.gmapi.shediao.com/?act=api.%s&time=%d&sign=%s' % (apiName, ct, sign)
    datas = dohttpquery(posturl, {})
    datas = json.loads(datas)
    dictdata = datas.get('retmsg', None)
    dictdata['IOS_3.901_weixin,tyGuest.alipay.0-hall777.lailai.ioshbmj']=17496
    return dictdata


if __name__ == '__main__':
    data = syncDataFromGdss('getClientIdDict')
    print json.dumps(data)
    pass
