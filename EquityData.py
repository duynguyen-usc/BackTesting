import os
import numpy as np
from PriceData import PriceData

# class Result:
# 	def __init__(self):

class Compute:
	def percent(val, total):
		return format(100 * val / total, "0.2f")

class EquityData:	
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
		print("\n")

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
		p = '20day'
		midline = self.data[idx].movavg[p]
		stddev = self.__calcStdDev(idx, idx + PriceData.periods[p])
		self.data[idx].bollingerband.calculate(midline, stddev)

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

	def touches(self, val, idxStart, idxEnd):
		mx = self.__getMax(idxStart, idxEnd)
		mn = self.__getMin(idxStart, idxEnd)
		return (val < mn or val > mx)

	def __trend(self, period):		
		daysabove = 0
		daysbelow = 0
		for day in self.data:
			ma = day.movavg[period]
			if (ma > 0):
				if(day.close > ma):
					daysabove += 1
				else:
					daysbelow += 1
		pctAbove = Compute.percent(daysabove, daysabove + daysbelow)
		pctBelow = Compute.percent(daysbelow, daysabove + daysbelow)
		print("Above {0}: ({1}%)".format(period, pctAbove))
		print("Below {0}: ({1}%)\n".format(period, pctBelow))

	def __pctDown(self, pctdown, holdperiod):
		wins = 0
		loss = 0
		for idx, day in enumerate(self.data):
			offset = idx - holdperiod
			strike = day.close * (1 - pctdown) 
			if (offset >= 0):
				if (strike <= self.data[offset].close):
					wins += 1
				else: 
					loss += 1
		pctWin = Compute.percent(wins, wins + loss)
		pctLoss = Compute.percent(loss, wins + loss)
		print("Win: {0}%".format(pctWin))
		print("Loss: {0}%\n".format(pctLoss))

	def trend(self):
		for p in PriceData.periods:		
			self.__trend(p)

	def pctDown(self):
		pcts = [0.03, 0.05, 0.07, 0.08, 0.09, 0.10]
		holdperiod = 20
		for pct in pcts:
			self.__pctDown(pct, holdperiod)

	def toString(self): 
		s = ''
		for day in reversed(self.data):
			s += day.toString()
		return s

def main():
	path = os.path.dirname(os.path.realpath(__file__))
	os.chdir(path)	
	spx = EquityData('Data/SPX.csv')
	spx.pctDown()

if __name__ == "__main__":
    main()