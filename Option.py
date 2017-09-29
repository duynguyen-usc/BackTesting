import math
from Result import Result
from Tools import StringBuilder
from Tools import DateHelper
from Tools import Constants

class Option:	
	SHORT_VERTICAL_PUT = 0
	LONG_VERTICAL_PUT = 1	
	SHORT_VERTICAL_CALL = 2
	LONG_VERTICAL_CALL = 3

	def __init__(self, optstruct, hpdata, repair=False):
		self.hpdata = hpdata
		self.today = self.hpdata[0]
		self.expday = self.hpdata[len(hpdata) - 1]		
		self.longstrike = None
		self.shortstrike = None	
		self.isRepair = repair	
		self.result = Result()
		self.__setoptstructure(optstruct)
		self.__setStrikes()
		self.__setTradeResult()		

	def __setoptstructure(self, optstruct):
		if(optstruct not in (self.SHORT_VERTICAL_PUT, 
					 		 self.SHORT_VERTICAL_CALL)):
			raise ValueError('optionstructure not valid')
		self.structure = optstruct

	def __setSpread(self):
		return 20 if (self.today.close >= 100) else 5

	def __getSpread(self):
		return "-{0}/{1}\t".format(self.shortstrike, self.longstrike)

	def __setLegs(self):
		if (self.__isBullPut()):
			self.longstrike = self.shortstrike - self.__setSpread()

		if (self.__isBearCall()):
			self.longstrike = self.shortstrike + self.__setSpread()

	def __roundStrike(self, x, base=5):
		if(self.structure == self.SHORT_VERTICAL_PUT):
			return int(base * math.floor(float(x) / base))
		else:
			return int(base * math.ceil(float(x) / base))

	def __isBullPut(self):
		return self.structure == self.SHORT_VERTICAL_PUT

	def __isBearCall(self):
		return self.structure == self.SHORT_VERTICAL_CALL

	def __setStrikes(self):
		if (self.__isBullPut()):
			if(self.isRepair):
				self.shortstrike = self.__roundStrike(
					self.today.close * (1 - Constants.REPAIR_STRIKE_PCT_DOWN))
			else:
				pct = self.today.close * (1 - Constants.STRIKE_PCT_DOWN)				
				ma = self.today.movavg['200day']
				self.shortstrike = self.__roundStrike(min([ma, pct]))

		if (self.__isBearCall()):			
			self.shortstrike = self.__roundStrike(self.today.close + 
				(self.today.change * Constants.SHORT_MULTIPLIER))
		self.__setLegs()

	def __setTradeResult(self):
		self.itm = self.__daysInTheMoney()		
		if (self.__isBullPut()):
			if (self.itm > 1):
				self.result.loss = 1
				if (self.longstrike > self.expday.close):
					self.result.maxLoss = 1
				if (self.itm > 5):
					self.result.itm5 = 1

			if (self.shortstrike < self.expday.close):
				self.result.win = 1				
				self.result.maxGain = 1

		if (self.__isBearCall()):
			if (self.shortstrike < self.expday.close):				
				self.result.loss = 1
				if (self.longstrike < self.expday.close):
					self.result.maxLoss = 1
				if (self.itm > 5):
					self.result.itm5 = 1

			if (self.shortstrike > self.expday.close):
				self.result.win = 1				
				self.result.maxGain = 1

	def __isInTheMoney(self, d):		
		if(self.structure == self.SHORT_VERTICAL_PUT):
			return d.close < self.shortstrike
		if(self.structure == self.SHORT_VERTICAL_CALL):
			return d.close > self.shortstrike
		return False

	def __daysInTheMoney(self):
		return sum([1 for d in self.hpdata if self.__isInTheMoney(d)])

	def __isWin(self):
		if (self.result.win == 1):
			return 'W'
		else:
			return 'ML' if self.result.maxLoss == 1 else 'L'

	def getFirstTouchIdx(self):
		for idx, day in enumerate(self.hpdata):
			if (self.__isInTheMoney(day)):
				return idx
		return -1
			
	def toString(self):	
		strOpt = StringBuilder()		
		strOpt.addDate(self.today.date)
		strOpt.addtab(('%.2f' % self.today.close))
		strOpt.addtab('%.2f' % self.today.percentChange)
		strOpt.addtab(self.__getSpread())		
		strOpt.addtab(('%.2f' % self.expday.close))
		strOpt.addtab(DateHelper.getWeekday(self.expday.date))
		strOpt.addtab(self.__isWin())
		return strOpt.toString()