# Databricks notebook source
import sklearn 
from keras.models import Sequential
from keras.layers import Activation, LSTM, Dense, BatchNormalization
from keras.optimizers import sgd
import tensorflow as tf


import pandas as pd
import numpy as np


# COMMAND ----------

# MAGIC %md 
# MAGIC # databricks (spark) 관련 setting

# COMMAND ----------


# Enable Arrow-based columnar data transfers
# docs.databricks.com/spark/latest/spark-sql/spark-pandas.html
spark.conf.set("spark.sql.execution.arrow.enabled", "true")

# COMMAND ----------

# MAGIC %md # sql server에서 data를 읽어서 delta and parquet 파일로 저장
# MAGIC 
# MAGIC JDBC를 이용하여 SQL 연결 
# MAGIC https://docs.microsoft.com/en-us/azure/databricks/data/data-sources/sql-databases

# COMMAND ----------


jdbcHostname = "tooneserver.database.windows.net"
jdbcDatabase = "toonedatabase"
jdbcUsername = "admin_orange"
jdbcPassword  = "!1Zenithncom"
jdbcPort = 1433
jdbcUrl = "jdbc:sqlserver://{0}:{1};database={2}".format(jdbcHostname, jdbcPort, jdbcDatabase)
connectionProperties = {
  "user" : jdbcUsername,
  "password" : jdbcPassword,
  "driver" : "com.microsoft.sqlserver.jdbc.SQLServerDriver"
}

# COMMAND ----------

pushdown_query = "(select * from dbo.toone_stock_day) stock"
df = spark.read.jdbc(url=jdbcUrl, table=pushdown_query, properties=connectionProperties)
display(df)

# COMMAND ----------

# MAGIC %md 
# MAGIC # DB로 부터 읽은 데이터를 parquet 형태로 저장 

# COMMAND ----------

# parquet 파일 쓰기 
 
# 기존에 있던 파일의 데이터와 다르게 생성된 데이터를 입력 하는 방법 
# 기본적으로 parquet 파일은 append가 안되는 것으로 보임 overwrite 의 기능이 기존 데이터 비교하여 input 하는지는 확인 필요 

df.write.mode("overwrite").parquet("/mnt/hoadls2/chart_day/chart_data")

# COMMAND ----------

parquet_df = sqlContext.read.parquet("/mnt/hoadls2/chart_day/chart_data")

display(parquet_df)

# COMMAND ----------

# MAGIC %md 
# MAGIC # preprocessing ( pandas )
# MAGIC 읽어 들인 데이터에 대한 처리 후 parquet 파일로 저장 
# MAGIC 
# MAGIC 
# MAGIC import numpy as np 
# MAGIC import pandas as pd
# MAGIC 
# MAGIC spark.conf.set("spark.sql.execution.arrow.enabled", "true")
# MAGIC 
# MAGIC pdf = pd.DataFrame(np.random.rand(100, 3))
# MAGIC 
# MAGIC df = spark.createDataFrame(pdf)
# MAGIC 
# MAGIC result_pdf = df.select("*").toPandas()

# COMMAND ----------

parquet_df = sqlContext.read.parquet("/mnt/hoadls2/chart_day/chart_data")
print (parquet_df.printSchema())

# COMMAND ----------

#training_data = parquet_df.select("*").to_Pandas()
char_data = parquet_df.toPandas()

prep_data = char_data
windows = [5, 10, 20, 60, 120]
for window in windows:
    prep_data['close_ma{}'.format(window)] = prep_data['close'].rolling(window).mean()
    prep_data['volume_ma{}'.format(window)] = ( prep_data['volume'].rolling(window).mean())

