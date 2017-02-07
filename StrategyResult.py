from datetime import datetime

class StrategyResult:
	def __init__(self, name):
		self.__name = name
		self.__total = 0
		self.__wins = 0
		self.__tradeDays = []

	def __percent(self, x, total):
		return format(100 * x / total, '0.2f')

	def addTradeDay(self, singleDayPriceData, strikePrice):		
		if (singleDayPriceData.oneMonthCloseIsAbove(strikePrice)): 
			self.__wins += 1
			singleDayPriceData.winLoss = 'W'
		else:
			singleDayPriceData.winLoss = 'L'
		self.__tradeDays.append(singleDayPriceData)

	def displayResults(self):
		total = len(self.__tradeDays)
		losses = total - self.__wins
		s = "Strategy name: {0}\nTotal = {1}\n".format(self.__name, total)
		s += "Wins = {0} ({1}%)\n".format(self.__wins, self.__percent(self.__wins, total))
		s += "Losses = {0} ({1}%)\n".format(losses, self.__percent(losses, total))
		return s

	def toString(self):
		srString = ""
		for day in self.__tradeDays:
			srString += "{0}\t{1}\n".format(day.toString(), day.winLoss)
		return srString