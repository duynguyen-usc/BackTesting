from datetime import datetime

class StrategyResult:
	def __init__(self, name):
		self.__name = name
		self.__total = 0
		self.__wins = 0
		self.__tradeDays = []

	def __percent(self, x, total):
		return format(100 * x / total, '0.2f')

	def addWin(self):
		self.__wins += 1

	def addTradeDay(self, singleDayPriceData):
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
			srString += day.toString() + '\n'
		return srString

class BollingerBand:
	def __init__(self, movAvgMidline, stddeviation):
		self.midLine = movAvgMidline
		self.upperBand = 2 * stddeviation + self.midLine
		self.lowerBand = -2 * stddeviation + self.midLine
		self.bandWidth = self.upperBand - self.lowerBand		

class PriceData:
	def __init__(self, csvLine):
		self.__parseCsvLine(csvLine)
		self.change = None
		self.percentChange = None
		self.movAvg = []
		self.bollingerBand = BollingerBand(0,0)		

	def __parseCsvLine(self, csvLine):
		csvData = csvLine.split(',')
		self.date = datetime.strptime(csvData[0], "%Y-%m-%d")
		# self.open = float(csvData[1])
		# self.high = float(csvData[2])
		# self.low = float(csvData[3])
		self.close = float(csvData[4])
		# self.adjClose = float(csvData[5])
		# self.volume = float(csvData[6])

	def percentChangeIsAbove(self, x):
		return (True if(self.percentChange != None and self.percentChange > x) else False)

	def percentChangeIsBelow(self, x):
		return (True if(self.percentChange != None and self.percentChange < x) else False)

	def closeIsAbove(self, x):
		return self.close > x

	def closeIsBelow(self, x):
		return self.close < x

	def closeAboveOpen(self):
		return self.close > self.open

	def toString(self):
		return "{0}\t{1}\t{2}%".format(format(self.date, "%Y-%m-%d"), format(self.close, '0.2f'), format(self.percentChange, '0.2f'))