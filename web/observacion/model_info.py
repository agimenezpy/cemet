from web.observacion.models import *

estacion_info_json = {
    "queryset" : Estacion.objects.all(),
    "mimetype" : "text/plain; charset=iso8859-1",
    "template_name" : "observacion/estacion_list.json"
}

estacion_detail_json = {
    "queryset" : Estacion.objects.all(),
    "mimetype" : "text/plain; charset=iso8859-1",
    "template_name" : "observacion/estacion_detail.txt",
    "extra_context" : {"sensor_list" : Sensor.objects.all }
}   