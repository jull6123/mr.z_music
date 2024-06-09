import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useCounterStore = defineStore('counter', () => {
  const count = ref(0)
  const doubleCount = computed(() => count.value * 2)
  function increment() {
    count.value++
  }

  return { count, doubleCount, increment }
})

import Vue from 'vue'  
import Vuex from 'vuex'  
  
Vue.use(Vuex)  
  
export default new Vuex.Store({
  state: {  
    count: 0,
    commentHot: [],
    commentNew: [],
  },  
  mutations: {  
    increment (state) {  
      state.count++  
    },
    updateCommentHot(state, newDataHot, newDataNew) {
      state.commentHot = newDataHot;
      state.commentNew = newDataNew;
    }
  }  
})

