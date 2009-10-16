# -*- coding: iso-8859-1 -*-
from django.db import models
from django.contrib import admin
from django.contrib.gis.db import models as gismodels

class Pais(models.Model):
    codigo_pais = models.CharField(u"c�digo de pa�s", max_length=2, primary_key=True)
    nombre = models.CharField(u"nombre de pa�s", max_length=60)
    
    def __unicode__(self):
        return u"%s - %s" % (self.codigo_pais, self.nombre)
    
    class Meta:
        verbose_name = u"pa�s"
        verbose_name_plural = "paises"
        db_table = "pais"
        ordering = ['codigo_pais']

class Observatorio(models.Model):
    nombre = models.CharField(u"nombre del observatorio", max_length=80)
    siglas = models.CharField(u"siglas del observatorio", max_length=30)
    sitio_web = models.URLField(u"sitio web",null=True,blank=True)
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
    codigo = models.CharField(u"c�digo de variable",max_length=8, primary_key=True)
    descripcion = models.CharField(u"descripci�n de variable", max_length=80)
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
    codigo = models.CharField(u"c�digo de estaci�n", null=True, max_length=40)
    nombre = models.CharField(u"nombre de estaci�n",max_length=80)
    tipo = models.CharField(u"tipo de estaci�n", max_length=1, choices=TIPOS_ESTACIONES)
    ubicacion = gismodels.PointField(u"ubicaci�n geogr�fica",srid=4326)
    elevacion = models.SmallIntegerField(u"elevaci�n", help_text="metros")
    observatorio = models.ForeignKey(Observatorio, verbose_name=u"observatorio")
    variables = models.ManyToManyField(Variable, through='Sensor')
    objects = gismodels.GeoManager()
    
    def __unicode__(self):
        return u"%s -  %s" % (self.id, self.nombre)
    
    class Meta:
        verbose_name = u"estaci�n"
        verbose_name_plural = "estaciones"
        db_table = "estacion"
        ordering = ["id"]

class Sensor(models.Model):
    UNIDADES = (
        (u"�", "Grados"),
        ("km/h","Kilometros por hora"),
        ("hPa","Hectopascal"),
        ("%","Porcentual"),
        (u"�C","Grados Celcius")
    )
    MUESTREO = (
        (3600, "1H"),
        (10800, "3H"),
        (300, "5M"),
        (900, "15M")
    )
    estacion = models.ForeignKey(Estacion, verbose_name=u"estaci�n")
    variable = models.ForeignKey(Variable, verbose_name="variable")
    descripcion = models.CharField(u"descripci�n de sensor", max_length=80,null=True,blank=True)
    unidad = models.CharField(u"unidad de medida", choices=UNIDADES, help_text=u"utilice la notaci�n de UDUNITS", max_length=10)
    intervalo = models.IntegerField(u"intervalo de muestra", choices=MUESTREO, help_text="segundos")
    
    def __unicode__(self):
        return u"%s - %s (%s)" % (self.estacion.nombre, self.variable.codigo, self.unidad)
    
    class Meta:
        verbose_name = "sensor"
        verbose_name_plural = "sensores"
        db_table = "sensor"
        ordering = ["id"]

class Medida(models.Model):
    sensor = models.ForeignKey(Sensor, verbose_name=u"sensor")
    tiempo = models.DateTimeField(u"tiempo de medici�n")
    valor = models.FloatField(u"valor de medici�n")
    
    class Meta:
        verbose_name = "medida instantanea"
        verbose_name_plural = "medidas"
        db_table = "medida"

    def __unicode__(self):
        return u"(%s) %s %s %s" % (self.tiempo, self.variable.codigo, self.estacion.id, self.valor)
    
class Resumen(models.Model):
    TIPO_CONSOLIDACION = (
        ("MAX",u"M�ximo Valor"),
        ("MIN",u"M�nimo Valor"),
        ("AVG",u"Valor Promedio"),
        ("SUM",u"Valor Acumulado")
    )
    CAT_AGRUPACION = (
        ("D","Diario"),
        ("M","Mensual"),
        ("Y","Anual"),
    )
    sensor = models.ForeignKey(Sensor, verbose_name=u"sensor")
    fecha = models.DateField(u"fecha de agrupaci�n")
    valor = models.FloatField(u"valor resumido")
    tipo = models.CharField(u"tipo de resumen", max_length="3", choices=TIPO_CONSOLIDACION)
    agrupacion = models.CharField(u"categor�a de agrupaci�n", choices=CAT_AGRUPACION)
    
    class Meta:
        verbose_name = "medida resumida"
        verbose_name_plural = "medidas resumidas"
        db_table = "resumen"
        abstract = True
    
    def __unicode__(self):
        return u"(%s) %s %s %s %s %s" % (self.fecha, self.variable.codigo, self.estacion.id, self.valor, self.tipo, self.agrupacion)