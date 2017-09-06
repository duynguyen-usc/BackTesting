import os
import numpy as np
from Option import Option
from PriceData import PriceData
from Result import Result
from Tools import StringBuilder

class EquityData:
	BOLBAND_P = '20day'
	HOLD_PERIOD = 25
	MONTH = 25
	TWO_WEEKS = 10	

	def __init__(self, csvFile):		
		self.data = []
		self.vixdata = []
		self.results = Result()
		self.touchresults = Result()
		self.csvFile = csvFile
		self.__parseCsvFile(csvFile)
		self.__parseVixFile()		
		self.__lastIdx = len(self.data) - 1
		self.__interDayCalculations()
		self.__bullput()
		

	def __parseCsvFile(self, csvFile):
		data = [line.rstrip('\n') for line in open(csvFile)]
		for idx, csvline in enumerate(data):
			if(idx != 0):		
				self.data.append((PriceData(csvline)))

	def __parseVixFile(self):
		data = [line.rstrip('\n') for line in open('Data/VIX.csv')]
		for idx, csvline in enumerate(data):
			if(idx != 0):		
				self.vixdata.append((PriceData(csvline)))

	def __getVixValue(self, d):
		for idx, vx in enumerate(self.vixdata):
			if (vx.date == d):
				return vx.close

	def __addVixValue(self, idx):
		self.data[idx].vix = self.__getVixValue(self.data[idx].date)

	def __interDayCalculations(self):
		for idx, day in enumerate(self.data):
			self.__addVixValue(idx)		
			self.__calcChange(idx)
			self.__calcMovAvgs(idx)
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
			offset =  idx - PriceData.periods[p]
			self.data[idx].movavg[p] = self.__getAverage(offset, idx)

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
		if(idxStart > 0):
			return np.max([self.data[i].close for i in range(idxStart, idxEnd)])
		return 0

	def __getMin(self, idxStart, idxEnd):		
		if(idxStart > 0):
			return np.min([self.data[i].close for i in range(idxStart, idxEnd)])
		return 0

	def __getAverage(self, idxStart, idxEnd):		
		if(idxStart > 0):
			return sum(self.data[i].close for i in range(idxStart, idxEnd)) / (idxEnd - idxStart)
		return 0

	def __calcStdDev(self, idxStart, idxEnd):		
		if(idxStart > 0):
			return np.std([self.data[i].close for i in range(idxStart, idxEnd)])
		return 0

	def __isDown(self, idx, pct=0):
		return self.data[idx].percentChange < pct

	def __uptrend(self, idx):			
		idxstart = idx - self.MONTH
		if (idxstart > 0):
			for i in range(idxstart, idx):
				if (self.data[i].close < self.data[i].movavg['200day'] or
					self.data[i].movavg['20day'] < self.data[i].movavg['50day']):
					return False
			return True
		return False

	def __entry(self, idx):		
		return self.__uptrend(idx) and self.__isDown(idx)

	def __getPeriodData(self, idxstart, idxend):
		return [self.data[i] for i in range(idxstart, idxend)]

	def __bullput(self):				
		for idx, day in enumerate(self.data):
			expidx = idx + self.HOLD_PERIOD + 1
			if (day.close > 0 and expidx < self.__lastIdx and self.__entry(idx)):				
				put = Option(Option.SHORT_VERTICAL_PUT, self.__getPeriodData(idx, expidx))
				
				self.results.addStat(put.result)
				if (put.shortstrike != 0 and put.itm > 1):
					self.touchresults.addStat(put.result)
					if(put.result.maxLoss == 1):
						print(put.toString())

	def toString(self):	
		eq = StringBuilder()
		eq.addline('')
		eq.addline('Overall:')
		eq.addline(self.results.toString())
		eq.addline('Touch results:')
		eq.addline(self.touchresults.toString())
		return eq.toString()

def main():
	path = os.path.dirname(os.path.realpath(__file__))
	os.chdir(path)
	spx = EquityData('Data/SPX.csv')
	print(spx.toString())

if __name__ == "__main__":
    main()