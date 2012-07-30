/**
 * GLOBALS
 */

var gMapViewer = new Object();
gMapViewer.maps = {};

if (GBrowserIsCompatible()) {
    // Bug in the Google Maps: Copyright for Overlay is not correctly displayed
    var gcr = GMapType.prototype.getCopyrights;
        GMapType.prototype.getCopyrights = function(bounds,zoom) {
        return [""].concat(gcr.call(this,bounds,zoom));
    }

    gMapViewer.createTileLayer = function(mapDef, name, props) {
        var tilelayer = new GTileLayer(GCopyrightCollection(''), mapDef.minZoom, mapDef.maxZoom);
        tilelayer.priority = props.priority;
        tilelayer.type = props.type;
        var timed = props.time;
        var mercator = new GMercatorProjection(mapDef.maxZoom+1);
        var tileDir = mapDef.baseUrl + mapDef.date;
        tilelayer.getTileUrl = function(tile,zoom) {
            if ((zoom < mapDef.minZoom) || (zoom > mapDef.maxZoom)) {
                return mapDef.baseUrl + "none.png";
            }
            tileBounds = new GLatLngBounds(
              mercator.fromPixelToLatLng( new GPoint( (tile.x)*256, (tile.y+1)*256 ) , zoom ),
              mercator.fromPixelToLatLng( new GPoint( (tile.x+1)*256, (tile.y)*256 ) , zoom )
            );

            if (mapDef.bounds.intersects(tileBounds)) {
                return tileDir+"/"+name+"/"+((timed) ? mapDef.time+"/" : "")+zoom+"/"+tile.x+"_"+tile.y+".png";
            } else {
                return mapDef.baseUrl + "none.png";
           }
        }
        // IE 7-: support for PNG alpha channel
        // Unfortunately, the opacity for whole overlay is then not change    able, either or...
        tilelayer.isPng = function() { return true;};
        tilelayer.getOpacity = function() { return this.opacity; }
        tilelayer.opacity = 0.75;
        return tilelayer;
    }

    gMapViewer.initialize = function(id, mapinfo) {
        xmlhttp = GXmlHttp.create();
        xmlhttp.open("GET", mapinfo, false);
        xmlhttp.send();
        modelinfo = eval("(" + xmlhttp.responseText + ")");

        this.maps[id] = {};
        this.maps[id].maxZoom = modelinfo["zoom"][modelinfo["zoom"].length-1];
        this.maps[id].minZoom = modelinfo["zoom"][0];

        this.maps[id].bounds = new GLatLngBounds(new GLatLng(modelinfo["bounds"][1], modelinfo["bounds"][0]),
                                     new GLatLng(modelinfo["bounds"][3], modelinfo["bounds"][2]));

        this.maps[id].map = new GMap2(document.getElementById(id), { backgroundColor: '#fff' });

        this.maps[id].map.addMapType(G_PHYSICAL_MAP);
        this.maps[id].map.removeMapType(G_HYBRID_MAP);
        this.maps[id].map.addMapType(G_SATELLITE_MAP);

        this.maps[id].map.setCenter( this.maps[id].bounds.getCenter(), this.maps[id].map.getBoundsZoomLevel( this.maps[id].bounds));

        hybridOverlay = new GTileLayerOverlay( G_HYBRID_MAP.getTileLayers()[1], {zPriority: 1000} );
        this.maps[id].map.addOverlay(hybridOverlay);
        that = this;
        var lays = modelinfo["layers"];

        this.maps[id].overlays = {};
        this.maps[id].curOverlay;
        this.maps[id].time = "00";
        this.maps[id].baseUrl = modelinfo["baseUrl"];
        this.maps[id].date = modelinfo["date"];
        this.maps[id].times = modelinfo["time"];

        
        for (k in lays) {
            overlay = new GTileLayerOverlay( this.createTileLayer(this.maps[id], k, lays[k]),{ zPriority: lays[k]["priority"]});
            overlay.name = k;
            overlay.timed = lays[k]["time"];
            this.maps[id].map.addOverlay(overlay);
            this.maps[id].overlays[k] = overlay;
            if (!this.maps[id].curOverlay && lays[k]["type"] == "shaded") {
                this.maps[id].curOverlay = overlay;
            }
            overlay.hide();
        }

        this.maps[id].map.addControl(new GLargeMapControl());
        this.maps[id].map.addControl(new GHierarchicalMapTypeControl());
        this.maps[id].map.addControl(new CTransparencyControl( this.maps[id] ));
        this.maps[id].map.enableContinuousZoom();
        this.maps[id].map.enableScrollWheelZoom();

        this.maps[id].map.setMapType(G_PHYSICAL_MAP);
        var colorBar = new ColorBar(this.maps[id]);
        this.maps[id].map.addControl(colorBar);
        GEvent.addListener(this.maps[id], "changeLayer", colorBar.setImage);
        GEvent.addListener(this.maps[id], "changeLayer", this.setDateDesc);

        $("#" + id + "_title").html(modelinfo["titulo"]);
        /*$("#" + id + "_slider").slider({
			range: "min",
			min: 0,
			max: 120,
			value: 0,
            step: 3,
			slide: function( event, ui ) {
				gMapViewer.setTime(id, ui.value > 9 ?  ui.value : "0" + ui.value);
			}
		});*/
        timebar("#" + id + "_slider", id, this.maps[id]);
        $("#timebar_" + id).selectToUISlider({
            labels:12,
            id: id
        });
    }

    gMapViewer.setTime = function(id, time) {
        this.maps[id].time = time;
        that = this;
        $.each(this.maps[id].overlays, function (index,value) {
            if (!value.isHidden()) {
                that.maps[id].map.removeOverlay(value);
                that.maps[id].map.addOverlay(value,{zPriority: value.getTileLayer().priority});
            }
        });
        GEvent.trigger(this.maps[id],"changeLayer",this.maps[id], id);
    }

    gMapViewer.showLayers = function (id, layers) {
        that = this;
        $.each(this.maps[id].overlays, function (index,value) {
            value.hide();
        });
        var showOverlay = false;
        $.each(layers, function (index,value) {
            if (that.maps[id].overlays[value].getTileLayer().type == "shaded") {
                that.maps[id].curOverlay = that.maps[id].overlays[value];
                showOverlay = true;
            }
            else {
                that.maps[id].overlays[value].show();
            }
        });
        if (showOverlay)
            this.maps[id].curOverlay.show();
        GEvent.trigger(this.maps[id],"changeLayer",this.maps[id], id);
    }

    gMapViewer.setDateDesc= function (mObj, id) {
        var hour = parseInt(mObj.time,10);
        var day = parseInt(mObj.date.slice(6,8),10) + parseInt(hour/24,10)
        hour = hour % 24;
        if (hour < 10)
            hour = "0" + hour;
        var fecha = [mObj.date.slice(0,4),mObj.date.slice(4,6),day].join("/");
        var post = " " + hour + ":00:00 UTC";
        var d = new Date(fecha);
        $("#" + id + "_time").html($.datepicker.formatDate("DD dd/mm/yy",d) + post);
    }

}
