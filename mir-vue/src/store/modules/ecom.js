/* eslint-disable */

import axios from 'axios';


const state = {
    products: [],
    cart: []
};

const getters = {
  getProducts: state => state.products,

};

const actions = {


  async fetchProducts({commit}){
    axios.get('http://localhost:8085/products').then((response) => {
      commit('setProducts', response.data)
    }, (error) => {
      console.log(error);
    });
  },

  async addDeleteItem({commit}, product){
    console.log("The product looks like with quantity" + product.quantity)
    commit('addDeleteItem', product)
  } 


};

const mutations = {
    
    setProducts: (state, products) => (state.products = products),
    addDeleteItem (state, product ) {
        console.log("what the fuc" + product.id)

        if(state.cart.has(product.id)){
             state.cart.set(state.cart.get(product.id) + product.quantity)
        }else {
           state.cart.set(product.id, product.quantity)
        }
        // if(state.cart.get(id) == 0){
        //     state.cart.delete(id)
        // }
      },
};

export default {
  state,
  getters,
  actions,
  mutations
};
