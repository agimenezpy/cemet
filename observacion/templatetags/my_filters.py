from django import template
from django.utils import simplejson
import locale

register = template.Library()

def tojson(value):
    di = {}
    for i in value._meta.fields:
        if i.rel:
            di[i.name] = getattr(value, i.name + "_id")
        else:
            di[i.name] = getattr(value, i.name)
        
    return simplejson.dumps(di,ensure_ascii=False,encoding="iso8859-1")

def lformat(value, fmt):
    locale.setlocale(locale.LC_ALL, 'es_PY')
    return locale.format(fmt, value)

register.filter("tojson", tojson)
register.filter("lformat", lformat)
