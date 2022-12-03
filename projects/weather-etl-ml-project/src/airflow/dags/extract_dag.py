from airflow import DAG
from airflow.operators.bash import BashOperator
#from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
#from includes import extract_func, transform_func


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2022,12,2,20,15),
    'schedule_interval':timedelta(minutes=15),
    'email': ['airflow@airflow.com'],
    }

with DAG('extract_dag',
        default_args=default_args) as dag:
        
        task1 = BashOperator(
        task_id='extract_weather_api',
        bash_command="ls",
        dag=dag)

        # task2 = BashOperator(
        # task_id='transform_data',
        # bash_command="python includes/transform.py")

        # task1.set_downstream(task2)