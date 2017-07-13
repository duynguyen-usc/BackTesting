class Result:
	def __init__(self):
		self.win = 0
		self.loss = 0
		self.maxLoss = 0
		self.maxGain = 0
		
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

	def toString(self):
		tr = "W:\t{0}({1}%)\n".format(self.win, self.__percent(self.win))
		tr += "MG:\t{0}({1}%)\n".format(self.maxGain, self.__percent(self.maxGain))
		tr += "L:\t{0}({1}%)\n".format(self.loss, self.__percent(self.loss))
		tr += "ML:\t{0}({1}%)\n".format(self.maxLoss, self.__percent(self.maxLoss))
		return tr
		

		