import sys, os, re
import airflow
from airflow import DAG
from airflow.operators.bash_operator import BashOperator

from datetime import datetime, timedelta
import iso8601


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date' : iso8601.parse_date("2016-12-01"),
}

dag = DAG('GH_spark', default_args = default_args, schedule_interval = None)

pyspark_local_task_one = BashOperator(
    task_id = "pyspark_local_task_one",
    bash_command = """ spark-submit --master {{ params.master }} {{params.base_path}}/{{params.filename}} {{ts}} {{params.base_path}}""",
    params = {
        "master": "local[8]",
        "filename": "gh_spark/pyspark_task_one.py",
        "base_path": "/home/ec2-user/airflow/dags"},
    dag=dag)

pyspark_local_task_two = BashOperator(
    task_id = "pyspark_local_task_two", 
    bash_command = """ spark-submit --master {{params.master}} {{params.base_path}}/{{params.filename}} {{ts}} {{params.base_path}}""",
    params = {
        "master": "local[8]",
        "filename": "gh_spark/pyspark_task_two.py",
        "base_path": "/home/ec2-user/airflow/dags"},
    dag=dag)

pyspark_local_task_two.set_upstream(pyspark_local_task_one)
