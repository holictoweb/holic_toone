import pyodbc
import pandas as pd




class OrangeModel:
    def __init__(self): #개별 오브젝트 생성 시 연결이 생성 되는 것인가?
        print("#### ModelHoilcStock is __init__ ")
        

        ## PyMySQL
        #self.alchemy_engine = create_engine('mysql+pymysql://root:1004cjstk@localhost/stock')
        #self.conn = pyodbc.connect(server='orangedatabase.database.windows.net', user='admin_orange', password='!1Zenithncom')
        self.conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=orangedatabase.database.windows.net;'
                      'UID=admin_orange;'
                      'PWD=!1Zenithncom')




    def insert_stock_day(self,df_stock):
        print("[ insert_stock_data ]")
        #df_stock.drop("cprice", axis=1, inplace=True)

        df_stock.to_sql('stock_data', con=self.alchemy_engine, index=False, if_exists='append')
        #df_return =self.alchemy_engine.execute("SELECT * FROM stock_data").fetchall()
        #print(df_return)
        try:
            with self.conn.cursor() as cursor:
                for index,row in df.iterrows():
                    cursor.execute("INSERT INTO dbo.vSalesPerson_test([BusinessEntityID],[FirstName],[LastName]) values (?, ?,?)", row['BusinessEntityID'], row['FirstName'] , row['LastName']) 
                    connStr.commit()
                cursor.close()
                connStr.close()
                
        except ZeroDivisionError as e:
            print(e)
        finally:
            self.conn.close()
        

if __name__ == "__main__":
    ornageModel = OrangeModel()