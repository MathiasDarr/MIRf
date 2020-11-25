<template>
 <div>
   <v-card  tile flat>
    <v-card-text>
      <v-card-title>
        Audio Recordings
      </v-card-title>
    </v-card-text>
    {{ getUserUploads }}
  </v-card>
 </div>   
</template>

<script>

import { mapGetters, mapActions } from "vuex";

export default {
    created(){
        this.fetchUserUploads(this.getEmail)
    },
    props: {

    },
    data(){
        return{
    
        }
    },
    methods:{
        ...mapActions(["fetchUserUploads"]),
        
    },
    computed:{
        ...mapGetters(["getUserUploads", "getEmail"]),
    }

}
</script>