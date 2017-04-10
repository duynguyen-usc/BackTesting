import numpy
from PriceData import PriceData

class EquityData:	
	def __init__(self, csvFile):		
		self.data = []
		self.__parseCsvFile(csvFile)		
		self.__lastIndex = len(self.data) - 1
		self.__interDayCalculations()		

	def __parseCsvFile(self, csvFile):
		data = [line.rstrip('\n') for line in open(csvFile)]
		for idx, csvline in enumerate(data):
			if(idx != 0):		
				self.data.append((PriceData(csvline)))

	def __interDayCalculations(self):
		for idx, day in enumerate(self.data):
			self.__calcChange(idx)

	def __calcChange(self, index):
		month = 20
		if(index < self.__lastIndex):
			yesterdaysClose = self.data[index + 1].close
			self.data[index].change = self.data[index].close - yesterdaysClose
			self.data[index].percentChange = (self.data[index].change / yesterdaysClose) * 100

	def getMax(self, indexStart, indexEnd):		
		if(indexEnd < self.__lastIndex):
			return numpy.max([self.data[i].close for i in range(indexStart, indexEnd)])
		return 0

	def getMin(self, indexStart, indexEnd):		
		if(indexEnd < self.__lastIndex):
			return numpy.min([self.data[i].close for i in range(indexStart, indexEnd)])
		return 0

	def getAverage(self, indexStart, indexEnd):		
		if(indexEnd < self.__lastIndex):
			return sum(self.data[i].close for i in range(indexStart, indexEnd)) / (indexEnd - indexStart)
		return 0

	def calcStdDev(self, indexStart, indexEnd):		
		if(indexEnd < self.__lastIndex):
			return numpy.std([self.data[i].close for i in range(indexStart, indexEnd)])
		return 0

	def toString(self):
		s = ''
		for day in self.data:
			s += day.toString()
		return s