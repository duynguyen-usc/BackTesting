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
				yesterdaysClose = self.allData[idx + 1].close
				priceData.netChange = priceData.close - yesterdaysClose
				priceData.netPercentChange = (priceData.netChange / yesterdaysClose) * 100

			for period in self.MOV_AVG:
				if(idx > period):
					periodStart = idx - period
					priceData.movAvg.append(sum(self.allData[i].close for i in range(periodStart, idx)) / period)
				else:
					priceData.movAvg.append(0)

	def displayData(self):
		for day in self.allData:
			print("{0} {1} {2}".format(str(day.date.strftime('%m/%d/%y')), 
								  	   str(round(day.close, self.ROUND_PERCISION)),
									   str(round(day.netPercentChange, self.ROUND_PERCISION)) + '%'))