 # -*- coding: utf-8 -*-

from django import forms
from .models import InvoiceImage, Invoice
from django.forms.models import modelformset_factory, BaseModelFormSet
from django.utils.translation import ugettext_lazy as _
from django.forms.widgets import RadioChoiceInput
from django.forms.widgets import ClearableFileInput, CheckboxInput, Input
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape, format_html, html_safe
from django.utils.html import escape
from django.utils.encoding import force_unicode
from django.utils.translation import ugettext_lazy

class ImageFileInput(ClearableFileInput):

    # initial_text = ugettext_lazy('Currently')
    # input_text = ugettext_lazy('Change')
    # clear_checkbox_label = ugettext_lazy('Clear')

    #why nothing show if add this variant????
    # template_with_initial = (
    #     '%(initial_text)s: <a href="%(initial_url)s">%(initial)s</a> '
    #     '%(clear_template)s<br />%(input_text)s: %(input)s'
    # )
    # template_with_clear = '%(clear)s <label for="%(clear_checkbox_id)s">%(clear_checkbox_label)s</label>'

    template_with_initial = ('<p class="file-upload">%s</p>'
                            % forms.ClearableFileInput.template_with_initial)
    template_with_clear = ('<span class="clearable-file-input">%s</span>'
                           % forms.ClearableFileInput.template_with_clear)

    # https://stackoverflow.com/questions/27071648/django-imagefield-widget-to-add-thumbnail-with-clearable-checkbox
    def render(self, name, value, attrs=None):
        substitutions = {
            'initial_text': self.initial_text,
            'input_text': self.input_text,
            'clear_template': '',
            'clear_checkbox_label': self.clear_checkbox_label,
        }
        template = '%(input)s'
        substitutions['input'] = super(ClearableFileInput, self).render(name, value, attrs)

        if self.is_initial(value):
            template = self.template_with_initial
            substitutions.update(self.get_template_substitution_values(value))
            ### 
            substitutions['initial'] = (
                '<img src="%s" alt="%s" style="max-width: 200px; max-height: 200px; border-radius: 5px;" /><br/>' % (
                    escape(value.url), escape(force_unicode(value))
                )
            )
            ###
            if not self.is_required:
                checkbox_name = self.clear_checkbox_name(name)
                checkbox_id = self.clear_checkbox_id(checkbox_name)
                substitutions['clear_checkbox_name'] = conditional_escape(checkbox_name)
                substitutions['clear_checkbox_id'] = conditional_escape(checkbox_id)
                substitutions['clear'] = CheckboxInput().render(checkbox_name, False, attrs={'id': checkbox_id})
                substitutions['clear_template'] = self.template_with_clear % substitutions

        return mark_safe(template % substitutions)

class InvoiceImageForm(forms.ModelForm):
    class Meta:
        model = InvoiceImage
        fields = ['image']

class InvoiceForm(forms.ModelForm):

    currency = forms.ChoiceField(
            label=_('currency'),
            choices=Invoice.invoice_currency_option,
            # empty_label = None, #not show enmpty
            required=True
            )      

    invoice_type = forms.ChoiceField(
            label=_('invoice type'),
            choices=Invoice.invoice_type_option,
            # empty_label = None, #not show enmpty
            widget = forms.RadioSelect,
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

        self.fields['image'].widget.attrs['class'] = \
            "weui-uploader__input" if not self.fields['image'].widget.attrs.get("class") \
            else self.fields['image'].widget.attrs.get("class") + " weui-uploader__input"

        # self.fields['end'].widget.attrs['class'] ="calenda"

    class Meta:
        model = Invoice
        exclude = ['invoice_status']    

        widgets = {
            'image': ImageFileInput(),
        }

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