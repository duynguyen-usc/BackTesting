from PriceData import PriceData

class EquityData:
	def __init__(self, csvFile):
		self.allData = []
		self.parseCsvFile(csvFile)

	def parseCsvFile(self, csvFile):
		data = [line.rstrip('\n') for line in open(csvFile)]
		for idx, csvline in enumerate(data):
			if(idx != 0):		
				self.allData.append((PriceData(csvline)))

	def displayData(self):
		for day in self.allData:
			print(str(day.date) +  ': ' + str(round(day.close, 2)))