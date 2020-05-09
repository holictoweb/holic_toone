# Databricks notebook source
df = spark.read.json("/databricks-datasets/samples/people/people.json")

# COMMAND ----------

# table 생성

display(df)

# COMMAND ----------

# MAGIC % sql
# MAGIC create table toone_test using delta location ''

# COMMAND ----------

dbutils.fs.ls

# COMMAND ----------

from pyspark import SparkContext, SparkConf, SQLContext
import _mssql
import pandas as pd

appName = "PySpark SQL Server Example - via ODBC"
master = "local"

'''
sc = SparkContext()
sqlContext = SQLContext(sc)
spark = sqlContext.sparkSession
'''

database = "toonedatabase"
table = "dbo.Employees"
user = "admin_orange"
password  = "!1Zenithncom"

database = "toonedatabase"
table = "dbo.toone_stock_day"
user = "admin_orange"
password  = "!1Zenithncom"

conn = _mssql.connect(server='tooneserver.database.windows.net', user='admin_orange', password='!1Zenithncom',database='toonedatabase')
query = f"SELECT * FROM {table}"

conn.execute_query(query)
rs = [ row for row in conn ]
pdf = pd.DataFrame(rs)
sparkDF = spark.createDataFrame(pdf)
sparkDF.show()
conn.close()



# COMMAND ----------

import pyodbc
server = 'tooneserver.database.windows.net'
database = 'toonedatabase'
username = 'admin_orange'
password = '!1Zenithncom'
driver= '{ODBC Driver 17 for SQL Server}'
cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()
cursor.execute("SELECT TOP 20 pc.Name as CategoryName, p.name as ProductName FROM [SalesLT].[ProductCategory] pc JOIN [SalesLT].[Product] p ON pc.productcategoryid = p.productcategoryid")
row = cursor.fetchone()
while row:
    print (str(row[0]) + " " + str(row[1]))
    row = cursor.fetchone()

# COMMAND ----------

Class.forName("com.microsoft.sqlserver.jdbc.SQLServerDriver")

# COMMAND ----------

import com.microsoft.azure.sqldb.spark.config.Config
import com.microsoft.azure.sqldb.spark.connect._

