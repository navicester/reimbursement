
from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import pre_save

class InvoiceImage(models.Model):
	image = models.ImageField(upload_to='img/upload')	

	def __unicode__(self):
		return self.id

def total_amount_saved(sender, instance, *args, **kwargs):
    instance.total_amount = instance.base_amount + instance.VAT_amount

class Invoice(models.Model):
	total_amount = models.DecimalField(_('total amount'), decimal_places=2, max_digits=20, blank=False, null=False)
	currency = models.CharField(_('currency'), max_length=30,blank=False, null=False)
	base_amount = models.DecimalField(_('base amount'), decimal_places=2, max_digits=20, blank=False, null=False)
	VAT_amount = models.DecimalField(_('VAT amount'), decimal_places=2, max_digits=20, blank=True, null=True)
	invoice_type = models.CharField(_('invoice type'), max_length=30, blank=False, null=False)
	invoice_date = models.DateField(_('invoice date'), blank=False, null=False)
	invoice_category = models.CharField(_('invoice category'), max_length=30, blank=False, null=False)
	invoice_project = models.CharField(_('invoice project'), max_length=30, blank=False, null=False)
	comments = models.CharField(_('invoice comments'), max_length=30, blank=True, null=True)

	def __unicode__(self): 
		return "{0}".format(self.id)

	def get_absolute_url(self):
		return reverse("invoice_detail", kwargs={"pk": self.pk })

pre_save.connect(total_amount_saved, sender=Invoice)
