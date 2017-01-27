from datetime import datetime

class PriceData:
	def __init__(self, csvLine):
		self.parseCsvLine(csvLine)
		self.netChange = None
		self.netPercentChange = None
		self.movAvg = []
		self.upperBand = None
		self.lowerBand = None

	def parseCsvLine(self, csvLine):
		csvData = csvLine.split(',')
		self.date = datetime.strptime(csvData[0], "%Y-%m-%d")
		self.open = float(csvData[1])
		self.high = float(csvData[2])
		self.low = float(csvData[3])
		self.close = float(csvData[4])
		self.adjClose = float(csvData[5])
		self.volume = float(csvData[6])

class StrategyResult:
	def __init__(self, desc):
		self.total = 0
		self.wins = 0
		self.description = desc

	def losses(self):
		return self.total - self.wins

	def winPercent(self):
		return (self.wins / self.total) * 100

	def lossPercent(self):
		return 100 - self.winPercent()

	def display(self):
		print(self.description)
		print("Wins: {0} ({1}%)".format(self.wins, format(self.winPercent(), '0.2f')))
		print("Losses: {0} ({1}%)".format(self.losses(), format(self.lossPercent(), '0.2f')))


