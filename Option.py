
class Option:
	def __init__(self, longshort, optiontype):
		self.type = optiontype
		self.longshort = longshort	
		self.shortstrike = 0
		self.longstrike = 0

class BullPut(Option):
	def __init__(self):
		Option.__init__(self, put)