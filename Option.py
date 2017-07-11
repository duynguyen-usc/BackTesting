
class Option:
	SHORT = 0
	LONG = 1	
	VERTICAL_PUT = 2
	VERTICAL_CALL = 3

	SPREAD = 20
	PCT_DOWN = 0.07
	PCT_UP = 0.015

	def __init__(self, pos, opt, daydata):		
		self.d = daydata # PriceData
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
		if (self.longstrike == None):
			if (self.pos == self.SHORT):
				self.longstrike = self.shortstrike - self.SPREAD
			else:
				self.longstrike = self.shortstrike + self.SPREAD
		else:
			if (self.pos == self.SHORT):
				self.shortstrike = self.longstrike + self.SPREAD
			else:
				self.shortstrike = self.longstrike - self.SPREAD

	def __setStrikes(self):
		if(self.__isShortPutVertical()):
			self.shortstrike = self.d.close * (1 - self.PCT_DOWN)		
		else:
			self.longstrike = self.d.close * (1 + self.PCT_UP)
		self.__setspread()

	def __isShortPutVertical(self):
		return (self.pos == self.SHORT and self.structure == self.VERTICAL_PUT)

	def __isShortCallVertical(self):
		return (self.pos == self.SHORT and self.structure == self.VERTICAL_CALL)

	def __isLongPutVertical(self):
		return (self.pos == self.LONG and self.structure == self.VERTICAL_PUT)

	def __isLongCallVertical(self):
		return (self.pos == self.LONG and self.structure == self.VERTICAL_CALL)

	def isWin(self, expclose):
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