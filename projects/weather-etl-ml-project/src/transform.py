from pathlib import Path
import pandas as pd

p = Path("/Users/gagandeepkundi/data-engineering/projects/weather-etl-ml-project")

raw_data_path = p/'data/01_raw'
intermediate_data_path = p/'data/02_intermediate'

files = list(raw_data_path.iterdir())

df_main = []
for i in files:
    df = pd.read_csv(i)
    df_main.append(df)
df_final = pd.concat(df_main,axis=0)                 
df_final.to_csv(f'{str(intermediate_data_path)}/weather.csv', index=False)