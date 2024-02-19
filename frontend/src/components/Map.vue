<!-- <template>
    <div class="world-map">
        <img src="../assets/worldmap.png" alt="map"/>
        <div class="pin usa">
            <span>United States</span>
        </div>
        <div class="pin france">
            <span>France</span>
        </div>
        <div class="pin sweden">
            <span>Sweden</span>
        </div>
        <div class="pin south-africa">
            <span>South Africa</span>
        </div>
        <div class="pin china">
            <span>China</span>
        </div>
    </div>
</template>

<style scoped>

.world-map {
    width: 70%;
    max-width: 1100px;
    margin-left: 300px;
    padding: 1em;
}

.world-map img {
    width: 100%;
    height: 100%;
}

.pin {
    background: #4362f8;
    position: absolute;
    width: 0.7em;
    height: 0.7em;
    border-radius: 50%;
}

.pin::before {
    content: '';
    background: #4362f8;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 100%;
    height: 100%;
    border-radius: 50%;
    animation: pulse 1.3s ease-in-out infinite; 
}

.pin span {
    display: inline-block; 
    white-space: nowrap; 
    position: absolute;
    left: 1.5em;
    top: 50%;
    transform: translateY(-50%);
    background: #fff;
    border-radius: 3em;
    padding: 0.3em 0.6em;
    font-size: 0.9em
}
.usa {
    top: 50%;
    left: 21%;
}

.france {
    top: 45%;
    left: 48%;
}

.sweden{
    top: 33%;
    left: 52%;
}
.south-africa {
    top: 78%;
    left: 53%
}

.china {
    top: 52%;
    left: 74%
}

@keyframes pulse {
    100% {
        opacity: 0;
        transform: 
            translate(-50%, -50%)
            scale(2.5);
    }
}

@media screen and (max-width: 600px) {
    .world-map {
        font-size: 13px
    }
}

</style> -->

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
<template>
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
  