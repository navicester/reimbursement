from django import forms
from .models import InvoiceImage, Invoice

class InvoiceImageForm(forms.ModelForm):
    class Meta:
        model = InvoiceImage
        fields = ['image']

class InvoiceForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(InvoiceForm, self).__init__(*args, **kwargs)
        # self.fields['start'].widget.attrs['class'] ="calenda"
        # self.fields['end'].widget.attrs['class'] ="calenda"

    class Meta:
      model = Invoice
      exclude = ['']    

