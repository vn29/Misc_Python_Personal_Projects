
class Rebar():
	area=diameter=size=None
	minspacing = None

	def __init__(self,size):
		self.size = size
		self.diameter = self.Dia(size)
		self.area = self.Area(size)
		self.minspacing = max(self.diameter,1.*inch)

	def Dia(self,size):
		return size/8.*inch

	def Area(self,Dia):
		bars = {3.:.11*inch*inch,
				4.:.2*inch*inch,
				5.:.31*inch*inch,
				6.:.44*inch*inch,
				7.:.6*inch*inch,
				8.:.79*inch*inch,
				9.:1.0*inch*inch,
				10.:1.27*inch*inch,
				11.:1.56*inch*inch}

		return bars[Dia]


class Stirrups():
	spacing=None
	rebar=None
	total=None

	def __init__(self,numlegs,size,spacing):
		self.rebar = Rebar(size)
		self.spacing = spacing
		self.total = numlegs


class As():
	layers=None
	rebar=None
	total=None
	rcbeam=None
	rho = None

	def __init__(self,total,size,layers,rcbeam):
		self.rebar = Rebar(size)
		self.total = total
		self.layers = layers
		self.cover = rcbeam.cover
		self.rcbeam = rcbeam
		self.func_rho()

	def checkspacing(self):
		dia = self.rebar.diameter
		tot = self.total
		cover = self.cover
		stdia = self.rcbeam.As_v.rebar.diameter
		b = self.rcbeam.b
		spacing = (b-2.*(cover+stdia)-tot*dia)/(tot-1)
		if self.rebar.minspacing >spacing:
			print('minspacing criteria not met')
		else:
			return spacing

	def func_rho(self):
		self.rho = (self.rebar.area*self.total)/(self.rcbeam.b*self.rcbeam.h)

	def getLayerLocation(self,layerNum):
		if layerNum > self.layers: print('You have attempted to select a layer that does not exist')
		else:
			cc = self.cover
			stdia = self.rcbeam.As_v.rebar.diameter
			dia = self.rebar.diameter
			return cc+stdia+0.5*dia+(dia+self.rebar.minspacing)*(layerNum-1.)

	def compute_d(self):
		return sum([self.getLayerLocation(l+1.) for l in range(int(self.layers))])/(self.layers)



class RCBeam():
	b=None
	h=None
	As_top=None
	As_bot=None
	As_v=None
	cover=None
	length=None

	def __init__(self,b,h,length,cover):
		self.b = b
		self.h = h
		self.length = length
		self.assignCover(cover)
		self.As_v = Stirrups(2.,3.,4.*inch)

	def assignCover(self,cover):
		self.cover = cover

	def assignTopAs(self,total,size,layers):
		self.As_top = As(total,size,layers,self)
		self.As_top.checkspacing()

	def assignBotAs(self,total,size,layers):
		self.As_bot = As(total,size,layers,self)
		self.As_bot.checkspacing()

	def assignStirrups(self,numlegs,size,spacing):
		self.As_v = Stirrups(numlegs,size,spacing)

	def getLayerLocationTop(self,layerNum):
		return self.As_top.getLayerLocation(layerNum)

	def getLayerLocationBot(self,layerNum):
		return (self.h-self.As_bot.getLayerLocation(layerNum))

	def get_d_top(self):
		return self.As_top.compute_d()

	def get_d_bot(self):
		return self.h-self.As_bot.compute_d()

	def get_rho_top(self):
		return rcbeam.As_top.rho

	def get_rho_bot(self):
		return rcbeam.As_bot.rho

	def get_weight_per_length(self):
		'''returns the weight per unit length of the RCBeam'''
		b = self.b 
		h = self.h 
		gamma = 150.*lb/(ft**3)
		return gamma*(b*h)

	def get_Asv_per_length(self):
		tot = self.As_v.total
		area = self.As_v.rebar.area
		spacing = self.As_v.spacing
		return (tot*area)/spacing

	def computeSSMaxMomentSelfWeight(self):
		w = self.get_weight_per_length()
		return (w*(self.length)**2.)/8.



if __name__ == '__main__':
	import math
	inch = 1.
	ft = 12.*inch
	lb = 1.
	kip = 1000.*lb
	psi = lb/(inch**2)
	ksi = kip/(inch**2)

	#instantiate a beam with dimensions, length, and cover
	rcbeam = RCBeam(b=24.*inch,h=36.*inch,length=20.*ft,cover=1.5*inch)
	#assign top and bottom rebar number, size, and number of layers
	rcbeam.assignTopAs(total=4.,size=9.*inch,layers=1.)
	rcbeam.assignBotAs(total=4.,size=9.*inch,layers=1.)
	#assign size and spacing of stirrups
	rcbeam.assignStirrups(numlegs=2.,size=3.*inch,spacing=4.*inch)


	print(rcbeam.getLayerLocationBot(layerNum=1.))
	print(rcbeam.get_rho_top())
	print(rcbeam.get_d_bot())
	print(rcbeam.get_d_top())
	print(rcbeam.get_Asv_per_length())
	print(rcbeam.get_weight_per_length()*1/(kip/ft))
	print(rcbeam.computeSSMaxMomentSelfWeight()*1/(kip*ft))#returns kip-ft max moment along span of member due to self weight







