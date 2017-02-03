import os
import numpy
from PriceData import PriceData
from PriceData import BollingerBand
from PriceData import StrategyResult

class EquityData:
	MOVAVG_10 = 0
	MOVAVG_20 = 1
	MOVAVG_50 = 2
	MOVAVG_150 = 3
	MOVAVG_200 = 4	
	PERIODS = [10, 20, 50, 150, 200]

	MONTH = 20
	PERCENT_DOWN_MIN = 0.03
	PERCENT_CHANGE_TRIGGER = -0.50
	
	def __init__(self, csvFile):
		self.allData = []
		self.__parseCsvFile(csvFile)		
		self.lastIndex = len(self.allData) - 1
		self.__interDayCalculations()
		self.__trendStats()
		self.__strategyMovAvg()	

	def __parseCsvFile(self, csvFile):
		data = [line.rstrip('\n') for line in open(csvFile)]
		for idx, csvline in enumerate(data):
			if(idx != 0):		
				self.allData.append((PriceData(csvline)))

	def __interDayCalculations(self):
		for idx, day in enumerate(self.allData):
			self.__calcChange(idx)
			self.__calcMovAvgs(idx)
			self.__calcBollingerBand(idx)
				
	def __calcMovAvgs(self, idx):
		for n in self.PERIODS:
			self.allData[idx].movAvg.append(self.__getAverage(idx, idx + n))

	def __calcBollingerBand(self, idx):
		n = self.PERIODS[self.MOVAVG_20]
		self.allData[idx].bollingerBand = BollingerBand(self.allData[idx].movAvg[self.MOVAVG_20], self.__calcStdDev(idx, idx + n))

	def __calcChange(self, index):
		if(index < self.lastIndex):
			yesterdaysClose = self.allData[index + 1].close
			self.allData[index].change = self.allData[index].close - yesterdaysClose
			self.allData[index].percentChange = (self.allData[index].change / yesterdaysClose) * 100
		if(index - self.MONTH > 0):
			self.allData[index].closeMonthLater = self.allData[index - self.MONTH].close

	def __getMax(self, indexStart, indexEnd):		
		if(indexEnd < self.lastIndex):
			return numpy.max([self.allData[i].close for i in range(indexStart, indexEnd)])
		return 0

	def __getMin(self, indexStart, indexEnd):		
		if(indexEnd < self.lastIndex):
			return numpy.min([self.allData[i].close for i in range(indexStart, indexEnd)])
		return 0

	def __getAverage(self, indexStart, indexEnd):		
		if(indexEnd < self.lastIndex):
			return sum(self.allData[i].close for i in range(indexStart, indexEnd)) / (indexEnd - indexStart)
		return 0

	def __getBandAverage(self, indexStart, indexEnd):		
		if(indexEnd < self.lastIndex):
			return sum(self.allData[i].bandWidth for i in range(indexStart, indexEnd)) / (indexEnd - indexStart)
		return 0

	def __calcStdDev(self, indexStart, indexEnd):		
		if(indexEnd < self.lastIndex):
			return numpy.std([self.allData[i].close for i in range(indexStart, indexEnd)])
		return 0

	def __percent(self, x, total):
		return format(100 * x / total, '0.2f')
	
	def __movAvgStrike(self, day):		
		strike = day.close * (1 - self.PERCENT_DOWN_MIN)
		if (day.movAvg[self.MOVAVG_200] < strike):
			strike = day.movAvg[self.MOVAVG_200]
		return strike

	def __trendStats(self):		
		self.__daysBelow = sum(1 if(day.movAvg[self.MOVAVG_200] != 0 and day.close < day.movAvg[self.MOVAVG_200]) else 0 for day in self.allData)
		self.__daysAbove = len(self.allData) - self.__daysBelow

	def __strategyMovAvg(self):
		self.__movAvgStrategy = StrategyResult('Moving Average')
		for idx, day in enumerate(self.allData):
			if(idx - self.MONTH >= 0 and day.percentChangeIsBelow(self.PERCENT_CHANGE_TRIGGER) and day.closeIsAbove(day.movAvg[self.MOVAVG_20])):
				self.__movAvgStrategy.addTradeDay(day, self.__movAvgStrike(day))

	def displayAll(self):
		print("Days above {0} moving average = {1} ({2}%)".format(self.PERIODS[self.MOVAVG_200], self.__daysAbove, self.__percent(self.__daysAbove, len(self.allData))))
		print("Days below {0} moving average = {1} ({2}%)\n".format(self.PERIODS[self.MOVAVG_200], self.__daysBelow, self.__percent(self.__daysBelow, len(self.allData))))
		print(self.__movAvgStrategy.toString())
		print(self.__movAvgStrategy.displayResults())



def runAllData():
	datadir = 'Data/'
	for f in os.listdir(datadir):
		if f.endswith(".csv"):
			print(f)
			historicalData = EquityData(datadir + f)			

def main():
	path = os.path.dirname(os.path.realpath(__file__))
	os.chdir(path)
	spx = EquityData('Data/SPX.csv')
	spx.displayAll()	

if __name__ == "__main__":
    main()