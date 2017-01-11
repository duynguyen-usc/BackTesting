from datetime import datetime


# 0-Date,1-Open,2-High,3-Low,4-Close,5-Volume,6-Adj Close	
def getDate(csvLine):	
	return csvLine.split(',')[0]

def getOpenPrice(csvLine):	
	return csvLine.split(',')[1]

def getHighPrice(csvLine):	
	return csvLine.split(',')[2]

def getClosePrice(csvLine):	
	return csvLine.split(',')[3]

def getClosePrice(csvLine):	
	return csvLine.split(',')[4]

def getVolume(csvLine):	
	return csvLine.split(',')[5]

def getAdjClosePrice(csvLine):	
	return csvLine.split(',')[6]


# Main

csvData = [line.rstrip('\n') for line in open('Data\SPX.csv')]
for idx, val in enumerate(csvData):
	print(getDate(val) + ' = ' + getClosePrice(val))
	
	
