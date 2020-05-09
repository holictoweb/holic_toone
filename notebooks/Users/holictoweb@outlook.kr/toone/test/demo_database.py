# Databricks notebook source
# MAGIC %sql
# MAGIC 
# MAGIC show databases

# COMMAND ----------

# MAGIC %sql
# MAGIC 
# MAGIC describe database toonedatabase

# COMMAND ----------

dbutils.fs.ls("dbfs:/mnt/hoadls2")

# COMMAND ----------

# MAGIC %sql
# MAGIC --데이터 베이스 생성
# MAGIC 
# MAGIC CREATE DATABASE database_hoadls2
# MAGIC   COMMENT 'create on azure data lake gen2 '
# MAGIC   LOCATION 'dbfs:/mnt/hoadls2'

# COMMAND ----------

# MAGIC %sql
# MAGIC 
# MAGIC CREATE TABLE tbl_delta_stock_hoadls2 USING DELTA LOCATION '/mnt/adls2/delta_stock'

# COMMAND ----------

# MAGIC %sql
# MAGIC /*
# MAGIC show tables
# MAGIC describe deetail tbl_delta_stock_hoadls2
# MAGIC */
# MAGIC 
# MAGIC 
# MAGIC describe detail tbl_delta_stock_hoadls2

# COMMAND ----------

sql_df = spark.sql ("show tables ")
display(sql_df)

# COMMAND ----------

# MAGIC %sql 
# MAGIC 
# MAGIC show databases

# COMMAND ----------

# MAGIC %sql
# MAGIC use default;
# MAGIC show tables;

# COMMAND ----------

# MAGIC %sql
# MAGIC --DESCRIBE formatted delta_stock;
# MAGIC DESCRIBE detail delta_stock;

# COMMAND ----------

# MAGIC %sql
# MAGIC --통계 생성
# MAGIC 
# MAGIC ANALYZE TABLE delta_stock COMPUTE STATISTICS NOSCAN

# COMMAND ----------

# MAGIC %sql 
# MAGIC 
# MAGIC select * From delta_stock