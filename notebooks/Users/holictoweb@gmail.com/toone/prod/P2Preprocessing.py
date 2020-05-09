# Databricks notebook source
import numpy as np
import pandas as pd


# COMMAND ----------

# MAGIC %md 
# MAGIC #### 1. 학습 데이터 준비

# COMMAND ----------

# MAGIC %md
# MAGIC #### 1.1 data load

# COMMAND ----------

# 단일 디렉토리 및에 있는 파일을 읽는것은 가능. 
#chart_df = spark.read.format("avro").load("/mnt/tooneadls/qchart/*/")

# 전체 데이터 로드로 진행 
chart_df = spark.read.format("parquet").load("/mnt/tooneadls/rchart/dbo.toone_chart_day.parquet")

chart_df.count()

# COMMAND ----------

# MAGIC %md
# MAGIC #### 1.1.1 data 를 table로 저장
# MAGIC 각 코드 별로 데이터 처리가 필요 

# COMMAND ----------

# MAGIC %sql
# MAGIC 
# MAGIC create table toone_chart_day_raw
# MAGIC using parquet
# MAGIC OPTIONS (
# MAGIC       path "/mnt/tooneadls/rchart/dbo.toone_chart_day.parquet"
# MAGIC     )
# MAGIC     
# MAGIC   

# COMMAND ----------

# MAGIC %sql
# MAGIC /*
# MAGIC select * 
# MAGIC from toone_chart_day_raw
# MAGIC group by Code
# MAGIC 
# MAGIC */

# COMMAND ----------

# MAGIC %md
# MAGIC #### 1.2 null, 중복 데이터 제거 

# COMMAND ----------

# 중복 데이터 제거 
training_DF = chart_df.drop_duplicates()
#result_df = source_df.drop_duplicates(keep='last')

training_df = training_DF.toPandas()
#result_pdf = df.select("*").toPandas()

# COMMAND ----------

from pyspark.sql.functions import monotonically_increasing_id
  

df_index = df.select("*").withColumn("id", monotonically_increasing_id())

# COMMAND ----------

# MAGIC %md 
# MAGIC #### 1.3 형변환

# COMMAND ----------

training_df[["Close", "Open", "High", "Low", "Volume"]] = training_df[["Close", "Open", "High", "Low", "Volume"]].apply(pd.to_numeric)

#training_df.head()
training_df.dtypes


# COMMAND ----------

# MAGIC %md
# MAGIC #### 2. Feature 생성 (각 코드별로 생성 필요 )

# COMMAND ----------

# MAGIC %md 
# MAGIC #### 2.1 코드별로 연산을 진행 하기 위한 방법 필요 

# COMMAND ----------

training_data = training_df


training_data.groupby("code")

# COMMAND ----------

# training_data = training_df

training_data['open_lastclose_ratio'] = np.zeros(len(training_data))
training_data.loc[1:, 'open_lastclose_ratio'] = (training_data['Open'][1:].values - training_data['Close'][:-1].values) /  training_data['Close'][:-1].values
training_data['high_close_ratio'] =  (training_data['High'].values - training_data['Close'].values) / training_data['Close'].values
training_data['low_close_ratio'] =  (training_data['Low'].values - training_data['Close'].values) /  training_data['Close'].values
training_data['close_lastclose_ratio'] = np.zeros(len(training_data))
training_data.loc[1:, 'close_lastclose_ratio'] =  (training_data['Close'][1:].values - training_data['Close'][:-1].values) / training_data['Close'][:-1].values
training_data['volume_lastvolume_ratio'] = np.zeros(len(training_data))
training_data.loc[1:, 'volume_lastvolume_ratio'] =  (training_data['Volume'][1:].values - training_data['Volume'][:-1].values) / training_data['Volume'][:-1]\
        .replace(to_replace=0, method='ffill') \
        .replace(to_replace=0, method='bfill').values

# COMMAND ----------

training_data.head()

# COMMAND ----------

windows = [5, 10, 20, 60, 120]
for window in windows:
  training_data['close_ma%d_ratio' % window] = (training_data['Close'] - training_data['close_ma%d' % window]) / training_data['close_ma%d' % window]
  training_data['volume_ma%d_ratio' % window] = (training_data['Volume'] - training_data['volume_ma%d' % window]) /  training_data['volume_ma%d' % window]

# COMMAND ----------

import datetime

dt = datetime.datetime.now()
print(dt)

print(dt.strftime("%H시 %M분 %S초"))

print(dt.strftime('%Y%m%d'))


# COMMAND ----------

pd.read_csv (os.path.join (INPUT_PATH