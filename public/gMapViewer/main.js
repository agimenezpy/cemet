function ColorBar(mapDef){this.baseUrl=mapDef.baseUrl;this.date=mapDef.date;this.size=new GSize(mapDef.map.getSize().width,24);mapDef.colorBar=this;}
ColorBar.prototype=new GControl();ColorBar.prototype.getDefaultPosition=function(){return new GControlPosition(G_ANCHOR_BOTTOM_LEFT,new GSize(0,15));}
ColorBar.prototype.initialize=function(map){this.map=map;this.cont=document.createElement("div");this.img=document.createElement("img");this.cont.appendChild(this.img);this.img.src=this.baseUrl+"/none.png";this.cont.style.width=this.size.width+"px";this.cont.style.height=this.size.height+"px";this.cont.style.textAlign="center";map.getContainer().appendChild(this.cont);return this.cont;}
ColorBar.prototype.setImage=function(mObj,id){mObj.colorBar.img.src=[mObj.baseUrl,mObj.date,mObj.curOverlay.name,"COLORBAR"+(mObj.curOverlay.timed?"_"+mObj.time:"")+".gif"].join("/");}
var CTransparencyLENGTH=58;function CTransparencyControl(overlayContainer){this.overlayC=overlayContainer;this.opacity=overlayContainer.curOverlay.getTileLayer().getOpacity();}
CTransparencyControl.prototype=new GControl();CTransparencyControl.prototype.setSlider=function(pos){var left=Math.round((CTransparencyLENGTH*pos));this.slide.left=left;this.knob.style.left=left+"px";this.knob.style.top="0px";}
CTransparencyControl.prototype.setOpacity=function(){this.overlayC.curOverlay.getTileLayer().opacity=this.slide.left/CTransparencyLENGTH;this.map.removeOverlay(this.overlayC.curOverlay);this.map.addOverlay(this.overlayC.curOverlay,{zPriority:this.overlayC.curOverlay.getTileLayer().priority});}
CTransparencyControl.prototype.initialize=function(map){var that=this;this.map=map;var agent=navigator.userAgent.toLowerCase();if((agent.indexOf("msie")>-1)&&(agent.indexOf("opera")<1)){this.ie=true}else{this.ie=false}
var container=document.createElement("div");container.style.width="70px";container.style.height="21px";if(this.ie){container.innerHTML='<div class="cnt_child_ie" ></div>';}else{container.innerHTML='<div class="cnt_child" ></div>';}
if(this.ie){this.knob=document.createElement("div");$(this.knob).addClass("knob_ie");this.knob_img=document.createElement("div");$(this.knob_img).addClass("knob_img");this.knob.appendChild(this.knob_img);}else{this.knob=document.createElement("div");$(this.knob).addClass("knob");}
container.appendChild(this.knob);this.slide=new GDraggableObject(this.knob,{container:container});this.slide.setDraggableCursor('pointer');this.slide.setDraggingCursor('pointer');this.container=container;map.getContainer().appendChild(container);this.setSlider(this.opacity);GEvent.addListener(this.slide,"dragend",function(){that.setOpacity()});return container;}
CTransparencyControl.prototype.getDefaultPosition=function(){return new GControlPosition(G_ANCHOR_TOP_RIGHT,new GSize(7,47));}
var gMapViewer=new Object();gMapViewer.maps={};if(GBrowserIsCompatible()){var gcr=GMapType.prototype.getCopyrights;GMapType.prototype.getCopyrights=function(bounds,zoom){return[""].concat(gcr.call(this,bounds,zoom));}
gMapViewer.createTileLayer=function(mapDef,name,props){var tilelayer=new GTileLayer(GCopyrightCollection(''),mapDef.minZoom,mapDef.maxZoom);tilelayer.priority=props.priority;tilelayer.type=props.type;var timed=props.time;var mercator=new GMercatorProjection(mapDef.maxZoom+1);var tileDir=mapDef.baseUrl+mapDef.date;tilelayer.getTileUrl=function(tile,zoom){if((zoom<mapDef.minZoom)||(zoom>mapDef.maxZoom)){return mapDef.baseUrl+"none.png";}
tileBounds=new GLatLngBounds(mercator.fromPixelToLatLng(new GPoint((tile.x)*256,(tile.y+1)*256),zoom),mercator.fromPixelToLatLng(new GPoint((tile.x+1)*256,(tile.y)*256),zoom));if(mapDef.bounds.intersects(tileBounds)){return tileDir+"/"+name+"/"+((timed)?mapDef.time+"/":"")+zoom+"/"+tile.x+"_"+tile.y+".png";}else{return mapDef.baseUrl+"none.png";}}
tilelayer.isPng=function(){return true;};tilelayer.getOpacity=function(){return this.opacity;}
tilelayer.opacity=0.75;return tilelayer;}
gMapViewer.initialize=function(id,mapinfo){xmlhttp=GXmlHttp.create();xmlhttp.open("GET",mapinfo,false);xmlhttp.send();modelinfo=eval("("+xmlhttp.responseText+")");this.maps[id]={};this.maps[id].maxZoom=modelinfo["zoom"][modelinfo["zoom"].length-1];this.maps[id].minZoom=modelinfo["zoom"][0];this.maps[id].bounds=new GLatLngBounds(new GLatLng(modelinfo["bounds"][1],modelinfo["bounds"][0]),new GLatLng(modelinfo["bounds"][3],modelinfo["bounds"][2]));this.maps[id].map=new GMap2(document.getElementById(id),{backgroundColor:'#fff'});this.maps[id].map.addMapType(G_PHYSICAL_MAP);this.maps[id].map.removeMapType(G_HYBRID_MAP);this.maps[id].map.addMapType(G_SATELLITE_MAP);this.maps[id].map.setCenter(this.maps[id].bounds.getCenter(),this.maps[id].map.getBoundsZoomLevel(this.maps[id].bounds));hybridOverlay=new GTileLayerOverlay(G_HYBRID_MAP.getTileLayers()[1],{zPriority:1000});this.maps[id].map.addOverlay(hybridOverlay);that=this;var lays=modelinfo["layers"];this.maps[id].overlays={};this.maps[id].curOverlay;this.maps[id].time="00";this.maps[id].baseUrl=modelinfo["baseUrl"];this.maps[id].date=modelinfo["date"];this.maps[id].times=modelinfo["time"];for(k in lays){overlay=new GTileLayerOverlay(this.createTileLayer(this.maps[id],k,lays[k]),{zPriority:lays[k]["priority"]});overlay.name=k;overlay.timed=lays[k]["time"];this.maps[id].map.addOverlay(overlay);this.maps[id].overlays[k]=overlay;if(!this.maps[id].curOverlay&&lays[k]["type"]=="shaded"){this.maps[id].curOverlay=overlay;}
overlay.hide();}
this.maps[id].map.addControl(new GLargeMapControl());this.maps[id].map.addControl(new GHierarchicalMapTypeControl());this.maps[id].map.addControl(new CTransparencyControl(this.maps[id]));this.maps[id].map.enableContinuousZoom();this.maps[id].map.enableScrollWheelZoom();this.maps[id].map.setMapType(G_PHYSICAL_MAP);var colorBar=new ColorBar(this.maps[id]);this.maps[id].map.addControl(colorBar);GEvent.addListener(this.maps[id],"changeLayer",colorBar.setImage);GEvent.addListener(this.maps[id],"changeLayer",this.setDateDesc);$("#"+id+"_title").html(modelinfo["titulo"]);timebar("#"+id+"_slider",id,this.maps[id]);$("#timebar_"+id).selectToUISlider({labels:12,id:id});}
gMapViewer.setTime=function(id,time){this.maps[id].time=time;that=this;$.each(this.maps[id].overlays,function(index,value){if(!value.isHidden()){that.maps[id].map.removeOverlay(value);that.maps[id].map.addOverlay(value,{zPriority:value.getTileLayer().priority});}});GEvent.trigger(this.maps[id],"changeLayer",this.maps[id],id);}
gMapViewer.showLayers=function(id,layers){that=this;$.each(this.maps[id].overlays,function(index,value){value.hide();});var showOverlay=false;$.each(layers,function(index,value){if(that.maps[id].overlays[value].getTileLayer().type=="shaded"){that.maps[id].curOverlay=that.maps[id].overlays[value];showOverlay=true;}
else{that.maps[id].overlays[value].show();}});if(showOverlay)
this.maps[id].curOverlay.show();GEvent.trigger(this.maps[id],"changeLayer",this.maps[id],id);}
gMapViewer.setDateDesc=function(mObj,id){var hour=parseInt(mObj.time,10);var day=parseInt(mObj.date.slice(6,8),10)+parseInt(hour/24,10)
hour=hour%24;if(hour<10)
hour="0"+hour;var fecha=[mObj.date.slice(0,4),mObj.date.slice(4,6),day].join("/");var post=" "+hour+":00:00 UTC";var d=new Date(fecha);$("#"+id+"_time").html($.datepicker.formatDate("DD dd/mm/yy",d)+post);}}
function timebar(cont,id,mapDef){var day=parseInt(mapDef.date.slice(6,8),10);var mes=parseInt(mapDef.date.slice(4,6),10);var anio=parseInt(mapDef.date.slice(0,4),10);var days=(mapDef.times.length-1)/8
var select="<select id='timebar_"+id+"' style='display:none'>";var ndays=30;if(mes==2){ndays=28;if(anio%400==0||(anio%100!=0&&anio%4==0))
ndays=29;}
else if(mes<8&&mes%2==1){ndays=31;}
else if(mes>7&&mes%2==0){ndays=31;}
for(var d=0;d<days+1;d++){var curday=day+d;if(curday>ndays)
curday=ndays-curday;var fecha=[anio,mes,curday].join("/");var dt=new Date(fecha);select+="<optgroup label='"+$.datepicker.formatDate("DD",dt)+"'>";var dtt=$.datepicker.formatDate("DD dd/mm",dt);var inicio=d*8;var fin=inicio+8;for(var i=inicio;i<fin&&i<mapDef.times.length;i++){select+="<option value='"+mapDef.times[i]+"'>"+dtt+" H+"+mapDef.times[i]+"</option>";}
select+="</optgroup>";}
select+="</select>";$(cont).html(select);}