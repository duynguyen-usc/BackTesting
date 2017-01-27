import numpy
from PriceData import PriceData
from PriceData import StrategyResult

class EquityData:
	PRINT_SPACING = '   '
	NUMBER_FORMAT = '.2f'
	
	MOVAVG_20 = 0
	MOVAVG_50 = 1
	MOVAVG_150 = 2
	MOVAVG_200 = 3
	MOVAVG_250 = 4
	PERIODS = [20, 50, 150, 200, 300]	

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
			for n in self.PERIODS:
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
		daysBelow = sum(1 if(day.movAvg[period] != 0 and day.close < day.movAvg[period]) else 0 for day in self.allData)
		daysAbove = len(self.allData) - daysBelow
		print("Days above {0} moving average = {1} ({2}%)".format(self.PERIODS[period], daysAbove, self.__percent(daysAbove, len(self.allData))))
		print("Days below {0} moving average = {1} ({2}%)".format(self.PERIODS[period], daysBelow, self.__percent(daysBelow, len(self.allData))))

	def strategyMovAvg(self):
		d = 'Sell puts @ 200 moving day averge one month out '
		d += 'if day net change is down at least 0.50 percent '
		d += 'and below the 20 day movAvg but above 50 movAvg'
		strategyResult = StrategyResult(d)
		expiration = 20 # one month ~ 20 trading days
		for idx, day in enumerate(self.allData):
			if(day.netPercentChange != None and 
			   day.netPercentChange < -0.50 and 
			   day.close < day.movAvg[self.MOVAVG_20] and 
			   day.close > day.movAvg[self.MOVAVG_50] and 
			   day.close > day.movAvg[self.MOVAVG_150]):
				strategyResult.total += 1
				if(self.allData[idx - expiration].close > day.movAvg[self.MOVAVG_250]):
					strategyResult.wins += 1

		strategyResult.display()