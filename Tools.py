class StringBuilder:
	def __init__(self, str=""):
		self.s = str

	def add(self, s):
		self.s += s

	def addline(self, s):
		self.s += s + '\n'

	def addtab(self, s):
		self.s += s + '\t'

	def prepend(self, s):
		self.s = s + self.s

	def toString(self):
		return self.s

