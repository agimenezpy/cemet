from django.conf.urls.defaults import *

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
    #(r'^admin/(.*)', admin.site.root),
    (r'^admin/(.*)', admin.site.urls),
    (r'^$', 'observacion.views.default', {'page' : 'index'}),
    (r'^static/([^/]+)$', 'observacion.views.default'),
    (r'^(?P<format>gviz|json|xml|html|csv)/medida/(?P<sensor_id>\w+)/(?P<fecha>[0-9]{14})/(?P<ws>\d+[YmdHMS])?$', 'observacion.views.medida'),
    (r'^(?P<format>json|xml|html|csv)/(?P<model>\w+)/$', 'observacion.views.list_handler'),
    (r'^(?P<format>json|xml|html|csv)/(?P<model>\w+)/(?P<object_id>\w+)/$', 'observacion.views.detail_handler'),
    (r'^accounts/', include('django.contrib.auth.urls')),
    (r'^accounts/$', 'observacion.views.account', {'section':'profile'})
)

