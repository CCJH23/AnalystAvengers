<template><div id="map"></div></template>

<script setup lang="ts">
import leaflet from "leaflet";
import { onMounted, watchEffect } from "vue";
import { useGeolocation } from "@vueuse/core";
import { userMarker, nearbyMarkers} from "@/stores/mapStore";
import {countriesData} from "@/components/countries";
import axios from 'axios';

const { coords } = useGeolocation();

let map: leaflet.Map;
let userGeoMarker: leaflet.Marker;

onMounted(() => {
  map = leaflet
  .map('map')
  .setView([userMarker.value.latitude, userMarker.value.longitude], 13);

  leaflet
  .tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
  }).addTo(map);

  nearbyMarkers.value.forEach(({latitude, longitude})=> {
    leaflet
      .marker([latitude, longitude])
      .addTo(map)
      .bindPopup(`Saved Marker at (<strong>${latitude.toFixed(2)},${longitude.toFixed(2)}</strong>)`);
    nearbyMarkers.value.push({latitude, longitude})

  });

  map.addEventListener('click', (e) => {
    
    const {lat: latitude, lng: longitude} = e.latlng;

    leaflet
      .marker([latitude, longitude])
      .addTo(map)
      .bindPopup(`Saved Marker at (<strong>${latitude.toFixed(2)},${longitude.toFixed(2)}</strong>)`);

    nearbyMarkers.value.push({latitude, longitude})
  })

  leaflet.geoJSON(countriesData).addTo(map);

  function getColor(d) {
    return d > 1000 ? '#800026' :
           d > 500  ? '#BD0026' :
           d > 200  ? '#E31A1C' :
           d > 100  ? '#FC4E2A' :
           d > 50   ? '#FD8D3C' :
           d > 20   ? '#FEB24C' :
           d > 10   ? '#FED976' :
                      '#FFEDA0';
  }

  function style(feature) {
    return {
        fillColor: getColor(feature.properties.density),
        weight: 2,
        opacity: 1,
        color: 'white',
        dashArray: '3',
        fillOpacity: 0.7
    };
}

  leaflet.geoJson(countriesData, {style: style}).addTo(map);

  function highlightFeature(e) {
  var layer = e.target;

  layer.setStyle({
      weight: 5,
      color: '#666',
      dashArray: '',
      fillOpacity: 0.7
  });

  layer.bringToFront();
  info.update(layer.feature.properties);
}

function resetHighlight(e) {
    geojson.resetStyle(e.target);
    info.update();
}

var geojson;
// ... our listeners
geojson = leaflet.geoJson(countriesData); 

function zoomToFeature(e) {
    map.fitBounds(e.target.getBounds());
}

function onEachFeature(feature, layer) {
    layer.on({
        mouseover: highlightFeature,
        mouseout: resetHighlight,
        click: zoomToFeature
    });
}

geojson = leaflet.geoJson(countriesData, {
    style: style,
    onEachFeature: onEachFeature
}).addTo(map);

var info = leaflet.control();

info.onAdd = function (map) {
    this._div = leaflet.DomUtil.create('div', 'info'); // create a div with a class "info"
    this.update();
    return this._div;
};

// method that we will use to update the control based on feature properties passed
info.update = function (props) {
    this._div.innerHTML = '<h4>Country Population Density</h4>' +  (props ?
        '<b>' + props.name + '</b><br />' + props.density + ' people / mi<sup>2</sup>'
        : 'Hover over a country');
};

var legend = leaflet.control({position: 'bottomright'});

legend.onAdd = function (map) {
    var div = leaflet.DomUtil.create('div', 'info legend'),
        grades = [0, 10, 20, 50, 100, 200, 500, 1000],
        labels = [];

    // loop through our density intervals and generate a label with a colored square for each interval
    for (var i = 0; i < grades.length; i++) {
        var color;
        var d = grades[i] + 1;
        if (d > 1000) {
            color = '#800026';
        } else if (d > 500) {
            color = '#BD0026';
        } else if (d > 200) {
            color = '#E31A1C';
        } else if (d > 100) {
            color = '#FC4E2A';
        } else if (d > 50) {
            color = '#FD8D3C';
        } else if (d > 20) {
            color = '#FEB24C';
        } else if (d > 10) {
            color = '#FED976';
        } else {
            color = '#FFEDA0';
        }
        div.innerHTML +=
            '<i style="background:' + color + '"></i> ' +
            grades[i] + (grades[i + 1] ? '&ndash;' + grades[i + 1] + '<br>' : '+');
    }

    return div;
}


legend.addTo(map);

info.addTo(map);

// fetchIpAddressAndInitializeMap();

});

// async function fetchIpAddressAndInitializeMap() {
//   try {
//     const response = await axios.get('https://ipinfo.io/json');
//     const { loc } = response.data;
//     const [latitude, longitude] = loc.split(',').map(parseFloat);

//     const marker = leaflet.marker([latitude, longitude]).addTo(map);
//     marker.bindPopup('Your Location');
//   } catch (error) {
//     console.error('Error resolving IP address:', error);
//   }
// }

watchEffect(() => {
  if (coords.value.latitude !== Number.POSITIVE_INFINITY && coords.value.longitude !== Number.POSITIVE_INFINITY) {
      userMarker.value.latitude = coords.value.latitude;
      userMarker.value.longitude = coords.value.longitude;

//       // removes old marker before adding a new one
      if(userGeoMarker) {
        map.removeLayer(userGeoMarker)
        
      }

      userGeoMarker = leaflet
      .marker([userMarker.value.latitude, userMarker.value.longitude])
      .addTo(map)
      .bindPopup('User Marker');

      map.setView([52.1326, 5.2913], 3)
      
//       // changes marker color
      const el = userGeoMarker.getElement();
      if(el){
        el.style.filter = "hue-rotate(120deg)";
      }
  }
})

</script>

<style scoped>
  #map {
    width: 80%;
    height: 50vh;
    margin-left: 150px;
  }

  .info {
    padding: 6px 8px;
    font: 14px/16px Arial, Helvetica, sans-serif;
    background: white;
    background: rgba(255,255,255,0.8);
    box-shadow: 0 0 15px rgba(0,0,0,0.2);
    border-radius: 5px;
  }

  .info h4 {
      margin: 0 0 5px;
      color: #777;
  }
  
  .legend {
    line-height: 18px;
    color: #555;
}

  .legend i {
      width: 18px;
      height: 18px;
      float: left;
      margin-right: 8px;
      opacity: 0.7;
  }

  .info.legend {
    background-color: white;
    padding: 5px;
    border-radius: 5px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
}

.info.legend i {
    width: 20px;
    height: 20px;
    display: inline-block;
    margin-right: 5px;
}


</style>