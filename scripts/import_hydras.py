#!/usr/bin/env python
from os import environ
from sys import path,exit
from time import tzset,strptime,strftime,mktime
from datetime import datetime
from csv import reader
from psycopg2 import connect

datas = ["direcc_vto.txt","humedad.txt","precipitacion.txt","presion_atm.txt","rad_glob.txt","radiac_neta.txt","taire.txt","trocio.txt","tsuelo.txt","viento.txt"]

CODS = {
    "0002" : "DD",
    "0004" : "RH",
    "0003" : "PCP",
    "0010" : "P",
    "0013" : "RG",
    "0014" : "RN",
    "0008" : "T",
    "0017" : "TD",
    "0007" : "TSOIL",
    "0001" : "FF"
}

def cargar():
    environ["TZ"] = "UTC"
    db = connect("host=localhost user=cemet password=c3m3t dbname=cemet")
    cur = db.cursor()
    tzset()
    fechahora = ""
    for data in datas:
        try:
            rd = reader(open(environ["HYDRAS_DUMP"] + data),delimiter=";")
            print data
            linea = 0
            max = -1
            medidor = -1
            for fila in rd:
                if medidor == -1:
                    cur.execute(
                        """SELECT medidor.id FROM medidor 
                           JOIN estacion ON estacion.id = medidor.estacion_id
                           WHERE estacion.codigo = 'FPUNA'
                           AND   medidor.variable_id = %s
                        """, [CODS[fila[1]]])
                    for r in cur:
                        medidor = r[0]
                    if medidor == -1:
                        exit(1)
                
                if max == -1:
                    cur.execute(
                        """SELECT MAX(tiempo) FROM medida
                           WHERE medidor_id = %s
                        """
                        , [medidor])
                    max = 0
                    for r in cur:
                        max = r[0]
                fechahora = datetime.strptime("%s %s" % (fila[2],fila[3][:7]),"%d/%m/%Y %H:%M:%S")
                if fila[4] != "---" and fechahora > max:
                    #fechahora = strptime("%s %s" % (fila[2],fila[3][:7]),"%d/%m/%Y %H:%M:%S")
                    #print strftime("%Y-%m-%d %H:%M:%S",fechahora)
                    print fechahora.strftime("%Y-%m-%d %H:%M:%S")
                    #id = int(mktime(fechahora))
                    cur.execute("INSERT INTO medida VALUES (%s,%s,%s)", [fechahora.strftime("%Y-%m-%d %H:%M:%S"), medidor, float(fila[4])])
                linea += 1
            db.commit()
        except Exception, e:
            print e
            print fechahora
            db.rollback()

if __name__ == '__main__':
    cargar()
    #crear_tablas()
   