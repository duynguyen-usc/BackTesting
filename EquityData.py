import numpy
from PriceData import PriceData

class EquityData:
	PRINT_SPACING = '   '
	NUMBER_FORMAT = '.2f'
	
	MOVAVG_10 = 0
	MOVAVG_20 = 1
	MOVAVG_50 = 2
	MOVAVG_150 = 3
	MOVAVG_200 = 4
	MOVAVG_250 = 5
	MOVAVG_300 = 5
	PERIODS = [10, 20, 50, 150, 200]

	MONTH = 20

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

	def displayTrendStats(self):		
		daysBelow = sum(1 if(day.movAvg[self.MOVAVG_200] != 0 and day.close < day.movAvg[self.MOVAVG_200]) else 0 for day in self.allData)
		daysAbove = len(self.allData) - daysBelow
		print("Days above {0} moving average = {1} ({2}%)".format(self.PERIODS[self.MOVAVG_200], daysAbove, self.__percent(daysAbove, len(self.allData))))
		print("Days below {0} moving average = {1} ({2}%)".format(self.PERIODS[self.MOVAVG_200], daysBelow, self.__percent(daysBelow, len(self.allData))))

	def displayStrategyResult(self, name, total, wins):
		losses = total - wins
		print("Strategy name: " + name)
		print("Total = {0}".format(total))
		print("Wins = {0} ({1}%)".format(wins, self.__percent(wins, total)))
		print("Losses = {0} ({1}%)\n".format(losses, self.__percent(losses, total)))

	def strategyMovAvg(self):
		t = 0
		w = 0
		for idx, day in enumerate(self.allData):
			if(idx - self.MONTH >= 0 and 
			   day.netPercentChange != None and 
			   day.netPercentChange < 0 and 
			   day.close > day.movAvg[self.MOVAVG_200]):
				t += 1
				if(self.allData[idx - self.MONTH].close > day.movAvg[self.MOVAVG_200]):
					w += 1
		self.displayStrategyResult('Moving average', t, w)

	def strategyPercentDown(self, percentDown):
		t = 0
		w = 0
		for idx, day in enumerate(self.allData):
			if(idx - self.MONTH >= 0 and 
			   day.netPercentChange != None and 
			   day.netPercentChange < 0):
				t += 1
				if(self.allData[idx - self.MONTH].close > day.close * (1 - percentDown)):
					w += 1
		self.displayStrategyResult(str(100 * percentDown) + " percent down strategy", t, w)