import requests
import pandas as pd

url = "https://weatherapi-com.p.rapidapi.com/current.json"

querystring = {"q":"Warsaw"}

headers = {
        "X-RapidAPI-Key": "24eeab2ba1mshe19cfdccdd89090p1e1cc3jsnf0935a53f711",
        "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)

response_json = response.json()

df = pd.json_normalize(response_json)

for col in df.columns:
    df.rename(columns={col:col.replace("location.","").replace("current.","")},inplace=True)

col_name = df['localtime_epoch'][0]

df.to_csv(f'/Users/gagandeepkundi/data-engineering/projects/weather-etl-ml-project/data/01_raw/{col_name}_weather_api.csv',index=False)