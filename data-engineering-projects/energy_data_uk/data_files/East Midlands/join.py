import glob
import os
import pandas as pd  

df = pd.concat(map(pd.read_csv, glob.glob(os.path.join('', "*.csv"))))

#df.to_csv("/Users/gagandeepkundi/Education/data-engineering/data-engineering-projects/energy_data_uk/data_files/East Midlands/east_midlands.csv", index=False)