#!/usr/bin/env python
import sys
from matplotlib.pyplot import cm
from cmaplib import cmap_discretize

COLORES = ['red','green','blue']

if __name__ == '__main__':
    if len(sys.argv) > 1:
        paleta = sys.argv[1]
        try:
            niveles = int(sys.argv[2])
            cmap = cm.get_cmap(paleta)
            r_c = cmap_discretize(cmap, niveles)
            fd = open(paleta + ".gs", "w")
            color = {'red' : 0, 'green' : 0, 'blue' : 0}
            base = 99 - niveles
            for i in range(1, niveles+1):
                for c in COLORES:
                    color[c] = int(r_c._segmentdata[c][i][1]*255)
                fd.write("'set rgb %d %d %d %d'\n" %
                         (base + i, color['red'], color['green'], color['blue']))
            fd.write("'set rbcols %s'\n" % (reduce(lambda u, v: "%s %s" % (u,v), range(base + 1, 100))))
        except:
            print "Ha ocurrido un error: Paleta no existente o numero de niveles invalido"
    else:
        print "utiliza: %s nombre_paleta niveles" % sys.argv[0]