from popen2 import popen2
from xml.dom.minidom import parseString

metaf2xml = "/home/agimenez/metaf2xml/bin/metaf2xml.pl"

def process(coded):
    outst, inst = popen2("%s -s -x- '%s'" % (metaf2xml, coded))
    xmldoc = ""
    try:
        while True:
            xmldoc += outst.next().strip()
    except:
        pass
    dom = parseString(xmldoc)
    report = dom.firstChild
    if report and report.tagName == "reports":
        if not report.firstChild:
            raise Exception("Ilegal argument")
        for node in report.firstChild.childNodes:
            if node.tagName == "ERROR":
                print  "ERROR: " + node.getAttribute("errorType")
            elif node.tagName == "warning":
                print "Warning: " + node.getAttribute("warningType")
            elif node.tagName == "obsStationId":
                stationId = None
                if node.firstChild and node.firstChild.tagName == "id":
                    stationId = int(node.firstChild.getAttribute("v"))
            elif node.tagName == "":
                pass
    return [stationId,None]

if __name__ == '__main__':
    result = process("AAXX 25004 86086 21670 70902 10260 20230 40079 56013 71399 81970 333 10350 60011 81940")
    print result[0], result[1]