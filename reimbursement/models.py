
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
    invoice_category_option = [
        ('1', _('Operation')),
        ('2', _('Market')),
        ('3', _('R&D')),
    ]

    invoice_project_option = [
        ('1', _('Meals')),
        ('2', _('Rent')),
        ('3', _('Travel')),
    ] 

    invoice_status_option = [
        ('notsubmitted', _('not submitted')),
        ('inprogress', _('in progress')),
        ('approved', _('approved')),
    ] 

    total_amount = models.DecimalField(_('total amount'), decimal_places=2, max_digits=20, blank=False, null=False)
    currency = models.CharField(_('currency'), max_length=30,blank=False, null=False)
    base_amount = models.DecimalField(_('base amount'), decimal_places=2, max_digits=20, blank=False, null=False)
    VAT_amount = models.DecimalField(_('VAT amount'), decimal_places=2, max_digits=20, blank=True, null=True)
    invoice_type = models.CharField(_('invoice type'), max_length=30, blank=False, null=False)
    invoice_date = models.DateField(_('invoice date'), blank=False, null=False)
    invoice_category = models.CharField(_('invoice category'), choices=invoice_category_option, max_length=30, blank=False, null=False)
    invoice_project = models.CharField(_('invoice project'), choices=invoice_project_option, max_length=30, blank=False, null=False)
    comments = models.CharField(_('invoice comments'), max_length=30, blank=True, null=True)
    invoice_status = models.CharField(_('invoice status'), choices=invoice_status_option, max_length=30, blank=True, null=True, default="notsubmitted")
    reimbursement_request = models.ForeignKey('ReimbusementRequest', default=None, blank=True, null=True, verbose_name=_("reimbusement request"))

    def __unicode__(self): 
        return "IV{0:0>5d}-{1}-{2}".format(self.id, self._get_FIELD_display(self._meta.get_field('invoice_category')), \
        	self._get_FIELD_display(self._meta.get_field('invoice_project')))

    def get_absolute_url(self):
        return reverse("invoice_detail", kwargs={"pk": self.pk })

    class Meta:
        verbose_name = _("invoice")
        verbose_name_plural = _("invoice")

pre_save.connect(total_amount_saved, sender=Invoice)

class ReimbusementRequest(models.Model):
    reimbursement_status_option = [
        ('inprogress', _('in progress')),
        ('approved', _('approved')),
        ('rejected', _('rejected')),        
    ] 

    # Number = models.CharField(_('reimbursement number'), max_length=30, blank=True, null=False)
    status = models.CharField(_('reimbursement status'), choices=reimbursement_status_option, max_length=30, blank=True, null=True, default="inprogress")
    # current_approver = models.CharField(_('current approver'), max_length=30, blank=True, null=False)
    total_amount = models.DecimalField(_('total amount'), decimal_places=2, max_digits=20, blank=False, null=False)

    class Meta:
        verbose_name = _("reimbusement request")
        verbose_name_plural = _("reimbusement request")