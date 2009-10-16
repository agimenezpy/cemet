# -*- coding: iso-8859-1 -*-
from django.shortcuts import render_to_response
from django.http import Http404, HttpResponse
from django.template import TemplateDoesNotExist, RequestContext
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.views.generic import list_detail
from django.contrib.contenttypes.models import ContentType

CONTENT = {
    "json" : "text/plain",
    "xml" : "text/xml",
    "html" : "text/html",
    "csv" : "text/plain"
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
    "estacion" : "sensor",
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

def get_filter(model, dep_class, object_id):
    if model == "estacion":
        return dep_class.objects.filter(estacion=object_id)
    elif model == "observatorio":
        return dep_class.objects.filter(observatorio=object_id)
    else:
        return None