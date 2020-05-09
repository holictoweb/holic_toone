
import pandas as pd
import pymongo


class Cosmosdb:
    def __init__(self): #개별 오브젝트 생성 시 연결이 생성 되는 것인가?
        print(">>> ModelHoilcStock is __init__ ")
        
        #connect cosmosdb-mongodb
        uri = "mongodb://toonecosmosdb:QYzYAF3Si1tNFxmKxs00SvKyIba4Pbig6GKIhqOiUWGr4zbT2vUvLj54ySN1DsiPqNWr1JkyWB9REygXz8wxGQ==@toonecosmosdb.documents.azure.com:10255/?ssl=true&replicaSet=globaldb"
        client = pymongo.MongoClient(uri)
        self.toonecosmosdb_collection = client.toonecosmosdb
        self.astock = self.toonecosmosdb_collection.automated_stock
        
        print (self.astock)
        print(">>> [finished] ModelHoilcStock is __init__ ")

    def set_db_stock(self,df_stock_list):
        try:
            #post = {"data_type":"min", "author": "Mike", "text": "test input", "code":"11222" }
            #self.astock.insert(post)

            # pandas dataframe to mongodb
            self.astock.insert_many(df_stock_list.to_dict('records'))

            print(">>>> set_db_stock inserted")
        except ZeroDivisionError as e:
            print(e)
            

    def get_db_stock(self, data_type, stock_code):
        print(">>>> read_my_stock")
        try:
            # 039490
            myquery = { "code": "005930" }
            myresult = self.astock.find(myquery)
            
            #for x in myresult:
            #    print(x)

            df = pd.DataFrame(list(myresult))
            #print (df)
            return(df)

            '''
            date = df['date'][-50:]
            high = df['고가'][-50:]
            low = df['저가'][-50:]
            close = df['현재가'][-50:]
            ret = ta.ATR(high, low, close)
            '''

            #plt.plot(date, ret[-50:], color='yellow')
            #plt.show()

            

        except ZeroDivisionError as e:
            print(e)

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


if __name__ == "__main__":

    modeltoone = Cosmosdb()

    #modeltoone.set_db_stock()

    #df=get_db_stock('005930')
    #     #print(df)


