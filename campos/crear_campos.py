# -*- coding: latin-1 -*-
#!/usr/bin/env python
import ConfigParser
import sys
from datetime import datetime
from grads import GaNum
from os import path,mkdir
from re import match

W,H = (640,480)

PRE = u"""
clear
set display color white
set mpdraw off
set grads off
set grid off
set parea 0.2 9 0.3 8
set csmooth on
sa
"""

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

if __name__ == '__main__':
    if len(sys.argv) > 2:
        try:
            ga = GaNum(Echo=False,Window=False)
            cfg = ConfigParser.RawConfigParser()
            cfg.read(sys.argv[1])
            fh = ga.open(sys.argv[2])
            if len(sys.argv) == 4 and match("[0-9]+x[0-9]+",sys.argv[3]):
                W,H = map(int,sys.argv[3].split("x"))
            qh = ga.query('dims')
            if cfg.get("DEFAULT", "date"):
                fecha = datetime.strptime(qh.time[0],"%HZ%d%b%Y")
                outdir = cfg.get("DEFAULT","directory") + "/" + fecha.strftime("%Y%m%d%H")
            else:
                outdir = cfg.get("DEFAULT","directory") + "/"
            if not path.exists(outdir):
                mkdir(outdir)
            r_base = True
            print fh.nt
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
                    if not r_base:
                        ga('set gxout shaded')
                        ga(PRE)
                        ga('set mpdraw on')
                        ga('set mpdset hires')
                        ga('set level %d' % 0)
                        ga(BASEMAP % (s, s))
                        ga("printim %s.gif x%d y%d -t 0 -t 4" % (outdir + "/BASE", W, H))
                        r_base = True
                    if cfg.has_option(s,"colormap"):
                        ga('set gxout shaded')
                        if cfg.has_option(s, 'paleta'):
                            for n in niveles:
                                lev = ""
                                if n > 0:
                                    lev = "%04d" % n
                                ga(PRE)
                                ga('set lev %d' % n)
                                ga(TITULO % ("TIEMPO DE PRONOSTICO: %s h %s" % (delta, ahora.strftime("%H %Z %a, %d %b %Y").title())))
                                if cfg.has_option(s, 'cint'):
                                    ga('set cint %s' % cfg.get(s,'cint'))
                                ga(COLORMAP % (cfg.get(s,'paleta'), s, unit))
                                ga(POST % ("%s/COLOR_%s_%s_%s" % (outdir,nombre,lev,delta), W, H))
                    if cfg.has_option(s,"contour"):
                        ga(PRE)
                        ga('set gxout contour')
                        if cfg.has_option(s, 'ccolor'):
                            for n in niveles:
                                lev = ""
                                if n > 0:
                                    lev = "%04d" % n
                                ga(PRE)
                                ga('set lev %d' % n)
                                ga(TITULO % ("TIEMPO DE PRONOSTICO: %s h %s" % (delta, ahora.strftime("%H %Z %a, %d %b %Y").title())))
                                if cfg.has_option(s, 'cint'):
                                    ga('set cint %s' % cfg.get(s,'cint'))
                                ga(CONTOUR % (cfg.get(s,'ccolor'), s, unit))
                                ga(POST % ("%s/CONTOUR_%s_%s_%s" % (outdir,nombre,lev,delta), W, H))
                    if cfg.has_option(s,"vector"):
                        ga(PRE)
                        ga('set gxout vector')
                        if cfg.has_option(s, 'ccolor'):
                            for n in niveles:
                                lev = ""
                                if n > 0:
                                    lev = str(n) 
                                ga(PRE)
                                ga(TITULO % ("TIEMPO DE PRONOSTICO: %s h %s" % (delta, ahora.strftime("%H %Z %a, %d %b %Y").title())))
                                ga('set lev %d' % n)
                                ga(VECTOR % (cfg.get(s,'ccolor'), s, unit))
                                ga(POST % ("%s/VECTOR_%s_%s_%s" % (outdir,nombre,lev,delta), W, H))
                
        except Exception, e:
            print "Error al utilizar: %s" % e
    else:
        print "utilizar: %s config salida_brams [wxh]"