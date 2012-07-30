# -*- coding: iso-8859-1 -*-
from django.contrib import admin
from django.contrib.gis import admin as gisadmin
from django.conf import settings
from observacion.models import *

class PaisAdmin(admin.ModelAdmin):
    list_per_page = 15
    list_display = ['fips', 'nombre']
    search_fields = ['nombre']

class ObservatorioAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'siglas', 'pais']
    search_fields = ['siglas']
    list_select_related = True
    
class VariablesInline(admin.TabularInline):
    model = Medidor
    raw_id_fields = ("variable",)
    exclude = ("comentarios",)
    #extra = 1

class EstacionAdmin(gisadmin.GeoModelAdmin):
    list_display = ['id', 'nombre', 'tipo', 'codigo', 'norm_ubicacion', 'elevacion']
    list_filter = ['tipo']
    search_fields = ['codigo', 'wmo','icao']
    list_per_page = 15
    # Para Google
    openlayers_url = '/customs/js/OpenLayers.js'
    default_zoom = 10
    max_resolution = 156543.0339
    num_zoom = 17
    max_extent = '-20037508,-20037508,20037508,20037508'
    map_template = 'gis/admin/google.html'
    extra_js = ['http://maps.google.com/maps?file=api&amp;v=2&amp;key=%s' % settings.GOOGLE_MAPS_API_KEY]
    units = 'm'
    map_srid = 900913
    display_srid = 4326
    default_zoom = 6
    fieldsets = (
        (None, {
            'fields' : ('codigo','nombre', 'tipo', 'observatorio')
        }),
        (u"Información Geográfica", {
            'fields' : ('ubicacion', 'elevacion'),
            'classes' : ('collapse',)
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

class MedidaAdmin(admin.ModelAdmin):
    list_display = ['id', 'tiempo', 'medidor', 'valor']
    list_per_page = 15
    list_filter = ['tiempo']
    raw_id_fields = ("medidor",)

class MedidorAdmin(admin.ModelAdmin):
    list_display = ['id', 'estacion', 'variable', 'unidad']
    list_per_page = 15
    list_select_related = True
    raw_id_fields = ('estacion',)

class UnidadAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'simbolo']

admin.site.register(Pais, PaisAdmin)
admin.site.register(Observatorio, ObservatorioAdmin)
admin.site.register(Variable, VariableAdmin)
admin.site.register(Estacion, EstacionAdmin)
admin.site.register(Unidad, UnidadAdmin)
admin.site.register(Medida, MedidaAdmin)
admin.site.register(Medidor, MedidorAdmin)