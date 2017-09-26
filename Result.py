from Tools import StringBuilder

class Result:
	def __init__(self):
		self.win = 0
		self.loss = 0
		self.maxLoss = 0
		self.maxGain = 0
		self.itm5 = 0
		
	def __total(self):
		return self.wins + self.loss

	def __percent(self, val):
		total = self.win + self.loss
		if (total > 0):
			return format(100 * val / total, "0.2f")
		return 0

	def addStat(self, r):
		self.win += r.win 
		self.loss += r.loss
		self.maxLoss += r.maxLoss
		self.maxGain += r.maxGain
		self.itm5 += r.itm5

	def toString(self):
		tr = StringBuilder()
		tr.addline("W:\t{1}%\t({0})".format(self.win, self.__percent(self.win)))
		tr.addline("MG:\t{1}%\t({0})".format(self.maxGain, self.__percent(self.maxGain)))
		tr.addline("L:\t{1}%\t({0})".format(self.loss, self.__percent(self.loss)))
		tr.addline("ML:\t{1}%\t({0})".format(self.maxLoss, self.__percent(self.maxLoss)))
		tr.addline("T5:\t{1}%\t({0})".format(self.itm5, self.__percent(self.itm5)))
		return tr.toString()
		

		