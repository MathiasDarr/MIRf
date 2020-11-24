/* eslint-disable */

import axios from 'axios';


const state = {
  tweets: [],

};

const getters = {
  getUploadedFile: state => state.tweets,

};

const actions = {  
    async uploadFile({commit}, file_user_object){
      var fd = file_user_object.fd
      var user = file_user_object.user
      const api_url = 'http://localhost:5000/'+'upload/'+user
        axios.post(api_url, fd).then((response) => {
          console.log(response)
        }, (error) => {
        console.log(error);
      });
    } 
};

const mutations = {
    setUploadedFile: (state, tweets) => (state.tweets = tweets)
};

export default {
  state,
  getters,
  actions,
  mutations
};
