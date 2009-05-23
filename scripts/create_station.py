#!/usr/bin/env python
import csv
from os import system

signos = {'N':1,'S':-1,'W':-1,'E':1}

def create_point(strPoint):
    strPoint = strPoint.strip()
    if len(strPoint) > 1:
        return signos[strPoint[-1]]*(int(strPoint[:-3]) + int(strPoint[-3:-1])/60.0)
    else:
        return -1

if __name__ == '__main__':
    fd = open("station.txt", "r")
    reader = csv.reader(fd, delimiter="\t",quoting=csv.QUOTE_NONE)
    for line in reader:
        if len(line) == 7:
            wmo_id1, wmo_id2, location, country, lat, lon, elev = line
        else:
            wmo_id1, wmo_id2, location, country, lat, lon, elev, rest1, rest2 = line
        lat, lon = create_point(lat), create_point(lon)
        command = """dbfadd station.dbf "%s" "%s" "%s" "%s" "%s"; shpadd station.shp %s %s +""" % (wmo_id1, wmo_id2, location, country, elev, lon, lat)
        print command
        result = system(command)
        if result:
            break
    fd.close()