training_data = prep_data
training_data['open_lastclose_ratio'] = np.zeros(len(training_data))
training_data.loc[1:, 'open_lastclose_ratio'] = (training_data['open'][1:].values - training_data['close'][:-1].values) / training_data['close'][:-1].values
training_data['high_close_ratio'] = (training_data['high'].values - training_data['close'].values) / training_data['close'].values
training_data['low_close_ratio'] = (training_data['low'].values - training_data['close'].values) / training_data['close'].values
training_data['close_lastclose_ratio'] = np.zeros(len(training_data))
training_data.loc[1:, 'close_lastclose_ratio'] = (training_data['close'][1:].values - training_data['close'][:-1].values) / training_data['close'][:-1].values
training_data['volume_lastvolume_ratio'] = np.zeros(len(training_data))
training_data.loc[1:, 'volume_lastvolume_ratio'] = (training_data['volume'][1:].values - training_data['volume'][:-1].values) / training_data['volume'][:-1]\
            .replace(to_replace=0, method='ffill') \
            .replace(to_replace=0, method='bfill').values

windows = [5, 10, 20, 60, 120]
for window in windows:
    training_data['close_ma%d_ratio' % window] = (training_data['close'] - training_data['close_ma%d' % window]) / training_data['close_ma%d' % window]
    training_data['volume_ma%d_ratio' % window] = (training_data['volume'] - training_data['volume_ma%d' % window]) / training_data['volume_ma%d' % window]

display( training_data.head(100) )

# COMMAND ----------

# MAGIC %md 
# MAGIC preprocessing data를 다시 parquet 파일로 저장 

# COMMAND ----------

preprocessing_data = spark.createDataFrame(training_data)

preprocessing_data.write.mode("overwrite").parquet("/mnt/hoadls2/chart_day/training_data")

# COMMAND ----------

check_preprocessing_data = sqlContext.read.parquet("/mnt/hoadls2/chart_day/training_data")
display(check_preprocessing_data)



# COMMAND ----------

check_raw_data = sqlContext.read.parquet("/mnt/hoadls2/chart_day/chart_data")
display(check_raw_data)

# COMMAND ----------

# MAGIC %md avro 파일로 쓰기
# MAGIC 
# MAGIC https://docs.microsoft.com/ko-kr/azure/databricks/_static/notebooks/read-avro-files.html

# COMMAND ----------

check_preprocessing_data.write.mode("overwrite").format("avro").save("/mnt/hoadls2/chart_day/temp")

# COMMAND ----------

# MAGIC %sql
# MAGIC     CREATE TEMPORARY TABLE avroTable
# MAGIC     USING avro
# MAGIC     OPTIONS (
# MAGIC       path "/mnt/hoadls2/chart_day/temp"
# MAGIC     )

# COMMAND ----------

# MAGIC %md 각 코드 별로 데이터 저장 

# COMMAND ----------

df.groupby(['Animal']).mean()
        

# COMMAND ----------

# MAGIC %md # LSTM 학습

# COMMAND ----------

input_dim = 0
output_dim = 0

# LSTM 신경망
model = Sequential()

model.add(LSTM(256, input_shape=(1, input_dim), return_sequences=True, stateful=False, dropout=0.5))
model.add(BatchNormalization())
model.add(LSTM(256, return_sequences=True, stateful=False, dropout=0.5))
model.add(BatchNormalization())
model.add(LSTM(256, return_sequences=False, stateful=False, dropout=0.5))
model.add(BatchNormalization())
model.add(Dense(output_dim))
model.add(Activation('sigmoid'))

model.compile(optimizer=sgd(lr=lr), loss='mse')
prob = None



# COMMAND ----------

# 특정 Database를 지정하여 table 생성 
# dataframe.write.option('path', "<your-storage-path>").saveAsTable("<example-table>")

# dataframe.write.mode("overwrite").saveAsTable("<example-table>") // Managed Overwrite
# dataframe.write.mode("overwrite").option("path","<your-s3-path>").saveAsTable("<example-table>")  // Unmanaged Overwrite

df.write.mode("overwrite").saveAsTable("toonedatabase.toone_stock_day")


# COMMAND ----------

# MAGIC %sql
# MAGIC 
# MAGIC describe detail toonedatabase.toone_stock_day