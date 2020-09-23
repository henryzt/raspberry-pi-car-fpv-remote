const app = new Vue({
  el: '#app',
  delimiters: ['[[', ']]'],
  data: {
    control: "joy",
    status: {
      motor: {
        lastSpeed: 0,
        lastDir: null
      },
      gimbal: {
        lastSpeed: 0,
        lastDir: null
      }
    }
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
        this.handleJoyMove('motor', data.direction.angle, data.distance)
    });
    car.on('end', () => {
        this.stop('motor')
    });

    gimbal.on('move', (evt, data) => {
      if(!data.direction) return;
      this.handleJoyMove('gimbal', data.direction.angle, data.distance)
    });
    gimbal.on('end', () => {
        this.stop('gimbal')
    });
  },
  methods: {
    move(type, direction, speed){
      const sp = speed ?? 30;
      const t = type ?? 'motor';
      fetch(`/${t}/${direction}/${sp}`);
    },
    handleJoyMove(joyName, dir, dist){
      const speed = Math.floor(dist / 10) * 10;
      if(dir != this.status[joyName].lastDir || 
          speed != this.status[joyName].lastSpeed){
        this.status[joyName].lastDir = dir;
        this.status[joyName].lastSpeed = speed;
        this.move(joyName, dir, speed)
      }
    },
    stop(type){
      this.move(type, "stop")
    },
    buzz(){
      this.move("motor", "buzz")
    },
    recenter(){
      this.move("gimbal", "recenter")
    }
  }
})
console.log("OK")