# -*- coding: iso-8859-1 -*-
from django.db import models
from django.contrib import admin
from django.contrib.gis.db import models as gismodels

class Pais(models.Model):
    codigo_pais = models.CharField(u"c�digo de pa�s", max_length=2, primary_key=True)
    nombre = models.CharField(u"nombre de pa�s", max_length=50)
    
    def __unicode__(self):
        return "%s - %s" % (self.codigo_pais, self.nombre)
    
    class Meta:
        verbose_name = u"pa�s"
        verbose_name_plural = "paises"
        db_table = "pais"
        ordering = ['codigo_pais']

class Region(gismodels.Model):
    nombre= models.CharField(u"nombre de regi�n", max_length=50)
    pais = models.ForeignKey(Pais, verbose_name=u"pa�s", null=True, blank=True)
    region = gismodels.PolygonField(u"regi�n de inter�s")
    objects = gismodels.GeoManager()
    
    def __unicode__(self):
        return "%s - %s" % (self.id, self.nombre)
    
    class Meta:
        verbose_name = u"regi�n"
        verbose_name_plural = "regiones"
        db_table = "region"
        ordering = ["id"]

class Organizacion(models.Model):
    nombre = models.CharField(u"nombre de organizaci�n", max_length=50)
    siglas = models.CharField(u"siglas de organizaci�n", max_length=30)
    sitio_web = models.URLField(u"sitio web",null=True)
    pais = models.ForeignKey(Pais, verbose_name=u"pa�s")
    
    def __unicode__(self):
        return "%s - %s" % (self.siglas, self.nombre)
    
    class Meta:
        verbose_name = u"organizaci�n"
        verbose_name_plural = "organizaciones"
        db_table = "organizacion"

class Unidad(models.Model):
    descripcion = models.CharField(u"descripci�n de unidad",max_length=50)
    notacion = models.CharField(u"notaci�n de unidad", max_length=20)
    
    def __unicode__(self):
        return self.notacion
    
    class Meta:
        verbose_name = "unidad"
        verbose_name_plural = "unidades"
        db_table = "unidad_medida"
        ordering = ['id']

class VariableManager(models.Manager):
    def get(self, **kargs):
        try:
            return super(VariableManager, self).get(**kargs)
        except:
            return None

class Variable(models.Model):
    codigo = models.CharField(u"c�digo de variable",max_length=8, primary_key=True)
    descripcion = models.CharField(u"descripci�n de variable", max_length=60)
    unidad = models.ForeignKey(Unidad, verbose_name="unidad")
    valor_inf = models.DecimalField(u"l�mite inferior", max_digits=10, decimal_places=2)
    valor_sup = models.DecimalField(u"l�mite superior", max_digits=10, decimal_places=2)
    objects = VariableManager()
    
    def __unicode__(self):
        return "%s - %s (%s)" % (self.codigo, self.descripcion, self.unidad.notacion)
    
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
    nombre = models.CharField(u"nombre de estaci�n",max_length=50)
    tipo = models.CharField(u"tipo de estaci�n", max_length=1, choices=TIPOS_ESTACIONES)
    ubicacion = gismodels.PointField(u"ubicaci�n geogr�fica")
    elevacion = models.SmallIntegerField(u"elevaci�n", help_text="metros")
    propietario = models.ForeignKey(Organizacion, verbose_name=u"organizaci�n")
    comentario = models.TextField("comentario", null=True)
    variables = models.ManyToManyField(Variable, through='Medidor')
    objects = gismodels.GeoManager()
    
    def __unicode__(self):
        return "%s -  %s" % (self.id, self.nombre)
    
    class Meta:
        verbose_name = u"estaci�n"
        verbose_name_plural = "estaciones"
        db_table = "estacion"
        ordering = ["id"]

class Medidor(models.Model):
    estacion = models.ForeignKey(Estacion, verbose_name=u"estaci�n")
    variable = models.ForeignKey(Variable, verbose_name="variable")
    
    def __unicode__(self):
        return "%s %s (%s)" % (self.estacion.nombre, self.variable.codigo, self.variable.unidad)
    
    class Meta:
        verbose_name = "medidor"
        verbose_name_plural = "medidores"
        db_table = "estacion_variable"
        unique_together = ('variable', 'estacion')

class Medida(models.Model):
    QC_DESCRIPTOR = (
        ('Z', "Preliminar, Sin QC"),
        ('C', "Aprobado"),
        ('S', "Monitoreado"),
        ('V', "Verificado"),
        ('X', "Rechazado/errorneo"),
        ('Q', "En duda"),
        ('G', "Subjectivamento bueno"),
        ('B', "Subjetivamente malo")
    )
    estacion = models.IntegerField(u"estaci�n", db_column="estacion_id")
    variable = models.CharField("variable", db_column="variable_id", max_length=8)
    tiempo = models.DateTimeField(u"tiempo de medici�n")
    valor = models.FloatField(u"valor de medici�n")
    qc_desc = models.CharField(u"descriptor de QC", max_length=1, default='Z', choices=QC_DESCRIPTOR)
    
    class Meta:
        verbose_name = "medida instantanea"
        verbose_name_plural = "medidas"
        db_table = "medida"

    def __unicode__(self):
        return "(%s) %s %s %s" % (self.tiempo, self.variable.codigo, self.estacion.id, self.valor)
    
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
    estacion = models.IntegerField(u"estaci�n", db_column="estacion_id")
    variable = models.CharField("variable", db_column="variable_id", max_length=8)
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
        return "(%s) %s %s %s %s %s" % (self.fecha, self.variable.codigo, self.estacion.id, self.valor, self.tipo, self.agrupacion)