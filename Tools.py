class StringBuilder:
	def __init__(self, str=""):
		self.s = str

	def add(self, s):
		self.s += "{0}\t".format(s)

	def addline(self, s):
		self.s += "{0}\n".format(s)

	def toString(self):
		return self.s