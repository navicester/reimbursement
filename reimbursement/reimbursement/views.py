# -*- coding: utf-8 -*- 

from django.shortcuts import render, get_object_or_404, redirect
import os
import re
import chardet

from django.core.urlresolvers import reverse
from django.views.generic.base import View, TemplateResponseMixin, ContextMixin, TemplateView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin, ModelFormMixin
from django.http import HttpResponseRedirect
from django.conf import settings
from django.utils.translation import ugettext as _
from django.http import HttpResponse, Http404
from django.forms.models import modelformset_factory
from django.forms import models as model_forms

# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')

#from django import forms
#from django.forms import models as model_forms
from .forms import InvoiceImageForm
from .models import InvoiceImage, Invoice
try:
    import Image
except ImportError:
    from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract'
from django.conf import settings

def decodeTrainInvoice():
    path = os.path.join(settings.MEDIA_ROOT,"20170730090411.png")
    print path
    file = Image.open(path)
    print pytesseract.image_to_string(file,lang='chi_sim')
    
def home(request):

    context = {}
    #context['form'] = model_forms.modelform_factory(InvoiceImage,fields = ['image'])
    form = InvoiceImageForm()
    context['form'] = form
    #decodeTrainInvoice()
   
    if request.method == "POST":
        form = InvoiceImageForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            in_mem_image_file = form.cleaned_data['image']
            file = Image.open(in_mem_image_file)
            output = pytesseract.image_to_string(file,lang='chi_sim')
            context['output'] = output
            return render(request, 'home.html',context)

    s="""
            en: Regular expression is a powerful tool for manipulating text. 
            zh: 汉语是世界上最优美的语言，正则表达式是一个很有用的工具
            """

    fencoding = chardet.detect(s)

    #非ansi
    re_words=re.compile(r"[\x80-\xff]+")
    m =  re_words.search(s,0)            
    context['output'] = m.string.decode(fencoding['encoding']).encode('utf-8')
    
    #unicode
    s = unicode(s.decode(fencoding['encoding']))
    re_words = re.compile(u"[\u4e00-\u9fa5]+")
    m =  re_words.search(s,0)
    res = re.findall(re_words, s)
    context['output2'] = res[0].encode('utf-8')

    return render(request, 'home.html',context)
    
# class OcrView(View):
    # def post(self, request, *args, **kwargs):
        # with PyTessBaseAPI() as api:
            # with Image.open(request.FILES['image']) as image:
                # sharpened_image = image.filter(ImageFilter.SHARPEN)
                # api.SetImage(sharpened_image)
                # utf8_text = api.GetUTF8Text()

        # return JsonResponse({'utf8_text': utf8_text})    

class InvoiceCreateView(CreateView):
    #form_class = OfficeInspectionForm
    # fields = ['total_amount',]
    form_class = model_forms.modelform_factory(Invoice, exclude=["",], )
    template_name = "invoices/invoice_create.html"

    def form_valid(self, form, *args, **kwargs):
        obj = form.save(commit = False)
        obj.save()
        return HttpResponseRedirect(self.get_success_url())

    def post(self, request, *args, **kwargs):        

        form = self.form_class(request.POST or None, request.FILES or None)
        if form.is_valid():
            # obj = form.save(commit = False)
            # obj.save()
            # return reverse("home", kwargs={})
            # return HttpResponseRedirect(self.get_success_url())
            return self.form_valid(args, kwargs)
        else:
            print form.errors
        #     return self.form_invalid(form)

        return super(InvoiceCreateView, self).post(request, *args, **kwargs)

    def get_success_url(self, *args, **kwargs):
        return reverse("invoice_list", kwargs={}) 

class InvoiceListView(ListView): 
    model = Invoice
    template_name = "invoices/invoice_list.html"

    def get_context_data(self, *args, **kwargs):
        context = super(InvoiceListView, self).get_context_data(*args, **kwargs)
        context["objects"] = self.model.objects.all()
        
        return context

