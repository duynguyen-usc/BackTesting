import os
from EquityData import EquityData


def runAllData():
	datadir = 'Data/'
	for f in os.listdir(datadir):
		if f.endswith(".csv"):
			print(f)
			historicalData = EquityData(datadir + f)
			historicalData.runAll()

def main():
	path = os.path.dirname(os.path.realpath(__file__))
	os.chdir(path)
	spx = EquityData('Data/SPX.csv')
	spx.runAll()	

if __name__ == "__main__":
    main()