# -*- coding: iso-8859-1 -*-
from django.shortcuts import render_to_response
from django.http import Http404, HttpResponse
from django.template import TemplateDoesNotExist, RequestContext
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page

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