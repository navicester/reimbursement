from django.shortcuts import render, HttpResponseRedirect, Http404,render_to_response, HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.template.context import RequestContext
from django.template.loader import get_template
from django.utils.encoding import smart_str, smart_unicode
import xml.etree.ElementTree as ET
from wechat.views import responseMsg
#from curses.has_key import has_key

@csrf_exempt
def handleDebug(request):
    #context = {}
    template = "debug/wechat.html"

    if request.method == 'GET':
        if 'send-content' in request.GET: #submit throught "debug" button
            sendContent = request.GET['send-content'].strip()
            rawStr = smart_str(sendContent)
            msg = ET.fromstring(rawStr) 
            returnStr = ET.tostring(msg)
            returnUnicode = smart_unicode(returnStr)
            
            context = RequestContext(request, {
                'receivedContent' : responseMsg(request).replace('\r','').replace('\n',''),
                'SendContent' : sendContent.replace('\r','').replace('\n',''),
            })
            
            if request.GET.has_key('ajax'):            
                response = HttpResponse(sendContent,content_type="application/xml")
                return response
            else:
                #redirectionLink = "/debug/?type=text&send-content=%s" % rawStr
                #return HttpResponseRedirect(redirectionLink)
                return render_to_response(template,context)
        else: # startup
            context = {}
            context = RequestContext(request, {
                'receivedContent' : "loading...."
            })
            return render(request, template, context)
    elif request.method == 'POST':
        '''
        if request.POST.has_key('mptoken') and request.POST['mptoken'] != "" and request.POST.has_key('mpxml') == False:
            token = smart_str(request.POST['mptoken'])
            url = smart_str(request.POST['mpurl'])
        '''
        if request.POST.has_key('mpxml') == False:
            import json            
            response_data = json.loads('{"status":"1", "type":{"name":"seq", "parameter":["1", "2"]}}')            
            '''
            # or we can use below method
            response_data = {}  
            response_data['status'] = '1'  
            response_data['message'] = 'You messed up' 
            '''
            response = HttpResponse(json.dumps(response_data),content_type="application/json")
            return response
        elif request.POST.has_key('mpxml') and request.POST['mpxml'] != "":
            rawStr = smart_str(request.POST['mpxml'])
            msg = ET.fromstring(rawStr) 
            returnStr = ET.tostring(msg)
            returnUnicode = smart_unicode(returnStr)
            returnUnicode = returnUnicode.replace('    ','\r\n')
            response = HttpResponse(returnUnicode,content_type="application/xml")
            return response
        else:
            c = RequestContext(request,{'result':'wrong POST data'})
            t = get_template('{{result}}')
            response = HttpResponse(t.render(c),content_type="application/xml")
            return response
    else:
        return "welcome to zakkabag"    