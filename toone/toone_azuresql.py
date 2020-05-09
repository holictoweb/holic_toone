import pyodbc
import pandas.io.sql as sql

import pandas as pd

import sqlalchemy as sa
import urllib

from datetime import date


class TooneAzuresql:

    def __init__ (self):
        server = 'toonesqlserver.database.windows.net'
        database = 'toonedatabase'
        username = 'admin_orange'
        password = '!1Zenithncom'
        #driver= '{SQL Server}'
        driver= '{ODBC Driver 17 for SQL Server}'
        

        self.cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)

        self.engine = sa.create_engine("mssql+pyodbc://{user}:{pw}@{svr}/{db}?driver=SQL+Server"
                       .format(user=username,
                               pw=password,
                               svr=server,
                               db=database))
        
    def get_chart_day(self, code):
        print (">>> get chart day....")


    def get_test(self):
        self.cursor = self.cnxn.cursor()
        self.cursor.execute("select * from sys.databases;")
        row = self.cursor.fetchall()
        while row:
            print (str(row[0]) + " " + str(row[1]))
            row = self.cursor.fetchone()
            
    def set_chart_day(self, stock_df):
        print(">>> [TooneAzuresql] set_stock_day... ")
        
        self.cursor = self.cnxn.cursor()
        cols = "],[".join([str(i) for i in stock_df.columns.tolist()])
        #print(cols)
        stock_df.columns = stock_df.columns.str.strip()

        for i,row in stock_df.iterrows():
            sql = "INSERT INTO toone_chart_day ( [" +cols + "] ) VALUES (" + "?,"*(len(row)-1) + "?)"
            #print(i)
            print(tuple(row))
            #print(sql )
            
            self.cursor.execute(sql, tuple(row))
            self.cnxn.commit()

        self.cursor.close()
        
    

    def set_chart_min(self, stock_df):
        #index 처리 
        print(stock_df)

        
        
        print ( self.engine.has_table('toone_stock_min') ) 
        stock_df.to_sql(name = 'toone_stock_min', schema='dbo', con = self.engine, if_exists='append', index=False  )
        

    def set_stock_min_old(self, stock_df):
        self.cursor = self.cnxn.cursor()

        cols = "','".join([str(i) for i in stock_df.columns.tolist()])

        print (cols)

        
        for i,row in stock_df.iterrows():
            sql = "INSERT INTO 'toone_stock_min' ('" +cols + "') VALUES (" + "%s,"*(len(row)-1) + "%s)"
            print(sql)
            print (tuple(row))
            self.cursor.execute(sql, tuple(row))
            self.cnxn.commit()

        self.cursor.close()
        
if __name__ == '__main__':
    tooneAzuresql = TooneAzuresql()
    tooneAzuresql.get_test()

