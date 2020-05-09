# Databricks notebook source
display(dbutils.fs.ls("/mnt/hoadls2"))

# COMMAND ----------

dbutils.fs.rm("/mnt/adls2")

# COMMAND ----------

dbutils.fs.ls("/tmp/hive/root ")

# COMMAND ----------

dbutils.fs.ls("/user/hive/warehouse/")

# COMMAND ----------

# MAGIC %sql
# MAGIC 
# MAGIC --show databases
# MAGIC 
# MAGIC describe database database_hoadls2

# COMMAND ----------

dbutils.fs.mkdirs("/databricks/driver/databricks_import_python_module/")

# COMMAND ----------

display(dbutils.fs.ls("/databricks/driver/"))

# COMMAND ----------

# MAGIC %md 
# MAGIC - copy local file to DBFS
# MAGIC - windows 로컬 환경에서 파일 업로드 시 이슈 사항 발생  
# MAGIC dbutils.fs.cp('file:/E:\databricks\lstm.py', 'dbfs:/databricks/lstm.py')   
# MAGIC 위 형태로 진행시 오류 발생 

# COMMAND ----------

dbutils.fs.cp('dbfs:/mnt/hoadls2/nativepy/lstm.py','dbfs:/databricks/driver/databricks_import_python_module/lstm.py')