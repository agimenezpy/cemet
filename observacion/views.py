# -*- coding: iso-8859-1 -*-
from django.shortcuts import render_to_response
from django.http import Http404, HttpResponse
from django.template import TemplateDoesNotExist, RequestContext
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.views.generic import list_detail
from django.contrib.contenttypes.models import ContentType
from datetime import datetime, timedelta
from observacion.models import Medida, Medidor
from re import match

CONTENT = {
    "json" : "text/plain",
    "xml" : "text/xml",
    "html" : "text/html",
    "csv" : "text/csv",
    "gviz" : "text/plain"
}

TITULOS = {
    "index" : u"Página Principal",
    "productos" : u"Productos Meteorológicos",
    "academico" : u"Área Académica",
    "contactos" : u"Contactos Disponibles"
}

#@cache_page(60*15)
def default(request, page):
    try:
        return render_to_response(page + ".html", {'title' : TITULOS[page] }, RequestContext(request))
    except TemplateDoesNotExist:
        raise Http404()

@login_required
def account(request, section):
    if not section or section == 'profile':
        request.user.message_set.create(message=u"Ha iniciado sesión en el sistema.")
        return render_to_response("profile.html", {'title': 'Mi Perfil'}, RequestContext(request))
    else:
        raise Http404()

def list_handler(request, format, model):
    try:
        c = ContentType.objects.get(app_label="observacion", model=model)
        model_class = c.model_class()
        return list_detail.object_list(
            request,
            queryset = model_class.objects.all(),
            template_name = "observacion/%s_list.%s" % (model,format),
            mimetype = "%s; charset=iso8859-1" % (CONTENT[format])
        )
    except:
        raise Http404()

DEPS = {
    "estacion" : "medidor",
    "observatorio" : "estacion"
}

def detail_handler(request, format, model, object_id):
    try:
        c = ContentType.objects.get(app_label="observacion", model=model)
        model_class = c.model_class()
        extra = None
        if DEPS.has_key(model):
            c = ContentType.objects.get(app_label="observacion", model=DEPS[model])
            dep_class = c.model_class()
            extra = {DEPS[model] + "_list" : get_filter(model, dep_class, object_id)}
        return list_detail.object_detail(
            request,
            queryset = model_class.objects.all(),
            object_id = object_id,
            template_name = "observacion/%s_detail.%s" % (model, format),
            mimetype = "%s; charset=iso8859-1" % (CONTENT[format]),
            extra_context = extra
        )
    #except Exception, e:
    #    raise e
    except:
        raise Http404()

def medida(request, format, medidor_id, fecha, ws="1d"):
    try:
        numero, cual = match("(\d+)([YmdHMS])", ws).groups()
        if cual == "Y":
            delta = timedelta(days=365*int(numero))
        elif cual == "m":
            delta = timedelta(days=30*int(numero))
        elif cual == "d":
            delta = timedelta(days=1*int(numero))
        elif cual == "H":
            delta = timedelta(hours=int(numero))
        elif cual == "M":
            delta = timedelta(minutes=int(numero))
        elif cual == "S":
            delta = timedelta(seconds=int(numero))
        fecha_final = datetime.strptime(fecha, "%Y%m%d%H%M%S")
        fecha_inicial = fecha_final - delta
        if format != "gviz":
            return list_detail.object_list(
                request,
                queryset = Medida.objects.filter(medidor__id__exact=medidor_id, tiempo__range=(fecha_inicial, fecha_final)).order_by("tiempo"),
                template_name = "observacion/medida_list.%s" % (format),
                mimetype = "%s; charset=iso8859-1" % (CONTENT[format])
            )
        else:
            import gviz_api
            s = Medidor.objects.get(pk=medidor_id)
            description = {"tiempo": ("string", "Tiempo de Muestra"),
                           "valor": ("number", "%s, %s" % (s.descripcion, s.unidad))}
            data_table = gviz_api.DataTable(description)
            data_table.LoadData(map(to_dict, Medida.objects.filter(medidor__id__exact=medidor_id, tiempo__range=(fecha_inicial, fecha_final)).order_by("tiempo")))
            return render_to_response("observacion/medida_list.gviz",
                                      {'json_data' : data_table.ToJSonResponse(columns_order=("tiempo", "valor"),
                                                     order_by="tiempo")},
                                      RequestContext(request), mimetype="%s; charset=iso8859-1" % (CONTENT[format]))
    except Exception, e:
        raise e
    #except:
    #    raise Http404()

def get_filter(model, dep_class, object_id):
    if model == "estacion":
        return dep_class.objects.filter(estacion=object_id)
    elif model == "observatorio":
        return dep_class.objects.filter(observatorio=object_id)
    else:
        return None

def to_dict(item):
    return {"tiempo" : item.tiempo, "valor":item.valor}