# -*- coding: utf-8 -*- 
#!/usr/bin/env python
import re
from django.contrib.gis import geos
from pymongo import Connection,GEO2D

def safe(array):
    if len(array) > 0:
        return array[0]
    else:
        return ""

def escribir_txt():
    fd = open("../../observacion/sql/estacion.pgsql")
    est = open("estaciones_py.txt","w")
    for line in fd.readlines()[24:51]:
        (id, nombre, tipo, elevacion, comentario, propietario_id, ubicacion) = \
        line.split("\t")
        wmo = re.findall("\d+",comentario)
        icao = re.findall("\|(\w+)", comentario)
        point = geos.fromstr(ubicacion)
        est.write("%s,%s,%s,%s,%s,%s,%.5f,%.5f\n" % (id,nombre,tipo,elevacion,safe(wmo),safe(icao),point[0],point[1]))
    est.close()
    fd.close()

def importar_py():
    fd = open ("estaciones_py.txt")
    con = Connection()
    db = con.observacion
    for line in fd.readlines():
        (id, nombre, codename, tipo, elevacion, wmo, icao, lon, lat) = \
        line.strip().split(",")
        estacion = {}
        estacion["name"] = nombre
        estacion["codename"] = codename
        estacion["type"] = "METEOROLOGICA"
        estacion["elevation"] = int(elevacion)
        if wmo:
            estacion["wmo"] = int(wmo)
        if icao:
            estacion["icao"] = icao
        estacion["location"] = {"lon" : float(lon), "lat" : float(lat)}
        estacion["country"] = "PY"
        db.station.insert(estacion)
    #estacion = {}
    #estacion["name"] = "Facultad Politécnica"
    #estacion["type"] = "Meteorológica"
    #estacion["codename"] = "FPUNA"
    #estacion["elevation"] = 138
    #estacion["location"] = {"lon" : -57.521369, "lat" : -25.336534}
    #estacion["country"] = "PY"
    #db.station.insert(estacion)
    fd.close()

def create_indexes():
    con = Connection()
    db = con.observacion
    db.station.create_index([("location", GEO2D)])
    db.station.create_index("codename")
    db.station.create_index("wmo")
    db.station.create_index("icao")

def agregar_variables():
    con = Connection()
    db = con.observacion
    est = db.station.find_one({"codename": "FPUNA"})
    est["variables"] = [{
        "name" : "DD",
        "description" : "DIRECCION DEL VIENTO",
        "unit" : "deg",
        "data" : "FPUNA_0002"
    },{
        "name" : "RH",
        "description" : "HUMEDAD RELATIVA",
        "unit" : "%",
        "data" : "FPUNA_0004"
    },{
        "name" : "PCP",
        "description" : "PRECIPITACION",
        "unit" : "mm",
        "data" : "FPUNA_0003"
    },{
        "name" : "P",
        "description" : "PRESION",
        "unit" : "hPa",
        "data" : "FPUNA_0010"
    },{
        "name" : "RG",
        "description" : "RADIACION GLOBAL",
        "unit" : "w/m2",
        "data" : "FPUNA_0013"
    },{
        "name" : "RN",
        "description" : "RADIACION NETA",
        "unit" : "w/m2",
        "data" : "FPUNA_0014"
    },{
        "name" : "T",
        "description" : "TEMPERATURA DEL AIRE",
        "unit" : "degC",
        "data" : "FPUNA_0008"
    },{
        "name" : "TD",
        "description" : "TEMPERATURA DE ROCIO",
        "unit" : "degC",
        "data" : "FPUNA_0017"
    },{
        "name" : "TS",
        "description" : "TEMPERATURA DEL SUELO",
        "unit" : "degC",
        "data" : "FPUNA_0007"
    },{
        "name" : "FF",
        "description" : "VELOCIDAD DEL VIENTO",
        "unit" : "m/s",
        "data" : "FPUNA_0001"
    }]
    db.station.save(est)

if __name__ == '__main__':
    #escribir_txt()
    #importar_py()
    #create_indexes()
    #agregar_variables()