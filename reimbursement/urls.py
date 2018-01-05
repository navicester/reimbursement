"""reimbursement URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from reimbursement.views import (home, 
    InvoiceCreateView, 
    InvoiceDetailView,
    InvoiceCreateQRScanView,
    InvoiceListView, 
    ApplicationListView,
    ApplicationFromMeListView,
    ApplicationToMeListView,
    ApplicationDetailView,
    
    )

admin.autodiscover()

urlpatterns = [
    url(r'^wechat/', include('wechat.urls')),

    url(r'^admin/', admin.site.urls),
    url(r'^home', home, name="home"),
    url(r'^$', home, name="home"),
    url(r'^invoices$', InvoiceListView.as_view(), name='invoice_list'),
    url(r'^invoices/(?P<pk>\d+)$', InvoiceDetailView.as_view(), name='invoice_detail'),
    url(r'^invoices/create$', InvoiceCreateView.as_view(), name='invoice_create'),
    url(r'^invoices/create/qrscan$', InvoiceCreateQRScanView.as_view(), name='invoice_create_qrscan'),
    url(r'^applications/(?P<pk>\d+)/$', ApplicationDetailView.as_view(), name='application_detail'),
    url(r'^applications/$', ApplicationListView.as_view(), name='application_list'),    
    url(r'^applications/fromme/$', ApplicationFromMeListView.as_view(), name='application_from_me_list'),
    url(r'^applications/tome/$', ApplicationToMeListView.as_view(), name='application_to_me_list'),
    url(r'^accounts/', include('registration.backends.default.urls')),        
]

import os
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
