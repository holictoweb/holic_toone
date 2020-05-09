# Databricks notebook source
df = spark.read.json("/databricks-datasets/samples/people/people.json")

# COMMAND ----------

# MAGIC %fs ls

# COMMAND ----------

dbutils.fs.ls("/user/hive/warehouse/stock_chart_day")

# COMMAND ----------

dbutils.fs.ls("/mnt/tooneadls")

# COMMAND ----------

dbutils.library.installPyPI("torch")
dbutils.library.installPyPI("scikit-learn")
dbutils.library.installPyPI("azureml-sdk", version="1.0.8", extras="databricks")
dbutils.library.restartPython() # 특정 라이브러리는 리스타트 필요



# COMMAND ----------

import torch
from sklearn.linear_model import LinearRegression
import azureml
# do the actual wor

# COMMAND ----------

dbutils.library.list()

# COMMAND ----------

df = spark.read.json("/databricks-datasets/samples/people/people.json")

# 전역 테이블 생성

df.write.saveAsTable("toone_python_table")

df.createOrReplaceTempView("toone_python_table_02")

# COMMAND ----------

diamonds = spark.sql("select * from toone_python_table")
display(diamonds.select("*"))

# COMMAND ----------

# azure data lake gen2 mount 되어 있는 avro 파일 읽기
dbutils.fs.ls("/mnt/tooneadls")

# Creates a DataFrame from a specified directory
df = spark.read.format("avro").load("/mnt/tooneadls/dbo.toone_stock_day.avro")

print(df.head(10))

