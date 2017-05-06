class OptStructure:
	SHORT_VERTICAL_CALL = 0
	SHORT_VERTICAL_PUT = 1
	LONG_VERTICAL_CALL = 3
	LONG_VERTICAL_PUT = 4

class Math:

	def percent(val, total):		
		return format(100 * val / total, "0.2f")

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
		return Math.percent(self.wins, self.__total())

	def pctloss(self): 
		return Math.percent(self.loss, self.__total())	

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