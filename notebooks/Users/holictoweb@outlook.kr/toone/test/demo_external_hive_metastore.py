# Databricks notebook source
# MAGIC %md # local 모드로 ui 상에서 수행 

# COMMAND ----------



# JDBC connect string for a JDBC metastore
javax.jdo.option.ConnectionURL jdbc:mysql://<metastore-host>:<metastore-port>/<metastore-db>

# Username to use against metastore database
javax.jdo.option.ConnectionUserName <mysql-username>

# Password to use against metastore database
javax.jdo.option.ConnectionPassword <mysql-password>

# Driver class name for a JDBC metastore (Runtime 3.4 and later)
javax.jdo.option.ConnectionDriverName org.mariadb.jdbc.Driver

# Driver class name for a JDBC metastore (prior to Runtime 3.4)
# javax.jdo.option.ConnectionDriverName com.mysql.jdbc.Driver

# COMMAND ----------

# MAGIC %md # 테스트 불가
# MAGIC 정상 동작 방법을 확인 하지 못함. 
# MAGIC init script 구성 후에 오류 발생. ( SQl database로 테스트 ) 

# COMMAND ----------

# MAGIC %sql 
# MAGIC 
# MAGIC show databases

# COMMAND ----------

dbutils.fs.ls("/databricks/init")

# COMMAND ----------

dbutils.fs.rm("dbfs:/databricks", True)

# COMMAND ----------

# MAGIC %md
# MAGIC HDInsight를 통해 metastore로 사용한 SQL Database를 사용 하는 방법 

# COMMAND ----------

dbutils.fs.mkdirs("dbfs:/databricks/init/")

# COMMAND ----------

# MAGIC %scala
# MAGIC 
# MAGIC dbutils.fs.put(
# MAGIC     "/databricks/init/external-metastore.sh",
# MAGIC     """#!/bin/sh
# MAGIC       |# Loads environment variables to determine the correct JDBC driver to use.
# MAGIC       |source /etc/environment
# MAGIC       |# Quoting the label (i.e. EOF) with single quotes to disable variable interpolation.
# MAGIC       |cat << 'EOF' > /databricks/driver/conf/00-custom-spark.conf
# MAGIC       |[driver] {
# MAGIC       |    # Hive specific configuration options for metastores in the local mode.
# MAGIC       |    "spark.hadoop.javax.jdo.option.ConnectionURL" = "jdbc:sqlserver://zchosqlserver.database.windows.net:1433;database=hivemetastore;encrypt=true;trustServerCertificate=true;create=false;loginTimeout=300"
# MAGIC       |    "spark.hadoop.javax.jdo.option.ConnectionUserName" = "admin_orange"
# MAGIC       |    "spark.hadoop.javax.jdo.option.ConnectionPassword" = "!1Zenithncom"
# MAGIC       |    "hive.metastore.schema.verification.record.version" = "true"
# MAGIC       |    "spark.sql.hive.metastore.jars" = "maven"
# MAGIC       |    "hive.metastore.schema.verification" = "true"
# MAGIC       |    "spark.sql.hive.metastore.version" = "1.1.0"
# MAGIC       |EOF
# MAGIC       |# Add the JDBC driver separately since must use variable expansion to choose the correct
# MAGIC       |# driver version.
# MAGIC       |cat << EOF >> /databricks/driver/conf/00-custom-spark.conf
# MAGIC       |    "spark.hadoop.javax.jdo.option.ConnectionDriverName" = "com.microsoft.sqlserver.jdbc.SQLServerDriver"
# MAGIC       |}
# MAGIC       |EOF
# MAGIC       |""".stripMargin,
# MAGIC     overwrite = true
# MAGIC )

# COMMAND ----------

# MAGIC %sql
# MAGIC 
# MAGIC show tables

# COMMAND ----------

# MAGIC %md # test MS guide
# MAGIC 
# MAGIC https://kb.databricks.com/_static/notebooks/metastore/external-metastore-hive-2.1.1.html