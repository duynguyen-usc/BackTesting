import os
import numpy
from PriceData import PriceData
from BollingerBand import BollingerBand
from StrategyResult import StrategyResult
from MovingAverage import MovAvg

class EquityData:	
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

	def __calcChange(self, index):
		month = 20
		if(index < self.__lastIndex):
			yesterdaysClose = self.__allData[index + 1].close
			self.__allData[index].change = self.__allData[index].close - yesterdaysClose
			self.__allData[index].percentChange = (self.__allData[index].change / yesterdaysClose) * 100
		if(index - month > 0):
			self.__allData[index].closeMonthLater = self.__allData[index - month].close

	def getMax(self, indexStart, indexEnd):		
		if(indexEnd < self.__lastIndex):
			return numpy.max([self.__allData[i].close for i in range(indexStart, indexEnd)])
		return 0

	def getMin(self, indexStart, indexEnd):		
		if(indexEnd < self.__lastIndex):
			return numpy.min([self.__allData[i].close for i in range(indexStart, indexEnd)])
		return 0

	def getAverage(self, indexStart, indexEnd):		
		if(indexEnd < self.__lastIndex):
			return sum(self.__allData[i].close for i in range(indexStart, indexEnd)) / (indexEnd - indexStart)
		return 0

	def calcStdDev(self, indexStart, indexEnd):		
		if(indexEnd < self.__lastIndex):
			return numpy.std([self.__allData[i].close for i in range(indexStart, indexEnd)])
		return 0
	

def main():
	path = os.path.dirname(os.path.realpath(__file__))
	os.chdir(path)
	spx = EquityData('Data/SPX.csv')


if __name__ == "__main__":
    main()