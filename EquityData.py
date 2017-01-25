import os
import numpy
from PriceData import PriceData

class EquityData:
	PRINT_SPACING = '   '
	NUMBER_FORMAT = '.2f'
	MOV_AVG = [20, 200]

	def __init__(self, csvFile):
		self.allData = []
		self.parseCsvFile(csvFile)
		self.count = len(self.allData) - 1

	def parseCsvFile(self, csvFile):
		data = [line.rstrip('\n') for line in open(csvFile)]
		for idx, csvline in enumerate(data):
			if(idx != 0):		
				self.allData.append((PriceData(csvline)))

	def calcNetChange(self):
		for idx, priceData in (enumerate(self.allData)):
			if(idx < self.count):
				yesterdaysClose = self.allData[idx + 1].close
				priceData.netChange = priceData.close - yesterdaysClose
				priceData.netPercentChange = (priceData.netChange / yesterdaysClose) * 100

	def calcMovAvg(self, numberOfDays, indexStart):
		indexEnd = indexStart + numberOfDays
		if(indexEnd < self.count):
			return sum(self.allData[i].close for i in range(indexStart, indexEnd)) / numberOfDays
		return 0

	def calcStdDev(self, numberOfDays, indexStart):
		indexEnd = indexStart + numberOfDays
		if(indexEnd < self.count):
			return numpy.std([self.allData[i].close for i in range(indexStart, indexEnd)])
		return 0

	def calcAllMovAvgs(self):
		for idx, priceData in (enumerate(self.allData)):
			for period in self.MOV_AVG:				
				priceData.movAvg.append(self.calcMovAvg(period, idx))
				if (period == 20):
					stddev = self.calcStdDev(period, idx)
					priceData.upperBand = 2 * stddev
					priceData.lowerBand = -2 * stddev

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


# Main
path = os.path.dirname(os.path.realpath(__file__))
os.chdir(path)
testData = EquityData('Data/SPX.csv')
# print(testData.calcMovAvg(20, 0))
# print(testData.calcStdDev(20, 0))
testData.calcAllMovAvgs()
testData.movAvgTable()