from django.contrib import admin
# Register your models here.
# from .forms import SignUpForm
from .models import Invoice

class InvoiceAdmin(admin.ModelAdmin):
	list_display = [ 
		"total_amount", 
		"currency", 
		"base_amount",
		"VAT_amount",
		"invoice_type",
		"invoice_date",
		"invoice_category",
		"invoice_project",
		"comments",
		"invoice_status",
		"reimbursement_request"
		]
	class Meta:
		model = Invoice

admin.site.register(Invoice, InvoiceAdmin)
		