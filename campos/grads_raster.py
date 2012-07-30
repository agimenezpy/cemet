# -*- coding: latin-1 -*-
#!/usr/bin/env python
import ConfigParser
import sys
from datetime import datetime
from grads import GaNum
from os import path,mkdir,sep,remove
from math import ceil,floor
from simplejson import dumps
from PIL import Image
from osgeo import gdal,osr
import time
from globalmaptiles import GlobalMercator

C0 = 180.0/256
RESOLUTIONS = [C0/2**i for i in range(0,21)]
GMERC = GlobalMercator()

PRIORITY = {"shaded": 10, "vector": 30, "grdfill": 10, "barb" : 30, "contour" : 30}

PRE = u"""
clear
set display color white
set mpdraw off
set mproj scaled
set grads off
set grid off
set parea 0 11 0 8.5
set clopts -1 -1 0.12
set csmooth on
set xlab off
set ylab off
set lat %d %d
set lon %d %d
"""

COLORBAR = u"""
set parea 0 10 0 8
run %s.gs
d %s
run cbarn_only.gs 1 0 5 8.3
"""
#run cbarn_only.gs 1 0 0.1 4

POST = u"""
printim %s.%s x%d y%d -t 0
"""

def getClevs(fh,ga,expr,min,max,steps):
    if max == 0:
        ga("d max(max(max(%s,lon=%s,lon=%s),lat=%s,lat=%s),t=1,t=%s)" %
           (expr,LONS[0],LONS[1],LATS[0],LATS[1],fh.nt))        
        max = float(ga.rline(ga.rline()).split()[3])
        if max > 0:
            max = ceil(max)
        else:
            max = floor(max)
    if min == 9999:
        ga("d min(min(min(%s,lon=%s,lon=%s),lat=%s,lat=%s),t=1,t=%s)" %
           (expr,LONS[0],LONS[1],LATS[0],LATS[1],fh.nt))
        min = float(ga.rline(ga.rline()).split()[3])
        if min > 0:
            min = floor(min)
        else:
            min = ceil(min)
    lvls = ""
    cur = min
    while (cur < max):
        lvls += "%s " % cur
        cur += steps
    lvls += "%s" % cur
    return lvls

def crop_file(filename,ext):
    im = Image.open(filename+"."+ext)
    for xi in range(0, im.size[0]):
        if im.getpixel((xi,7)) != 0:
            break
    for xf in range(xi, im.size[0]):
        if im.getpixel((xf,7)) == 0 and im.getpixel((xf-1,7)) != 0 and xf - xi > 10:
            break
    im = im.crop((xi-1,0,xf+1,24)) #.convert('RGBA')
    im.save(filename+"."+ext, transparency=0)
    del(im)

def georeference_file(filename, ulx, uly, lrx, lry):
    im = Image.open(filename + ".png")
    im = im.convert('RGBA')
    im.save(filename+".tif", "TIFF")
    del(im)
    remove(filename + ".png")

    srs = osr.SpatialReference()
    srs.ImportFromProj4('+proj=longlat  +datum=NAD83')
    dst_ds = gdal.Open(filename+".tif", gdal.GA_Update)
    dst_ds.SetGeoTransform([ulx, (lrx - ulx)/float(dst_ds.RasterXSize), 0.0, uly, 0.0, (lry - uly) / float(dst_ds.RasterYSize)])
    dst_ds.SetProjection( srs.ExportToWkt() )
    del(dst_ds)

def getLLtoPX(lon,lat,z):
    tx = floor((lon+180)/RESOLUTIONS[z]/256)
    ty = floor((90-lat)/RESOLUTIONS[z]/256)
    return (int(tx),int(ty))

def getPXtoLL(px,py,z):
    lon = px*RESOLUTIONS[z]*256 - 180
    lat = 90 - py*RESOLUTIONS[z]*256
    return (lon,lat)

def get_ll(x0, y0, x1, y1, z):
    tx0, ty0 = getLLtoPX(x0, y0,z)
    tx1, ty1 = getLLtoPX(x1, y1,z)
    ty0 += 1
    tx1 += 1

    W, H = (tx1 - tx0)*256, (ty0 - ty1)*256
    lon0, lat0 = getPXtoLL(tx0, ty0,z)
    lon1, lat1 = getPXtoLL(tx1, ty1,z)
    return (lon0,lat0,lon1,lat1),(W,H),(tx0,ty0,tx1,ty1)

