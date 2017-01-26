import os
from EquityData import EquityData

# Main

path = os.path.dirname(os.path.realpath(__file__))
os.chdir(path)
datadir = 'Data/'
for f in os.listdir(datadir):
    if f.endswith(".csv"):
    	print(f)
    	historicalData = EquityData(datadir + f)
    	historicalData.trendStats(EquityData.TWO_HUNDRED_DAY)	