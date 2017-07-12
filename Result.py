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