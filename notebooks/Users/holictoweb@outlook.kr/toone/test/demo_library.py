# Databricks notebook source
# MAGIC %fs ls

# COMMAND ----------

dbutils.fs.mkdirs("/mnt/")

# COMMAND ----------

dbutils.fs.mkdirs("/foobar/")

# COMMAND ----------

display(dbutils.fs.ls("dbfs:/databricks-datasets"))

# COMMAND ----------

dbutils.library.installPyPI("scikit-learn")

# COMMAND ----------

dbutils.library.restartPython()

# COMMAND ----------

