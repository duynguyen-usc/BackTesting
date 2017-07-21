class StringBuilder:
	def __init__(self, str=""):
		self.s = str

	def add(self, s):
		self.s += "{0}\t".format(s)

	def addline(self):
		self.s += '\n'

	def addtab(self):
		self.s += '\t'

	def toString(self):
		return self.s