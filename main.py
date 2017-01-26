import os
from EquityData import EquityData

# Main

path = os.path.dirname(os.path.realpath(__file__))
os.chdir(path)
datadir = 'Data/'
csvfiles=[]
for file in os.listdir(datadir):
    if file.endswith(".csv"):
        csvfiles.append(file)

for f in csvfiles:
	print(f)
	historicalData = EquityData(datadir + f)
	historicalData.trendStats(EquityData.TWO_HUNDRED_DAY)