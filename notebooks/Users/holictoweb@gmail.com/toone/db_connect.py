# Databricks notebook source
# MAGIC %scala
# MAGIC 
# MAGIC lass.forName("org.mariadb.jdbc.Driver") // |DBR| 3.4 and above
# MAGIC Class.forName("com.mysql.jdbc.Driver") // |DBR| 3.3 and below

# COMMAND ----------

# my sql connect 
#url ="jdbc:mysql://zcmysql.mysql.database.azure.com:3306/{your_database}?useSSL=true&requireSSL=false"; myDbConn = DriverManager.getConnection(url, "admin_orange@zcmysql", "!1Zenithncom");

#cnx = mysql.connector.connect(user="admin_orange@zcmysql", password={your_password}, host="zcmysql.mysql.database.azure.com", port=3306, database={your_database}, ssl_ca={ca-cert filename}, ssl_verify_cert=true)


jdbcHostname = "zcmysql.mysql.database.azure.com"
jdbcDatabase = "toonemysql"
jdbcPort = 3306
jdbcUrl = "jdbc:mysql://{0}:{1}/{2}?user={3}&password={4}".format(jdbcHostname, jdbcPort, jdbcDatabase, username, password)

# COMMAND ----------

# MAGIC %sql
# MAGIC 
# MAGIC CREATE TABLE <jdbcTable>
# MAGIC USING org.apache.spark.sql.jdbc
# MAGIC OPTIONS (
# MAGIC   url "jdbc:<databaseServerType>://<jdbcHostname>:<jdbcPort>",
# MAGIC   dbtable "<jdbcDatabase>.atable",
# MAGIC   user "<jdbcUsername>",
# MAGIC   password "<jdbcPassword>"
# MAGIC )