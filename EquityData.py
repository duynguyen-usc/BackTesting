import os
import numpy as np
from PriceData import PriceData

class Result:
	def __init__(self):
		self.wins = 0
		self.loss = 0

	def __total(self):
		return self.wins + self.loss

	def addwin(self):
		self.wins += 1

	def addloss(self):
		self.loss += 1

	def pctwin(self):
		return Compute.percent(self.wins, self.__total())

	def pctloss(self): 
		return Compute.percent(self.loss, self.__total())

	def print(self):
		print("Win: {0}%".format(self.pctwin()))
		print("Loss: {0}%\n".format(self.pctloss()))

class ResultTable:
	def __init__(self, cname):
		self.hrow = cname + "\t"
		self.wrow = "W\t"
		self.lrow = "L\t"

	def add(self, h, w, l):
		self.hrow += "{0}\t".format(h)
		self.wrow += "{0}\t".format(w)
		self.lrow += "{0}\t".format(l)

	def print(self):
		print("{0}\n{1}\n{2}".format(self.hrow, self.wrow, self.lrow))

class Compute:

	PERCENT_5 = 0.05
	PERCENT_7 = 0.07
	PERCENT_9 = 0.09

	WEEKS_2 = 10
	WEEKS_3 = 15
	WEEKS_4 = 20
	WEEKS_5 = 25
	WEEKS_6 = 30
	WEEKS_7 = 35

	def percent(val, total):
		return format(100 * val / total, "0.2f")

class EquityData:
	
	H_PERIODS = [10, 15, 20, 25, 30, 35, 40, 50, 60, 70]

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
			# self.__calcBolBand(idx)

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

	def __touchesPutStrike(self, strike, idxStart, idxEnd):		
		return strike > self.__getMin(idxStart, idxEnd)

	def __touchesCallStrike(self, strike, idxStart, idxEnd):		
		return strike < self.__getMin(idxStart, idxEnd)

	def __trend(self, period):		
		result = Result()
		for day in self.data:
			ma = day.movavg[period]
			if (ma > 0):
				if(day.close > ma):
					result.addwin()
				else:
					result.addloss()
		return result

	def __pctDown(self, pctdown, holdperiod):
		result = Result()
		for idx, day in enumerate(self.data):
			offset = idx - holdperiod
			strike = day.close * (1 - pctdown) 
			if (offset >= 0 and day.close > day.movavg['200day']):
				if (strike <= self.data[offset].close):
					result.addwin()
				else: 
					result.addloss()
		return result

	def __movavgdown(self, ma, holdperiod):
		result = Result()
		for idx, day in enumerate(self.data):			
			offset = idx - holdperiod
			strike = day.movavg[ma]			
			if (offset >= 0 and strike > 0 and day.close > strike):
				strikemin = (1 - Compute.PERCENT_7) * day.close
				if (strike > strikemin):
					strike = strikemin
				if (strike <= self.data[offset].close):
					result.addwin()
				else: 
					result.addloss()
		return result

	def trend(self):
		rt = ResultTable("Trend")
		rt.wrow = "Above\t"
		rt.lrow = "Below\t"
		for p in PriceData.periods:
			r = self.__trend(p)
			rt.add(p, r.pctwin(), r.pctloss())			
		rt.print()

	def pctDown(self):		
		pcts = [Compute.PERCENT_5, Compute.PERCENT_7, Compute.PERCENT_9]
		for hp in self.H_PERIODS:
			rt = ResultTable("D")			
			print("\nPctDown; Holding Period = {0}".format(hp))
			for pct in pcts:
				r = self.__pctDown(pct, hp)
				rt.add("{0}%".format(format(round(pct * 100), '0.2f')), r.pctwin(), r.pctloss())
			rt.print()

	def movavgdown(self):
		for hp in self.H_PERIODS:
			rt = ResultTable("MA")
			print("\nMovAvgDown; Holding Period = {0}".format(hp))	
			for p in PriceData.periods:			
				r = self.__movavgdown(p, hp)
				rt.add(p, r.pctwin(), r.pctloss())				
			rt.print()

def main():
	path = os.path.dirname(os.path.realpath(__file__))
	os.chdir(path)	
	spx = EquityData('Data/SPX.csv')
	spx.trend()
	spx.pctDown()
	# spx.movavgdown()

if __name__ == "__main__":
    main()