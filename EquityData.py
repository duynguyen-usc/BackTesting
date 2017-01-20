from PriceData import PriceData

class EquityData:

	ROUND_PERCISION = 2
	MOV_AVG = [20,30]

	def __init__(self, csvFile):
		self.allData = []
		self.parseCsvFile(csvFile)
		self.calcMovAvg()

	def parseCsvFile(self, csvFile):
		data = [line.rstrip('\n') for line in open(csvFile)]
		for idx, csvline in enumerate(data):
			if(idx != 0):		
				self.allData.append((PriceData(csvline)))	

	def calcMovAvg(self):
		for idx, priceData in reversed(list(enumerate(self.allData))):
			if(idx > self.MOV_AVG[0]):
				periodStart = idx - self.MOV_AVG[0]
				priceData.movAvg1 = sum(self.allData[i].close for i in range(periodStart, idx)) / self.MOV_AVG[0]


	def displayData(self):
		for day in self.allData:
			print(str(day.date.strftime('%m/%d/%Y')) + ' ' + str(round(day.close, self.ROUND_PERCISION)) + ' ' + str(round(day.movAvg1, self.ROUND_PERCISION)))