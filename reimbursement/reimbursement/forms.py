from django import forms
from .models import InvoiceImage

class InvoiceImageForm(forms.ModelForm):
  #image = forms.ImageField()
  class Meta:
    model = InvoiceImage
    fields = ['image']