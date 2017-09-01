class StringBuilder:
	def __init__(self, str=""):
		self.s = str

	def add(self, s):
		self.s += "{0}".format(s)

	def addline(self, s):
		self.s += "{0}\n".format(s)

	def addtab(self, s):
		self.s += "{0}\t".format(s)

	def addDate(self, d):
		self.s += "{0}\t".format(d.strftime('%Y-%m-%d'))

	def prepend(self, s):
		self.s = "{0}{1}".format(s, self.s)

	def toString(self):
		return self.s

