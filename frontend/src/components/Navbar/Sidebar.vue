/* global $vuetify */
<!-- App.vue -->

<!-- <template>
    <div style="margin-top:100px">
      <v-app-bar app color="#c5dad2" dark>
        <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
        &nbsp;
        <img src="../../assets/logo.png" style="height: 40px; opacity: 100%;" class="my-5">
        <v-toolbar-title class="font-weight-bold font-italic mx-0 text-h5">Analyst Avengers</v-toolbar-title>
        <v-spacer></v-spacer>
        <span class="mr-14">
            <v-btn text to="/dashboard">Dashboard</v-btn>
            |
            <v-btn text to="/viewall">View All</v-btn>
        </span>
        <button class="btn btn-none btn-sign-out mb-2 pr-4" @click="signOut">Sign out&nbsp;&nbsp;<v-icon>mdi-logout</v-icon></button>
      </v-app-bar>
    </div>
</template>
  
<script>
  import Auth from '../../utils/auth'
  export default {
    data() {
      return {
        drawer: false,
        mini: false,
        clipped: false, 
      };
    },
    methods: {
      signOut() {
        try {
          Auth.signout()
          this.$router.push('/login')
        } catch (error) {
          console.error(error.message)
        }
      },
    },
  };
</script>
   -->
   <template>
    <nav>
        <!-- left side of app bar -->
        <v-app-bar flat app class="px-2">
    
            <!-- hamburger bar/navigation drawer for small screens -->
            <v-app-bar-nav-icon class="brown--text hidden-md-and-up" @click="hamburger=!hamburger"></v-app-bar-nav-icon>
    
    
            <!-- logo -->
            <v-btn plain color="brown" to="/">
            <v-img :src="require('../assets/Dog1Invert.png')" class="mr-2" max-height="40" max-width="40" contain/>
            <v-app-bar-title class="text-no-wrap">
                <div>
                    <span class="font-weight-regular">findpet</span>
                    <span class="font-weight-bold">now</span>
                </div>
            </v-app-bar-title>
            </v-btn>
    
        <v-spacer></v-spacer>
    
        <!-- right side of app bar -->
    
        <div class="hidden-sm-and-down">
            <span v-for="(link,i) in links" :key="i">
                <v-btn v-if="i<4" plain depressed color="primary" :to="link.route" 
                class="font-weight-bold hidden-sm-only">
                <v-icon small left>{{link.icon}}</v-icon>
                <span plain color="primary" class="text-body-2 font-weight-bold">{{ link.text }}</span>
            </v-btn>
            </span>
    
            <!-- Profile Drop down-->
            <v-menu bottom :offset-y=true>
                <template v-slot:activator="{ on, attrs }">
                    <v-btn fab small elevation="1" class="brown lighten-4 hidden-sm-only ml-3" v-bind="attrs" v-on="on">
                        <v-icon >mdi-account</v-icon>
                    </v-btn>
                </template>
    
            <!-- dropdown items. LINKS TO BE ADDED -->
                <v-list class="">
                    <span v-for="(link,i) in links" :key="i"> 
                    <v-list-item v-if="i>=4" :to="link.route">
                        <v-icon small left>{{link.icon}}</v-icon>
                        <v-list-item-title>{{ link.text }}</v-list-item-title>
                    </v-list-item>
                    </span>
                    <!-- logout -->
                    <v-list-item v-if="userLoggedIn" @click="onLogout">
                                <v-icon small left>mdi-logout</v-icon>
                            <v-list-item-content>
                                <v-list-item-title>Logout</v-list-item-title>
                            </v-list-item-content>
                        </v-list-item>
                </v-list>
            </v-menu> 
            </div>
            </v-app-bar>
    
            <!-- navigation drawer -->
            /* global $vuetify */
            <v-navigation-drawer v-if="!$vuetify.breakpoint.mdAndUp" v-model="hamburger" app temporary>
                    <v-list-item>
                        <v-list-item-content>
                            <v-list-item-title class="text-h6">
                                    Menu
                            </v-list-item-title>
                            <br><br>
                            <v-list-item-subtitle>
                                    Select a page to visit
                            </v-list-item-subtitle>
                        </v-list-item-content>
                    </v-list-item>
                 <v-divider></v-divider>
    
                    <v-list class="hidden-md-and-up">
                        <v-list-item v-for="link in links" :key="link.text" :to="link.route">
                            <v-list-item-action>
                                <v-icon>{{link.icon}}</v-icon>
                            </v-list-item-action>
                            <v-list-item-content>
                                <v-list-item-title>{{ link.text }}</v-list-item-title>
                            </v-list-item-content>
                        </v-list-item>
                        <!-- logout -->
                        <v-list-item v-if="userLoggedIn" @click="onLogout">
                            <v-list-item-action>
                                <v-icon>mdi-logout</v-icon>
                            </v-list-item-action>
                            <v-list-item-content>
                                <v-list-item-title>Logout</v-list-item-title>
                            </v-list-item-content>
                        </v-list-item>
                    </v-list>
                </v-navigation-drawer>
        </nav>
    </template>
    
    <script>
    export default {
        data(){
            return{
                showDropdown: false,
                hamburger: false,
            }
        },
        computed:{
            links(){
                let linkitems=[ {text: 'Home', route: '/', icon: 'mdi-home'},
                    {text:'Register', route:'/register', icon:'mdi-account-plus'},
                    {text:'Login', route:'/login', icon:'mdi-login'},
                    
                ]
                if(this.userLoggedIn){
                    linkitems=[
                    {text: 'Home', route: '/', icon: 'mdi-home'},
                    {text: 'Report Pet', route:'/ReportPet', icon: 'mdi-dog-side'},
                    {text: 'Search Pet', route:'/SearchAllPets', icon: 'mdi-magnify'},
                    {text: 'Learn More', route:'/Learn', icon: 'mdi-book-outline'},
                    {text: 'My Account', route:'/Account', icon: 'mdi-account'},
                    {text: 'Matched Pets', route:'/MatchedPets', icon: 'mdi-paw'},
                    {text: 'Inbox', route:'/Inbox', icon: 'mdi-inbox'},
                ]
            }
            return linkitems
            },
        userLoggedIn(){
            return this.$store.getters.getuser!=null && this.$store.getters.getuser!=undefined
        }
        },
        methods:{
            onLogout(){
                this.$store.dispatch('logout')
                this.$router.push('/login')
            }
        }
    }
    </script>