def getLLGoogle(x0, y0, x1, y1, z):
    mx0,my0 = GMERC.LatLonToMeters(y0,x0)
    mx1,my1 = GMERC.LatLonToMeters(y1,x1)
    tx0,ty0 = GMERC.MetersToTile(mx0,my0,z)
    tx1,ty1 = GMERC.MetersToTile(mx1,my1,z)

    lat0, lon0, d1, d2 = GMERC.TileLatLonBounds(tx0,ty0,z)
    lat1, lon1, d1, d2 = GMERC.TileLatLonBounds(tx1+1,ty1+1,z)

    tx0,ty0 = GMERC.GoogleTile(tx0,ty0,z)
    tx1,ty1 = GMERC.GoogleTile(tx1,ty1,z)
    ty0 += 1
    tx1 += 1

    W, H = (tx1 - tx0)*256, (ty0 - ty1)*256
    return (lon0,lat0,lon1,lat1),(W,H),(tx0,ty0,tx1,ty1)

def generate_tiles(filename, zoom, tiles, size):
    print zoom,tiles,size
    im = Image.open(filename + ".png")
    if not path.exists(filename):
        mkdir(filename)
    zoom_dir = sep.join((filename, str(zoom)))
    if not path.exists(zoom_dir):
        mkdir(zoom_dir)

    for x in range(tiles[0],tiles[2]):
        for y in range(tiles[3],tiles[1]):
            tx = x - tiles[0]
            ty = y - tiles[3]
            sim = im.crop((tx*256,ty*256,(tx+1)*256,(ty+1)*256)).convert("RGBA")
            sim.save(zoom_dir + "%s%d_%d.png" % (sep,x,y))
            del(sim)
    remove(filename + ".png")

def cut_tiles(filename, zoom, tiles, size):
    im = Image.open(filename + ".png")
    if not path.exists(filename):
        mkdir(filename)
    zoom_dir = sep.join((filename, str(zoom)))
    if not path.exists(zoom_dir):
        mkdir(zoom_dir)

    for x in range(tiles[0],tiles[2]):
        for y in range(tiles[3],tiles[1]):
            tx = x - tiles[0]
            ty = y - tiles[3]
            sim = im.crop((tx*256,ty*256,(tx+1)*256,(ty+1)*256)).convert("RGBA")
            sim.save(zoom_dir + "%s%d_%d.png" % (sep,x,y))
            del(sim)


