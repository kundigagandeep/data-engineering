from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from airflow.decorators import task
from pathlib import Path
import requests
import pandas as pd
import logging
import yaml
with open('/opt/airflow/dags/config.yml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2022,12,4,2,30),
    'end_date': datetime(2022,12,31),
    'email': ['airflow@airflow.com'],
    }


with DAG('extract_dag', 
        default_args=default_args, 
        schedule_interval='*/15 * * * *', 
        catchup=False) as dag:
    
    @task
    def extract_func():
        url = config['url']

        querystring = {"q":"Warsaw"}

        headers = {
                "X-RapidAPI-Key": config['headers']['X-RapidAPI-Key'],
                "X-RapidAPI-Host": config['headers']['X-RapidAPI-Host']
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        response_json = response.json()

        df = pd.json_normalize(response_json)

        for col in df.columns:
            df.rename(columns={col:col.replace("location.","").replace("current.","")},inplace=True)

        col_name = df['localtime_epoch'][0]

        df.to_csv(f'/opt/airflow/dags/data/01_raw/{col_name}_weather_api.csv',index=False)

        logging.info(f'New weather updated succesfully.')

        p = Path("/opt/airflow/dags/data")

        raw_data_path = p/'01_raw'
        intermediate_data_path = p/'02_intermediate'

        files = list(raw_data_path.iterdir())

        df_main = []
        for i in files:
            df = pd.read_csv(i)
            df_main.append(df)
        df_final = pd.concat(df_main,axis=0)                 
        df_final.to_csv(f'{str(intermediate_data_path)}/weather.csv', index=False)

        logging.info(f'Weather CSV created succesfully.')
    
    def print_now():
        logging.info('WRITING NOW')
        logging.info(datetime.utcnow().isoformat())
        logging.info('TIME WRITTEN')

    print_time_task = PythonOperator(task_id='print_now', python_callable=print_now, dag=dag)

    print_time_task >> [extract_func()]
