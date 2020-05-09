# Databricks notebook source
#dbutils.fs.ls("/toone/day")

#삭제
#dbutils.fs.rmrf("/toone/day")



dbutils.fs.ls("/mnt/tooneadls")

# COMMAND ----------

# MAGIC %md
# MAGIC 
# MAGIC ### dataframe read write

# COMMAND ----------

df.write.format("delta").save("/mnt/delta/events")

# COMMAND ----------

# MAGIC %md
# MAGIC ### table create

# COMMAND ----------

# MAGIC %SQL
# MAGIC CREATE TABLE events (
# MAGIC   date DATE,
# MAGIC   eventId STRING,
# MAGIC   eventType STRING,
# MAGIC   data STRING)
# MAGIC USING DELTA
# MAGIC PARTITIONED BY (date)
# MAGIC LOCATION '/mnt/delta/events'

# COMMAND ----------

# import pyspark class Row from module sql
from pyspark.sql import *

# COMMAND ----------

# 특정컬럼의통계정보
DF.describe("salary").show()

# DF 설명
DF.explain()

# COMMAND ----------

from datetime import datetime, timedelta

time1 = datetime(2018, 7, 13, 21, 40, 5)
time2 = datetime.now()
print(time1) # 2018-07-13 21:40:05
print(time2) # 2018-07-23 20:58:59.666626

print(time2-time1) # 9 days, 23:18:54.666626
print(type(time2-time1)) # <class 'datetime.timedelta'>

# COMMAND ----------

from datetime import datetime, timedelta

print('현재 시간부터 5일 뒤')
print(time2 + timedelta(days=5)) # 2018-07-28 20:58:59.666626
print('현재 시간부터 3일 전')
print(time2 + timedelta(days=-3)) # 2018-07-20 20:58:59.666626
print('현재 시간부터 1일 뒤의 2시간 전')
print(time2 + timedelta(days=1, hours=-2)) #2018-07-24 18:58:59.666626