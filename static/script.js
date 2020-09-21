const app = new Vue({
  el: '#app',
  delimiters: ['[[', ']]'],
  data: {},
  methods: {
    move(direction){
      fetch('/motor/' + direction)
    }
  }
})
console.log("OK")