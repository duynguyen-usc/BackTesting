from datetime import datetime

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
		# '50day':50,
		'100day':100,
		'200day':200,
		'300day':300		
	}
	def __init__(self, csvLine):
		self.__parseCsvLine(csvLine)
		self.change = None
		self.percentChange = 0
		self.movavg = {}
		self.bollingerband = BollingerBand()

	def __parseCsvLine(self, csvLine):
		csvData = csvLine.split(',')
		self.date = datetime.strptime(csvData[0], "%Y-%m-%d")
		# self.open = float(csvData[1])
		# self.high = float(csvData[2])
		# self.low = float(csvData[3])
		self.close = float(csvData[4])
		# self.adjClose = float(csvData[5])
		# self.volume = float(csvData[6])

	def toString(self):
		fmt = '0.2f'
		cl = format(self.close, fmt)
		return "{0}\t{1}\t{2}".format(self.date, cl, self.bollingerband.toString())