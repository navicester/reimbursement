
from django.utils.encoding import smart_str, smart_unicode
import time

def paraseMsgXml(rootElem):
    msg = {}
    if rootElem.tag == 'xml':
        for child in rootElem:
            msg[child.tag] = smart_str(child.text)
    return msg

def paraseYouDaoXml(rootElem):
    replyContent = ''
    if rootElem.tag == 'youdao-fanyi':
        for child in rootElem:
            # error code
            if child.tag == 'errorCode':
                if child.text == '20':
                    return 'too long to translate\n'
                elif child.text == '30':
                    return 'can not be able to translate with effect\n'
                elif child.text == '40':
                    return 'can not be able to support this language\n'
                elif child.text == '50':
                    return 'invalid key\n'

            # query
            elif child.tag == 'query':
                replyContent = "%s%s\n" % (replyContent, child.text)

            # translation
            elif child.tag == 'translation': 
                replyContent = '%s%s\n%s\n' % (replyContent, '-' * 3 + u'YouDao translate' + '-' * 3, child[0].text)

            # basic dictionary
            elif child.tag == 'basic': 
                replyContent = "%s%s\n" % (replyContent, '-' * 3 + u'basic dic' + '-' * 3)
                for c in child:
                    if c.tag == 'phonetic':
                        replyContent = '%s%s\n' % (replyContent, c.text)
                    elif c.tag == 'explains':
                        for ex in c.findall('ex'):
                            replyContent = '%s%s\n' % (replyContent, ex.text)

            # web
            elif child.tag == 'web': 
                replyContent = "%s%s\n" % (replyContent, '-' * 3 + u'web dict' + '-' * 3)
                for explain in child.findall('explain'):
                    for key in explain.findall('key'):
                        replyContent = '%s%s\n' % (replyContent, key.text)
                    for value in explain.findall('value'):
                        for ex in value.findall('ex'):
                            replyContent = '%s%s\n' % (replyContent, ex.text)
                    replyContent = '%s%s\n' % (replyContent,'--')
    return replyContent

def getReplyXml(msg,replyContent):
    extTpl = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[%s]]></MsgType><Content><![CDATA[%s]]></Content><FuncFlag>0</FuncFlag></xml>";
    extTpl = extTpl % (msg['FromUserName'],msg['ToUserName'],str(int(time.time())),'text',replyContent)
    return extTpl