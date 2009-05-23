{% extends "gis/admin/openlayers.js" %}
{% block base_layer %}
new OpenLayers.Layer.Google("Google Normal", {type: G_NORMAL_MAP, 'sphericalMercator': true});
{% endblock %}

{% block extra_layers %}
 {{ module }}.layers.overlay = new OpenLayers.Layer.Google("Google Hybrid", {type: G_HYBRID_MAP, 'sphericalMercator': true});
 {{ module }}.map.addLayer({{ module }}.layers.overlay);
 {{ module }}.layers.overlay = new OpenLayers.Layer.Google("Google Terrain", {type: G_PHYSICAL_MAP, 'sphericalMercator': true});
 {{ module }}.map.addLayer({{ module }}.layers.overlay);
{% endblock %}