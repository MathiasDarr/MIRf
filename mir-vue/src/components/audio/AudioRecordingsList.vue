<template>
 <div>
   <v-card  tile flat>
    <v-card-text>
      <v-card-title>
        Audio Recordings
      </v-card-title>
    </v-card-text>



    <v-card flat>
            <v-list two-line>
            <v-list-item-group >
                <template v-for="(item) in getUserUploads">
                  <v-list-item :key="item.filename">
                
                    
                        <div>
                            <h4 class = "white00text mb-0 text-left" > {{item.filename}} </h4>
                            <div> 
                              <!-- <v-btn text small  > Read More </v-btn> -->
                              <v-btn text small v-on:click="selectReport(item.filename)"> Delete </v-btn>
                            </div>
                        </div>

                
                  </v-list-item>
                  <!-- <v-divider
                    v-if="index + 1 < items.length"
                    :key="index">
                  </v-divider> -->
                
                </template>
              </v-list-item-group>
            </v-list>  
    </v-card>

  </v-card>
 </div>   
</template>

<script>

import { mapGetters, mapActions } from "vuex";
// import router from '../../router'


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