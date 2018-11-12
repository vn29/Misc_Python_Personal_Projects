#a state machine implementation for a calculator device simulation

class Machine():
    state = None
    lightstate = None
    brightness = 0

    def __init__(self):
        self.state = CalcOffClass()
        self.lightstate = LightOffClass()
    
    def calcOn(self):
        self.state.calcOn(self)
    
    def calcOff(self):
        self.state.calcOff(self)

    def setBrightness(self,brightness):
        if isinstance(self.state,CalcOffClass):
            print('calculator is off, cant turn on light')
        else: 
            self.brightness = brightness


    def lightOn(self):
        if  isinstance(self.state,CalcOffClass):
            print('calculator is off, cant turn on light')
        else:
            self.lightstate.lightOn(self)
    
    def lightOff(self):
        if  isinstance(self.state,CalcOffClass):
            print('calculator is off, cant turn on light')
        else:
            self.lightstate.lightOff(self)


class CalcOnClass():
    def calcOn(self,machine):
        print("Calculator is already on")
    def calcOff(self,machine):
        machine.brightness = 0
        machine.state = CalcOffClass()
        print("Calculator switching to off mode")


class CalcOffClass():
    def calcOn(self,machine):
        machine.state = CalcOnClass()
        machine.brightness = 10
        machine.lightstate = LightOnClass()
        print("Calculator switching to On")
    def calcOff(self,machine):
        print("Calculator is already off")

class LightOnClass():
    def lightOn(self,machine):
        print("light is already on")
    def lightOff(self,machine):
        machine.brightness=0
        machine.lightstate = LightOffClass()
        print("turning off light")


class LightOffClass():
    def lightOn(self,machine):
        machine.brightness=10
        machine.lightstate = LightOnClass()
        print("turning light on")
    def lightOff(self,machine):
        print("light is already off")








if __name__=='__main__':

    #initialize state
    machine=Machine()

    machine.calcOn()
    print(machine.brightness)
    machine.lightOff()
    print(machine.brightness)
    machine.lightOn()
    machine.setBrightness(8)
    print(machine.brightness)
    machine.calcOff()
    print(machine.brightness)
    machine.setBrightness(8)




