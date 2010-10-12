# -*- coding: iso-8859-1 -*-
from django.contrib import admin
from django.conf import settings
from observacion.models import *

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

class EstacionAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'tipo', 'codigo', 'norm_ubicacion', 'elevacion']
    list_filter = ['tipo']
    list_per_page = 15
    fieldsets = (
        (None, {
            'fields' : ('codigo','nombre', 'tipo', 'observatorio')
        }),
        (u"Información Geográfica", {
            'fields' : ('longitud', 'latitud', 'elevacion')
        })
    )
    
    def norm_ubicacion(self, obj):
        x, y = obj.longitud, obj.latitud
        
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
    list_display = ['id', 'tiempo', 'sensor', 'valor']
    list_per_page = 15
    list_filter = ['tiempo']
    raw_id_fields = ("sensor",)

class SensorAdmin(admin.ModelAdmin):
    list_display = ['id', 'estacion', 'descripcion','variable', 'unidad','intervalo']
    list_per_page = 15

admin.site.register(Pais, PaisAdmin)
admin.site.register(Observatorio, ObservatorioAdmin)
admin.site.register(Variable, VariableAdmin)
admin.site.register(Estacion, EstacionAdmin)
#admin.site.register(Medida, MedidaAdmin)
admin.site.register(Sensor, SensorAdmin)