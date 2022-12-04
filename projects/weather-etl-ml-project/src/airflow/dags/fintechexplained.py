import os
from datetime import datetime
import requests
from airflow import DAG
from airflow.decorators import task
import logging

from airflow.operators.python import PythonOperator

with DAG('fintechexplained', description='BlogExampleFinTechExplained',
          schedule_interval='0 */2 * * *',
          start_date=datetime(2022, 8, 18), catchup=False) as dag:


    @task
    def custom_get_contents_then_save_task():
        data_path = f"/opt/airflow/dags/data{datetime.now()}.csv"
        logging.info('Write Dir')
        os.makedirs(os.path.dirname(data_path), exist_ok=True)
        logging.info(f'File={data_path}')

        url = "https://raw.githubusercontent.com/apache/airflow/main/docs/apache-airflow/pipeline_example.csv"

        response = requests.request("GET", url)

        with open(data_path, "w") as file:
            file.write(response.text)

        logging.info(f'Data written to File={data_path}')


    def print_now():
        logging.info('WRITING NOW')
        logging.info(datetime.utcnow().isoformat())
        logging.info('TIME WRITTEN')

    print_time_task = PythonOperator(task_id='print_now', python_callable=print_now, dag=dag)

    print_time_task >> custom_get_contents_then_save_task()