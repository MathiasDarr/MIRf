/* eslint-disable */

import axios from 'axios';


const state = {
  user_uploads: [],

};

const getters = {
  getUserUploads: state => state.user_uploads,

};

const actions = {  
    async fetchUserUploads({commit}, user){
        console.log('I GET CALLED')
        var url = 'http://localhost:5000/recordings/' + user  

        axios.get(url).then((response) => {
            var response_string = JSON.stringify(response.data.body)
            console.log(response.data)
            // var data = JSON.parse(response_string)
            commit('setUserUploads', response.data)
        
          }, (error) => {
            console.log(error);
          });
    }
};

const mutations = {
    setUserUploads: (state, uploads) => (state.user_uploads = uploads)
};

export default {
  state,
  getters,
  actions,
  mutations
};
