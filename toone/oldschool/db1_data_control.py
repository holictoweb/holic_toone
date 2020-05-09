# -*- coding: utf-8 -*-

from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.models import Entity
import json
import time

import pandas as pd

from db2_data_manager import * 


#azure table - The entity must be either in dict format or an entity object.

class DataControl: 

    def __init__(self):
        self.table_service = TableService(account_name='toonestorage01', account_key='sIo3TKwG40eH2a9MpjZdGgWwetkGDV3NcgFhwZN2sFerhrj3kWLTiKQO3wGO7bd9sjmGoBnPl2CbqrIJcsnG8g==')
        #table_service = TableService(connection_string='DefaultEndpointsProtocol=https;AccountName=toonestorage01;AccountKey=sIo3TKwG40eH2a9MpjZdGgWwetkGDV3NcgFhwZN2sFerhrj3kWLTiKQO3wGO7bd9sjmGoBnPl2CbqrIJcsnG8g==;EndpointSuffix=core.windows.net')
        #SOURCE_TABLE = "stockday"


###########################################################################################################################
    def set_table(self, tabletype, tooneday):
        if tabletype == 'D':
            table_name = 'stock' + tabletype  + tooneday
            #오늘 날짜 분석 테이블이 존재 하면 삭제 하고 새로 생성 / Azure Table은 삭제 후 재 생성 불가 (delay 발생)
            print(table_name)
            if self.table_service.exists(table_name) == False:
                self.table_service.create_table(table_name)
                print(">> table created : " + table_name )
            else :
                print(">> table exists " + table_name)

        elif tabletype =='5M':
            print(">>> 5M table")

        return table_name

    def set_target(self, targetdf):
        prep_df = preprocess(targetdf)
        print ( prep_df )

###########################################################################################################################
    def set_stock_day(self, targettable, stockdf):
        # print('>> insert data to azure table')

        '''
        for data in stockdata:
            task = {'PartitionKey': 'tasksSeattle', 'RowKey': '001','description': 'Take out the trash', 'priority': 200}   
            self.table_service.insert_entity('stockday', task)
        '''
        # dataframe에서 partitionkey 및 row_id 로 칼럼명 변경 필요
        # key 값을 두개만 가질 수 있음
        # particionkey = code / date = row_id

        #print (stockdf.head())
        stockdf_table = stockdf.rename(columns={"code": "PartitionKey", "date": "RowKey"})
        #print (stockdf_table)
        
        for index, row in stockdf_table.iterrows():
            #print(row)
            #print(row['PartitionKey'])
            #print(">> start row")
            #print(row)

            task = Entity()
            task.PartitionKey = row.to_dict()['PartitionKey']
            task.RowKey = str(row.to_dict()['RowKey'])
            task.open = row.to_dict()['open']
            task.high = row.to_dict()['high']
            task.low = row.to_dict()['low']
            task.close = row.to_dict()['close']
            task.volume = row.to_dict()['volume']
            
            self.table_service.insert_or_merge_entity(targettable, task, timeout=None)

        #print('>> end set stockday')
    
    def get_stock_day(self, code):
        print('>> start get data ')
        
        # 여러 데이타 추출 
        target_table = 'stockD' + time.strftime('%Y%m%d')
        filter_target = "PartitionKey eq '" + code+ "'" 
        rows = self.table_service.query_entities( target_table , filter=filter_target, select='PartitionKey,RowKey,open,high,low,volume,close')
        
        df_stock_day = pd.DataFrame(rows)
        #print(df_stock_day.head())
    
        return df_stock_day
    
    def set_stock_min(self, stockdf):
        # print('>> insert data to azure table')
        
        #print (stockdf.head())
        stockdf_table = stockdf.rename(columns={"code": "PartitionKey", "date": "RowKey"})
        #print (stockdf_table)

        stockdf_table = stockdf_table.astype({"time":str, "RowKey": str})

        # date column을 time 컬럼과 합성
        if len(str(stockdf_table["time"])) <= 3:
            stockdf_table["time"] = '0' + str(stockdf_table["time"])
        print(stockdf_table.head())

        stockdf_table["RowKey"] = stockdf_table["RowKey"]  + stockdf_table["time"]
        print(stockdf_table.head())

        stockdf_last = pd.DataFrame()
        stockdf_last = stockdf_table[ ['PartitionKey', 'RowKey', 'time', 'open', 'high', 'low', 'close', 'volume'] ]
        print(stockdf_last)

        for index, row in stockdf_last.iterrows():
            task = Entity()
            task.PartitionKey = row.to_dict()['PartitionKey']
            task.RowKey = str(row.to_dict()['RowKey'])
            task.time = row.to_dict()['time']
            task.open = row.to_dict()['open']
            task.high = row.to_dict()['high']
            task.low = row.to_dict()['low']
            task.close = row.to_dict()['close']
            task.volume = row.to_dict()['volume']
            
            #print(task)
            self.table_service.insert_or_merge_entity('stockM', task, timeout=None)
    

###########################################################################################################################

    def get_max_date(self, stockcode):
        filter_str = "PartitionKey eq '" + stockcode +"'" 
        rows = self.table_service.query_entities( 'stockday', filter=filter_str, select='open,close')
        #print (rows.RowKey)
        for row in rows:
            print (row)
        return row
    
    
    def get_max_time(self, stockcode):
        filter_str = "RowKey eq '" + stockcode +"'" 
        rows = self.table_service.query_entities( 'stockM', filter=filter_str, select='open,close')
        #print (rows.RowKey)
        for row in rows:
            print (row)
        return row
    
    def set_target_stock(self,df_target):
        # ['price','volume', 'per','eps']
        df_target["date"]=time.strftime('%Y%m%d')
        stockdf_table = df_target.rename(columns={"date": "PartitionKey", "code": "RowKey"})
        
        for index, row in stockdf_table.iterrows():
            #print(row)
            #print(row['PartitionKey'])
            #print(">> start row")
            #print(row)

            task = Entity()
            task.PartitionKey = row.to_dict()['PartitionKey']
            task.RowKey = str(row.to_dict()['RowKey'])
            task.price = row.to_dict()['price']
            task.volume = row.to_dict()['volume']
            task.per = row.to_dict()['per']
            task.eps = row.to_dict()['eps']
            
            self.table_service.insert_or_merge_entity('stocktarget', task)
            print(">> set target stock..." + str(row.to_dict()['RowKey']) )

    def get_target_stock(self):
        
        filter_target = "PartitionKey eq '" + time.strftime('%Y%m%d')+ "'"
        rows = self.table_service.query_entities( 'stocktarget', filter= filter_target, select='RowKey, status')
        #print (rows.RowKey)
        df_target = pd.DataFrame(rows)
        
        return df_target

if __name__ == '__main__':
    datacontrol = DataControl()
    
    #table_name = datacontrol.set_table('D', '20191109') 
    #print (table_name)

    # get_stock
    #datacontrol.get_target_stock()
    #datacontrol.get_stock_day('A002800')
    
    



