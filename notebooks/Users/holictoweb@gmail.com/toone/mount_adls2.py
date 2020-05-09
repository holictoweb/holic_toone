# Databricks notebook source
dbutils.fs.ls("/mnt/tooneadls")

# COMMAND ----------

dbutils.fs.ls("/mnt/tooneadls")

# COMMAND ----------

dbutils.fs.mkdirs("/mnt/chartdata")

# COMMAND ----------

configs = {"fs.azure.account.auth.type": "OAuth",
           "fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
           "fs.azure.account.oauth2.client.id": "ffef840e-e8fe-442a-acc9-29eec41030f9",
           "fs.azure.account.oauth2.client.secret": "D@:xOFq2W5?8gQV2QChgUk-aF5??Lt94",
           "fs.azure.account.oauth2.client.endpoint": "https://login.microsoftonline.com/fa104665-7f2e-427b-b922-11d544911021/oauth2/token"}

dbutils.fs.mount(
  source = "abfss://toonecontainer@tooneadls.dfs.core.windows.net/",
  mount_point = "/mnt/tooneadls",
  extra_configs = configs)