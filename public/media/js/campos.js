function iniciar() {
    d = new Date()
    $("id_fecha").value = d.getFullYear() + "-" + (d.getMonth() + 1)+ "-" + d.getTwoDigitDate()
    if (d.getHours() > 12) {
        $("id_hora").value = "12";
    }
    cambiar_campo();
}

function cambiar_campo() {
    var f = $("id_fecha").value;
    if (f.match(/[0-9]{4}\-[0-9]{2}\-[0-9]{2}/)) {
        var tf = $("id_fecha").value.split("-");
        var fecha = tf[0]+tf[1]+tf[2]+$("id_hora").value;
        var delta = $("slider-converted-value") ? $("slider-converted-value").value : "00";
        $$(".capa").each(function (item) {
            var field = "";
            var contenido = "";
            if (item.name == "S") {
                field = "color_field";
            }
            if (item.name == "C") {
                field = "contour_field";
            }
            if (item.name == "V") {
                field = "vector_field";
            }
            if (item.value != "Nada") {
                contenido = "<img src='/brams/" + fecha + "/" + item.value + delta + item.name + ".gif'>";
            }
            $(field).update(contenido);
        });
    }
    else {
        alert("Fecha Invalida");
    }
}

function slider() {
    var Event = YAHOO.util.Event,
        Dom   = YAHOO.util.Dom,
        lang  = YAHOO.lang,
        slider,
        bg="slider-bg", thumb="slider-thumb", 
        valuearea="slider-value", textfield="slider-converted-value"

    // The slider can move 0 pixels up
    var topConstraint = 0;
    // The slider can move 200 pixels down
    var bottomConstraint = 480;
    // Custom scale factor for converting the pixel offset into a real value
    var scaleFactor = 1.5;
    // The amount the slider moves when the value is changed with the arrow keys
    var keyIncrement = 20;
    var tickSize = 20;
    Event.onDOMReady(function() {
        slider = YAHOO.widget.Slider.getHorizSlider(bg, 
                         thumb, topConstraint, bottomConstraint, 20);
        // Sliders with ticks can be animated without YAHOO.util.Anim
        slider.animate = false;
        slider.getRealValue = function() {
            return Math.round(this.getValue() * scaleFactor);
        }
        slider.subscribe("change", function(offsetFromStart) {
            var valnode = Dom.get(valuearea);
            var fld = Dom.get(textfield);
            // Display the pixel value of the control
            var actualValue = slider.getRealValue()/10;
            pre = "+"
            if (actualValue < 10)
                pre = pre + "0";
            valnode.innerHTML = "H" + pre + actualValue;
            // update the text box with the actual value
            pre = ""
            if (actualValue < 10)
                pre = pre + "0";
            fld.value = pre + actualValue;
            cambiar_campo();
        });

        Event.on(textfield, "keydown", function(e) {
            // set the value when the 'return' key is detected
            if (Event.getCharCode(e) === 13) {
                var v = parseFloat(this.value, 10);
                v = (lang.isNumber(v)) ? v : 0;
                // convert the real value into a pixel offset
                slider.setValue(Math.round(v/scaleFactor));
            }
        });
    });
};