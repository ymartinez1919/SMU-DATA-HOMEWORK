$(document).ready(function() {
    doWork();
});

function doWork() {
//    choosing to display all week: https://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php, https://github.com/fraxen/tectonicplates
    var url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_week.geojson";
    var url_plates = "static/plates_data/PB2002_boundaries.json";
    requestD3(url, url_plates);
}

function requestD3(url,url_plates) {

    // Perform a GET request to the query URL., first for map and then plates
    d3.json(url).then(function(data) {
        d3.json(url_plates).then(function(plates_data){
            console.log(data);
            console.log(plates_data);
            createMap(data,plates_data);
        });
    });

}


function onEachFeature(feature, layer) {
    // adding popup content title and time of earthquake
    if (feature.properties) {
        layer.bindPopup(`<h3>${feature.properties.title}</h3><hr><p>Time:${new Date(feature.properties.time)}</p >`);
    }
}


// createMap() takes the earthquake data and incorporates it into the vis
function createMap(data, plates_data) {

    // apply the filter (if necessary)
    var earthquakes = data.features

    // My chosen Base Layers : https://docs.mapbox.com/api/maps/styles/
    var dark_layer = L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        id: 'mapbox/dark-v10',
        accessToken: API_KEY
    });

    var light_layer = L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        id: 'mapbox/light-v10',
        accessToken: API_KEY
    });

    var satellite_layer = L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        id: 'mapbox/satellite-v9',
        accessToken: API_KEY
    });

    var outdoors_layer = L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        id: 'mapbox/outdoors-v11',
        accessToken: API_KEY
    });


    // Create plate layer and change color
    var techtonicplates = L.geoJSON(plates_data.features,{
        style: { "color": "#ffbf00", "weight": "3",}
    });

    // create my circles
    var circles = [];
    for (let i = 0; i < earthquakes.length; i++) {
        let earthquake = earthquakes[i];
        let circle_color = getColor(earthquake.geometry.coordinates[2]);
        let radius_size = getRadius(earthquake.properties.mag);

        // the coordinates are reversed in data set 
        let location = [earthquake.geometry.coordinates[1], earthquake.geometry.coordinates[0]]

        let circle = L.circle(location, {
            color: circle_color,
            fillColor: circle_color,
            fillOpacity: 0.8,
            radius: radius_size, 
        }).bindPopup(`<h3>${ earthquake.properties.title }</h3><hr><p>${new Date(earthquake.properties.time)}</p >`);
        circles.push(circle);
    }

    var circleLayer = L.layerGroup(circles);
    
    //let the radius of my circles depend on magnitude. higher magnitude=bigger circle
    function getRadius(mag) {
        return mag * 10000
    }
    

    //color of my circles based depth .The depth of the earth can be found as the third coordinate for each earthquake.
    function getColor(coordinates) {
        let color = '#ff0000';
    
        if (coordinates >= 90) {
            color = "#ff0000";
        } else if (coordinates >= 70) {
            color = "#ff8000";
        } else if (coordinates >= 50) {
            color = "#ffbf00";
        } else if (coordinates >= 30) {
            color = "#ffff00";
        } else if (coordinates >= 10) {
            color = "#bfff00";
        } else {
            color = '#40ff00';
        }
    
        return (color);
    }
 
    // Create a baseMaps object.
    var baseMaps = {
        "Dark": dark_layer,
        "Light": light_layer,
        "Satellite": satellite_layer,
        "Outdoors": outdoors_layer
    };

    // Overlays that can be toggled on or off
    var overlayMaps = {
        // Pins: earthquakeLayer,
        Earthquakes: circleLayer,
        Techtonic_Plates: techtonicplates,
    };

    
    // Create a new map.
    // Edit the code to add the earthquake data to the layers.
    var myMap = L.map("map", {
        center: [
            37.09, -95.71
        ],
        zoom: 5,
        layers: [satellite_layer, circleLayer, techtonicplates]
    });

    // Create a layer control that contains our baseMaps.
    // Be sure to add an overlay Layer that contains the earthquake GeoJSON.
    L.control.layers(baseMaps, overlayMaps).addTo(myMap);

    //add my legend to map//rember to add css
    // https://gis.stackexchange.com/questions/133630/adding-leaflet-legend
    var legend = L.control({
        position: "bottomright",
    });

    legend.onAdd = function() {
        var div = L.DomUtil.create('div', 'info legend');
        var labels = ["DEPTH OF EARTHQUAKE:","-10-10", "10-30", "30-50", "50-70", "70-90", "90+"];
        var colors = ["white","#40ff00", "#bfff00", "#ffff00", "#ffbf00", "#ff8000", "#ff0000"];

        for (let i = 0; i < labels.length; i++) {
            let label = labels[i];
            let color = colors[i];

            let html = `<i style='background:${color}'></i>${label}<br>`;
            div.innerHTML += html;
        }
        return div;
        };

    legend.addTo(myMap);




}