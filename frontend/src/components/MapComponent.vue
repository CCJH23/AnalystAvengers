<!-- Map component to be included when viewing the status of each service group  -->
<template>
  <div>
    <div ref="map" style="height: 500px;"></div>
  </div>
</template>

<script>
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import countriesData from './countries'

export default {
  props: {
    mapData: Object,
    servers: Object,
    group: Number,
  },
  watch: {
    servers: {
      handler: function (newServers) {
        // Clear the existing map
        if (this.map) {
          this.map.remove();
          this.map = null;
        }
        // Rebuild the map
        this.buildMapComponent()
      },
      deep: true // Ensure deep watching for changes in nested objects
    }
  },
  mounted(){
    this.buildMapComponent()
  },
  data() {
    return {
      map: null,
      countriesData: countriesData,
      countriesColorData: {"type":"FeatureCollection","features":[]},
      geojson: null,
      info: null,
    };
  },
  methods: {
    buildMapComponent(){
      this.map = L.map(this.$refs.map).setView([0, 0], 2); // Centered at (0, 0) with zoom level 2

      L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: '© OpenStreetMap contributors',
      }).addTo(this.map);

      // Record server status and countries in service group
      var dummyCountriesData = JSON.parse(JSON.stringify(this.countriesData));
      for (var server in this.servers){
        var serverStatus = this.servers[server]
        var mapData = this.mapData[server]
        if (mapData){
          var country = mapData['country']
          var groupId = mapData['groupId']
          if (groupId == this.group){
            if (dummyCountriesData.hasOwnProperty(country)){
              var countryProperties = dummyCountriesData[country]['properties']
              serverStatus = serverStatus.toLowerCase()
              countryProperties[serverStatus] += 1
              this.countriesColorData['features'].push(dummyCountriesData[country])
            } else {
              console.log(`${country} does not exist`)
            }
          }
        }
      }

      // Add styling to countries based on server status
      this.geojson = L.geoJson(this.countriesColorData, {
        style: this.style,
        onEachFeature: this.onEachFeature
      }).addTo(this.map);

      // Initialize the custom control and add it to the map
      this.info = L.control();
      this.info.onAdd = function (map) {
        this._div = L.DomUtil.create('div', 'info');
        this.update();
        return this._div;
      };
      // Create server status summary text on top right of map
      this.info.update = function (props) {
        this._div.innerHTML = '<h4>Server Status</h4>' +  (props ?
            '<b>' + props.name + '</b><br />' + 
            (props.healthy === 1 ? '<b>' + props.healthy + '</b> healthy server' : '<b>' + props.healthy + '</b> healthy servers') +
            '<br />' +
            (props.unhealthy === 1 ? '<b>' + props.unhealthy + '</b> unhealthy server' : '<b>' + props.unhealthy + '</b> unhealthy servers') + 
            '<br />' +
            (props.degraded === 1 ? '<b>' + props.degraded + '</b> degraded server' : '<b>' + props.degraded + '</b> degraded servers')
            : 'Hover over a highlighted country');
      };
      this.info.addTo(this.map);
    },
    createMarkerIcon(color) {
      return new L.Icon({
        iconUrl: `https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-${color}.png`,
        shadowUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-shadow.png',
        iconSize: [25, 41],
        iconAnchor: [12, 41],
        popupAnchor: [1, -34],
        shadowSize: [41, 41],
      });
    },
    getColor(healthy, degraded, unhealthy) {
      if (unhealthy > 0){
        // If there is unhealthy, return red
        return "#FF0000";
      } else if (degraded > 0){
        // if there is degraded, return orange
        return "orange";
      } else if (healthy > 0) {
        // else return green
        return "green";
      }
    },
    // style map on country according to server status
    style(feature){
      return {
          fillColor: this.getColor(feature.properties.healthy, feature.properties.degraded, feature.properties.unhealthy),
          weight: 2,
          opacity: 1,
          color: 'white',
          dashArray: '3',
          fillOpacity: 1.0
      };
    },
    // highlights area on mouseover
    highlightFeature(e){
      var layer = e.target;
      layer.setStyle({
          weight: 5,
          color: '#666',
          dashArray: '',
          fillOpacity: 0.7
      });
      layer.bringToFront();
      this.info.update(layer.feature.properties);
    },
    // returns to normal after mouseout
    resetHighlight(e){
      this.geojson.resetStyle(e.target);
      this.info.update();
    },
    zoomToFeature(e){
      this.map.fitBounds(e.target.getBounds());
    },
    onEachFeature(feature,layer){
      layer.on({
          mouseover: this.highlightFeature,
          mouseout: this.resetHighlight,
          click: this.zoomToFeature
      });
    }
  }
};
</script>

<style>
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
</style>