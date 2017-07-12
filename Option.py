
class Option:	
	SHORT_VERTICAL_PUT = 0
	LONG_VERTICAL_CALL = 1

	PCT_DOWN = 0.07
	PCT_UP = 0.015

	def __init__(self, optstruct, today):		
		self.today = today # PriceData
		self.longstrike = None
		self.shortstrike = None		
		self.__setoptstructure(optstruct)
		self.__setStrikes()

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
		return int(base * round(float(x) / base))

	def __setStrikes(self):
		if (self.__isBullPut()):						
			self.shortstrike = self.__roundStrike(self.today.close * (1 - self.PCT_DOWN))		
		self.__setLegs()		

	def __isBullPut(self):
		return self.structure == self.SHORT_VERTICAL_PUT

	def __isWin(self, expclose):
		if (self.__isBullPut()):
			return expclose > self.shortstrike
		return False		

	def __isMaxLoss(self, expclose):
		if(not self.isWin(expclose)):
			if (self.pos == self.SHORT):
				return expclose >= self.longstrike
			else:
				return expclose <= self.longstrike
		return False

	def toString(self):
		strOpt = "{0}/{1}".format(self.shortstrike, self.longstrike)		
		return strOpt