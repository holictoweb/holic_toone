import pyodbc
server = 'toonesqlserver.database.windows.net'
database = 'toonedatabase'
username = 'admin_orange'
password = '!1Zenithncom'
driver= '{ODBC Driver 17 for SQL Server}'


cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()
cursor.execute("select * from sys.databases")
row = cursor.fetchone()
while row:
    print (str(row[0]) + " " + str(row[1]))
    row = cursor.fetchone()