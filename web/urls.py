from django.conf.urls.defaults import *
from observacion.models import Estacion

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^cemet/', include('cemet.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/(.*)', admin.site.root),
    (r'^$', 'cemet.observacion.views.default', {'page' : 'index'}),
    (r'^static/([^/]+)$', 'cemet.observacion.views.default'),
    (r'^accounts/', include('django.contrib.auth.urls')),
    (r'^accounts/$', 'cemet.observacion.views.account', {'section':'profile'})
)