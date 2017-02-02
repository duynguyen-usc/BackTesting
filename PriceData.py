from datetime import datetime

class PriceData:
	def __init__(self, csvLine):
		self.__parseCsvLine(csvLine)
		self.change = None
		self.percentChange = None
		self.movAvg = []
		self.upperBand = None
		self.lowerBand = None
		self.bandWidth = None
		self.bandAverage = None

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