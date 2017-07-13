class Result:
	def __init__(self):
		self.win = 0
		self.loss = 0
		self.maxLoss = 0
		self.maxGain = 0
		
	def __total(self):
		return self.wins + self.loss

	def __percent(self, val, total):
		if (total > 0):
			return format(100 * val / total, "0.2f")
		return 0

	def addStat(self, r):
		self.win += r.win 
		self.loss = r.loss
		self.maxLoss = r.maxLoss
		self.maxGain = r.maxGain