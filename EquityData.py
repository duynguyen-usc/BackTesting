from PriceData import PriceData

class EquityData:
	PRINT_SPACING = '   '
	NUMBER_FORMAT = '.2f'
	MOV_AVG = [20, 50, 100, 200, 300]

	def __init__(self, csvFile):
		self.allData = []
		self.parseCsvFile(csvFile)

	def parseCsvFile(self, csvFile):
		data = [line.rstrip('\n') for line in open(csvFile)]
		for idx, csvline in enumerate(data):
			if(idx != 0):		
				self.allData.append((PriceData(csvline)))

	def calcNetChange(self):
		indexCount = len(self.allData) - 1
		for idx, priceData in (enumerate(self.allData)):
			if(idx < indexCount):
				yesterdaysClose = self.allData[idx + 1].close
				priceData.netChange = priceData.close - yesterdaysClose
				priceData.netPercentChange = (priceData.netChange / yesterdaysClose) * 100

	def calcAllMovAvgs(self):
		indexCount = len(self.allData) - 1
		for idx, priceData in (enumerate(self.allData)):
			for period in self.MOV_AVG:
				idxOfFirstDay = idx + period
				if(idxOfFirstDay < indexCount):
					priceData.movAvg.append(sum(self.allData[i].close for i in range(idx, idxOfFirstDay)) / period)
				else:
					priceData.movAvg.append(0)

	def displayPercentChange(self):
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
