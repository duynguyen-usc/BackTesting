from datetime import datetime

class PriceData:
	def __init__(self, csvLine):
		self.parseCsvLine(csvLine)
		self.netChange = 0
		self.netPercentChange = 0
		self.movAvg = []
		self.upperBand = 0
		self.lowerBand = 0

	def parseCsvLine(self, csvLine):
		csvData = csvLine.split(',')
		self.date = datetime.strptime(csvData[0], "%Y-%m-%d")
		self.open = float(csvData[1])
		self.high = float(csvData[2])
		self.low = float(csvData[3])
		self.close = float(csvData[4])
		self.adjClose = float(csvData[5])
		self.volume = float(csvData[6])