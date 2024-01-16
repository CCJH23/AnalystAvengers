<script setup>
    import TopNavbar from "@/components/Navbar/TopNavbar.vue";
    import Sidebar from "@/components/Navbar/Sidebar.vue";
</script>

<style>
table {
    border-collapse: collapse;
    width: 100%;
    max-width: 740px;
    margin: 0 auto;
    border-radius: 10px;
    overflow: hidden;
  }
  
  th, td {
    text-align: center;
    padding: 10px;
    background-color: #f2f6f5f0;
  }
  
  th {
    background-color: #f2f6f5f0;
    font-weight: bold;
  }

</style>
<template>
    <div>
        <!-- <TopNavbar/> -->
        <Sidebar/>
        <div class="container-flex p-3" style="margin-left:4.5rem;">
            <!-- Welcome back -->
            <div class="row px-3 pt-2 pb-4">
                <div class="col-md-7 col-sm-auto" data-aos="fade-down">
                    <h3 class="pt-3 ps-3">Welcome back,</h3>
                    <h5 class="pt-1 ps-3">track your tools today</h5>
                </div>
                
                
            </div>
            <hr>
            
            <!-- Your listings -->
            <div class="px-3 py-2" data-aos="fade-down">
                <h3 class="ps-3">Monitoring Dashboard</h3>
            </div>
            <!-- <div class="row pb-4" data-aos="fade-up" style="min-height:50vh">
                <template v-if="!noOffers" v-for="each in offers">
                    <ListingCard :offer="offer" :listingInfo="each"></ListingCard>
                </template>

                <div v-if="noOffers" class="text-center mt-3"><small>There are no listings to show.</small></div>
                
            </div> -->
        </div>
     
        <!-- <scroll-to-top></scroll-to-top> -->
        <!-- <Footer style="margin-left:4.5rem;"></Footer> -->

    </div>


</template>

<script>
    

</script>