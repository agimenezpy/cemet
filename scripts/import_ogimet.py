#!/usr/bin/env python
from metaf_parser import process
from sys import argv, path
from os import environ
from os.path import isfile
from datetime import datetime
from time import time
from re import compile
path.insert(0, "/media/KINGSTON/Facultad/")
environ["DJANGO_SETTINGS_MODULE"] = "cemet.settings"

from cemet.telemetria.models import Estacion

parse = compile("^#|^$")
entry = compile("^[0-9]{12}")
datefmt = compile("^([0-9]{4})([0-9]{2})([0-9]{2})([0-9]{2})([0-9]{2})$")

if __name__ == '__main__':
    if len(argv) > 1 and isfile(argv[1]):
        print "Procesando %s" % (argv[1])
        inicio_t = time()
        try:
            fd = open(argv[1], "r")
            last = None
            while True:
                linea = fd.next().strip()
                if not parse.match(linea):
                    if not entry.match(linea):
                        last = last + linea + " "
                    else:                        
                        if last:
                            contenido = last.strip().split(" ", 1)
                            ds = map(int, filter(lambda(st): st != '', datefmt.split(contenido[0])))
                            fecha = datetime(ds[0], ds[1], ds[2], ds[3], ds[4])
                            inicio_t = time()
                            valores = process(contenido[1], "SYNOP")
                            fin_t = time()
                            if valores:
                                id, dd, ff, t, td, rh, p, slp = valores
                                #print "%s - %s,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f" % (fecha.strftime("%d/%m/%Y %H:%M:%S"), id, dd, ff, t, td, rh, p, slp)
                                
                        last = linea + " "
        except Exception, e:
            print e.message
        print "Trabajo completado en %.4f segundos" % (time() - t)
    else:
        print "No existe el archivo"

