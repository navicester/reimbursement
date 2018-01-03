
from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import pre_save
from django.conf import settings
# from django.contrib.auth import get_user_model
# User = get_user_model()

class InvoiceImage(models.Model):
    image = models.ImageField(upload_to='img/upload')    

    def __unicode__(self):
        return self.id

def total_amount_saved(sender, instance, *args, **kwargs):
    instance.total_amount = instance.base_amount or 0 + instance.VAT_amount or 0

class Invoice(models.Model):
    invoice_currency_option = [
        ('RMB', _('RMB')),
        ('USD', _('USD')),
        ('EUR', _('EUR')),
    ]

    invoice_type_option = [
        ('ordinary', _('ordinary VAT invoice')),
        ('special', _('special invoice')),
        ('notinvoice', _('not invoice')),
    ]

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
    currency = models.CharField(_('currency'), choices=invoice_currency_option,max_length=30,blank=False, null=False)
    base_amount = models.DecimalField(_('base amount'), decimal_places=2, max_digits=20, blank=False, null=False)
    VAT_amount = models.DecimalField(_('VAT amount'), decimal_places=2, max_digits=20, blank=True, null=True)
    invoice_type = models.CharField(_('invoice type'), choices=invoice_type_option, max_length=30, blank=False, null=False)
    invoice_date = models.DateField(_('invoice date'), blank=False, null=False)
    invoice_category = models.CharField(_('invoice category'), choices=invoice_category_option, max_length=30, blank=False, null=False)
    invoice_project = models.CharField(_('invoice project'), choices=invoice_project_option, max_length=30, blank=False, null=False)
    comments = models.CharField(_('invoice comments'), max_length=30, blank=True, null=True)
    invoice_status = models.CharField(_('invoice status'), choices=invoice_status_option, max_length=30, blank=True, null=True, default="notsubmitted")
    reimbursement_request = models.ForeignKey('ReimbusementRequest', default=None, blank=True, null=True, verbose_name=_("reimbusement request"))

    def __unicode__(self): 
        if self.id:
            return "IV{0:0>5d}-{1}-{2}".format(self.id, self.invoice_category, self.invoice_project)
        else:
            return "unexpected result"

    # def __unicode__(self): 
    #     return "IV{0:0>5d}-{1}-{2}".format(self.id, self._get_FIELD_display(self._meta.get_field('invoice_category')), \
    #         self._get_FIELD_display(self._meta.get_field('invoice_project')))

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
    launcher = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('launcher'),blank=True, null=False)
    current_approver_chain = models.ForeignKey('ApprovalChain', verbose_name=_('current approver chain'),blank=True, null=False)

    class Meta:
        verbose_name = _("reimbusement request")
        verbose_name_plural = _("reimbusement request")

    def __unicode__(self): 
        return "IV{0:0>5d}-{1}".format(self.id, self.status)

    def get_absolute_url(self):
        return reverse("application_detail", kwargs={"pk": self.pk })

# pre_save.connect(user_saved, sender=ReimbusementRequest)

class ApprovalChain(models.Model):
    # type : chain for each project / type
    prev_approver = models.ForeignKey('ApprovalChain', verbose_name=_('prev approver'),blank=True, null=True)
    current_approver = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('current approver'),blank=False, null=False)    

    class Meta:
        verbose_name = _("approval chain")
        verbose_name_plural = _("approval chain")

    def __unicode__(self): 
        return "{0}".format(self.current_approver)
