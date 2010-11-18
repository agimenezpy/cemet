#!/usr/bin/env python
from osgeo import ogr
import os
from pymongo import Connection,GEO2D

def find_and_insert(fips):
    ds = ogr.Open("../../map/world_borders.shp")
    if ds:
        ly = ds.ExecuteSQL("SELECT * FROM world_borders WHERE FIPS = %s" % fips)
        feat = ly.next()
        if feat:
            pais = {
                "fips" : feat.GetField(0),
                "iso2" : feat.GetField(1),
                "iso3" : feat.GetField(2),
                "name" : feat.GetField(4).upper(),
                "location" : {"lon" : feat.GetField(9), "lat" : feat.GetField(10)} 
            }
            con = Connection()
            db = con.observacion
            db.country.insert(pais)
        ds.Release()

def create_indexes():
    con = Connection()
    db = con.observacion
    db.country.create_index([("location", GEO2D)])
    db.country.create_index("iso2")

if __name__ == '__main__':
    find_and_insert("PA")
    create_indexes()

