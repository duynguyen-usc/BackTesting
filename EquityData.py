import os
import numpy
from PriceData import PriceData
from BollingerBand import BollingerBand
from StrategyResult import StrategyResult

class EquityData:
	MOVAVG_10 = 0
	MOVAVG_20 = 1
	MOVAVG_50 = 2
	MOVAVG_150 = 3
	MOVAVG_200 = 4	
	MOVAVG_250 = 5
	MOVAVG_300 = 6
	PERIODS = [10, 20, 50, 150, 200, 250, 300]

	MONTH = 20
	
	
	def __init__(self, csvFile):		
		self.__allData = []
		self.__parseCsvFile(csvFile)		
		self.__lastIndex = len(self.__allData) - 1
		self.__interDayCalculations()		

	def __parseCsvFile(self, csvFile):
		data = [line.rstrip('\n') for line in open(csvFile)]
		for idx, csvline in enumerate(data):
			if(idx != 0):		
				self.__allData.append((PriceData(csvline)))

	def __interDayCalculations(self):
		for idx, day in enumerate(self.__allData):
			self.__calcChange(idx)
			self.__calcMovAvgs(idx)
			self.__calcBollingerBand(idx)
				
	def __calcMovAvgs(self, idx):
		for n in self.PERIODS:
			self.__allData[idx].movAvg.append(self.__getAverage(idx, idx + n))

	def __calcBollingerBand(self, idx):
		n = self.PERIODS[self.MOVAVG_20]
		mid = self.__allData[idx].movAvg[self.MOVAVG_20]
		stddev = self.__calcStdDev(idx, idx + n)
		self.__allData[idx].bollingerBand = BollingerBand(mid, stddev)

	def __calcChange(self, index):
		if(index < self.__lastIndex):
			yesterdaysClose = self.__allData[index + 1].close
			self.__allData[index].change = self.__allData[index].close - yesterdaysClose
			self.__allData[index].percentChange = (self.__allData[index].change / yesterdaysClose) * 100
		if(index - self.MONTH > 0):
			self.__allData[index].closeMonthLater = self.__allData[index - self.MONTH].close

	def __getMax(self, indexStart, indexEnd):		
		if(indexEnd < self.__lastIndex):
			return numpy.max([self.__allData[i].close for i in range(indexStart, indexEnd)])
		return 0

	def __getMin(self, indexStart, indexEnd):		
		if(indexEnd < self.__lastIndex):
			return numpy.min([self.__allData[i].close for i in range(indexStart, indexEnd)])
		return 0

	def __getAverage(self, indexStart, indexEnd):		
		if(indexEnd < self.__lastIndex):
			return sum(self.__allData[i].close for i in range(indexStart, indexEnd)) / (indexEnd - indexStart)
		return 0

	def __getBandAverage(self, indexStart, indexEnd):		
		if(indexEnd < self.__lastIndex):
			return sum(self.__allData[i].bandWidth for i in range(indexStart, indexEnd)) / (indexEnd - indexStart)
		return 0

	def __calcStdDev(self, indexStart, indexEnd):		
		if(indexEnd < self.__lastIndex):
			return numpy.std([self.__allData[i].close for i in range(indexStart, indexEnd)])
		return 0

	def __percent(self, x, total):
		return format(100 * x / total, '0.2f')
	

def main():
	path = os.path.dirname(os.path.realpath(__file__))
	os.chdir(path)
	spx = EquityData('Data/SPX.csv')	

if __name__ == "__main__":
    main()