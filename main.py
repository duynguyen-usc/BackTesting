import os
from EquityData import EquityData

# Main

path = os.path.dirname(os.path.realpath(__file__))
os.chdir(path)
testData = EquityData('Data/SPX.csv')

testData.trendStats(EquityData.ONE_HUNDRED_FIFTY_DAY)
testData.trendStats(EquityData.TWO_HUNDRED_DAY)
testData.trendStats(EquityData.TWO_HUNDRED_FIFTY_DAY)