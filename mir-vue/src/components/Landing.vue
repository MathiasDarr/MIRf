<template>
  <v-container>
    <v-layout row>
      <v-flex md2>

      </v-flex> 
      <v-flex md10>
        <div class="title font-weight-medium">
          <v-layout row>
            <v-flex md8>
              <v-card flat>
                {{ getEmail }} 
                <AudioRecordingsList />

              </v-card>
              


              <v-card  tile flat>
                <v-card-text>
                  <v-card-title>
                    Upload an audio file
                  </v-card-title>
                </v-card-text>
              </v-card>
              <UploadFile />
            </v-flex>
          </v-layout>
        
        </div>
      </v-flex>
    </v-layout> 
  </v-container>
</template>

<script>

import { mapGetters } from "vuex";
import UploadFile from './uploads/UploadFile'
import AudioRecordingsList from './audio/AudioRecordingsList'


// import axios from 'axios';
// import * as  AmazonCognitoIdentity from "amazon-cognito-identity-js";
// import { CognitoAuth } from 'amazon-cognito-auth-js'
export default {
  
  components:{
    UploadFile,
    AudioRecordingsList
  },

  methods:{
    getUserEmail(){
        var jwtDecode = require('jwt-decode');
        var decoded_token = jwtDecode(this.getIdToken)
        return decoded_token.email.split('@')[0]
    }
  },
  created(){

    var email = this.getEmail
    console.log('WELCOME ' + email)

// var name = "mddarr@gmail.com"
    // var split = name.split("@")
    // var prefix = split[0]
    // var host = split[1].split('.')[0]


    // console.log("Welcome " + prefix) // split[0] + " " + split[1])
    // console.log("Host " + host )

  },
  data(){
    return {

    }
  },
  computed: {
    ...mapGetters(["getUserUploads", "getEmail"]),

  },
}
</script>

<style>
code {
  font-family: Consolas,"courier new";
  color: crimson;
  background-color: #f1f1f1;
  padding: 2px;
  font-size: 105%;
}
</style>