from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from .views import handleCheckSignature
from .debug import handleDebug
from .menu import handleMenuRequest


urlpatterns = [
    url(r'^checksignature$', handleCheckSignature),
    url(r'^menu', handleMenuRequest, name='handleMenuRequest'),
    url(r'^debug', handleDebug, name='handleDebug'),
]