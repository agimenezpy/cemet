# -*- coding: iso-8859-1 -*-
from django.contrib import admin
from django.contrib.gis import admin as admingis
from django.conf import settings
from web.observacion.models import *

class PaisAdmin(admin.ModelAdmin):
    list_per_page = 15
    list_display = ['codigo_pais', 'nombre']
    search_fields = ['nombre']

class ObservatorioAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'siglas', 'pais']
    search_fields = ['siglas']
    
class VariablesInline(admin.TabularInline):
    model = Sensor
    raw_id_fields = ("variable",)
    extra = 1

class EstacionAdmin(admingis.GeoModelAdmin):
    list_display = ['id', 'nombre', 'tipo', 'codigo', 'norm_ubicacion', 'elevacion']
    list_filter = ['tipo']
    list_per_page = 15
    # Para WMS local 
    #openlayers_url = '/media/js/OpenLayers.js'
    #default_zoom = 10
    #max_resolution = 0.02197265625
    #num_zoom = 1
    #max_extent = "-62.643768, -27.588337, -54.243896, -19.296669"
    #wms_url = 'http://localhost/wms?'
    #wms_layer = 'default'
    #display_wkt = True
    
    # Para Google
    openlayers_url = '/media/js/OpenLayers.js'
    default_zoom = 10
    max_resolution = 156543.0339
    num_zoom = 17
    max_extent = '-20037508,-20037508,20037508,20037508'
    map_template = 'gis/admin/google.html'
    extra_js = ['http://maps.google.com/maps?file=api&amp;v=2&amp;key=%s' % settings.GOOGLE_MAPS_API_KEY]
    units = 'm'
    map_srid = 900913
    display_srid = 4326
    fieldsets = (
        (None, {
            'fields' : ('codigo','nombre', 'tipo', 'observatorio')
        }),
        (u"Información Geográfica", {
            'fields' : ('ubicacion', 'elevacion')
        })
    )
    
    def norm_ubicacion(self, obj):
        x, y = obj.ubicacion.x, obj.ubicacion.y
        
        xd = 'E'
        yd = 'N'
        if x < 0:
            xd = 'O'
        if y < 0:
            yd = 'S'
        x, y = abs(x), abs(y)
        return u"%dº%2d'%s %dº%d'%s" % (x, abs(x - int(x))*60, xd, y, abs(y - int(y))*60, yd)
    norm_ubicacion.short_description = u"ubicación geográfica"
    inlines = [VariablesInline]

class VariableAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'descripcion']
    list_per_page = 15

#class MedidaAdmin(admin.ModelAdmin):
#    list_display = ['id', 'tiempo', 'sensor', 'valor']
#    list_per_page = 15
#    list_filter = ['tiempo']
#    raw_id_fields = ("sensor",)

class SensorAdmin(admin.ModelAdmin):
    list_display = ['id', 'estacion', 'descripcion','variable', 'unidad','intervalo']
    list_per_page = 15

admin.site.register(Pais, PaisAdmin)
admin.site.register(Observatorio, ObservatorioAdmin)
admin.site.register(Variable, VariableAdmin)
admin.site.register(Estacion, EstacionAdmin)
#admin.site.register(Medida, MedidaAdmin)
admin.site.register(Sensor, SensorAdmin)