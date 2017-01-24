import os
from EquityData import EquityData

# Main

path = os.path.dirname(os.path.realpath(__file__))
os.chdir(path)
testData = EquityData('Data/SPX.csv')
print(testData.calcMovAvg(20, 0))
print(testData.calcStdev)
