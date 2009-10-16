{% extends "gis/admin/openlayers.js" %}
{% block base_layer %}
new OpenLayers.Layer.Google("Google Normal", {type: G_NORMAL_MAP, 'sphericalMercator': true});
{% endblock %}

{% block extra_layers %}
 {{ module }}.layers.overlay = new OpenLayers.Layer.Google("Google Hybrid", {type: G_HYBRID_MAP, 'sphericalMercator': true});
 {{ module }}.map.addLayer({{ module }}.layers.overlay);
 {{ module }}.layers.overlay = new OpenLayers.Layer.Google("Google Terrain", {type: G_PHYSICAL_MAP, 'sphericalMercator': true});
 {{ module }}.map.addLayer({{ module }}.layers.overlay);
 {{ module }}.map.restrictedExtent = new OpenLayers.Bounds(-62.643768, -27.588337, -54.243896, -19.296669)
                                         .transform({{ module }}.map.displayProjection, {{ module }}.map.projection);
 {{ module }}.map.zoomToExtent({{ module }}.map.restrictedExtent)
 // Esto es necesario debido a MySQL
 {{ module }}.wkt_f2 = new OpenLayers.Format.WKT({internalProjection: {{ module }}.map.projection, externalProjection: {{ module }}.map.displayProjection});
 {{ module }}.get_ewkt = function(feat){return 'SRID=4326;' + geodjango_ubicacion.wkt_f2.write(feat);}
{% endblock %}