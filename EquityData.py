import os
import numpy as np
from PriceData import PriceData

class Result:
	def __init__(self):
		self.wins = 0
		self.loss = 0
		self.touch = 0
		self.touch3pct = 0
		self.touch5pct = 0		

	def __total(self):
		return self.wins + self.loss

	def addwin(self):
		self.wins += 1

	def addloss(self):
		self.loss += 1

	def addtouch5pct(self):
		self.touch5pct += 1

	def addtouch3pct(self):
		self.touch3pct += 1

	def addtouch(self):
		self.touch += 1	

	def pctwin(self):
		return Compute.percent(self.wins, self.__total())

	def pctloss(self): 
		return Compute.percent(self.loss, self.__total())

	def pcttouch(self):
		return Compute.percent(self.touch, self.__total())

	def pcttouch3pct(self):
		return Compute.percent(self.touch3pct, self.__total())

	def pcttouch5pct(self):
		return Compute.percent(self.touch5pct, self.__total())

	def print(self):
		print("Win: {0}%".format(self.pctwin()))
		print("Loss: {0}%\n".format(self.pctloss()))

class ResultTable:
	def __init__(self, cname):
		self.hdr = []
		self.rslt = []
		self.hrow = cname + "\t"
		self.wrow = "W\t"
		self.lrow = "L\t"
		self.trow = "T\t"
		self.t3row = "T3\t"
		self.t5row = "T5\t"
		
	def add(self, h, r):
		self.hdr.append(h)
		self.rslt.append(r)		

	def pctprint(self):		
		for idx, r in enumerate(self.rslt):
			self.hrow += "{0}\t".format(self.hdr[idx])
			self.wrow += "{0}\t".format(r.pctwin())
			self.lrow += "{0}\t".format(r.pctloss())
			self.trow += "{0}\t".format(r.pcttouch())
			self.t3row += "{0}\t".format(r.pcttouch3pct())
			self.t5row += "{0}\t".format(r.pcttouch5pct())
		print("{0}\n{1}\n{2}\n{3}\n{4}\n{5}".format(self.hrow, self.wrow, 
													self.lrow, self.trow,
													self.t3row, self.t5row))

	def print(self):
		for idx, r in enumerate(self.rslt):
			self.hrow += "{0}\t".format(self.hdr[idx])
			self.wrow += "{0}\t".format(format(r.wins, '0.2f'))
			self.lrow += "{0}\t".format(format(r.loss, '0.2f'))
			self.trow += "{0}\t".format(format(r.touch, '0.2f'))
		print("{0}\n{1}\n{2}\n{3}".format(self.hrow, self.wrow, self.lrow, self.trow))

	def wlprint(self):
		for idx, r in enumerate(self.rslt):
			self.hrow += "{0}\t".format(self.hdr[idx])
			self.wrow += "{0}\t".format(r.wins)
			self.lrow += "{0}\t".format(r.loss)			
		print("{0}\n{1}\n{2}".format(self.hrow, self.wrow, self.lrow))

class Compute:

	def percent(val, total):
		return format(100 * val / total, "0.2f")

class EquityData:
	
	EXP = [20, 25]
	PCT_DOWN = [7, 9]

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

	def __daysdown(self, idx, daysdown, pctdownlimit):
		for i in range(idx, idx + daysdown):
			if (self.data[i].percentChange > pctdownlimit):
				return False
		return True

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
			strike = day.close * (1 - (pctdown/100))
			daysdown = 0
			downmag = 0
			if (offset >= 0 and idx + daysdown < self.__lastIdx and 
				day.close > day.movavg['200day'] and 
				self.__daysdown(idx, daysdown, downmag)):
				if (strike <= self.data[offset].close):
					result.addwin()
				else: 
					result.addloss()
				
				if (self.__touchesPutStrike(strike, offset, idx)):
					result.addtouch()

				if (self.__touchesPutStrike(strike * 1.03, offset, offset + 5)):
					result.addtouch3pct()

				if (self.__touchesPutStrike(strike * 1.05, offset, offset + 5)):
					result.addtouch5pct()
		return result

	def __movavgdown(self, ma, holdperiod, min_pct_down):
		result = Result()
		for idx, day in enumerate(self.data):			
			offset = idx - holdperiod
			strike = day.movavg[ma]			
			if (offset >= 0 and strike > 0 and day.close > strike):
				strikemin = (1 - min_pct_down) * day.close
				if (strike > strikemin):
					strike = strikemin
				if (strike <= self.data[offset].close):
					result.addwin()
				else: 
					result.addloss()
				
				if (self.__touchesPutStrike(strike, offset, idx)):
					result.addtouch()

				if (self.__touchesPutStrike(strike * 1.03, offset, offset + 5)):
					result.addtouch3pct()

				if (self.__touchesPutStrike(strike * 1.05, offset, offset + 5)):
					result.addtouch5pct()

		return result

	def trend(self):
		rt = ResultTable("Trend")
		rt.wrow = "Above\t"
		rt.lrow = "Below\t"
		for p in PriceData.periods:
			r = self.__trend(p)
			rt.add(p, r)
		rt.wlprint()

	def pctDown(self):
		for hp in self.EXP:
			rt = ResultTable("PD")			
			print("\nPctDown; Holding Period = {0}".format(hp))
			for pct in self.PCT_DOWN:
				r = self.__pctDown(pct, hp)
				rt.add("{0}%".format(format(round(pct), '0.2f')), r)
			rt.pctprint()
			# rt.print()

	def movavgdown(self):
		for hp in self.EXP:
			rt = ResultTable("MA")
			print("\nMovAvgDown; Holding Period = {0}".format(hp))	
			for p in PriceData.periods:			
				r = self.__movavgdown(p, hp, Compute.PERCENT_7)
				rt.add(p, r)
			rt.pctprint()

def main():
	path = os.path.dirname(os.path.realpath(__file__))
	os.chdir(path)	
	spx = EquityData('Data/SPX.csv')
	# spx.trend()
	spx.pctDown()
	# spx.movavgdown()

if __name__ == "__main__":
    main()