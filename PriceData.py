from datetime import datetime

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