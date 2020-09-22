const app = new Vue({
  el: '#app',
  delimiters: ['[[', ']]'],
  data: {
    control: "joy",
    lastSpeed: 0,
    lastDir: null
  },
  mounted(){
    const gimbal = nipplejs.create({
        zone: this.$refs.leftJoy,
        mode: 'semi',
        catchDistance: 150,
        color: '#0077ff',
        size: 120
    });
    const car = nipplejs.create({
        zone: this.$refs.rightJoy,
        mode: 'semi',
        catchDistance: 150,
        color: '#0077ff',
        size: 120
    });

    car.on('move', (evt, data) => {
        if(!data.direction) return;
        this.handleJoyMove(data.direction.angle, data.distance)
    });
    car.on('end', () => {
        this.stop()
    });
  },
  methods: {
    move(direction, speed){
      const sp = speed ?? 30;
      fetch(`/motor/${direction}/${sp}`)
    },
    handleMove(event){
      const action = event.target.dataset.action;
      if(!action) return;
      this.move(action)
    },
    handleJoyMove(dir, dist){
      const speed = Math.floor(dist / 10) * 10;
      if(dir != this.lastDir || speed != this.lastSpeed){
        this.lastDir = dir;
        this.lastSpeed = speed;
        this.move(dir, speed)
      }
    },
    stop(event){
      if(!event || event.target.dataset.action != "buzz"){
        this.move("stop")
      }
    }
  }
})
console.log("OK")