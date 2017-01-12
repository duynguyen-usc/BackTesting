from datetime import datetime

ROUND_PRECISION = 4

def getDate(csvLine):	
	return csvLine.split(',')[0]

def getOpenPrice(csvLine):	
	return float(csvLine.split(',')[1])

def getHighPrice(csvLine):	
	return float(csvLine.split(',')[2])

def getClosePrice(csvLine):	
	return float(csvLine.split(',')[3])

def getClosePrice(csvLine):	
	return float(csvLine.split(',')[4])

def getVolume(csvLine):	
	return float(csvLine.split(',')[5])

def getAdjClosePrice(csvLine):	
	return float(csvLine.split(',')[6])

def netChange(dataSet1, dataSet2):
	return round(getClosePrice(dataSet2) - getClosePrice(dataSet1), ROUND_PRECISION)

def percentChange(dataSet1, dataSet2):
	return round((netChange(dataSet1,dataSet2) / getClosePrice(dataSet1) * 100), ROUND_PRECISION)

def dayRange(dataSet):
	return round(getClosePrice - getOpenPrice(dataSet), ROUND_PRECISION)
	
# Main

SpxData = [line.rstrip('\n') for line in open('Data\Test.csv')]
for idx, val in enumerate(SpxData):
	if(idx != 0) and (idx < len(SpxData)-1):		
		print(percentChange(SpxData[idx + 1], val))