import Vuex from 'vuex';
import Vue from 'vue';
import auth from './modules/auth'
import upload from './modules/upload'
import user_recordings from './modules/user_recordings'

// Load Vuex
Vue.use(Vuex);

// Create store
export default new Vuex.Store({
  modules: {
    auth,
    upload,
    user_recordings
  }
});
