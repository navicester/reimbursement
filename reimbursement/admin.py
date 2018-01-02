from django.contrib import admin
# Register your models here.
# from .forms import SignUpForm
from .models import Invoice, ReimbusementRequest, ApprovalChain

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

class InvoiceInline(admin.TabularInline):
    model = Invoice  
    extra = 0

class ReimbusementRequestAdmin(admin.ModelAdmin):
    list_display = [ 
        "status", 
        "total_amount", 
        ]

    view_on_site = False

    inlines = [
        InvoiceInline,
    ]
            
    class Meta:
        model = ReimbusementRequest

class ApprovalChainAdmin(admin.ModelAdmin):
    list_display = [ 
        "prev_approver", 
        "current_approver", 
        ]

    view_on_site = False
  
    class Meta:
        model = ApprovalChain

admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(ReimbusementRequest, ReimbusementRequestAdmin)
admin.site.register(ApprovalChain, ApprovalChainAdmin)
        