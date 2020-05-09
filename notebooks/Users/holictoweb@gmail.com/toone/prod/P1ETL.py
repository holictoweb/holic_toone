# Databricks notebook source
# MAGIC %md
# MAGIC ### 입력 데이터 확인 (avro, parquet)

# COMMAND ----------

dbutils.fs.ls("/mnt/tooneadls/rdata")

# COMMAND ----------

# MAGIC %sql 
# MAGIC     CREATE TEMPORARY TABLE raw_chart_day_avro
# MAGIC     USING avro
# MAGIC     OPTIONS (
# MAGIC       path "/mnt/tooneadls/rdata/dbo.toone_chart_day.avro"
# MAGIC     )

# COMMAND ----------

# MAGIC %sql 
# MAGIC     CREATE TEMPORARY TABLE raw_chart_day_parquet
# MAGIC     USING parquet
# MAGIC     OPTIONS (
# MAGIC       path "/mnt/tooneadls/rdata/dbo.toone_chart_day.parquet"
# MAGIC     )

# COMMAND ----------

# MAGIC %sql
# MAGIC select  * From raw_chart_day_parquet
# MAGIC where date >= '20200227'
# MAGIC limit 10

# COMMAND ----------

#rdata_df = sqlContext.read.parquet("/mnt/tooneadls/rdata/dbo.toone_chart_day.parquet")

rdata_df= spark.read.format("avro").load("/mnt/tooneadls/rdata/dbo.toone_chart_day.avro")
  
  
#display(rdata_df.order)

avro_df = spark.read.format("avro").load("/mnt/tooneadls/rdata/dbo.toone_chart_day.avro")
avro_df.where("Date >= '20200202'").show(10)
#spark.read.format("avro").load("/mnt/tooneadls/rdata/dbo.toone_chart_day.avro").where("Date == '20200202'").show()

# COMMAND ----------


rdata_parquet_df= spark.read.format("parquet").load("/mnt/tooneadls/rdata/dbo.toone_chart_day.parquet")
  
rdata_parquet_df.printSchema()
#display(rdata_parquet_df)

#rdata_parquet_df.where("Date=='20200227'").show(10)

# COMMAND ----------

# MAGIC %md
# MAGIC ### 오늘 날짜로 데이터 분할

# COMMAND ----------

import pandas as pd
import datetime

today = datetime.datetime.now()
#today = dt.strftime('%Y%m%d')
yesterday = today + datetime.timedelta(days=-5)  

basedt = yesterday.strftime('%Y%m%d')
print(basedt)

# COMMAND ----------

# MAGIC %md
# MAGIC ### 일자별로 day chart를 구성

# COMMAND ----------

# Creates a DataFrame from a specified directorytime.strftime('%c', time.localtime(time.time()))
df = spark.read.format("avro").load("/mnt/tooneadls/rdata/dbo.toone_chart_day.avro")
#df.head()
#df.explain()

#  Saves the subset of the Avro records read in
subset_df = df.where("Date >= '" + basedt + "'" )
subset_df.write.format("avro").mode("append").save("/mnt/tooneadls/qchart/"+ basedt +"/")

#subset_df.show()

# COMMAND ----------

# MAGIC %md
# MAGIC ### 특정 폴더 하위에 있는 파일 정보 읽기

# COMMAND ----------

# 단일 디렉토리 및에 있는 파일을 읽는것은 가능. 
df = spark.read.format("avro").load("/mnt/tooneadls/qchart/*/")
df.count()

# COMMAND ----------

# MAGIC %md
# MAGIC ### 특정 폴더 하위의 정보를 모두 읽는 table 생성

# COMMAND ----------

# MAGIC %sql 
# MAGIC     CREATE TABLE toone_qchart_day
# MAGIC     USING avro
# MAGIC     OPTIONS (
# MAGIC       path "/mnt/tooneadls/qchart/*/"
# MAGIC     )

# COMMAND ----------

# MAGIC %sql
# MAGIC REFRESH TABLE toone_qchart_day

# COMMAND ----------

# MAGIC %sql
# MAGIC select count(*) From toone_qchart_day

# COMMAND ----------

# MAGIC %md
# MAGIC ### 각 코드별로 폴더 구성 생성

# COMMAND ----------

# Creates a DataFrame from a specified directorytime.strftime('%c', time.localtime(time.time()))
parquet_df = spark.read.format("parquet").load("/mnt/tooneadls/chartdata/dbo.toone_chart_day.parquet")


code_df = parquet_df.select("Code")
print(code_df)

'''
#P2 중복 데이터 제거 
target_code_list = code_df.drop_duplicates()
#result_df = source_df.drop_duplicates(keep='last')

print(target_code_list.head())
'''

# COMMAND ----------

for row in target_code_list:
  print(row)
  #dbutils.fs.mkdir("/mnt/tooneadls/qchart/"+row)
  #code_df = parquet_df.where("Code = " + str(row) )
  #code_df.write.saveAsTable("toone_chart_by_code_" + row)
  
  #dataframe.write.mode("overwrite").option("path","<your-s3-path>").saveAsTable("<example-table>") 

# COMMAND ----------

diamonds = spark.sql("select * from diamonds")
display(diamonds.select("*"))

# COMMAND ----------

# MAGIC %sql
# MAGIC select * From toone_chart_day_parquet

# COMMAND ----------

# Creates a DataFrame from a specified directorytime.strftime('%c', time.localtime(time.time()))
df = spark.read.format("parquet").load("/mnt/tooneadls/chartdata/dbo.toone_chart_day.parquet")
df.head()
pd_df = df.toPandas()
code_df = pd_df.groupby("Code")

print(code_df.head())


# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TEMPORARY VIEW toone_chart_day_20200403
# MAGIC USING avro
# MAGIC OPTIONS (path "/mnt/tooneadls/day/20200403/output")

# COMMAND ----------

# MAGIC %sql 
# MAGIC select * From toone_chart_day_20200404

# COMMAND ----------

dbutils.fs.ls("/tmp/output")


# COMMAND ----------

