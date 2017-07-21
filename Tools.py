class StringBuilder:
	def __init__(self, str):
		self.str = str

	def add(self, s):
		self.str += "{0}\t".format(s)

	def addline(self, s):
		self.str += "{0}\n".format(s)

	def toString(self)
		return self.str