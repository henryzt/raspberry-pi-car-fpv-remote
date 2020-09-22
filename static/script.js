const app = new Vue({
  el: '#app',
  delimiters: ['[[', ']]'],
  data: {},
  methods: {
    move(direction){
      fetch('/motor/' + direction)
    },
    handleMove(event){
      const action = event.target.dataset.action;
      if(!action) return;
      this.move(action)
    },
    stop(event){
      if(event.target.dataset.action != "buzz"){
        this.move("stop")
      }
    }
  }
})
console.log("OK")