import os
import numpy as np
from PriceData import PriceData
from Result import Result, ResultTable

class EquityData:
	
	EXP = [20, 25]
	PCT_DOWN = [7, 9]
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

	def __bandwidth(self, hp, pctdown):
		result = Result()
		for idx, day in enumerate(self.data):
			offset = idx - hp
			ba = self.__calcBandAvg(idx)			
			strike = (1 - pctdown) * day.close
			if(offset >= 0 and strike > 0 and day.close > strike and 				
				ba > 0 and day.bollingerband.bandwidth > ba):				
				# print("{0}\t{1}".format(day.toString(), ba))
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
				r = self.__movavgdown(p, hp, 0.07)
				rt.add(p, r)
			rt.pctprint()

	def bandwidth(self):		
		for hp in self.EXP:
			rt = ResultTable("BW")
			print("\nBandWidth; Holding Period = {0}".format(hp))			
			r = self.__bandwidth(hp, 0.07)
			rt.add('20day', r)
			rt.pctprint()			

def main():
	path = os.path.dirname(os.path.realpath(__file__))
	os.chdir(path)	
	spx = EquityData('Data/SPX.csv')
	# spx.trend()
	# spx.pctDown()
	# spx.movavgdown()
	spx.bandwidth()

if __name__ == "__main__":
    main()