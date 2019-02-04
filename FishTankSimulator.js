//fish tank simulator in javascript translating from python


class Fish {
     constructor() {
          this.species = this.rand_select(['Beta', 'Guppy', 'Neon tetra', 'suckermouth catfish', 'Cherry barb']);
          this.color = this.rand_select(['green', 'red', 'blue', 'yellow', 'orange', 'black', 'brown', 'grey']);
          this.size = this.rand_select([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);
          this.x = this.rand_select([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);
          this.y = this.rand_select([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);
          this.z = this.rand_select([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);
     }
     rand_select(array) {
          return array[Math.floor(Math.random() * array.length)];
     }
     new_loc() {
          this.x = Math.max(Math.min(this.x + this.rand_select([-2, -1, 0, 1, 2]), 10), 0);
          this.y = Math.max(Math.min(this.y + this.rand_select([-2, -1, 0, 1, 2]), 10), 0);
          this.z = Math.max(Math.min(this.z + this.rand_select([-2, -1, 0, 1, 2]), 10), 0);
     }
}


class Tank {
     constructor() {
          this.fish = {};
          for (var f of [...Array(10).keys()]) {
               this.fish[f] = new Fish();
          }
     }
     update_location() {
          for (var f of Object.values(this.fish)) {
               f.new_loc();
          }
     }
}

class Controller {
     constructor() {
          this.tank = new Tank();
     }
     begin_simulation() {
          var flag = false;
          while (flag === false) {
               this.fishsim();
               var userinput = prompt('enter q to end the simulation', '');
               if (userinput === 'q') {
                    flag = true;
                    console.log('exiting simulation');
               }
          }
     }
     fishsim() {
          this.tank.update_location();
          for (var f of Object.values(this.tank.fish)) {
               console.log(f);
          }
     }
}

c = new Controller();
c.begin_simulation();
