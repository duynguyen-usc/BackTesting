from datetime import datetime
from BollingerBand import BollingerBand	

class PriceData:
	def __init__(self, csvLine):
		self.__parseCsvLine(csvLine)
		self.change = None
		self.percentChange = None
		self.closeMonthLater = None
		self.winLoss = None
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
		return self.percentChange != None and self.percentChange > x

	def percentChangeIsBelow(self, x):
		return self.percentChange != None and self.percentChange < x

	def closeIsAbove(self, x):
		return self.close != 0 and self.close > x

	def closeIsBelow(self, x):
		return self.close != 0 and self.close < x

	def oneMonthCloseIsAbove(self, x):
		return self.closeMonthLater != 0 and self.closeMonthLater > x

	def oneMonthCloseIsBelow(self, x):
		return self.closeMonthLater != 0 and self.closeMonthLater < x

	def toString(self):
		return "{0}\t{1}\t{2}%\t{3}".format(format(self.date, "%Y-%m-%d"), 
											format(self.close, '0.2f'), 
											format(self.percentChange, '0.2f'),
											format(self.closeMonthLater, '0.2f'))