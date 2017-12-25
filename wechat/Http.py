#coding=utf-8
import urllib2,cookielib
import xml.etree.ElementTree as ET

class HTTPRefererProcessor(urllib2.BaseHandler):
    def __init__(self):
        self.referer = None

    def http_request(self, request):
        if ((self.referer is not None) and
            not request.has_header("Referer")):
            request.add_unredirected_header("Referer", self.referer)
        return request

    def http_response(self, request, response):
        self.referer = response.geturl()
        return response

    https_request = http_request
    https_response = http_response

from django.utils.encoding import smart_str, smart_unicode
def paraseMsgXml(rootElem):
    msg = {}
    if rootElem.tag == 'xml':
        for child in rootElem:
            msg[child.tag] = smart_str(child.text)
    return msg

import json
import urllib
if __name__ == "__main__":
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj), HTTPRefererProcessor(),)    
    urllib2.install_opener(opener)
        
    data = urllib.urlencode({"signature":0,"timestamp":1,"nonce":"","echostr":""})
    headers = {'Content-Type': 'application/xml', 'Accept':"text/xml", 'Accept-Charset':'gbk','AcceptLanguage':'en'}
    #headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    url     = 'http://pekingese.sinaapp.com'
    urlYoudao  = 'http://fanyi.youdao.com/openapi.do?keyfrom=zakkabag&key=1228130126&type=data&doctype=xml&version=1.1&q=dog'
    
    transfercontent = u'I' #u'中国'
    data1="\
    <xml>\
        <ToUserName><![CDATA[wxe90ebbe29377e650]]></ToUserName>\
        <FromUserName><![CDATA[ojpX_jig-gyi3_Q9fHXQ4rdHniQs]]></FromUserName>\
        <CreateTime>1451143558</CreateTime>\
        <MsgType><![CDATA[text]]></MsgType>\
        <Content><![CDATA[%s]]></Content>\
        <MsgId>1234567890abcdef</MsgId>\
    </xml>"
    data = data1 % (transfercontent)
        
    request = urllib2.Request(
            url     = url,
            headers = headers,
            data    = data)
    
    ret = opener.open(request)
    content = ret.read()
    print content
    xmlData = ET.fromstring(content)
    # xml handling
    
    # 下面处理是不对的，这个获得的是xml格式
    import chardet;
    detectedEncodingDict = chardet.detect(content);
    #msg = paraseMsgXml(content)
    try:
        content.decode(detectedEncodingDict['encoding'])
        content = json.loads(content)
        #json.dumps : dict转成str
        #json.loads:str转成dict
        print content
    except:
        print 'None'
    


    '''
    import urllib
    import urllib2
    import json
    d = '{"signature":0,"timestamp":1,"nonce":"","echostr":""}'    
    request = urllib2.Request(url="http://pekingese.sinaapp.com", data=d)    
    request.add_header("Content-Type", "application/json; charset=utf-8")
    f = urllib2.urlopen(request)
    content = f.read()
    content = content.decode("gbk")
    content = json.loads(content)
    '''