# Databricks notebook source
configs = {"fs.azure.account.auth.type": "OAuth",
           "fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
           "fs.azure.account.oauth2.client.id": "d01ceb3f-0905-4814-9c0d-59143170ecab",
           "fs.azure.account.oauth2.client.secret": "Vs7Mt[_Gr1.Imgorn[I22HjZAQw38bCW",
           "fs.azure.account.oauth2.client.endpoint": "https://login.microsoftonline.com/a9c21675-0cc8-4dd7-9818-d531b9ee2486/oauth2/token"}
######################################################################################
# Optionally, you can add <directory-name> to the source URI of your mount point.
######################################################################################
dbutils.fs.mount(
  source = "abfss://toonestock@hotooneadls2.dfs.core.windows.net/",
  mount_point = "/mnt/hoadls2",
  extra_configs = configs)


# COMMAND ----------

dbutils.fs.ls("dbfs:/mnt")

# COMMAND ----------

# read sql data to adls2

jdbcHostname = "tooneserver.database.windows.net"
jdbcDatabase = "toonedatabase"
username = "admin_orange"
password = "!1Zenithncom"
jdbcPort = 1433
jdbcUrl = "jdbc:sqlserver://{0}:{1};database={2}".format(jdbcHostname, jdbcPort, jdbcDatabase)
connectionProperties = {
  "user" : username,
  "password" : password,
  "driver" : "com.microsoft.sqlserver.jdbc.SQLServerDriver"
}

# COMMAND ----------

pushdown_query = "(select * From dbo.toone_stock_day) toonestock"
df = spark.read.jdbc(url=jdbcUrl, table=pushdown_query, properties=connectionProperties)
display(df)

# COMMAND ----------

# table to adls table

df.write.saveAsTable("global_stock")

# COMMAND ----------

df.createOrReplaceTempView("local_stock")

# COMMAND ----------

dbutils.fs.ls("dbfs:/mnt/hoadls2")

# COMMAND ----------

sql_df = spark.sql ("show tables ")
display(sql_df)

# COMMAND ----------

# delta 파일로 save
#df.write.format("delta").save("/mnt/hoadls2/delta_stock")
spark.sql("CREATE TABLE tbl_delta_stock USING DELTA LOCATION '/mnt/adls2/delta_stock'")

# COMMAND ----------

delta_stock = spark.sql("select * From tbl_delta_stock")
display(delta_stock)

# COMMAND ----------

# parquet 파일 쓰기 
df.write.mode("overwrite").parquet("/mnt/hoadls2/parquet")

# COMMAND ----------

# parquet 파일로 테이블 생성 
spark.sql("create table tbl_parquet_stock using parquet options( path '/mnt/hoadls2/parquet')")

# COMMAND ----------

parquet_df = spark.sql("select * From tbl_parquet_stock")
display(parquet_df)

# COMMAND ----------

data = sqlContext.read.parquet("/mnt/hoadls2/parquet")

display(data)

# COMMAND ----------

# avro 파일 쓰기
df.write.mode("overwrite").avro("/tmp/testParquet")

# COMMAND ----------

sql_df = spark.sql ("show tables ")
display(sql_df)

# COMMAND ----------

# MAGIC %sql
# MAGIC 
# MAGIC --show databases
# MAGIC 
# MAGIC --use toonedatabase;
# MAGIC 
# MAGIC --create table tbl_sql ( a int);
# MAGIC 
# MAGIC --show tables;
# MAGIC 
# MAGIC 
# MAGIC --insert into tbl_sql values ( 1 );
# MAGIC 
# MAGIC --select * From tbl_sql

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE formatted delta_stock

# COMMAND ----------

display( spark.sql("DESCRIBE detail delta_stock")) 