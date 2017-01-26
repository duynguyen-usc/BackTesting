import numpy
from PriceData import PriceData

class EquityData:
	PRINT_SPACING = '   '
	NUMBER_FORMAT = '.2f'
	
	TWENTY_DAY = 0
	ONE_HUNDRED_FIFTY_DAY = 1
	TWO_HUNDRED_DAY = 2
	TWO_HUNDRED_FIFTY_DAY = 3
	MOV_AVGS = [20, 150, 200, 250]	

	def __init__(self, csvFile):
		self.allData = []
		self.__parseCsvFile(csvFile)		
		self.count = len(self.allData) - 1
		self.__interDayCalculations()	

	def __parseCsvFile(self, csvFile):
		data = [line.rstrip('\n') for line in open(csvFile)]
		for idx, csvline in enumerate(data):
			if(idx != 0):		
				self.allData.append((PriceData(csvline)))

	def __interDayCalculations(self):
		for idx, priceData in enumerate(self.allData):
			self.__calcChange(idx)
			for n in self.MOV_AVGS:
				priceData.movAvg.append(self.__getAverage(idx, idx + n))
				if (n == 20):
					stddev = self.__calcStdDev(idx, idx + n)
					priceData.upperBand = 2 * stddev
					priceData.lowerBand = -2 * stddev

	def __calcChange(self, index):
		if(index < self.count):
			yesterdaysClose = self.allData[index + 1].close
			self.allData[index].netChange = self.allData[index].close - yesterdaysClose
			self.allData[index].netPercentChange = (self.allData[index].netChange / yesterdaysClose) * 100

	def __getMax(self, indexStart, indexEnd):		
		if(indexEnd < self.count):
			return numpy.max([self.allData[i].close for i in range(indexStart, indexEnd)])
		return 0

	def __getMin(self, indexStart, indexEnd):		
		if(indexEnd < self.count):
			return numpy.min([self.allData[i].close for i in range(indexStart, indexEnd)])
		return 0

	def __getAverage(self, indexStart, indexEnd):		
		if(indexEnd < self.count):
			return sum(self.allData[i].close for i in range(indexStart, indexEnd)) / (indexEnd - indexStart)
		return 0

	def __calcStdDev(self, indexStart, indexEnd):		
		if(indexEnd < self.count):
			return numpy.std([self.allData[i].close for i in range(indexStart, indexEnd)])
		return 0

	def __percent(self, x, total):
		return format(100 * x / total, self.NUMBER_FORMAT)

	def trendStats(self, period):		
		daysBelow200 = sum(1 if(day.close < day.movAvg[period]) else 0 for day in self.allData)
		daysAbove200 = len(self.allData) - daysBelow200
		print("Days above {0} moving average = {1} ({2}%)".format(self.MOV_AVGS[period], daysAbove200, self.__percent(daysAbove200, len(self.allData))))
		print("Days below {0} moving average = {1} ({2}%)".format(self.MOV_AVGS[period], daysBelow200, self.__percent(daysBelow200, len(self.allData))))