class LossAnalysis:
	def __init__(self, option, hpdata):
		self.option = option
		self.hpdata = hpdata

	def toString(self):
		strLa = self.option.toString() + "\n"
		for self.d in self.hpdata:
			strLa += self.d.toString() + "\n"
		return strLa