if __name__ == '__main__':
    MODEL_INFO = {}
    if len(sys.argv) > 2:
        ga = GaNum(Echo=False,Window=False)
        cfg = ConfigParser.RawConfigParser()
        cfg.read(sys.argv[1])
        fh = ga.open(sys.argv[2])
        #if len(sys.argv) == 4 and match("[0-9]+x[0-9]+",sys.argv[3]):
        #    W,H = map(int,sys.argv[3].split("x"))
        prefname = None
        if len(sys.argv) == 4:
            prefname = sys.argv[3]
        qh = ga.query('dims')
        fecha = datetime.strptime(qh.time[0],"%HZ%d%b%Y")
        if cfg.get("DEFAULT", "date") == "yes":
            outdir = cfg.get("DEFAULT","directory") + "/" + fecha.strftime("%Y%m%d%H")
        else:
            outdir = cfg.get("DEFAULT","directory") + "/last"

        zlevels = map(int, cfg.get("DEFAULT", "zoom").split(","))
        bounds = map(float, cfg.get("DEFAULT", "bounds").split())

        LATS = (bounds[1],bounds[3])
        LONS = (bounds[0],bounds[2])

        if not path.exists(outdir):
            mkdir(outdir)
        MODEL_INFO["titulo"] = cfg.get("DEFAULT","titulo") % fecha.strftime("%d/%m/%Y %HZ")
        MODEL_INFO["bounds"] = bounds
        MODEL_INFO["zoom"] = zlevels
        MODEL_INFO["baseUrl"] = cfg.get("DEFAULT","baseUrl")
        MODEL_INFO["layers"] = {}
        MODEL_INFO["date"] = fecha.strftime("%Y%m%d%H")
        MODEL_INFO["time"] = []
        print fh.nt
        clevels = {}

        LODINFO = [None for i in range(0,21)]

        for zoom in zlevels:
            #coords, size, tiles= get_ll(LONS[0],LATS[0],LONS[1],LATS[1],zoom)
            LODINFO[zoom] = getLLGoogle(LONS[0],LATS[0],LONS[1],LATS[1],zoom)
        for s in cfg.sections():
            if (prefname and prefname != cfg.get(s,"name")) or cfg.has_option(s,"draw") and cfg.get(s, "draw") == "no" \
            or not cfg.has_option(s,"output"):
                continue
            print s
            nombre = cfg.get(s,"name")
            if not path.exists(outdir+sep+nombre):
                mkdir(outdir+sep+nombre)
            if not MODEL_INFO["layers"].has_key(nombre):
                MODEL_INFO["layers"][nombre] = {"nombre":cfg.get(s,"name"),
                                                "descripcion":cfg.get(s,"desc"),
                                                "unidad" :  cfg.get(s,"unit"),
                                                "type" : cfg.get(s, "output"),
                                                "priority" : PRIORITY[cfg.get(s,"output")]}
            LAYER = MODEL_INFO["layers"][nombre]
            unit = cfg.get(s,"unit").decode("latin-1")
            if cfg.has_option(s,'clevs'):
                clevels[s] = cfg.get(s,'clevs')

            if cfg.has_option(s,"cparam") and not clevels.has_key(s) and not cfg.has_option(s,"vector"):
                steps = 1
                min, max, steps = map(int,cfg.get(s,'cparam').split(","))
                max = 0
                if min == -1:
                    min = 9999
                if max == -1:
                    max = 0
                clevels[s] = getClevs(fh,ga,s,min,max,steps)
                print clevels[s]
            for i in range(1,fh.nt+1):
                if (cfg.has_option(s,"once") and i > 1):
                    break
                ga('set t %d' % i)
                qh = ga.query('dims')
                ahora = datetime.strptime(qh.time[0],"%HZ%d%b%Y")
                delta = ahora - fecha
                delta = "%02d" % (delta.days*24 + delta.seconds/3600)
                if len(MODEL_INFO["time"]) < fh.nt:
                    MODEL_INFO["time"].append(delta)
                print ahora,delta
                for zoom in zlevels:
                    coords, size, tiles = LODINFO[zoom]
                    ga(PRE % (coords[1],coords[3], coords[0], coords[2]))
                    ga('set gxout %s' % cfg.get(s,'output'))
                    if cfg.has_option(s, 'paleta'):
                        ga('run %s' % cfg.get(s,'paleta'))
                    if cfg.has_option(s, 'ccolor'):
                        ga('set ccolor %s' % cfg.get(s,'ccolor'))
                    n = 0
                    if cfg.has_option(s,'level'):
                        n = int(cfg.get(s,'level'))
                    ga('set lev %d' % n)
                    if clevels.has_key(s):
                        ga('set clevs %s' % clevels[s])
                    if cfg.has_option(s, 'cint'):
                        ga('set cint %s' % cfg.get(s,'cint'))
                    if cfg.has_option(s, 'cmin'):
                        ga('set cmin %s' % cfg.get(s,'cmin'))
                    if cfg.has_option(s, 'cmax'):
                        ga('set cmax %s' % cfg.get(s,'cmax'))
                    if cfg.has_option(s, 'cthick'):
                        ga('set cthick %s' % cfg.get(s,'cthick'))
                    ga('d %s' % s)

                    filedscp = [outdir,nombre]
                    cbarpost = ""
                    if not cfg.has_option(s,"once"):
                        filedscp.append(delta)
                        LAYER["time"] = "true";
                        cbarpost = "_" + filedscp[2]
                    else:
                        filedscp.append("")
                    filename = sep.join(filedscp)
                    ga(POST % (filename, "png", size[0], size[1]))
                    #cut_tiles(filename, zoom, tiles, size)
                    generate_tiles(filename, zoom, tiles, size)
                if cfg.get(s, "output") == 'shaded' or \
                   cfg.get(s, "output") == 'grfill' or \
                   cfg.has_option(s,"colorbar"):
                    ga(COLORBAR % (cfg.get(s,'paleta'), s))
                    filedscp[2] = "COLORBAR" + cbarpost
                    cbarname = sep.join(filedscp)
                    ga(POST % (cbarname, "gif", 640, 480))
                    crop_file(cbarname, "gif")
        fd = open("%s/model_info.json" % cfg.get("DEFAULT","directory"),"w")
        fd.write(dumps(MODEL_INFO))
        fd.close()
    else:
        print "utilizar: %s config salida_brams [wxh]"

