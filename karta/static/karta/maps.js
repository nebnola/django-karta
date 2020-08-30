async function add_maps(map, geojson_url, on_each_feature){
    let response = await fetch(geojson_url);
    let features = await response.json();
    /* Es gibt zwei GeoJSON Layer, die dieselben Daten enthalten. viewlayer ist
    dazu da, die Polygone auf der Karte darzustellen.
     */
    window.viewlayer = L.geoJSON(null, {style:{fill: false, weight: 2}}).addTo(map);
    /* Das folgende Layer ist unsichtbar, hat aber einen dickeren Rand, um das klicken zu erleichtern.
    Unter layer.viewable ist das Äquivalent in viewlayer zu erreichen
     */
    L.geoJSON( features, {style: {fill: false, weight: 12, opacity: 0.0},
        onEachFeature: on_each_feature}).addTo(map);
    return features;
}

function onEachFeature(feature, layer){
    feature.properties.thisisnew = true;
    viewlayer.addData(feature);
    // now find the layer we just added :/
    for (var i in viewlayer._layers){
        if (viewlayer._layers[i].feature.properties.hasOwnProperty('thisisnew')){ //there it is
            layer.viewable = viewlayer._layers[i];
            delete viewlayer._layers[i].feature.properties.thisisnew;
            break;
        }
    }
    layer.on('popupopen', function(ev){
        layer.viewable.related.li.id="active-map";
        layer.viewable.related.li.scrollIntoView();
    });
    layer.on('popupclose', function(ev) {
        layer.viewable.related.li.id=""
    });
}

function onEachFeatureIndex(feature, layer){
    onEachFeature(feature, layer);
    layer.bindPopup(function(layer) {
        return `<a href=${layer.feature.properties.href}>${layer.feature.properties.karte}</a><br>${layer.feature.properties.massstab}`;
    });
    layer.onEachRelated = function(f){
        /* apply the function f on each related ansicht of this ansicht
        * f should take the viewable (!) layer which corresponds to the ansicht as an argument */
        var ansichten = layer.viewable.related.ansichten;
        for (var i = 0; i < ansichten.length; i++){
            f(ansichten[i]);
        }
    };

    layer.on('popupopen', function(ev) {
        layer.onEachRelated(function (layer) {
            layer._path.classList.add('focused');
        });
    });
    layer.on('popupclose', function(ev) {
        layer.onEachRelated(function(layer){
            layer._path.classList.remove('focused');
        });
    });
    layer.on('mouseover', function(ev){
        layer.onEachRelated(function(layer){
            layer._path.classList.add('hovered');
        });
    });
    layer.on('mouseout', function(ev){
        layer.onEachRelated(function(layer){
            layer._path.classList.remove('hovered');
        });
    });
}

function onEachFeatureMap(feature, layer){
    onEachFeature(feature, layer);
    layer.bindPopup(function (layer) {
        return `${feature.properties.description}<br>${feature.properties.massstab}`
    })
}
function resize_map (map, geojson){
    // zunächst alle Koordinaten von allen Ansichten der Karte sammeln
    allcoords=[];
    for (var i = 0; i<geojson.length; i++){
        allcoords = allcoords.concat(geojson[i].geometry.coordinates[0]);
    }
    // geojson benutzt lonlat stat latlon :/
    for (var i = 0; i<allcoords.length; i++){
        allcoords[i].reverse();
    }
    map.fitBounds(L.latLngBounds(allcoords));
}

function collect_related_li(){
    for (var i in viewlayer._layers){
        if (viewlayer._layers.hasOwnProperty(i)){
            layer=viewlayer._layers[i];
            layer.related={'li': document.querySelector("[pk = '"+layer.feature.properties.pk+"']")};
        }
    }
}

function collect_maps_by_pk(){
    var mapdict = {};
    for (var i in viewlayer._layers){
        if (viewlayer._layers.hasOwnProperty(i)){
            var layer = viewlayer._layers[i];
            var pk = layer.feature.properties.karte_pk;
            if (mapdict[pk]===undefined){
                mapdict[pk] = {ansichten:[]};
                mapdict[pk].li = document.querySelector("[pk = '"+pk+"']");
            }
            mapdict[pk].ansichten.push(layer);
            layer.related=mapdict[pk];
            var dummy=true;
        }
    }
}