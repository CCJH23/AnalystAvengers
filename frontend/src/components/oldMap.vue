
<!-- <template>
    <div>
        <div style="max-width: 800px; margin: 0 auto; display: flex; align-items: center; justify-content: space-between">
            <div>
                <h1>Your coordinates:</h1>
                <p>{{ myCoordinates.lat }} Latitude, {{ myCoordinates.lng }} Longitude</p>
            </div>
            <div>
                <h1>Map coordinates:</h1>
                <p>{{ mapCoordinates.lat }} Latitude, {{ mapCoordinates.lng }} Longitude</p>
            </div>
        </div>
        <GmapMap
            :center="myCoordinates"
            :zoom="zoom"
            style="width:640px; height:360px; margin: 32px auto;"
            ref="mapRef"
            @dragend="handleDrag"
        ></GmapMap>
    </div>
</template>
<script> -->
    <!-- export default {
        data() {
            return {
                map: null,
                myCoordinates: {
                    lat: 0,
                    lng: 0
                },
                zoom: 7
            }
        },
        created() {
            // does the user have a saved center? use it instead of the default
            if(localStorage.center) {
                this.myCoordinates = JSON.parse(localStorage.center);
            } else {
                // get user's coordinates from browser request
                this.$getLocation({})
                    .then(coordinates => {
                        this.myCoordinates = coordinates;
                    })
                    .catch(error => alert(error));
            }

            // does the user have a saved zoom? use it instead of the default
            if(localStorage.zoom) {
                this.zoom = parseInt(localStorage.zoom);
            }
        },
        mounted() {
            // add the map to a data object
            this.$refs.mapRef.$mapPromise.then(map => this.map = map);
        },
        methods: {
            handleDrag() {
                // get center and zoom level, store in localstorage
                let center = {
                    lat: this.map.getCenter().lat(),
                    lng: this.map.getCenter().lng()
                };
                let zoom = this.map.getZoom();

                localStorage.center = JSON.stringify(center);
                localStorage.zoom = zoom;
            }
        },
        computed: {
            mapCoordinates() {
                if(!this.map) {
                    return {
                        lat: 0,
                        lng: 0
                    };
                }

                return {
                    lat: this.map.getCenter().lat().toFixed(4),
                    lng: this.map.getCenter().lng().toFixed(4)
                }
            }
        }
    }
</script> -->
<!-- <template>

    <div class="GoogleMap">
      <div class="SearchArea" v-if="autocomplete">
        <input
          v-bind="$attrs"
          ref="SearchInput"
          :class="inputClass"
          :disabled="disabledSearch"
          v-model="address"
        />
      </div>
      <iframe
        :src="mapSrc"
        width="100%"
        height="500px"
        frameborder="0"
        style="border:0"
        allowfullscreen
      ></iframe>
    </div>
  </template>
  
  <script>
  export default {
    name: 'VueGoogleMapUI',
    emits: [
      'change-address',
      'update-circle',
      'update-polygon',
      'update-polyline',
      'update-rectangle',
      'update-marker'
    ],
    props: {
      disabledSearch: { type: Boolean },
      inputClass: { type: String, default: '' },
      autocomplete: { type: Boolean, default: false }
    },
    data() {
      return {
        address: ''
      };
    },
    computed: {
      mapSrc() {
        return "https://maps.google.com/maps?q=Tangesir%20Dates%20Products&amp;t=&amp;z=13&amp;ie=UTF8&amp;iwloc=&amp;output=embed";
      }
    },
    methods: {
      setAddressData(address) {
        if (!address) return;
        this.address = address.formatted_address;
        this.$emit('change-address', { info: address, address: this.address });
      },
      setAutoComplete() {
        // Implement autocomplete logic if needed
      },
      async setLocation() {
        // Implement location logic if needed
      },
      setCurrentAddres() {
        // Implement current address logic if needed
      }
      // Add more methods as needed
    },
    async mounted() {
      // Implement initialization logic if needed
    },
    watch: {
      language() {
        // Implement language change logic if needed
      }
    },
    beforeUnmount() {
      // Implement cleanup logic if needed
    }
  };
  </script>
  
  <style>
  .GoogleMap {
    height: max-content;
    background: rgb(229, 227, 223);
  }
  
  .GoogleMap .SearchArea {
    border: 1px solid #ddd;
    border-radius: 6px;
    display: flex;
  }
  
  .GoogleMap .SearchArea input {
    flex: 1;
    outline: none;
    border: none;
    height: 30px;
    padding: 10px;
  }
  </style>
   -->

   <!-- <template>
   Your existing template code for the map component goes here -->
  
    <!-- New template code for displaying current position -->
    <!-- <div class="d-flex text-center" style="height: 20vh">
      <div class="m-auto">
        <h4>Your Position</h4>
        Latitude {{ currPos.lat.toFixed(2) }}, Longitude: {{ currPos.lng.toFixed(2) }}
      </div>
    </div>
  </template>
   -->
  <!-- <script>
  import { computed } from 'vue'
  import { useGeolocation } from '../useGeolocation.js'
  
  export default {
    setup() {
      // Add the useGeoLocation logic here
      const { coords } = useGeolocation()
      const currPos = computed(() => ({
        lat: coords.value.latitude,
        lng: coords.value.longitude
      }))
      
      return { currPos }
    }
  }
  </script> -->

  <!-- <template>
    <div class="h-full w-full rounded overflow-hidden shadow">
        <l-map v-model:zoom="zoom" :zoom="zoom" :minZoom="4" :maxZoom="18" :zoomAnimation="true"
               :center="center" @click="addMarker" class="cursor-auto">
            <l-tile-layer :url="url" :attribution="attribution" layer-type="base"/>
            <l-marker v-if="modelValue" draggable :lat-lng="[modelValue.lat, modelValue.lng]"
                      @click="removeMarker" key="marker"></l-marker>

          <l-control>
               Hello, Map!
           </l-control>
        </l-map>
    </div>
</template>
<script setup>
import {LMap, LTileLayer, LMarker, LControl} from "@vue-leaflet/vue-leaflet";
import "leaflet/dist/leaflet.css";
import L from "leaflet"

const props = defineProps(['modelValue'])
const emits = defineEmits(['update:modelValue'])

const zoom = 10
const center = [9.9356124, -84.1483645]
const url = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
const attribution = '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'

const addMarker = (e) => {
    if (e.latlng !== undefined) {
        emits("update:modelValue", e.latlng)
    }
  }
</script> -->
