# Databricks notebook source
'''
from pyspark import SparkContext, SparkConf, SQLContext
from pyspark.sql import SparkSession
from pyspark.sql import *
from pyspark.dbutils import DBUtils
'''


import pandas as pd

# COMMAND ----------


# session 생성
#spark = SparkSession.builder.getOrCreate()


# data lake gen2 에 있는 파일 확인 
#dbutils = DBUtils(spark)
#print ( dbutils.fs.ls("/mnt/tooneadls") ) 


spark_df = spark.read.format("avro").load("/mnt/tooneadls/dbo.toone_stock_day.avro")
print (spark_df)

df = spark_df.select("*").toPandas()
print( df.head() ) 


df['sma5'] = df['close'].rolling(5).mean()
df['sma20'] = df['close'].rolling(20).mean()
df['sma100'] = df['close'].rolling(100).mean()
df['sma200'] = df['close'].rolling(200).mean()
print( df.head() ) 

# COMMAND ----------

# 전역 테이블 생성 ( saveAsTable 은 관리형 테이블로 실제 데이터도 함께 저장 ) 
spark_df.write.saveAsTable("stock_chart_day")

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from stock_chart_day

# COMMAND ----------

spark_df.write.option("path", "/mnt/tooneadls").saveAsTable("stock_chart_day_adls2")

# COMMAND ----------

# data preprocessing

# https://wikidocs.net/16582