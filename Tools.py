class Constants:
	ISUP = -10
	ISDOWN = 0

	STRIKE_PCT_DOWN = 0.05
	REPAIR_STRIKE_PCT_DOWN = 0.04
	NETCHANGE_PCT = 10	
	VIX_MIN = 1	

	HOLD_PERIOD = 25
	MONTH = 25	
	BOLBAND_PERIOD = '20day'

	SHORT_HOLD_PERIOD = 2
	SHORT_MULTIPLIER = 0

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

class DateHelper:
	MONDAY = 1
	TUESDAY = 2
	WEDNESDAY = 3
	THURSDAY = 4
	FRIDAY = 5

	@staticmethod
	def getWeekday(day):
		d = day.weekday()
		if(d == DateHelper.MONDAY):
			return 'M'
		elif(d == DateHelper.TUESDAY):
			return 'T'
		elif(d == DateHelper.WEDNESDAY):
			return 'W'
		elif(d == DateHelper.THURSDAY):
			return 'H'
		elif(d == DateHelper.FRIDAY):
			return 'F'

