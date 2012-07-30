# -*- coding: latin-1 -*-
#!/usr/bin/env python
import ConfigParser
import sys
from datetime import datetime
from grads import GaNum
from os import path,mkdir
from math import ceil,floor

W,H = (640,480)
LATS = (-39, -12)
LONS = (-73, -40)

PRE = u"""
clear
set display color white
set mpdraw off
set grads off
set grid off
set parea 0.2 9 0.3 8
set csmooth on
set lat %d %d
set lon %d %d
""" % (LATS[0],LATS[1],LONS[0],LONS[1])

TITULO = u"""
set string 1 c 2 0
set strsiz 0.19
draw string 4.7 8.3 %s
"""

COLORMAP = u"""
run %s.gs
d %s
set strsiz 0.15
draw string 9.35 7.6 BCOLOR
draw string 9.4 7.4 %s
cbarn 1 1 9.2 4.25
"""

CONTOUR = u"""
set ccolor %s
set clopts -1 -1 0.12
d %s
set strsiz 0.15
draw string 9.3 1.1 SLINE
draw string 9.35 0.9 %s
"""

VECTOR = u"""
set ccolor %s
run arrow.gs %s 9.1 0.1 0.3 20 %s
"""

BASEMAP = u"""
set ccolor 4
d %s - %s
"""

POST = u"""
printim %s.gif x%d y%d -t 0
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

if __name__ == '__main__':
    if len(sys.argv) > 2:
        ga = GaNum(Echo=False,Window=False)
        cfg = ConfigParser.RawConfigParser()
        cfg.read(sys.argv[1])
        fh = ga.open(sys.argv[2])
        if len(sys.argv) == 4 and match("[0-9]+x[0-9]+",sys.argv[3]):
            W,H = map(int,sys.argv[3].split("x"))
        qh = ga.query('dims')
        fecha = datetime.strptime(qh.time[0],"%HZ%d%b%Y")
        if cfg.get("DEFAULT", "date") == "yes":
            outdir = cfg.get("DEFAULT","directory") + "/" + fecha.strftime("%Y%m%d%H")
        else:
            outdir = cfg.get("DEFAULT","directory") + "/last"
        if not path.exists(outdir):
            mkdir(outdir)
        r_base = True
        print fh.nt
        clevels = {}
        for i in range(1,fh.nt+1):
            ga('set t %d' % i)
            qh = ga.query('dims')
            ahora = datetime.strptime(qh.time[0],"%HZ%d%b%Y")
            delta = ahora - fecha
            delta = "%02d" % (delta.days*24 + delta.seconds/3600)
            print ahora,delta
            for s in cfg.sections():
                if cfg.has_option(s,"draw") and cfg.get(s, "draw") == "no":
                    continue
                print s
                nombre = cfg.get(s,"name")
                unit = cfg.get(s,"unit").decode("latin-1")
                niveles = [0]
                if cfg.has_option(s,'levels'):
                    niveles = map(int,cfg.get(s,'levels').split(","))
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
                
                if not r_base:
                    ga('set gxout shaded')
                    ga(PRE)
                    ga('set mpdraw on')
                    ga('set mpdset hires')
                    ga('set level %d' % 0)
                    ga(BASEMAP % (s, s))
                    ga("printim %s.gif x%d y%d -t 0" % (outdir + "/BASE", W, H))
                    r_base = True
                if cfg.has_option(s,"colormap"):
                    ga('set gxout shaded')
                    if cfg.has_option(s, 'paleta'):
                        for n in niveles:
                            lev = ""
                            if n > 0:
                                lev = "%03d" % n
                            ga(PRE)
                            ga('set lev %d' % n)
                            if clevels.has_key(s):
                                ga('set clevs %s' % clevels[s])
                            if cfg.has_option(s, 'cint'):
                                ga('set cint %s' % cfg.get(s,'cint'))
                            if cfg.has_option(s, 'cmin'):
                                ga('set cmin %s' % cfg.get(s,'cmin'))
                            if cfg.has_option(s, 'cmax'):
                                ga('set cmax %s' % cfg.get(s,'cmax'))
                            ga(TITULO % ("TIEMPO DE PRONOSTICO: %s h %s" % (delta, ahora.strftime("%H %Z %a, %d %b %Y").title())))
                            ga(COLORMAP % (cfg.get(s,'paleta'), s, unit))
                            ga(POST % ("%s/COLOR_%s%s_%s" % (outdir,nombre,lev,delta), W, H))
                if cfg.has_option(s,"contour"):
                    ga(PRE)
                    ga('set gxout contour')
                    if cfg.has_option(s, 'ccolor'):
                        for n in niveles:
                            lev = ""
                            if n > 0:
                                lev = "%03d" % n
                            ga(PRE)
                            ga('set lev %d' % n)
                            if clevels.has_key(s):
                                ga('set clevs %s' % clevels[s])
                            if cfg.has_option(s, 'cint'):
                                ga('set cint %s' % cfg.get(s,'cint'))
                            if cfg.has_option(s, 'cmin'):
                                ga('set cmin %s' % cfg.get(s,'cmin'))
                            if cfg.has_option(s, 'cmax'):
                                ga('set cmax %s' % cfg.get(s,'cmax'))
                            ga(TITULO % ("TIEMPO DE PRONOSTICO: %s h %s" % (delta, ahora.strftime("%H %Z %a, %d %b %Y").title())))
                            ga(CONTOUR % (cfg.get(s,'ccolor'), s, unit))
                            ga(POST % ("%s/CONTOUR_%s%s_%s" % (outdir,nombre,lev,delta), W, H))
                if cfg.has_option(s,"vector"):
                    ga(PRE)
                    ga('set gxout vector')
                    if cfg.has_option(s, 'ccolor'):
                        for n in niveles:
                            lev = ""
                            if n > 0:
                                lev = "%03d" % n
                            ga(PRE)
                            ga('set lev %d' % n)
                            ga(TITULO % ("TIEMPO DE PRONOSTICO: %s h %s" % (delta, ahora.strftime("%H %Z %a, %d %b %Y").title())))
                            ga(VECTOR % (cfg.get(s,'ccolor'), s, unit))
                            ga(POST % ("%s/VECTOR_%s%s_%s" % (outdir,nombre,lev,delta), W, H))                
    else:
        print "utilizar: %s config salida_brams [wxh]"
