
# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.encoding import smart_str, smart_unicode
import xml.etree.ElementTree as ET
import urllib, urllib2
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def handleMenuRequest(request):
	template = "debug/menu.html"
	if request.method == 'GET':
		return render(request, template, {})
	elif request.method == 'POST':
		purpose = smart_str(request.POST.get("purpose", None))
		json_data = None
		if "get_token" == purpose:
			appid = smart_str(request.POST.get("appid", None))
			appsecret = smart_str(request.POST.get("appsecret", None))			
			get_token_url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" % (appid , appsecret);
			req = urllib2.Request(url=get_token_url)
			result = urllib2.urlopen(req).read()
			json_data = json.loads(result.decode("utf-8")) #json-format string to json
		elif "delete_menu" == purpose:
			access_token = smart_str(request.POST.get("access_token", None))
			delete_menu_url = "https://api.weixin.qq.com/cgi-bin/menu/delete?access_token=%s" % (access_token);
			req = urllib2.Request(url=delete_menu_url)
			result = urllib2.urlopen(req).read()
			json_data = json.loads(result) #json-format string to json	
		elif "add_menu" == purpose:
			menux = '''
			{
				"button":[
				{	
					"type":"click",
					"name":"xx",
					"key":"V1001_TODAY_MUSIC"
				},
				{
					"name":"xxx",
					"sub_button":[
					{	
						"type":"view",
						"name":"xxxxx",
						"url":"http://www.soso.com/"
					},
					{
						"type":"view",
						"name":"xxxxxx",
						"url":"http://v.qq.com/"
					},
					{
						"type":"click",
						"name":"xxxxxxxxxxxx",
						"key":"V1001_GOOD"
					}]
				}]
			}
 			'''

			access_token = smart_str(request.POST.get("access_token", None))
			create_menu_url = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s" % (access_token);
			menu_json = request.POST.get("menu_json", None)
			#menu_json = menu_json.decode(request.encoding).encode('utf-8')
			json_menu_data = json.loads(menu_json)
			data = json.dumps(json_menu_data, ensure_ascii=False).encode('utf-8')
			
			# or use the value directly
			# data = smart_str(request.POST.get("menu_json", None))			

			req = urllib2.Request(url=create_menu_url, data = data)
			result = urllib2.urlopen(req).read()
			json_data = json.loads(result)					
		else:
			pass

		#if request.GET.has_key('ajax'): 
		if request.is_ajax():
			try:
				response = HttpResponse(json.dumps(json_data),content_type="application/json")
				print response				
			except:
				response = HttpResponse("fail",content_type="application/xml")
			return response
		else:
			return render(request, template, {})
	else:
		return "welcome to zakkabag"
