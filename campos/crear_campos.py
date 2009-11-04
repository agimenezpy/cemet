#!/usr/bin/env python
import ConfigParser
import sys
import datetime
from grads import GaNum
from os import path,mkdir

PRE = """
clear
set display color white
set mpdraw off
set grads off
set grid off
set parea 0.2 9 0.3 8
set csmooth on
sa
"""

TITULO = """
set string 1 c 2 0
set strsiz 0.19
draw string 4.7 8.3 %s
"""

COLORMAP = """
run %s.gs
d %s
cbarn 1 1 9.2 4.25
"""

CONTOUR = """
set ccolor %s
set clopts -1 -1 0.12
d %s
"""

VECTOR = """
set arrowhead 0.09
set ccolor %s
d %s
"""

BASEMAP = """
set ccolor 4
d %s - %s
"""

POST = """
printim %s.gif x640 y480 -t 0
"""

if __name__ == '__main__':
    if len(sys.argv) > 3:
        try:
            ga = GaNum(Echo=False,Window=False)
            fecha = datetime.datetime.strptime(sys.argv[3] + "UTC","%Y%m%d%H%Z")
            cfg = ConfigParser.RawConfigParser()
            cfg.read(sys.argv[1])
            fh = ga.open(sys.argv[2])
            outdir = cfg.get("DEFAULT","directory") + "/" + fecha.strftime("%Y%m%d%H")
            if not path.exists(outdir):
                mkdir(outdir)
            r_base = True
            for s in cfg.sections():
                print s
                nombre = cfg.get(s,"name")
                niveles = [0]
                if cfg.has_option(s,'levels'):
                    niveles = map(int,cfg.get(s,'levels').split(","))
                if not r_base:
                    ga('set gxout shaded')
                    ga(PRE)
                    ga('set mpdraw on')
                    ga('set mpdset hires')
                    ga('set z %d' % 1)
                    ga(BASEMAP % (s, s))
                    ga("printim %s.gif x640 y480 -t 0 -t 4" % (outdir + "/BASE"))
                    r_base = True
                if cfg.has_option(s,"colormap"):
                    ga('set gxout shaded')
                    if cfg.has_option(s, 'paleta'):
                        for n in niveles:
                            lev = ""
                            if n > 0:
                                lev = str(n) 
                            ga(PRE)
                            ga('set z %d' % n)
                            ga(TITULO % ("TIEMPO DE PRONOSTICO: %d h %s" % (48, fecha.strftime("%H %Z %a, %d %b %Y").title())))
                            ga(COLORMAP % (cfg.get(s,'paleta'), s))
                            ga(POST % (outdir + "/" + nombre + lev + "S"))
                if cfg.has_option(s,"contour"):
                    ga(PRE)
                    ga('set gxout contour')
                    if cfg.has_option(s, 'ccolor'):
                        for n in niveles:
                            lev = ""
                            if n > 0:
                                lev = str(n) 
                            ga(PRE)
                            ga('set z %d' % n)
                            ga(TITULO % ("TIEMPO DE PRONOSTICO: %d h %s" % (48, fecha.strftime("%H %Z %a, %d %b %Y").title())))
                            ga(CONTOUR % (cfg.get(s,'ccolor'), s))
                            ga(POST % (outdir + "/" + nombre + lev + "C"))
                if cfg.has_option(s,"vector"):
                    ga(PRE)
                    ga('set gxout vector')
                    if cfg.has_option(s, 'ccolor'):
                        for n in niveles:
                            lev = ""
                            if n > 0:
                                lev = str(n) 
                            ga(PRE)
                            ga(TITULO % ("TIEMPO DE PRONOSTICO: %d h %s" % (48, fecha.strftime("%H %Z %a, %d %b %Y").title())))
                            ga('set z %d' % n)
                            ga(VECTOR % (cfg.get(s,'ccolor'), s))
                            ga(POST % (outdir + "/" + nombre + lev + "V"))
                
        except Exception, e:
            print "Error de utilizacion: %s" % e
    else:
        print "utiliza: %s config salida_brams"