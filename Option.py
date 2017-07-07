
class Option:
	SHORT = 0
	LONG = 1	
	VERTICAL_PUT = 2
	VERTICAL_CALL = 3

	SPREAD = 20

	def __init__(self, pos, opt):
		self.__setposition(pos)
		self.__setoptstructure(opt)		
		self.shortstrike = None
		self.longstrike = None

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
			if (self.pos == self.SHORT)
				self.shortstrike = self.longstrike + self.SPREAD
			else:
				self.shortstrike = self.longstrike - self.SPREAD

	def isWin(self, expclose):
		if (self.pos == self.SHORT and self.structure == self.VERTICAL_PUT):
			return expclose > self.shortstrike

		elif (self.pos == self.LONG and self.structure == self.VERTICAL_PUT):
			return expclose < longstrike

		elif (self.pos == self.SHORT and self.structure == self.VERTICAL_CALL):
			return expclose < shortstrike

		elif (self.pos == self.LONG and self.structure == self.VERTICAL_CALL):
			return expclose > longstrike

	def isMaxLoss(self, expclose):
		if(not self.isWin(expclose)):
			if (self.pos == self.SHORT):
				return expclose >= self.longstrike
			else:
				return expclose <= self.longstrike