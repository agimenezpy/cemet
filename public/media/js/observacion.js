var CEMET = new Object()

var API_KEY = "ABQIAAAA2EhgZ1jVWk36csfuDTqSMRRSIOWjXy1zsK4u2a3hmFiLU4CwkBRv_oU0ni1QI4TlSwwx2t9tP9iY1w";

var COLORES = {
  DD : "yellow",
  FF : "brown",
  T : "red",
  TD : "red",
  P : "green",
  RH : "blue"
};

CEMET.Viz = Class.create();
CEMET.Viz.prototype = {
  initialize: function(div_l, div_t) {
    this.linea;
    this.tabla;
    this.schema = new google.visualization.DataTable();
    this.schema.addColumn('string', 'tiempo');
    this.schema.addColumn('number', 'valor');
    this.numRows = 0;
    //var formatter = new google.visualization.DateFormat({pattern: "d/MM/y hh:mm"});
    this.nFormat = new google.visualization.NumberFormat({decimalSymbol:",",groupingSymbol:"."});
    this.div_l = div_l;
    this.div_t = div_t;
  },
  pushData: function(jsonData, sensor_data) {
    if (this.numRows > 0)
      this.schema.removeRows(0,this.numRows);
    this.schema.addRows(jsonData.length);
    for (var i = 0; i < jsonData.length; i++) {
      this.schema.setValue(i, 0, jsonData[i].tiempo);
      this.schema.setValue(i, 1, Number(jsonData[i].valor));
    }
    this.numRows = this.schema.getNumberOfRows();
    if (!this.linea) {
      this.linea = new google.visualization.LineChart($(this.div_l));
    }
    if (!this.tabla) {
      this.tabla = new google.visualization.Table($(this.div_t));
    }
    this.schema.setColumnLabel(0, "Tiempo de Muestra");
    this.schema.setColumnLabel(1, sensor_data.descripcion + " (" + sensor_data.unidad + ")");
    this.nFormat.format(this.schema, 1);
    this.linea.draw(this.schema,
                   {titleX: "Fecha/Hora",
                    titleY: sensor_data.unidad,
                    legend: 'bottom',
                    colors: [COLORES[sensor_data.variable]]});
    this.tabla.draw(this.schema, {allowHtml: true, showRowNumber: true});
  }
};

function estacion_list() {
  var obj = new Ajax.Request("/json/estacion/", {
    method: 'get',
    onSuccess: function(transport) {
      js = transport.responseText.evalJSON()
      js.each(function (item) {
        $("id_estacion").appendChild(new Element("option", {'value':item.id})
                        .update(item.nombre));
      });
    }
  });
}

function sensor_list(estacion) {
  if (estacion.value == "Ninguna")
    return;
  var obj = new Ajax.Request("/json/estacion/" + estacion.value, {
    method: 'get',
    onSuccess: function(transport) {
      js = transport.responseText.evalJSON();
      estacion_detail(js);
      $('id_sensor').options[0].selected = true;
      for (var i = 1; i < $('id_sensor').options.length; i++)
        $("id_sensor").removeChild($("id_sensor").options[i]);
      js.sensores.each(function (item) {
        $("id_sensor").appendChild(new Element("option", {'value':item.id})
                      .update(item.descripcion));
      });
    }
  });
}

function medida_list(sensor) {
  if (sensor.value == "Ninguna")
    return;
  var obj = new Ajax.Request("/json/sensor/" + sensor.value, {
    method: 'get',
    onSuccess: function(transport) {
      js = transport.responseText.evalJSON();
      sensor_data = js;
      sensor_detail(js);
      if (!$("id_fecha").value)
        DateTimeShortcuts.handleCalendarQuickLink(0, 0);
      if (!$("id_hora").value)
        DateTimeShortcuts.handleClockQuicklink(0, new Date().getHourMinuteSecond());
      $("tiempo").show();
      obtener_datos();
    }
  });
}

function validar_fecha(fecha) {
    if (!fecha.value.match(/[0-9]{4}\-[0-9]{2}\-[0-9]{2}/))
        fecha.value = "";
}

function validar_hora(hora) {
    if (!hora.value.match(/[0-9]{2}:[0-9]{2}:[0-9]{2}/))
        hora.value = "";
}

function obtener_datos() {
  var fecha = $("id_fecha").value.split("-");
  var hora = $("id_hora").value.split(":");
  var ventana = $("id_ventana").value;
  var timestamp = fecha[0] + fecha[1] + fecha[2] + hora[0] + hora[1] + hora[2];
  var obj = new Ajax.Request("/json/medida/" + sensor_data.id + "/" + timestamp + "/" + ventana, {
    method: 'get',
    onSuccess: function(transport) {
      js = transport.responseText.evalJSON();
      medidas.pushData(js, sensor_data);
    }
  });
}

function descargar_datos() {
  var fecha = $("id_fecha").value.split("-");
  var hora = $("id_hora").value.split(":");
  var ventana = $("id_ventana").value;
  var timestamp = fecha[0] + fecha[1] + fecha[2] + hora[0] + hora[1] + hora[2];
  var url = "/csv/medida/" + sensor_data.id + "/" + timestamp + "/" + ventana;
  $("id_descargar").href = url;
  $("id_descargar").click();
}

function estacion_detail(estacion) {
  var ll = getLatLon(estacion.ubicacion);
  $('estacion_detail').update(
  "<h2>Datos de la Estaci&oacute;n</h2>"+
  "<div class='level2'><p><b>Nombre</b>: " + estacion.nombre + "<br>" +
  "<b>C&oacute;digo</b>: " + estacion.codigo + "<br>" +
  "<b>Ubicacion</b>: <img src='http://maps.google.com/staticmap?center="+ll+"&zoom=14&size=400x300&maptype=terrain\&markers="+ll+",blues\&key="+API_KEY+"&sensor=false'<br>" +
  "<b>elevacion</b>: " + estacion.elevacion + "<br></p></div>");
}

function getLatLon(str) {
  ll = str.replace("POINT (","").replace(")","").split(" ");
  return ll[1] + "," + ll[0];
}

function sensor_detail(sensor) {
  $('sensor_detail').update(
  "<h2>Datos del Sensor</h2>" +
  "<div class='level2'><p><b>Descripci&oacute;n</b>: " + sensor.descripcion + "<br>" +
  "<b>Unidad</b>: " + sensor.unidad + "<br>" +
  "<b>Intervalo</b>: " + sensor.intervalo + " segundos" + "<br></p></div>");
}

estacion_list();
var medidas = new CEMET.Viz("linea","tabla");
var sensor_data;