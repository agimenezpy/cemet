# -*- coding: iso-8859-1 -*-
from django.db import models
from django.contrib import admin
from django.contrib.gis.db import models as gismodels
from myfields import DateTimeField,BigAutoField
from settings import DATABASE_ENGINE

class Pais(models.Model):
    fips = models.CharField(u"c�digo de fips", max_length=2, primary_key=True)
    iso2 = models.CharField(u"c�digo de ISO 2", max_length=2, unique=True)
    iso3 = models.CharField(u"c�digo de ISO 3", max_length=3, unique=True)
    nombre = models.CharField(u"nombre", max_length=60)
    
    def __unicode__(self):
        return u"%s - %s" % (self.fips, self.nombre)
    
    class Meta:
        verbose_name = u"pa�s"
        verbose_name_plural = "paises"
        db_table = "pais"
        ordering = ['fips']

class Observatorio(models.Model):
    nombre = models.CharField(u"nombre", max_length=80)
    dependencia = models.CharField(u"dependencia", max_length=80)
    siglas = models.CharField(u"siglas", max_length=30,null=True)
    sitio_web = models.URLField(u"sitio web",null=True,blank=True)
    contacto = models.TextField(u"contacto",null=True)
    pais = models.ForeignKey(Pais, verbose_name=u"pa�s")
    
    def __unicode__(self):
        return u"%s - %s" % (self.siglas, self.nombre)
    
    class Meta:
        verbose_name = u"observatorio"
        verbose_name_plural = "observatorios"
        db_table = "observatorio"

class VariableManager(models.Manager):
    def get(self, **kargs):
        try:
            return super(VariableManager, self).get(**kargs)
        except:
            return None

class Variable(models.Model):
    codigo = models.CharField(u"c�digo",max_length=8, primary_key=True)
    descripcion = models.CharField(u"descripci�n", max_length=80)

    if DATABASE_ENGINE == 'mysql':
        objects = VariableManager()
    
    def __unicode__(self):
        return u"%s - %s" % (self.codigo, self.descripcion)
    
    class Meta:
        verbose_name = "variable"
        verbose_name_plural = "variables"
        db_table = "variable"
        ordering = ['codigo']

class Estacion(gismodels.Model):
    TIPOS_ESTACIONES = (
        ('M', u"Meteorol�gica"),
        ('H', u"Hidrol�gica"),
        ('X', u"Hidrometeorol�gica")
    )
    codigo = models.CharField(u"c�digo", null=True, max_length=40, unique=True)
    wmo = models.CharField(u"c�digo WMO", null=True, max_length=6,unique=True)
    icao = models.CharField(u"c�digo ICAO", null=True, max_length=4,unique=True)
    nombre = models.CharField(u"nombre",max_length=80)
    tipo = models.CharField(u"tipo de estaci�n", max_length=1, choices=TIPOS_ESTACIONES)
    ubicacion = gismodels.PointField(u"Ubicaci�n Geogr�fica", srid=4326)
    elevacion = models.SmallIntegerField(u"elevaci�n", help_text="metros")
    observatorio = models.ForeignKey(Observatorio, verbose_name=u"observatorio")
    variables = models.ManyToManyField(Variable, through='Medidor')
    objects = gismodels.GeoManager()
    
    def __unicode__(self):
        return u"%s -  %s" % (self.id, self.nombre)
    
    class Meta:
        verbose_name = u"estaci�n"
        verbose_name_plural = "estaciones"
        db_table = "estacion"
        ordering = ["id"]

class Unidad(models.Model):
    codigo = models.CharField(u"c�digo", max_length=10, primary_key=True)
    simbolo = models.CharField(u"s�mbolo", max_length=10)
    descripcion = models.CharField(u"descripci�n", max_length=50)

    def __unicode__(self):
        return u"%s - %s" % (self.codigo, self.simbolo)
    
    class Meta:
        verbose_name = u"unidad"
        verbose_name_plural = "unidades"
        db_table = "unidad"
        ordering = ["simbolo"]

class Medidor(models.Model):
    estacion = models.ForeignKey(Estacion, verbose_name=u"estaci�n")
    variable = models.ForeignKey(Variable, verbose_name=u"variable")
    comentarios = models.TextField(u"comentarios",null=True)
    unidad = models.ForeignKey(Unidad)
    
    def __unicode__(self):
        return u"%s - %s (%s)" % (self.estacion.nombre, self.variable.codigo, self.unidad.simbolo)
    
    class Meta:
        verbose_name = "medidor"
        verbose_name_plural = "medidor"
        db_table = "medidor"
        ordering = ["estacion", "variable", "id"]

class Medida(models.Model):
    id = BigAutoField(primary_key=True)
    tiempo = DateTimeField(u"tiempo de medici�n")
    medidor = models.ForeignKey(Medidor)
    valor = models.DecimalField(u"valor de medici�n", max_digits=10,decimal_places=4)
    
    class Meta:
        verbose_name = "medida instantanea"
        verbose_name_plural = "medidas"
        db_table = "medida"
        unique_together = ('tiempo', 'medidor')

    def __unicode__(self):
        return u"(%s) %s %s" % (self.id, self.valor)