from PriceData import PriceData

class EquityData:
	PRINT_SPACING = '   '
	NUMBER_FORMAT = '.2f'
	MOV_AVG = [20, 50, 100, 200, 300]

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

	def percentChangeTable(self):
		for day in self.allData:
			print("{1}:{0}{2}{0}{3}".format(self.PRINT_SPACING,
											str(day.date.strftime('%m/%d/%y')),
								  	        str(format(day.close, self.NUMBER_FORMAT)),
									        str(format(day.netPercentChange, self.NUMBER_FORMAT)) + '%'))

	def movAvgTable(self):
		for day in self.allData:
			movAverages = ''
			for idx, period in enumerate(self.MOV_AVG):
				movAverages += str(format(day.movAvg[idx], self.NUMBER_FORMAT)) + self.PRINT_SPACING
			
			print("{1}:{0}{2}{0}{3}".format(self.PRINT_SPACING,
				                      str(day.date.strftime('%m/%d/%y')), 
								  	  str(format(day.close, self.NUMBER_FORMAT)),
									  movAverages))
