map_library = {}

map_library.make_map = function(map_div){
    var map = new ol.Map({
        target: map_div,
        layers: [
            new ol.layer.Tile({
                source: new ol.source.MapQuest({layer: 'sat'})
            })
        ],
        view: new ol.View({
            center: ol.proj.fromLonLat([-105.1314,40.6147]),
            zoom: 3
        })
    });
    return map;
};

map_library.initialize_map = function(map) {
  map.addControl(new ol.control.MousePosition());
  map.addControl(new ol.control.OverviewMap());
  return map;
};

map_library.make_point_layer = function(name, points) {
    var source = new ol.source.Vector({
        features: points
    });
    var layer = new ol.layer.Vector({
        name: name,
        source: source
    });
    return layer;
};

map_library.add_layer_to_map = function(map, layer) {
    map.addLayer(layer);
    return map;
};

map_library.zoom_map = function(map, zoom){
    map.getView().setZoom(zoom);
}
