from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime.now(),
    'schedule_interval': "*/15 * * * *",
    'email': ['airflow@airflow.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    }

with DAG('extract',
        default_args=default_args) as dag:
        
        task1 = BashOperator(
        task_id='extract_weather_api',
        bash_command='python /Users/gagandeepkundi/data-engineering/projects/weather-etl-ml-project/src/extract.py',
        dag=dag)

        task2 = BashOperator(
        task_id='transform_data',
        bash_command='python /Users/gagandeepkundi/data-engineering/projects/weather-etl-ml-project/src/transform.py',
        dag=dag)

        task1.set_downstream(task2)