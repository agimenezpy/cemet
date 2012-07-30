/**
 * Created by PyCharm.
 * User: agimenez
 * Date: 04/12/11
 * Time: 09:33 PM
 * To change this template use File | Settings | File Templates.
 */

function timebar(cont, id, mapDef) {
    var day = parseInt(mapDef.date.slice(6,8),10);
    var mes = parseInt(mapDef.date.slice(4,6), 10);
    var anio = parseInt(mapDef.date.slice(0,4), 10);
    var days = (mapDef.times.length - 1)/8
    var select = "<select id='timebar_" + id +"' style='display:none'>";
    var ndays = 30;
    if (mes == 2) {
        ndays = 28;
        if (anio % 400 == 0 || (anio % 100 != 0 && anio % 4 == 0))
            ndays = 29;
    }
    else if (mes < 8 && mes % 2 == 1) {
        ndays = 31;
    }
    else if (mes > 7 && mes % 2 == 0) {
        ndays = 31;
    }
    for (var d = 0; d < days+1; d++) {
        var curday = day + d;
        if (curday > ndays)
            curday = ndays - curday;
        var fecha = [anio,mes,curday].join("/");
        var dt = new Date(fecha);
        select += "<optgroup label='"+$.datepicker.formatDate("DD",dt)+"'>";
        var dtt = $.datepicker.formatDate("DD dd/mm",dt);
        var inicio = d*8;
        var fin = inicio + 8 ;
        for (var i = inicio; i < fin && i < mapDef.times.length ; i++) {
            select += "<option value='"+ mapDef.times[i]+"'>" + dtt + " H+" + mapDef.times[i]+"</option>";
        }
        select += "</optgroup>";
    }
    select += "</select>";
    $(cont).html(select);
}