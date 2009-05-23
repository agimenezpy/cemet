from subprocess import Popen, PIPE
from struct import unpack
from re import compile, match

TIPOS = {
    "SYNOP" : ("-s", "i7f"),
    "METAR" : ("-m", "4s7f")
}

def process(coded, tipo):
    child = Popen("./metaf_bridge.pl %s " % TIPOS[tipo][0], shell=True, stdin=PIPE, stdout=PIPE)
    child.stdin.write(coded)
    child.stdin.close()
    try:
        bindata = child.stdout.next()
        return unpack(TIPOS[tipo][1], bindata)
    except:
        return None


if __name__ == '__main__':
    result = process("AAXX 25004 86086 21670 70902 10260 20230 40079 56013 71399 81970 333 10350 60011 81940", "SYNOP")
    if result:
        id, dd, ff, t, td, rh, p, slp = result
        print "%s,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f" % (id, dd, ff, t, td, rh, p, slp)
    else:
        print "Sin resultados"

    result = process("SGAS 010000Z 17012KT CAVOK 30/20 Q1008", "METAR")
    if result:
        id, dd, ff, t, td, rh, p, slp = result
        print "%s,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f" % (id, dd, ff, t, td, rh, p, slp)
    else:
        print "Sin resultados"
