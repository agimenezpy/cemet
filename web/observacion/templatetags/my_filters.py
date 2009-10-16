from django import template
from django.utils import simplejson

register = template.Library()

def tojson(value):
    di = {}
    for i in value._meta.fields:
        if i.rel:
            di[i.name] = getattr(value, i.name + "_id")
        else:
            di[i.name] = getattr(value, i.name)
        
    return simplejson.dumps(di,ensure_ascii=False,encoding="iso8859-1")

register.filter("tojson", tojson)
