<template>
 <div>
   <v-card  tile flat>
    <v-card-text>
      <v-card-title>
        Audio Recordings
      </v-card-title>
    </v-card-text>
    {{ getUserUploads }}


    <v-card flat>
            <v-list two-line>
            <v-list-item-group >
                <template v-for="(item, index) in getUserUploads">
                  <v-list-item :key="item.filename">
                
                    <template>
                        {{ index }}
                      <!-- <v-list-item-content @click="selectUserUpload(item.filename)">
                        <v-list-item-title v-text="item.title"></v-list-item-title>
                        <v-list-item-subtitle class="text--primary">Guitar </v-list-item-subtitle>
                      </v-list-item-content> -->
                    </template>
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