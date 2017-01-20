from PriceData import PriceData

class EquityData:

	ROUND_PERCISION = 2

	def __init__(self, csvFile):
		self.allData = []
		self.parseCsvFile(csvFile)

	def parseCsvFile(self, csvFile):
		data = [line.rstrip('\n') for line in open(csvFile)]
		for idx, csvline in enumerate(data):
			if(idx != 0):		
				self.allData.append((PriceData(csvline)))	
				self.allData[idx - 1].movAvg20 = self.calcMovAvg(20)

	def calcMovAvg(self, period):
		# length = len(self.allData) - 1
		# if(int(period) < int(length)):
		# 	periodStart = len(self.allData) - period
		# 	return sum(self.allData[i].close for i in range(periodStart, length) / period
		return 0 

	def displayData(self):
		for day in self.allData:
			print(str(day.date.strftime('%m/%d/%Y')) + ' ' + str(round(day.close, self.ROUND_PERCISION)) + ' ' + str(round(day.movAvg20, self.ROUND_PERCISION)))