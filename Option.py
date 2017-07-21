import math
from Result import Result
from Tools import StringBuilder

class Option:	
	SHORT_VERTICAL_PUT = 0
	LONG_VERTICAL_PUT = 1	
	SHORT_VERTICAL_CALL = 2
	LONG_VERTICAL_CALL = 3

	PCT_MIN = 0.03

	def __init__(self, optstruct, hpdata):
		self.hpdata = hpdata
		self.today = self.hpdata[0]
		self.expday = self.hpdata[len(hpdata) - 1]		
		self.longstrike = None
		self.shortstrike = None
		self.result = Result()
		self.__setoptstructure(optstruct)
		self.__setStrikes()
		self.__setTradeResult()
		self.itm = self.__daysInTheMoney()

	def __setoptstructure(self, optstruct):
		if(optstruct not in (self.SHORT_VERTICAL_PUT, 
					 		 self.LONG_VERTICAL_CALL)):
			raise ValueError('optionstructure not valid')
		self.structure = optstruct

	def __getspread(self):
		return 20 if (self.today.close >= 100) else 5

	def __setLegs(self):
		if (self.__isBullPut()):
			self.longstrike = self.shortstrike - self.__getspread()		

	def __roundStrike(self, x, base=5):
		return int(base * math.floor(float(x) / base))

	def __setStrikes(self):
		if (self.__isBullPut()):			
			pct = self.today.close * (1 - self.PCT_MIN)
			ma = self.today.movavg['200day']
			self.shortstrike = self.__roundStrike(min([ma, pct]))
		self.__setLegs()		

	def __isBullPut(self):
		return self.structure == self.SHORT_VERTICAL_PUT

	def __setTradeResult(self):
		if (self.__isBullPut()):
			if (self.shortstrike < self.expday.close):
				self.result.win = 1
				self.result.maxGain = 1
			else:
				self.result.loss = 1
				if (self.longstrike > self.expday.close):
					self.result.maxLoss = 1					 

	def __isInTheMoney(self, d):		
		if(self.structure == self.SHORT_VERTICAL_PUT):
			return d.close < self.shortstrike
		return False

	def __daysInTheMoney(self):
		return sum([1 for d in self.hpdata if self.__isInTheMoney(d)])

	def __getLoss(self):
		ml = 'ML' if (self.result.maxLoss == 1) else ''
		w = 'W' if (self.result.win == 1) else 'L'
			
	def toString(self):	
		strOpt = StringBuilder()
		strOpt.add(self.today.date.strftime('%Y-%m-%d'))
		strOpt.add(round(self.today.close, 2))
		strOpt.add(round(self.today.movavg['200day']))
		strOpt.add("-{0}/{1}\t".format(self.shortstrike, self.longstrike))
		strOpt.add(self.expday.date.strftime('%Y-%m-%d'))		
		strOpt.add(round(self.expday.close))
		strOpt.add("itm:{0}\t".format(self.__daysInTheMoney()))
		return strOpt.toString()