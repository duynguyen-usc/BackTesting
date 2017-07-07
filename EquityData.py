import os
import numpy as np
from Option import Option
from PriceData import PriceData
from Result import Result, ResultTable

class EquityData:
	BOLBAND_P = '20day'

	def __init__(self, csvFile):		
		self.data = []
		self.__parseCsvFile(csvFile)		
		self.__lastIdx = len(self.data) - 1
		self.__interDayCalculations()
		print("\n" + csvFile)

	def __parseCsvFile(self, csvFile):
		data = [line.rstrip('\n') for line in open(csvFile)]
		for idx, csvline in enumerate(data):
			if(idx != 0):		
				self.data.append((PriceData(csvline)))

	def __interDayCalculations(self):
		for idx, day in enumerate(self.data):			
			self.__calcChange(idx)
			self.__calcMovAvgs(idx)
			#self.__calcBolBand(idx)
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

	def __consecutiveDaysChange(self, idx, days, change):
		for i in range(idx, idx + days):
			if((i > self.__lastIdx) or 
			   (self.data[i].change == None) or 
			   (change <= 0 and self.data[i].change > change) or
			   (change > 0 and self.data[i].change < change)):
				return False
		return True
	
	def __entryCriteria(self, d, optstruct, idx):
		uptrend = d.close > d.movavg['200day']
		if (optstruct == optype.SHORT_VERTICAL_PUT):
			return uptrend and self.__consecutiveDaysChange(idx, 1, 0)		
		return False

	def __studyhp(self, pct, holdperiod, optstruct):
		result = Result()
		for idx, day in enumerate(self.data):
			offset = idx - holdperiod
			strike = day.close * (1 + (pct/100))			 
			if (offset >= 0 and self.__entryCriteria(day, optstruct, idx)):
				if (self.__isWin(optstruct, strike, self.data[offset].close)):
					result.addwin()
				else: 
					result.addloss()
		return result

	def __runstudy(self, studytitle, pct, hps, optstruct):
		for hp in hps:
			rt = ResultTable(studytitle)
			print("\nHolding Period = {0}".format(hp))
			for p in pct:
				rt.add("{0:.2f}%".format(p), 
					self.__studyhp(p, hp, optstruct))
			print(rt.toString())

	def bullPut(self):
		put_pct = [-7]
		put_hps = [25]		
		self.__runstudy('BuPV', put_pct, put_hps, optype.SHORT_VERTICAL_PUT)


def main():
	path = os.path.dirname(os.path.realpath(__file__))
	os.chdir(path)

	# spx = EquityData('Data/SPX.csv')
	# spx.bullPut()
	print(Option.VERTICAL_PUT)

if __name__ == "__main__":
    main()