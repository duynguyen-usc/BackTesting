
class Option:
	SHORT = 0
	LONG = 1	
	VERTICAL_PUT = 2
	VERTICAL_CALL = 3

	PCT_DOWN = 0.07
	PCT_UP = 0.015

	def __init__(self, pos, opt, daydata):		
		self.d = daydata # PriceData
		self.longstrike = None
		self.shortstrike = None
		self.__setposition(pos)
		self.__setoptstructure(opt)
		self.__setStrikes()

	def __setposition(self, p):
		if(p not in (self.SHORT, self.LONG)):
			raise ValueError('position not valid')
		self.pos = p

	def __setoptstructure(self, o):
		if(o not in (self.VERTICAL_PUT, self.VERTICAL_CALL)):
			raise ValueError('optionstructure not valid')
		self.structure = o

	def __setspread(self):
		if (self.d.close >= 100): 
			spread = 20 
		else: 
			spread = 5
		if (self.longstrike == None):
			if (self.pos == self.SHORT):
				self.longstrike = self.shortstrike - spread
			else:
				self.longstrike = self.shortstrike + spread
		else:			
			if (self.pos == self.SHORT):
				self.shortstrike = self.longstrike + spread
			else:
				self.shortstrike = self.longstrike - spread

	def __roundStrike(self, x, base=5):		
		return int(base * round(float(x) / base))

	def __setStrikes(self):
		if(self.__isShortPutVertical()):
			x = self.d.close * (1 - self.PCT_DOWN)			
			self.shortstrike = self.__roundStrike(x)
		else:
			self.longstrike = self.__roundStrike(self.d.close * (1 + self.PCT_UP))
		
		self.__setspread()

	def __isShortPutVertical(self):
		return (self.pos == self.SHORT and self.structure == self.VERTICAL_PUT)

	def __isShortCallVertical(self):
		return (self.pos == self.SHORT and self.structure == self.VERTICAL_CALL)

	def __isLongPutVertical(self):
		return (self.pos == self.LONG and self.structure == self.VERTICAL_PUT)

	def __isLongCallVertical(self):
		return (self.pos == self.LONG and self.structure == self.VERTICAL_CALL)

	def __isWin(self, expclose):
		if (self.__isShortPutVertical()):
			return expclose > self.shortstrike

		elif (self.__isLongPutVertical()):
			return expclose < longstrike

		elif (self.__isShortCallVertical()):
			return expclose < shortstrike

		elif (self.__isLongCallVertical()):
			return expclose > longstrike

	def isMaxLoss(self, expclose):
		if(not self.isWin(expclose)):
			if (self.pos == self.SHORT):
				return expclose >= self.longstrike
			else:
				return expclose <= self.longstrike
		return False

	def toString(self):
		strOpt = "{0}/{1}".format(self.shortstrike, self.longstrike)		
		return strOpt