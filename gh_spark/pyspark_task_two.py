#!/usr/bin/env python

import sys, os, re
import json
import datetime, iso8601

# Pass date and base path to main() from airflow
def main(iso_date, base_path):
  APP_NAME = "pyspark_task_two.py"
  
  import pyspark
  import pyspark.sql
    
  sc = pyspark.SparkContext()
  spark = pyspark.sql.SparkSession(sc).builder.appName(APP_NAME).getOrCreate()

  
  # Get today's date
  today_dt = iso8601.parse_date(iso_date)
  rounded_today = today_dt.date()
  
  # Load today's data
  today_input_path = "{}/gh_spark/data/example_master_titles_daily.json/{}".format(
    base_path,
    rounded_today.isoformat()
  )
  
  # Otherwise load the data and proceed...
  people_master_titles_raw = sc.textFile(today_input_path)
  people_master_titles = people_master_titles_raw.map(json.loads)
  print(people_master_titles.first())

if __name__ == "__main__":
  main(sys.argv[1], sys.argv[2])
