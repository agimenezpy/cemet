#!/usr/bin/env python
from pymongo import Connection
from time import mktime,gmtime,strptime,tzset,strftime
from os import environ
from csv import reader

datas = ["direcc_vto.txt","humedad.txt","precipitacion.txt","presion_atm.txt","rad_glob.txt","radiac_neta.txt","taire.txt","trocio.txt","tsuelo.txt","viento.txt"]

def cargar():
    con = Connection()
    db = con.observacion
    environ["TZ"] = "UTC"
    tzset()
    
    var = 0;
    for data in datas:
        rd = reader(open("../../../fpuna/" + data),delimiter=";")
        firstdate = None
        print data
        for fila in rd:
            fechahora = strptime("%s %s" % (fila[2],fila[3][:7]),"%d/%m/%Y %H:%M:%S")
            #print strftime("%Y-%m-%d %H:%M:%S",fechahora)
            id = int(mktime(fechahora))
            dset = "FPUNA_%s" % fila[1]
            if fila[4] != "---":
                r = {"_id" : id, "measure" : float(fila[4])}
                db[dset].save(r)
                if firstdate == None:
                    firstdate = strftime("%Y-%m-%d %H:%M:%S",fechahora)
        db.station.update({"codename":"FPUNA"},{"$set":{"variables.%d.starttime"%var:firstdate}})
        db.station.update({"codename":"FPUNA"},{"$set":{"variables.%d.endtime"%var:strftime("%Y-%m-%d %H:%M:%S",fechahora)}})
        var += 1

def fechas():
    con = Connection(tz_aware=False)
    db = con.observacion
    est = db.station.find_one({"codename":"FPUNA"},{"variables":1})
    #db.station.update({"codename":"FPUNA"},{"$set":{"variables.0.starttime":"2010-01-01 00:05:00"}})
    #db.station.update({"codename":"FPUNA"},{"$set":{"variables.0.endtime":"2010-11-05 22:10:00"}})
    idx = 0
    for var in est['variables']:
        first = db[var['data']].find({},{"_id":1}).sort("_id").limit(1)[0]["_id"]
        last = db[var['data']].find({},{"_id":1}).sort("_id",-1).limit(1)[0]["_id"]
        firstd, enddate = strftime("%Y-%m-%d %H:%M:%S",gmtime(first)),strftime("%Y-%m-%d %H:%M:%S",gmtime(last))
        print var['data'],firstd,enddate
        db.station.update({"codename":"FPUNA"},{"$set":{"variables.%d.starttime"%idx:firstd}})
        db.station.update({"codename":"FPUNA"},{"$set":{"variables.%d.endtime"%idx:enddate}})
        idx += 1
    
if __name__ == '__main__':
    cargar()
    #fechas()
    