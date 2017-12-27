 # -*- coding: utf-8 -*-

from django import forms
from .models import InvoiceImage, Invoice
from django.forms.models import modelformset_factory

class InvoiceImageForm(forms.ModelForm):
    class Meta:
        model = InvoiceImage
        fields = ['image']

class InvoiceForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(InvoiceForm, self).__init__(*args, **kwargs)
        self.fields['total_amount'].widget.attrs['readonly'] = True
        self.fields['total_amount'].required = False
        self.fields['total_amount'].widget.attrs['placeholder'] = "0.00"
        self.fields['total_amount'].widget.attrs['pattern'] = "[0-9.]*"
        self.fields['total_amount'].widget.attrs['class'] = \
        	"weui-input" if not self.fields['total_amount'].widget.attrs.get("class") \
        	else self.fields['total_amount'].widget.attrs.get("class") + " weui-input"

        self.fields['base_amount'].widget.attrs['placeholder'] = "0.00"
        self.fields['base_amount'].widget.attrs['pattern'] = "[0-9.]*"
        self.fields['base_amount'].widget.attrs['class'] = \
        	"weui-input" if not self.fields['base_amount'].widget.attrs.get("class") \
        	else self.fields['base_amount'].widget.attrs.get("class") + " weui-input"

        self.fields['VAT_amount'].widget.attrs['placeholder'] = "请输入增值税税额"
        self.fields['VAT_amount'].widget.attrs['pattern'] = "[0-9.]*"
        self.fields['VAT_amount'].widget.attrs['class'] = \
        	"weui-input" if not self.fields['VAT_amount'].widget.attrs.get("class") \
        	else self.fields['VAT_amount'].widget.attrs.get("class") + " weui-input"

        # self.fields['end'].widget.attrs['class'] ="calenda"

    class Meta:
      model = Invoice
      exclude = ['invoice_status']    

InvoiceModelFormset = modelformset_factory(Invoice,
                                            form=InvoiceForm,
                                            extra=0)