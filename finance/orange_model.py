import pyodbc
import pandas as pd

class OrangeModel:
    def __init__(self): #개별 오브젝트 생성 시 연결이 생성 되는 것인가?
        print("#### ModelHoilcStock is __init__ ")
        

        ## PyMySQL
        #self.alchemy_engine = create_engine('mysql+pymysql://root:1004cjstk@localhost/stock')
        #self.conn = pyodbc.connect(server='orangedatabase.database.windows.net', user='admin_orange', password='!1Zenithncom')
        self.cnxn = pyodbc.connect('Driver={SQL Server};'
                      'Server=orangedatabase.database.windows.net;'
                      'UID=admin_orange;'
                      'PWD=!1Zenithncom;'
                      'Database=finance_01;')
    
    def retrieve_test(self):
        stmt = 'select * from test'

        df = pd.read_sql(stmt,self.cnxn)
        print (df)

    def insert_stock_day(self,df_stock):
        print("[ insert_stock_data ]")
        #df_stock.drop("cprice", axis=1, inplace=True)
        '''
        df_stock.to_sql('stock_data', con=self.alchemy_engine, index=False, if_exists='append')
        #df_return =self.alchemy_engine.execute("SELECT * FROM stock_data").fetchall()
        #print(df_return)
        try:
            with self.cnxn.cursor() as cursor:
                for index,row in df.iterrows():
                    cursor.execute("INSERT INTO dbo.vSalesPerson_test([BusinessEntityID],[FirstName],[LastName]) values (?, ?,?)", row['BusinessEntityID'], row['FirstName'] , row['LastName']) 
                    connStr.commit()
                cursor.close()
                connStr.close()
                
        except ZeroDivisionError as e:
            print(e)
        finally:
            self.cnxn.close()
        '''
        

if __name__ == "__main__":
    ornageModel = OrangeModel()

    ornageModel.retrieve_test()
    #print("test")