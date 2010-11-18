# -*- coding: iso-8859-1 -*-
from django.db import models
from django.contrib import admin

class Pais(models.Model):
    fips = models.CharField(u"código de fips", max_length=2, primary_key=True)
    iso2 = models.CharField(u"código de ISO 2", max_length=2, unique=True)
    iso3 = models.CharField(u"código de ISO 3", max_length=3, unique=True)
    nombre = models.CharField(u"nombre", max_length=60)
    
    def __unicode__(self):
        return u"%s - %s" % (self.codigo_pais, self.nombre)
    
    class Meta:
        verbose_name = u"país"
        verbose_name_plural = "paises"
        db_table = "pais"
        ordering = ['codigo_pais']

class Institucion(models.Model):
    nombre = models.CharField(u"nombre", max_length=80)
    dependencia = models.CharField(u"dependencia", max_length=80)
    siglas = models.CharField(u"siglas", max_length=30,null=True)
    sitio_web = models.URLField(u"sitio web",null=True,blank=True)
    contacto = models.TextField(u"contacto",null=True)
    pais = models.ForeignKey(Pais, verbose_name=u"país")
    
    def __unicode__(self):
        return u"%s - %s" % (self.siglas, self.nombre)
    
    class Meta:
        verbose_name = u"institucion"
        verbose_name_plural = "instituciones"
        db_table = "instituciones"

class VariableManager(models.Manager):
    def get(self, **kargs):
        try:
            return super(VariableManager, self).get(**kargs)
        except:
            return None

class Variable(models.Model):
    codigo = models.CharField(u"código",max_length=8, primary_key=True)
    descripcion = models.CharField(u"descripción", max_length=80)
    objects = VariableManager()
    
    def __unicode__(self):
        return u"%s - %s" % (self.codigo, self.descripcion)
    
    class Meta:
        verbose_name = "variable"
        verbose_name_plural = "variables"
        db_table = "variable"
        ordering = ['codigo']

class Estacion(models.Model):
    TIPOS_ESTACIONES = (
        ('M', u"Meteorológica"),
        ('H', u"Hidrológica"),
        ('X', u"Hidrometeorológica")
    )
    codigo = models.CharField(u"código", null=True, max_length=40, unique=True)
    wmo = models.CharField(u"código WMO", null=True, max_length=6,unique=True)
    icao = models.CharField(u"código ICAO", null=True, max_length=4,unique=True)
    nombre = models.CharField(u"nombre",max_length=80)
    tipo = models.CharField(u"tipo de estación", max_length=1, choices=TIPOS_ESTACIONES)
    longitud = models.FloatField(u"longitud",help_text="radianes")
    latitud = models.FloatField(u"latitud",help_text="radianes")
    elevacion = models.SmallIntegerField(u"elevación", help_text="metros")
    institucion = models.ForeignKey(Institucion, verbose_name=u"observatorio")
    variables = models.ManyToManyField(Variable, through='Medidor')
    
    def __unicode__(self):
        return u"%s -  %s" % (self.id, self.nombre)
    
    class Meta:
        verbose_name = u"estación"
        verbose_name_plural = "estaciones"
        db_table = "estacion"
        ordering = ["id"]

class Unidad(models.Model):
    codigo = models.CharField(u"código", max_length=10, primary_key=True)
    simbolo = models.CharField(u"símbolo", max_length=10)
    descripcion = models.CharField(u"descripción", max_length=50)
    
    class Meta:
        verbose_name = u"unidad"
        verbose_name_plural = "unidades"
        db_table = "unidad"
        ordering = ["simbolo"]

class Medidor(models.Model):
    estacion = models.ForeignKey(Estacion, verbose_name=u"estación")
    variable = models.ForeignKey(Variable, verbose_name=u"variable")
    comentarios = models.TextField(u"comentarios",null=True)
    unidad = models.CharField(models.ForeignKey(Unidad),u"unidad de medida", max_length=10)
    
    def __unicode__(self):
        return u"%s - %s (%s)" % (self.estacion.nombre, self.variable.codigo, self.unidad.simbolo)
    
    class Meta:
        verbose_name = "medidor"
        verbose_name_plural = "medidor"
        db_table = "medidor"
        ordering = ["estacion", "variable", "id"]

class Medida(models.Model):
    tiempo = models.DateTimeField(u"tiempo de medición")
    medidor = models.ForeignKey(Medidor)
    valor = models.DecimalField(u"valor de medición", max_digits=6,decimal_places=2)
    
    class Meta:
        verbose_name = "medida instantanea"
        verbose_name_plural = "medidas"
        db_table = "medida"

    def __unicode__(self):
        return u"(%s) %s %s" % (self.id, self.valor)