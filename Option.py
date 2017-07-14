from Result import Result


class Option:	
	SHORT_VERTICAL_PUT = 0
	LONG_VERTICAL_CALL = 1

	PCT_DOWN = 0.07
	PCT_UP = 0.015

	def __init__(self, optstruct, today, expday):		
		self.today = today # PriceData
		self.expday = expday # PriceData
		self.longstrike = None
		self.shortstrike = None
		self.result = Result()
		self.__setoptstructure(optstruct)
		self.__setStrikes()
		self.__setTradeResult()

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
			pctdown = self.today.close * (1 - self.PCT_DOWN)
			movavg = self.today.movavg['200day']
			self.shortstrike = self.__roundStrike(movavg)
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
			
	def toString(self):
		ml = 'ML' if (self.result.maxLoss == 1) else ''
		w = 'W' if (self.result.win == 1) else 'L'
		strOpt = "{0}\t".format(self.today.date.strftime('%Y-%m-%d'))
		strOpt += "{0}\t".format(round(self.today.close, 2))
		strOpt += "{0}\t".format(round(self.today.movavg['200day']))
		strOpt += "-{0}/{1}\t".format(self.shortstrike, self.longstrike)
		strOpt += "{0}\t{1}\t".format(w, ml)
		return strOpt