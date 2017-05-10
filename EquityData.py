import os
import numpy as np
from PriceData import PriceData
from Result import Result, ResultTable

class OptStructure:
	SHORT_VERTICAL_CALL = 0
	SHORT_VERTICAL_PUT = 1
	LONG_VERTICAL_CALL = 3
	LONG_VERTICAL_PUT = 4

class EquityData:
	
	BOLBAND_P = '20day'

	def __init__(self, csvFile):		
		self.data = []
		self.__parseCsvFile(csvFile)		
		self.__lastIdx = len(self.data) - 1
		self.__interDayCalculations()		

	def __parseCsvFile(self, csvFile):
		data = [line.rstrip('\n') for line in open(csvFile)]
		for idx, csvline in enumerate(data):
			if(idx != 0):		
				self.data.append((PriceData(csvline)))

	def __interDayCalculations(self):
		for idx, day in enumerate(self.data):
			print("idx: {0}".format(idx))
			self.__calcChange(idx)
			self.__calcMovAvgs(idx)
			self.__calcBolBand(idx)			

	def __calcChange(self, idx):
		if(idx < self.__lastIdx):
			prevClose = self.data[idx + 1].close
			self.data[idx].change = self.data[idx].close - prevClose
			self.data[idx].percentChange = (self.data[idx].change / prevClose) * 100

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

	def __entryCriteria(self, d):
		return d.close > d.movavg['200day']

	def __isWin(self, optstruct, strike, expclose):
		if ((optstruct == OptStructure.SHORT_VERTICAL_PUT and strike <= expclose) or
		   (optstruct == OptStructure.SHORT_VERTICAL_CALL and strike >= expclose)):
			return True
		return False

	def __runstudy(self, pct, holdperiod, optstruct):
		result = Result()
		for idx, day in enumerate(self.data):
			offset = idx - holdperiod
			strike = day.close * (1 + (pct/100))			 
			if (offset >= 0 and self.__entryCriteria(day)):
				if (self.__isWin(optstruct, strike, self.data[offset].close)):
					result.addwin()
				else: 
					result.addloss()
		return result

	def runstudy(self, studytitle, pct, hps, optstruct):
		for hp in hps:
			rt = ResultTable(studytitle)
			print("\nHolding Period = {0}".format(hp))
			for p in pct:
				rt.add("{0}%".format(format(round(p), '0.2f')), 
					self.__runstudy(p, hp, optstruct))
			rt.pctprint()

def main():
	path = os.path.dirname(os.path.realpath(__file__))
	os.chdir(path)

	spx = EquityData('Data/SPX.csv')

	put_pct = [-5, -7, -9]
	put_hps = [15, 20, 25]
	spx.runstudy('VP', put_pct, put_hps, OptStructure.SHORT_VERTICAL_PUT)

	call_pct = [1, 2, 3]
	call_hps = [1, 2, 3]
	spx.runstudy('VC', call_pct, call_hps, OptStructure.SHORT_VERTICAL_CALL)

if __name__ == "__main__":
    main()