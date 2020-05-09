import time

import pandas as pd 
import numpy as np
from db1_data_control import *
from co1_creon_basic import * 

class Analytics:
     # driven 

    def __init__(self):
        self.datacontrol = DataControl()
        self.creoncontrol = CreonControl()

    def get_target_stock(self): 
        # pandas로 받을지 list로 받을지
        df_target = self.datacontrol.get_target_stock()
        
        return df_target
    
    def analyze_batch(self):
        # 배치로 데이터 수집 및 target 선정
        # 데이터에 대한 분석 작업은 별도 펑션
        tooneday = time.strftime('%Y%m%d')

        #1. 해당일 테이블 생성 
        tablename = self.datacontrol.set_table('D', tooneday)
        

        #2. kosdaq 전체 정보 조회
        listkosdaq = self.creoncontrol.get_kosdaq_code()
        
        #listkosdaq = ['005940', '035420', '090710','009520', '019540']

        #3. basic 검토 
        df_basic = self.creoncontrol.get_basic_info(listkosdaq)
        df_basic.index = np.arange(0,len(df_basic))

        # volume 상위 order
        #df_basic = df_basic.sort_values(by=['volume'], ascending=True)

        df_source = df_basic.sort_values(by='volume', ascending=False).head(100)
        df_source.index = np.arange(0,len(df_source))
        print(df_source.head())
        
        drop_list = []
        for index, target in df_source.iterrows():
            print(">>> loop " + str(index))
            if target.price >= 30000 or target.price <= 1500 or target.volume <= 10000000:
                print(">>>> drop process")
                #df_source.drop(df_source.index[index], inplace=True)
                drop_list.append(index)
            else:
                print(">>>> no drop process")
            
        #print(drop_list )
        #print(df_source.drop(df_source.index[drop_list], inplace = True))
        #print ( df_source)
        
        
        # 1차 걸러진 데이터는 rela time 분석용 데이터로 사용 될 수 있기 때문에 저장 필요
        self.datacontrol.set_target_stock(df_source)
        #4. 1차 걸러진 리스트에 대해 6개월 데이터 수집  
        for idx, target in df_source.iterrows():
            
            df_target = self.creoncontrol.creon_chart_day(target.code, 120,'','')
            self.datacontrol.set_stock_day(tablename, df_target)
            print (">>> DATA insert azure complete : " + target.code )

            if idx%3 == 0:
                time.sleep(1)
        

        print (">>> batch fininshed : " + tooneday )


    def analyze_real(self, df_analytics):
        df_real = pd.DataFrame()

        df_real = self.datacontrol.get_target_stock(df_analytics)

        for idx, target in df_real.iterrows():
            
            df_source = self.creoncontrol.creon_chart_min(target.code, 120,'','')
            self.datacontrol.set_stock_min(tablename, df_source)
            print (">>> DATA insert azure complete : " + target.code )

            if idx%3 == 0:
                time.sleep(1)


        return df_real

if __name__ =='__main__':
    analytics = Analytics()
    #analytics.analyze_real()

    # 모든 분석의 시작
    analytics.analyze_batch()