import pymysql.cursors
import pandas as pd

from sqlalchemy import create_engine




class ModelHolicStock:
    def __init__(self): #개별 오브젝트 생성 시 연결이 생성 되는 것인가?
        print("#### ModelHoilcStock is __init__ ")
        self.conn = pymysql.connect(host='localhost',
                                port=3306,
                                user='root',
                                password='1004cjstk',
                                db='stock',
                                charset='utf8')


        ## PyMySQL
        self.alchemy_engine = create_engine('mysql+pymysql://root:1004cjstk@localhost/stock')

    def update_my_stock(self, update_list):
        # 구매 완료 나 신호 변경에 따른 진행.
        try:
            with self.conn.cursor() as cursor:
                data = (
                    update_list[0][1]
                )
                #insert or update 하는 로직 필요.
                sql = '''insert into stock.mystock 
                        values (%s, %s, %s)'''

                #values('017670', 'SK텔레콤', 0, 'sell', now())


                cursor.executemany(sql, data)

                print("#### inserted")
        finally:
            self.conn.commit()
            self.conn.close()


    def read_my_stock(self, stock_type):
        print("#### read_my_stock")
        try:
            with self.conn.cursor() as cursor:

                sql = '''select * 
                        from stock.mystock'''


                cursor.execute(sql)
                rows = cursor.fetchall()
                print(rows)  # 전체 rows

                df = pd.DataFrame(data=rows, index=None, columns=cursor.keys())
                print(df)
                return df

        except ZeroDivisionError as e:
            print(e)
        finally:
            self.conn.close()

    def insert_condition_stock(self,condition_list):
        print("#### insert_condition_stock")
        try:
            with self.conn.cursor() as cursor:

                data = (
                    condition_list[0],
                    condition_list[1],
                    condition_list[2],
                )

                sql = '''insert into condition_stock(condition_name, condition_type, condition_list, create_date)
                        values(%s, %s, %s, now())'''
                cursor.executemany(sql, data)

        except ZeroDivisionError as e:
            print(e)
        finally:
            self.conn.close()

    def insert_stock_data(self,df_stock):
        print("[ insert_stock_data ]")
        #df_stock.drop("cprice", axis=1, inplace=True)

        df_stock.to_sql('stock_data', con=self.alchemy_engine, index=False, if_exists='append')
        #df_return =self.alchemy_engine.execute("SELECT * FROM stock_data").fetchall()
        #print(df_return)



