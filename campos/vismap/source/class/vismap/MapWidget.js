qx.Class.define("vismap.MapWidget",
{
    extend: qx.ui.window.Window,
    construct: function (title) {
        this.base(arguments, title);
        this.url = "http://200.10.229.172/brams/";
        
        this.setLayout(new qx.ui.layout.HBox(2));
        
        this.add(this._createControls());
        
        var container = new qx.ui.container.Composite(new qx.ui.layout.VBox(2));
        container.add(this._createSlider());
        container.add(this._createMap());
        this.add(container);
        
        this.setShowClose(false);
        this.setShowMaximize(false);
        this.setShowMinimize(false);
        this.setWidth(700);
        this.setHeight(480);
    },
    members: {
       _changeMap : function (){
            if (this.form.validate()) {
                var delta = (this.group.slider.getValue() < 10) ? "0" + this.group.slider.getValue() : this.group.slider.getValue().toString();
                var imgsrc;
                if (this.color.getSelection()[0].getModel() != "Nada") {
                    imgsrc = this.url + "last/COLOR_" + this.color.getSelection()[0].getModel() + "_" + delta + ".gif";
                    this.color_field.setSource(imgsrc);
                    //this.color_field.setSource(imgsrc);
                    //if (this.color_field.getSource() != imgsrc) {
                    //    qx.io.ImageLoader.load(imgsrc, function() {
                    //        this.setSource(imgsrc)
                    //        slider.setEnabled(true);
                    //    }, this.color_field)
                    //}
                }
                else {
                    this.color_field.setSource("")
                }
                if (this.contor.getSelection()[0].getModel() != "Nada") {
                    imgsrc = this.url + "last/CONTOUR_" +  this.contor.getSelection()[0].getModel() + "_" +  delta + ".gif";
                    this.contour_field.setSource(imgsrc);
                    //if (this.contour_field.getSource() != imgsrc) {
                    //    qx.io.ImageLoader.load(imgsrc, function() {
                    //        this.setSource(imgsrc)
                    //    }, this.contour_field)
                    //}
                }
                else {
                    this.contour_field.setSource("");
                }
                if (this.vector.getSelection()[0].getModel() != "Nada") {
                    imgsrc = this.url + "last/VECTOR_" +  this.vector.getSelection()[0].getModel() + "_" + delta + ".gif";
                    this.vector_field.setSource(imgsrc);
                    //if (this.vector_field.getSource() != imgsrc) {
                    //    qx.io.ImageLoader.load(imgsrc, function() {
                    //        this.setSource(imgsrc)
                    //    }, this.vector_field)
                    //}
                }
                else {
                    this.vector_field.setSource("");   
                }
            }
        },
        _createSliderGroup : function(slider)
        {
          var group =
          {
            slider: slider,
            minimum: new qx.ui.basic.Label("0"+slider.getMinimum().toString()),
            maximum: new qx.ui.basic.Label(slider.getMaximum().toString()),
            value: new qx.ui.basic.Label("H+" +
                            ( (slider.getValue() < 10) ? "0" + slider.getValue().toString() : slider.getValue().toString()))
          };
    
          slider.addListener("changeValue", function(e) {
            group.value.setValue("H+" +
                            ( (slider.getValue() < 10) ? "0" + slider.getValue().toString() : slider.getValue().toString()));
            this._changeMap();
          },this);
    
          return group;
        },
        _createSlider : function () {
            var grid = new qx.ui.layout.Grid();
            var container = new qx.ui.container.Composite(grid);
        
            container.setWidth(400);
            container.setHeight(20);
        
            grid.setSpacing(5);
            grid.setColumnFlex(0, 1);
            grid.setColumnFlex(1, 1);
            grid.setColumnFlex(2, 1);
            grid.setColumnAlign(0, "left", "bottom");
            grid.setColumnAlign(1, "center", "bottom");
            grid.setColumnAlign(2, "right", "bottom");

    
            this.group = this._createSliderGroup(new qx.ui.form.Slider().set({
                minimum: 0,
                maximum: 120,
                singleStep: 3,
                pageStep: 3,
                value: 0
            }));
            
            this.group.slider.setOrientation("horizontal");
    
            this.group.value.setWidth(100);
            this.group.value.setTextAlign("center");
    
            container.add(this.group.minimum, {row: 0, column: 0});
            container.add(this.group.value, {row: 0, column: 1});
            container.add(this.group.maximum, {row: 0, column: 2});
    
            container.add(this.group.slider, {row: 1, column: 0, colSpan: 3, rowSpan: 0});
            return container;
        },
        _createMap : function () {
            this.shaded_relief = new qx.ui.basic.Image(this.url + "BASE_C.gif")
                            .set({zIndex:-50});
            this.color_field = new qx.ui.basic.Image()
                                .set({zIndex:-40});
            this.map = new qx.ui.basic.Image(this.url + "BASE.gif")
                                .set({zIndex:-30});
            this.contour_field = new qx.ui.basic.Image()
                                .set({zIndex:-20});
            this.vector_field = new qx.ui.basic.Image()
                                .set({zIndex:-10});
            
            var container = new qx.ui.container.Composite(new qx.ui.layout.Basic());
            
            container.add(this.shaded_relief, {left: 40,top:30});
            container.add(this.color_field);
            container.add(this.map);
            container.add(this.contour_field);
            container.add(this.vector_field);
            return container;
        },
        _createControls : function () {
              // create the form
            var form = new qx.ui.form.Form();
      
            // add the second header
            form.addGroupHeader("Campos");
            
            var color = new qx.ui.form.SelectBox();
            color.add(new qx.ui.form.ListItem("Ninguno",null,"Nada"));
            color.add(new qx.ui.form.ListItem("-- SUPERFICIE --",null,"Nada"));
            color.add(new qx.ui.form.ListItem("Temperatura a 2m",null,"TEMP2M"));
            color.add(new qx.ui.form.ListItem("Presión a nivel del mar",null,"SLP"));
            color.add(new qx.ui.form.ListItem("Viento a 10m",null,"WIND10M"));
            color.add(new qx.ui.form.ListItem("Precipitación Acumulada",null,"PCP"));
            color.add(new qx.ui.form.ListItem("-- AIRE --",null,"Nada"));
            color.add(new qx.ui.form.ListItem("Viento 250",null,"WIND250"));
            color.add(new qx.ui.form.ListItem("Viento 500",null,"WIND500"));
            color.add(new qx.ui.form.ListItem("Viento 700",null,"WIND700"));
            color.add(new qx.ui.form.ListItem("Viento 850",null,"WIND850"));
            color.add(new qx.ui.form.ListItem("Temperatura 250",null,"TEMP250"));
            color.add(new qx.ui.form.ListItem("Temperatura 500",null,"TEMP500"));
            color.add(new qx.ui.form.ListItem("Temperatura 700",null,"TEMP700"));
            color.add(new qx.ui.form.ListItem("Temperatura 850",null,"TEMP850"));
            color.add(new qx.ui.form.ListItem("Humedad Relativa 250",null,"RH250"));
            color.add(new qx.ui.form.ListItem("Humedad Relativa 500",null,"RH500"));
            color.add(new qx.ui.form.ListItem("Humedad Relativa 700",null,"RH700"));
            color.add(new qx.ui.form.ListItem("Humedad Relativa 850",null,"RH850"));
            color.add(new qx.ui.form.ListItem("Geopotential Height 250",null,"GEO250"));
            color.add(new qx.ui.form.ListItem("Geopotential Height 500",null,"GEO500"));
            color.add(new qx.ui.form.ListItem("Geopotential Height 700",null,"GEO700"));
            color.add(new qx.ui.form.ListItem("Geopotential Height 850",null,"GEO850"));
            color.add(new qx.ui.form.ListItem("-- DIAGNOSTICO --",null,"Nada"));
            color.add(new qx.ui.form.ListItem("Thick 1000-500",null,"GEOTHICK"));
            color.add(new qx.ui.form.ListItem("Nubes",null,"CLOUD"));
            form.add(color, "Color");
            
            var contor = new qx.ui.form.SelectBox();
            contor.add(new qx.ui.form.ListItem("Ninguno",null,"Nada"));
            contor.add(new qx.ui.form.ListItem("-- SUPERFICIE --",null,"Nada"));
            contor.add(new qx.ui.form.ListItem("Temperatura a 2m",null,"TEMP2M"));
            contor.add(new qx.ui.form.ListItem("Presión a nivel del mar",null,"SLP"));
            contor.add(new qx.ui.form.ListItem("Viento a 10m",null,"WIND10M"));
            contor.add(new qx.ui.form.ListItem("Precipitación Acumulada",null,"PCP"));
            contor.add(new qx.ui.form.ListItem("-- AIRE --",null,"Nada"));
            contor.add(new qx.ui.form.ListItem("Viento 250",null,"WIND250"));
            contor.add(new qx.ui.form.ListItem("Viento 500",null,"WIND500"));
            contor.add(new qx.ui.form.ListItem("Viento 700",null,"WIND700"));
            contor.add(new qx.ui.form.ListItem("Viento 850",null,"WIND850"));
            contor.add(new qx.ui.form.ListItem("Temperatura 250",null,"TEMP250"));
            contor.add(new qx.ui.form.ListItem("Temperatura 500",null,"TEMP500"));
            contor.add(new qx.ui.form.ListItem("Temperatura 700",null,"TEMP700"));
            contor.add(new qx.ui.form.ListItem("Temperatura 850",null,"TEMP850"));
            contor.add(new qx.ui.form.ListItem("Humedad Relativa 250",null,"RH250"));
            contor.add(new qx.ui.form.ListItem("Humedad Relativa 500",null,"RH500"));
            contor.add(new qx.ui.form.ListItem("Humedad Relativa 700",null,"RH700"));
            contor.add(new qx.ui.form.ListItem("Humedad Relativa 850",null,"RH850"));
            contor.add(new qx.ui.form.ListItem("Geopotential Height 250",null,"GEO250"));
            contor.add(new qx.ui.form.ListItem("Geopotential Height 500",null,"GEO500"));
            contor.add(new qx.ui.form.ListItem("Geopotential Height 700",null,"GEO700"));
            contor.add(new qx.ui.form.ListItem("Geopotential Height 850",null,"GEO850"));
            contor.add(new qx.ui.form.ListItem("-- DIAGNOSTICO --",null,"Nada"));
            contor.add(new qx.ui.form.ListItem("Thick 1000-500",null,"GEOTHICK"));
            contor.add(new qx.ui.form.ListItem("Nubes",null,"CLOUD"));
            form.add(contor, "Contorno");
            
            var vector = new qx.ui.form.SelectBox();
            vector.add(new qx.ui.form.ListItem("Ninguno",null,"Nada"));
            vector.add(new qx.ui.form.ListItem("Viento 250",null,"WIND250"));
            vector.add(new qx.ui.form.ListItem("Viento 500",null,"WIND500"));
            vector.add(new qx.ui.form.ListItem("Viento 700",null,"WIND700"));
            vector.add(new qx.ui.form.ListItem("Viento 850",null,"WIND850"));
            form.add(vector, "Viento");
        
            this.color = color, this.contor = contor, this.vector = vector;
            this.form = form;
            this.color.addListener("changeSelection", this._changeMap, this);
            this.contor.addListener("changeSelection", this._changeMap, this);
            this.vector.addListener("changeSelection", this._changeMap, this);
            // send button with validation
            //var sendButton = new qx.ui.form.Button("Cambiar Mapa");
            //sendButton.addListener("execute", this._changeMap, this);
            //form.addButton(sendButton);
            return new qx.ui.form.renderer.Single(form);
        }
    }
});
