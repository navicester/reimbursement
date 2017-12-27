 # -*- coding: utf-8 -*-

from django import forms
from .models import InvoiceImage, Invoice
from django.forms.models import modelformset_factory, BaseModelFormSet
from django.utils.translation import ugettext_lazy as _

class InvoiceImageForm(forms.ModelForm):
    class Meta:
        model = InvoiceImage
        fields = ['image']

class InvoiceForm(forms.ModelForm):

    currency = forms.ChoiceField(
            label=_('currency'),
            choices=Invoice.invoice_currency,
            # empty_label = None, #not show enmpty
            required=True
            )      

    def __init__(self, *args, **kwargs):
        super(InvoiceForm, self).__init__(*args, **kwargs)

        self.fields['currency'].widget.attrs['class'] = \
            "weui-select" if not self.fields['currency'].widget.attrs.get("class") \
            else self.fields['currency'].widget.attrs.get("class") + " weui-select"
        # self.fields['currency'].empty_label = None

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

class Invoice2Form(forms.ModelForm):
    class Meta:
      model = Invoice
      fields = ['reimbursement_request']    

class InvoiceModelFormSet(BaseModelFormSet):
    def is_valid(self):
        return super(InvoiceModelFormSet, self).is_valid()

    def add_fields(self, form, index):
        super(InvoiceModelFormSet, self).add_fields(form, index)
        form.fields["is_submit"] = forms.BooleanField(
                label="Check", 
                # widget = forms.Textarea(attrs={'cols': 10, 'rows': 5,}) , 
                required=False)

InvoiceModelFormset = modelformset_factory(Invoice,
                                            form=Invoice2Form,
                                            formset=InvoiceModelFormSet,
                                            extra=0)