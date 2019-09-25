import numpy as np

class CUtil():
  recorderList = []
  
  def recorderAdd(self,a):
    self.recorderList.append(a)
  
  def sad(self):
    print ("I feel sad")
    
  def happy(self):
    print ("I feel happy")
    
  def ready(self):
    print ("I am ready")
  
  def car(self):
    print ("the car is shiney")
    
  def song(self,types):
    print("play the song" + types)
  
  def focused(self):
    print("I am focused")
    
  def goForRun(self,timeOfRun):
    print("I went for a "+timeOfRun+" minute run")
    
  def talkWithFriend(self,friendsname):
    print("I talked with my friend "+friendsname+"!")
    
    
  def cleanRoom(self):
    print("my room is clean")
    
  def workOut(self):
    print("I went for a workout")

    
  def CallParents(self):
    print("I called mom and dad!")
  
  def CallBrother(self):
    print("I called my brother!")
    
  def EnjoyTimeWithGF(self,location):
    print("spending time with my GF at "+location)
    
  def wakeUp(self):
    print("time to wake up!")
    
  def goToWork(self):
    print("going to work now!")
    
  def brushMyTeeth(self):
    print("brushing my teeth")

  def getDressed(self):
    print("getting dressed for the day")
  
  def goForAHike(self, location):
    print("going for a hike at"+location)
    
    
    
  def Crush(self):
    print("I have a crush on someone at school")
    
  def MeetNewPerson(self):
    print("meeting a new person!")
  
  
  def Day1(self):
    self.happy()
    self.ready()
    self.focused()
    self.goForRun("30")
    self.cleanRoom()
    self.CallParents()
    self.CallBrother()
    self.talkWithFriend("Graham")
    
    
  def Day2(self):
    self.CallParents()
    self.CallBrother()
    self.focused()
    self.focused()
    self.happy()
    
  def Day3(self):
    
    self.wakeUp()
    self.getDressed()
    self.cleanRoom()
    self.EnjoyTimeWithGF("zoo")
    self.happy()
    self.ready()
    
    
  def Day4(self):
    self.wakeUp()
    self.goToWork()
    self.MeetNewPerson()
    
  def Day5(self):
    self.wakeUp()
    self.goForAHike(" big basin")
    
    
  def Week(self):
    Lweek = [self.Day3,
      self.Day2,
      self.Day5,
      self.Day4,
      self.Day1,
      self.Day5]
    for e in range(7):
      rnd = np.random.randint(0,6)
      print ("\n ~~~~~~~~~it's a new day!~~~~~~~~~~ \n")
      Lweek[rnd]()
      
    
  def Month(self):
    self.Week()
    self.Week()
    self.Week()
    self.Week()
    

LifeSim = CUtil() 
LifeSim.Month()
