class Result:
	WIN = 0
	LOSS = 1
	MAX_GAIN = 2
	MAX_LOSS = 3

	def __init__(self):
		self.result = []
		self.result[self.WIN] = 0 
		self.result[self.LOSS] = 0 
		self.result[self.MAX_GAIN] = 0 
		self.result[self.MAX_LOSS] = 0 

	def __total(self):
		return self.wins + self.loss

	def __percent(self, val, total):
		if (total > 0):
			return format(100 * val / total, "0.2f")
		return 0

	def addResult(self, r):
		self.result[self.WIN] += r.result[self.WIN]
		self.result[self.LOSS] += r.result[self.LOSS] 
		self.result[self.MAX_GAIN] += r.result[self.MAX_GAIN] 
		self.result[self.MAX_LOSS] += r.result[self.MAX_LOSS]