#coding=utf-8 

from django.core.urlresolvers import reverse
from weixin.client import WeixinMpAPI

from zakkabag.settings import APP_ID, APP_SECRET
#APP_ID = 'wxe90ebbe29377e650'
#APP_SECRET = 'd4624c36b6795d1d99dcf0547af5443d'

# http://www.cnblogs.com/txw1958/p/weixin-js-sharetimeline.html

class WechatAPI(object):
    """docstring for WechatAPI"""
    def __init__(self, request, arg=None):
        super(WechatAPI, self).__init__()
        self.arg = arg
        self.request = request

    def getAccessToken(self):
    	# access_token 应该全局存储与更新, 根据定时器判断是否需要重新获取
        import urllib
        url='https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential'#grant_type为固定值
        # 如果是企业号用以下URL获取access_token
        # $url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=$this->appId&corpsecret=$this->appSecret";
        data={'appid': APP_ID,'secret': APP_SECRET}
        data=urllib.urlencode(data)
        html=urllib.urlopen(url,data)#<addinfourl at 34758208 whose fp = <socket._fileobject object at 0x0212F570>>
        html= html.read()
        import json
        json_data = json.loads(html.decode("utf-8"))
        return json_data['access_token']

        #res=json_decode(res)
        # return str(res['access_token'])  
        
        '''
        {"access_token":"Isd_tm3QE8Kateyxjz_WEEXuerBZ0gnO6XwyjirZXY1umVIDqebi6GK2Zv2fv1hI7sXQfHXeaOa2A4XrOITwS5LnczFRXf4BbSnMdSRLKiwBQYgADASHP",
        "expires_in":7200}  #expires_in，定义access_token有效时间,单位为秒
        '''        
            
    def createNonceStr(self,length = 16):
        import random
        chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        str = "";
        for i in range(0,16):
            str += chars[random.randint(0, len(chars)-1):random.randint(0, len(chars)-1)+1]
        return str;


    def getJsApiTicket(self):
        import urllib2
        # jsapi_ticket 应该全局存储与更新
        #cookie('ticket',null);

        #获取access_token
        accessToken = self.getAccessToken()

        # 如果是企业号用以下 URL 获取 ticket
        # $url = "https://qyapi.weixin.qq.com/cgi-bin/get_jsapi_ticket?access_token=$accessToken";
        #获取jsapi_ticket
        url = "https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token={}&type=jsapi".format(accessToken)

        req = urllib2.Request(url)
        res_data = urllib2.urlopen(req)
        res = res_data.read()
        # res=json_decode(res)
        # return str(res['ticket'])
        import json
        json_data = json.loads(res.decode("utf-8"))
        return json_data['ticket']        
        

    def getSignPackage(self) :
        import hashlib
        #获得jsapi_ticket
        jsapiTicket = self.getJsApiTicket()


        # 注意 URL 一定要动态获取，不能 hardcode.
        # protocol = (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off' || $_SERVER['SERVER_PORT'] == 443) ? "https://" : "http://";
        # $url = "$protocol$_SERVER[HTTP_HOST]$_SERVER[REQUEST_URI]";
        #获取当前页面的url
        # url="{}://{}{}".format(self.request.protocol,self.request.host,self.request.uri)
        url= self.request.get_full_path()
        url="{}://{}{}".format(self.request.META['wsgi.url_scheme'],self.request.META['HTTP_HOST'],self.request.get_full_path())

        #获取timestamp（时间戳）
        import time
        timestamp = int(time.time())
        #获取noncestr（随机字符串）
        nonceStr = self.createNonceStr()

        # 这里参数的顺序要按照 key 值 ASCII 码升序排序
        string = "jsapi_ticket={}&noncestr={}&timestamp={}&url={}".format(jsapiTicket,nonceStr,timestamp,url)
        #得到signature
        signature = hashlib.sha1(string).hexdigest();
        signPackage = {
            "appId":APP_ID,
            "nonceStr":nonceStr,
            "timestamp":timestamp,
            "url":url,
            "signature":signature,
            "rawString":string
        }

        print signPackage

        return signPackage;
