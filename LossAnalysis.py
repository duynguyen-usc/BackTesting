from Option import Option

class LossAnalysis:
	def __init__(self, option, hpdata):
		self.option = option
		self.hpdata = hpdata

	def __isInTheMoney(self, day):		
		if(self.option.structure == Option.SHORT_VERTICAL_PUT):
			return day.close < self.option.shortstrike
		return False

	def __daysInTheMoney(self):
		return sum([1 for d in self.hpdata if self.__isInTheMoney(d)])

	def toString(self, verbose=False):
		strLa = "{0}\titm:{1}".format(self.option.toString(), self.__daysInTheMoney())
		if (verbose):
			for day in self.hpdata:
				itm = 'x' if self.__isInTheMoney(day) else ''
				strLa += "{0}\t{1}\n".format(day.toString(), itm)
		return strLa