from PriceData import PriceData

class EquityData:

	ROUND_PERCISION = 2
	MOV_AVG = [20,50, 100, 200, 300]

	def __init__(self, csvFile):
		self.allData = []
		self.parseCsvFile(csvFile)
		self.runInterDayCalculations()

	def parseCsvFile(self, csvFile):
		data = [line.rstrip('\n') for line in open(csvFile)]
		for idx, csvline in enumerate(data):
			if(idx != 0):		
				self.allData.append((PriceData(csvline)))

	def runInterDayCalculations(self):
		for idx, priceData in reversed(list(enumerate(self.allData))):
			if(idx < len(self.allData) - 1):
				priceData.netChange = priceData.close - self.allData[idx + 1].close

			for period in self.MOV_AVG:
				if(idx > period):
					periodStart = idx - period
					priceData.movAvg.append(sum(self.allData[i].close for i in range(periodStart, idx)) / period)
				else:
					priceData.movAvg.append(0)

	def displayData(self):
		for day in self.allData:
			print("{0} {1} {2} {3}".format(str(day.date.strftime('%m/%d/%Y')), 
								  	       str(round(day.close, self.ROUND_PERCISION)),
									       str(round(day.netChange, self.ROUND_PERCISION)), 
									       str(round(day.movAvg[len(day.movAvg)-1], self.ROUND_PERCISION))))