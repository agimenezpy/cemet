
function ColorBar(mapDef) {
    this.baseUrl = mapDef.baseUrl;
    this.date = mapDef.date;
    this.size = new GSize(mapDef.map.getSize().width, 24);
    mapDef.colorBar = this;
}

ColorBar.prototype = new GControl();

ColorBar.prototype.getDefaultPosition = function() {
    return new GControlPosition(G_ANCHOR_BOTTOM_LEFT, new GSize(0, 15));
}

ColorBar.prototype.initialize = function(map) {
    this.map = map;
    this.cont = document.createElement("div");
    this.img = document.createElement("img");
    this.cont.appendChild(this.img);
    this.img.src = this.baseUrl + "/none.png";
    this.cont.style.width = this.size.width + "px";
    this.cont.style.height = this.size.height + "px";
    this.cont.style.textAlign = "center";
    map.getContainer().appendChild(this.cont);
    return this.cont;
}

ColorBar.prototype.setImage = function (mObj, id) {
    mObj.colorBar.img.src = [mObj.baseUrl,mObj.date,mObj.curOverlay.name,"COLORBAR"+(mObj.curOverlay.timed ? "_" + mObj.time : "" )+".gif"].join("/");
}
