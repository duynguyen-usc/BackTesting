from datetime import datetime

class StrategyResult:
	def __init__(self, name):
		self.name = name
		self.total = 0
		self.wins = 0		

	def __percent(self, x, total):
		return format(100 * x / total, '0.2f')

	def addWin(self):
		self.wins += 1

	def addToTotal(self):
		self.total += 1

	def toString(self):
		losses = self.total - self.wins
		s = "Strategy name: {0}\nTotal = {1}\n".format(self.name, self.total)
		s += "Wins = {0} ({1}%)\n".format(self.wins, self.__percent(self.wins, self.total))
		s += "Losses = {0} ({1}%)\n".format(losses, self.__percent(losses, self.total))
		return s

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
		self.open = float(csvData[1])
		self.high = float(csvData[2])
		self.low = float(csvData[3])
		self.close = float(csvData[4])
		self.adjClose = float(csvData[5])
		self.volume = float(csvData[6])

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