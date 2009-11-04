function cambiar_campo(opcion) {
    var fecha = "2009100900";
    var contenido = "";
    var field = "";
    if (opcion.name == "S") {
        field = "color_field";
    }
    if (opcion.name == "C") {
        field = "contour_field";
    }
    if (opcion.name == "V") {
        field = "vector_field";
    }
    if (opcion.value != "Nada") {
        contenido = "<img src='/brams/" + fecha + "/" + opcion.value + opcion.name + ".gif'>";
    }
    $(field).update(contenido);
}