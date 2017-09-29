from datetime import datetime
from Tools import StringBuilder
from Tools import DateHelper
from Tools import Constants

class BollingerBand:
	def __init__(self):
		self.midLine = 0
		self.upperBand = 0
		self.lowerBand = 0
		self.bandwidth = 0
		self.bandavg = 0

	def calculate(self, movAvgMidline, stddeviation):
		self.midLine = movAvgMidline
		self.upperBand = 2 * stddeviation + self.midLine
		self.lowerBand = -2 * stddeviation + self.midLine
		self.bandwidth = self.upperBand - self.lowerBand

	def toString(self):
		fmt = '0.2f'
		ub = format(self.upperBand, fmt)
		lb = format(self.lowerBand, fmt)
		ml = format(self.midLine, fmt)
		bw = format(self.bandwidth, fmt)		
		return "{0}\t{1}\t{2}\t{3}".format(ub, ml, lb, bw)		

	def getbandwidth(self):
		return self.bandwidth

class PriceData:
	periods = {
		'20day':20,
		'50day':50,
		'100day':100,
		'200day':200,
		'300day':300		
	}
	def __init__(self, csvLine):
		self.__parseCsvLine(csvLine)
		self.change = 0
		self.percentChange = 0
		self.movavg = {}
		self.bollingerband = BollingerBand()
		self.vix = 0

	def __parseCsvLine(self, csvLine):
		csvData = csvLine.split(',')
		self.date = datetime.strptime(csvData[0], "%Y-%m-%d")
		# self.open = float(csvData[1])
		# self.high = float(csvData[2])
		# self.low = float(csvData[3])
		self.close = self.__getValue(csvData[4])
		# self.adjClose = float(csvData[5])
		# self.volume = float(csvData[6])

	def __getValue(self, csvData):
		try:
			return float(csvData)
		except ValueError:
			return 0

	def isUp(self, pct=0):
		return self.percentChange > pct

	def isDown(self, pct=0):
		return self.percentChange < pct

	def toString(self):	
		pd = StringBuilder()
		pd.addtab(DateHelper.getWeekday(self.date))
		pd.addtab(self.date.strftime('%Y-%m-%d'))
		pd.addtab(round(self.close, 2))
		pd.addtab(round(self.percentChange, 2))
		return pd.toString()