station_library = {};

station_library.get_ol_stations = function(station_array) {
    var stations = [];
    for(var i=0; i<station_array.length; i++) {
        var point = new ol.geom.Point(ol.proj.fromLonLat([station_array[i].location.point.coordinates[0],station_array[i].location.point.coordinates[1]]));
        var name = station_array[i].id;
        var program = station_array[i].program;
        var locality = station_array[i].location.locality;
        var station = new ol.Feature({
            geometry: point,
            name: name,
            program: program,
            locality: locality
        });
        stations.push(station);
    }
    return stations;
};
