class BollingerBand:
	def __init__(self, movAvgMidline, stddeviation):
		self.midLine = movAvgMidline
		self.upperBand = 2 * stddeviation + self.midLine
		self.lowerBand = -2 * stddeviation + self.midLine
		self.bandWidth = self.upperBand - self.lowerBand		