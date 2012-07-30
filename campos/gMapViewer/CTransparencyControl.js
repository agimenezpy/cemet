/*
* Create a Custom Opacity GControl
* http://www.maptiler.org/google-maps-overlay-opacity-control/
*/

var CTransparencyLENGTH = 58;
// maximum width that the knob can move (slide width minus knob width)

function CTransparencyControl( overlayContainer ) {
    this.overlayC = overlayContainer;
    this.opacity = overlayContainer.curOverlay.getTileLayer().getOpacity();
}
CTransparencyControl.prototype = new GControl();

// This function positions the slider to match the specified opacity
CTransparencyControl.prototype.setSlider = function(pos) {
    var left = Math.round((CTransparencyLENGTH*pos));
    this.slide.left = left;
    this.knob.style.left = left+"px";
    this.knob.style.top = "0px";
}

// This function reads the slider and sets the overlay opacity level
CTransparencyControl.prototype.setOpacity = function() {
    // set the global variable
    this.overlayC.curOverlay.getTileLayer().opacity = this.slide.left/CTransparencyLENGTH;
    this.map.removeOverlay(this.overlayC.curOverlay);
    this.map.addOverlay(this.overlayC.curOverlay,{zPriority: this.overlayC.curOverlay.getTileLayer().priority});
}

// This gets called by the API when addControl(new CTransparencyControl())
CTransparencyControl.prototype.initialize = function(map) {
    var that=this;
    this.map = map;

    // Is this MSIE, if so we need to use AlphaImageLoader
    var agent = navigator.userAgent.toLowerCase();
    if ((agent.indexOf("msie") > -1) && (agent.indexOf("opera") < 1)){this.ie = true} else {this.ie = false}

    // create the background graphic as a <div> containing an image
    var container = document.createElement("div");
    container.style.width="70px";
    container.style.height="21px";

    // Handle transparent PNG files in MSIE
    if (this.ie) {
      container.innerHTML = '<div class="cnt_child_ie" ></div>';
    } else {
      container.innerHTML = '<div class="cnt_child" ></div>';
    }

    // create the knob as a GDraggableObject
    // Handle transparent PNG files in MSIE
    if (this.ie) {
        this.knob = document.createElement("div");
        $(this.knob).addClass("knob_ie");
        this.knob_img = document.createElement("div");
        $(this.knob_img).addClass("knob_img");
        this.knob.appendChild(this.knob_img);
    } else {
        this.knob = document.createElement("div");
         $(this.knob).addClass("knob");
    }
    container.appendChild(this.knob);
    this.slide=new GDraggableObject(this.knob, {container:container});
    this.slide.setDraggableCursor('pointer');
    this.slide.setDraggingCursor('pointer');
    this.container = container;

    // attach the control to the map
    map.getContainer().appendChild(container);

    // init slider
    this.setSlider(this.opacity);

    // Listen for the slider being moved and set the opacity
    GEvent.addListener(this.slide, "dragend", function() {that.setOpacity()});
    //GEvent.addListener(this.container, "click", function( x, y ) { alert(x, y) });

    return container;
}

// Set the default position for the control
CTransparencyControl.prototype.getDefaultPosition = function() {
    return new GControlPosition(G_ANCHOR_TOP_RIGHT, new GSize(7, 47));
}
