import os
import numpy as np
from Option import Option
from PriceData import PriceData
from Result import Result

class EquityData:
	BOLBAND_P = '20day'
	HOLD_PERIOD = 25

	def __init__(self, csvFile):		
		self.data = []
		self.__parseCsvFile(csvFile)		
		self.__lastIdx = len(self.data) - 1

	def __parseCsvFile(self, csvFile):
		data = [line.rstrip('\n') for line in open(csvFile)]
		for idx, csvline in enumerate(data):
			if(idx != 0):		
				self.data.append((PriceData(csvline)))

	def __interDayCalculations(self):
		for idx, day in enumerate(self.data):			
			self.__calcChange(idx)
			# self.__calcMovAvgs(idx)
			# self.__calcBolBand(idx)
			# print("idx: {0} {1:.2f}".format(idx, day.change))

	def __calcChange(self, idx):
		if(idx < self.__lastIdx):
			prevClose = self.data[idx + 1].close
			if (prevClose > 0):
				self.data[idx].change = self.data[idx].close - prevClose
				self.data[idx].percentChange = (self.data[idx].change / prevClose) * 100
			else: 
				self.data[idx].change = 0
				self.data[idx].percentChange = 0

	def __calcMovAvgs(self, idx):		
		for p in PriceData.periods:
			offset =  idx + PriceData.periods[p]
			self.data[idx].movavg[p] = self.__getAverage(idx, offset)

	def __calcBolBand(self, idx):		
		midline = self.data[idx].movavg[self.BOLBAND_P]
		stddev = self.__calcStdDev(idx, idx + PriceData.periods[self.BOLBAND_P])
		self.data[idx].bollingerband.calculate(midline, stddev)

	def __calcBandAvg(self, idx):		
		bsum = 0
		bcount = 0
		idxend = idx + PriceData.periods[self.BOLBAND_P]
		for i in range(idx, idxend):			
			if(i < self.__lastIdx):				
				bw = self.data[i].bollingerband.bandwidth				
				if(bw > 0):					
					bcount += 1
					bsum += bw
		if(bcount > 0):
			return bsum / bcount
		return 0
		
	def __getMax(self, idxStart, idxEnd):		
		if(idxEnd < self.__lastIdx):
			return np.max([self.data[i].close for i in range(idxStart, idxEnd)])
		return 0

	def __getMin(self, idxStart, idxEnd):		
		if(idxEnd < self.__lastIdx):
			return np.min([self.data[i].close for i in range(idxStart, idxEnd)])
		return 0

	def __getAverage(self, idxStart, idxEnd):		
		if(idxEnd < self.__lastIdx):
			return sum(self.data[i].close for i in range(idxStart, idxEnd)) / (idxEnd - idxStart)
		return 0

	def __calcStdDev(self, idxStart, idxEnd):		
		if(idxEnd < self.__lastIdx):
			return np.std([self.data[i].close for i in range(idxStart, idxEnd)])
		return 0

	def bullput(self):
		r = Result()		
		for idx, day in enumerate(self.data):
			if (day.close > 0 and (idx + self.HOLD_PERIOD) < self.__lastIdx):
				putoption = Option(Option.SHORT_VERTICAL_PUT, day)
				print(putoption.toString())
		

def main():
	path = os.path.dirname(os.path.realpath(__file__))
	os.chdir(path)
	spx = EquityData('Data/SPX.csv')
	spx.bullput()

if __name__ == "__main__":
    main()