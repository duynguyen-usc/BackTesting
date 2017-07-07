class Result:
	def __init__(self):
		self.wins = 0
		self.loss = 0

	def __total(self):
		return self.wins + self.loss

	def __percent(self, val, total):
		if (total > 0):
			return format(100 * val / total, "0.2f")
		return 0

	def addwin(self):
		self.wins += 1

	def addloss(self):
		self.loss += 1

	def pctwin(self):
		return self.__percent(self.wins, self.__total())

	def pctloss(self): 
		return self.__percent(self.loss, self.__total())	

	def toString(self):
		print("Win: {0}%".format(self.pctwin()))
		print("Loss: {0}%\n".format(self.pctloss()))

class ResultTable:
	def __init__(self, cname):
		self.hdr = []
		self.rslt = []
		self.hrow = cname + "\t"
		self.wrow = "Win \t"
		self.lrow = "Loss\t"		
		
		
	def add(self, h, r):
		self.hdr.append(h)
		self.rslt.append(r)		

	def toString(self):		
		for idx, r in enumerate(self.rslt):
			self.hrow += "{0}\t[####]\t".format(self.hdr[idx])
			self.wrow += "{0}\t[{1}]\t".format(r.pctwin(), r.wins)
			self.lrow += "{0}\t[{1}]\t".format(r.pctloss(), r.loss)
		return "\n{0}\n{1}\n{2}".format(self.hrow, self.wrow, self.lrow)