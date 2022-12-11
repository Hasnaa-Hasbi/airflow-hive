from datetime import timedelta
from _datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
import yfinance as yf
import pandas as pd
from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
from pyspark.sql import SQLContext
import streamlit as st
import os
import sys

os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable

# Connecting to hive with spark
conf = SparkConf()  # Declare spark conf variable\
sc = SparkContext.getOrCreate(conf=conf)
spark = SparkSession(sc).builder.appName("Read-and-write-data-to-Hive-table-spark")\
    .config("hive.metastore.uris","thrift://airflow-hive-hive-metastore-1:9083")\
    .enableHiveSupport().getOrCreate()


# Initial Tickers List. It will be available globally for all functions.
tickers = ['AAPL', 'AMZN', 'BLK', 'T', 'TSLA'] 

def extract_transform(**kwargs):
    print('1 Fetching stock prices and remove duplicates...')
    stocks_prices = []
    for i in range(0, len(tickers)):
        prices = yf.download(tickers[i], period = 'max').iloc[: , :5].dropna(axis=0, how='any')
        prices = prices.loc[~prices.index.duplicated(keep='last')]
        prices = prices.reset_index()
        prices.insert(loc = 1, column = 'Stock', value = tickers[i])
        stocks_prices.append(prices)
    print('Completed \n\n')
    return stocks_prices
    # <-- This list is the output of the fetch_prices_function and the input for the functions below



def load(**kwargs):
    print("Task for loading data in hive")
    ti = kwargs['ti']
    stocks_prices = ti.xcom_pull(task_ids='fetch_prices_task')
    # # <-- xcom_pull is used to pull the stocks_prices list generated above
    stock_data = pd.concat(stocks_prices, ignore_index = True)
    #
    # Infer the schema, and register the DataFrame as a table.
    schemaStocks = spark.createDataFrame(stock_data)
    schemaStocks.registerTempTable("stocks")
    tables = spark.sql("show tables")
    tables.show()

    data = spark.sql("select * from stocks")
    print(data.show())



def traitementIndicators():
    print("Technical Indicators with Spark SQL")
    data = spark.sql("select * from stocks")

    print("Decsription du contenu de la table")
    print(data.describe())

    #Count of each stock
    data.groupBy("Stock").count().show()

    ##### MACD INDICATOR
    exp1 = data.Close.ewm(span=12, adjust=False).mean()
    exp2 = data.Close.ewm(span=26, adjust=False).mean()
    data['MACD'] = exp1 - exp2
    data['Signal line'] = data.MACD.ewm(span=9, adjust=False).mean()
    print(data.show())
    #Visualize with matplotlib
    fig, ax = plt.subplots()
    data[['MACD', 'Signal line']].plot(ax=ax)
    data.Close.plot(ax=ax, alpha=0.25, secondary_y=True)

    # Calculating Simple Moving Average (SMA)
    df_C = spark.sql("select Close from stocks")
    df_C['SMA30'] = df_C.rolling(30).mean()
    # removing all the NULL values using
    df_C.dropna(inplace=True)
    print(df_C.show())

    # Cumulative Moving Average (CMA)
    df_cum = data['Close'].to_frame()
    df_cum['CMA30'] = df_cum['Close'].expanding().mean()
    print(df_cum.show())


default_args = {'owner': 'airflow',
                'depends_on_past': False,
                'start_date': datetime.utcnow() - timedelta(minutes=10),
                'email_on_failure': False,
                'email_on_retry': False,
                'retries': 1,
                'retry_delay': timedelta(minutes=5),
                'schedule_interval': '@daily',
                'concurrency': 1,
                'max_active_runs': 1,
                'catchup ': False
}

dag = DAG(dag_id='dag_for_yahoo_data', default_args=default_args)
    

extract_transform_data = PythonOperator(task_id = 'extract_data', python_callable = extract_transform, dag=dag)
load_data = PythonOperator(task_id = 'load_data', python_callable = load, dag=dag)
trait_data = PythonOperator(task_id = 'trait_data', python_callable = traitementIndicators, dag=dag)
vis_data = BashOperator(task_id = 'vis_data', bash_command="streamlit run vis.py", dag=dag)

extract_transform_data >> load_data >> trait_data >> vis_data

