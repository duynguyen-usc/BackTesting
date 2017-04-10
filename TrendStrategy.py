import os
from EquityData import EquityData

def main():
	path = os.path.dirname(os.path.realpath(__file__))
	os.chdir(path)
	
	spx = EquityData('Data/SPX.csv')
	print(spx.toString())
	

if __name__ == "__main__":
    main()

