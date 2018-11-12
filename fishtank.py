import random
import time

#Random.choice
#Random.random
#time.sleep(5) waits for 5 seconds
rint = random.randint


class Fish():
    species = None
    color = None
    size = None
    
    def __init__(self):
        rint = random.randint
        self.species = random.choice(['Beta','Guppy','Neon tetra','suckermouth catfish','Cherry barb'])
        self.color = random.choice(['green','red','blue','yellow','orange','black','brown','grey'])
        self.size = rint(1,10)
        self.x = rint(1,10)
        self.y = rint(1,10)
        self.z = rint(1,10)
    
    def new_loc(self):
        self.x = max(min(self.x + rint(-2,2), 10),0)
        self.y = max(min(self.y + rint(-2,2), 10),0)
        self.z = max(min(self.z + rint(-2,2), 10),0)
        


class Tank():
    fish = {}
    def __init__(self):
        for f in range(rint(1,10)):
            self.fish[f] = Fish()
    
    def update_location(self):
        for f in self.fish.values():
            f.new_loc()


class Controller():
    def __init__(self):
        self.tank = Tank()

    def beginSimulation(self):
        flag = False
        while flag==False:
            self.fishsim()
            userinput = input()
            if userinput == 'q':
                flag = True
                print('exiting simulation')
            
    

    def fishsim(self):
        time.sleep(4)
        self.tank.update_location()
        for f in self.tank.fish.values():
            print(vars(f))


if __name__ == "__main__":
    c = Controller()
    c.beginSimulation()