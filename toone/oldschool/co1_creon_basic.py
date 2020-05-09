# -*- coding: utf-8 -*-

import time
from datetime import date
import logging
from logging.handlers import TimedRotatingFileHandler

import win32com.client
import pandas as pd



class CreonControl:

    def __init__(self):
        self.obj_CpCodeMgr = win32com.client.Dispatch('CpUtil.CpCodeMgr')
        self.obj_CpCybos = win32com.client.Dispatch('CpUtil.CpCybos')
        self.obj_StockChart = win32com.client.Dispatch('CpSysDib.StockChart')
        self.obj_MarketEye = win32com.client.Dispatch("CpSysDib.MarketEye")

        self.list_field_key = [0, 1, 2, 3, 4, 5, 8]
        self.list_field_name = ['date', 'time', 'open', 'high', 'low', 'close', 'volume']
        self.check_basic_field_name = ['price','volume', 'per','eps']

###########################################################################################################################
    def get_kosdaq_code(self):
        kospi_list = []
        kosdaq_tuple = self.obj_CpCodeMgr.GetStockListByMarket(2)

        for creon_stockcode in kosdaq_tuple: 
            if creon_stockcode[0] == 'A': 
                kospi_list.append(creon_stockcode)

        return kospi_list

    def get_basic_info(self, codelist):
        #print( '>>>' + codelist )
        b_connected = self.obj_CpCybos.IsConnect
        if b_connected == 0:
            print("연결 실패")
            return None
        
        if type(codelist) != list :
            #print (codelist)
            codelist_tmp = list()
            codelist_tmp.append(codelist) 
            codelist = codelist_tmp
            #print (codelist)

        df_return=pd.DataFrame()

        for code in codelist:
            dict_basic = {name: [] for name in self.check_basic_field_name}

            self.obj_MarketEye.SetInputValue(0, (4, 10, 67, 70)) # 4:price, 10:volume, 67:per 70:eps
            if code[:1] != 'A':
                self.obj_MarketEye.SetInputValue(1, 'A' + code)
            else :
                self.obj_MarketEye.SetInputValue(1, code)
            self.obj_MarketEye.BlockRequest()

            
            '''
            cur_price = self.obj_MarketEye.GetDataValue(0, 0)
            cur_volume = self.obj_MarketEye.GetDataValue(1, 0)
            cur_per = self.obj_MarketEye.GetDataValue(2, 0)

            df_basic = pd.DataFrame(columns = self.check_basic_field_name)
            '''


            status = self.obj_MarketEye.GetDibStatus()
            msg = self.obj_MarketEye.GetDibMsg1()
            print("통신상태: {} {}".format(status, msg))

            if status != 0:
                return None

            cnt = self.obj_MarketEye.GetHeaderValue(2)  # 수신개수

            for i in range(cnt):
                dict_item = (
                    {name: self.obj_MarketEye.GetDataValue(pos, i) 
                    for pos, name in zip(range(len(self.check_basic_field_name)), self.check_basic_field_name)}
                )
            
                for k, v in dict_item.items():
                    dict_basic[k].append(v)

            #print("차트: {} {}".format(cnt, dict_basic))
            df_code = pd.DataFrame(dict_basic, columns=self.check_basic_field_name)
            df_code['code'] = code
            df_code['date'] = time.strftime('%Y%m%d')
            #print(df_code)
            df_return=df_return.append(df_code)

            time.sleep(1)
        
        return df_return

        

    def _wait(self):
        
        time_remained = self.obj_CpCybos.LimitRequestRemainTime
        cnt_remained = self.obj_CpCybos.GetLimitRemainCount(1)  # 0: 주문 관련, 1: 시세 요청 관련, 2: 실시간 요청 관련
        if cnt_remained <= 0:
            timeStart = time.time()
            while cnt_remained <= 0:
                time.sleep(time_remained / 1000)
                time_remained = self.obj_CpCybos.LimitRequestRemainTime
                cnt_remained = self.obj_CpCybos.GetLimitRemainCount(1)


###########################################################################################################################
    
    def creon_chart_day(self, codelist, getcount, date_from, date_to):
        #print( '>>>' + codelist )
        b_connected = self.obj_CpCybos.IsConnect
        if b_connected == 0:
            print("연결 실패")
            return None
        
        if type(codelist) != list :
            #print (codelist)
            codelist_tmp = list()
            codelist_tmp.append(codelist) 
            codelist = codelist_tmp
            #print (codelist)

        df_return=pd.DataFrame()
        
        for code in codelist:
            dict_chart = {name: [] for name in self.list_field_name}

            if code[:1] != 'A':
                self.obj_StockChart.SetInputValue(0, 'A'+code)
            else :
                self.obj_StockChart.SetInputValue(0, code)

            if getcount == 0 or getcount =='': 
                #print (">>> date")
                self.obj_StockChart.SetInputValue(1, ord('1'))  # 0: 개수, 1: 기간
                #self.obj_StockChart.SetInputValue(2, date_to)  # 종료일
                self.obj_StockChart.SetInputValue(3, date_from)  # 시작일  
                
            else:
                #print (">>>> count")
                self.obj_StockChart.SetInputValue(1, ord('2'))  # 0: ??, 1: 기간 2: 개수
                self.obj_StockChart.SetInputValue(4, getcount)
                    
            self.obj_StockChart.SetInputValue(5, self.list_field_key)  # 필드
            self.obj_StockChart.SetInputValue(6, ord('D'))  # 'D', 'W', 'M', 'm', 'T'
            self.obj_StockChart.SetInputValue(9, ord('1'))
            self.obj_StockChart.BlockRequest()


            status = self.obj_StockChart.GetDibStatus()
            msg = self.obj_StockChart.GetDibMsg1()
            print("통신상태: {} {}".format(status, msg))

            if status != 0:
                return None

            cnt = self.obj_StockChart.GetHeaderValue(3)  # 수신개수

            for i in range(cnt):
                dict_item = (
                    {name: self.obj_StockChart.GetDataValue(pos, i) 
                    for pos, name in zip(range(len(self.list_field_name)), self.list_field_name)}
                )
            
                for k, v in dict_item.items():
                    dict_chart[k].append(v)

            #print("차트: {} {}".format(cnt, dict_chart))
            df_code = pd.DataFrame(dict_chart, columns=self.list_field_name)
            df_code['code'] = code
            #print(df_code)
            df_return=df_return.append(df_code)
            
        return df_return
    
    def creon_chart_min(self, codelist, getcount, date_from, date_to):
        #print( '>>>' + codelist )
        b_connected = self.obj_CpCybos.IsConnect
        if b_connected == 0:
            print("연결 실패")
            return None
        
        if type(codelist) != list :
            #print (codelist)
            codelist_tmp = list()
            codelist_tmp.append(codelist) 
            codelist = codelist_tmp
            #print (codelist)

        df_return=pd.DataFrame()
        
        for code in codelist:
            dict_chart = {name: [] for name in self.list_field_name}

            if code[:1] != 'A':
                self.obj_StockChart.SetInputValue(0, 'A'+code)
            else :
                self.obj_StockChart.SetInputValue(0, code)

            if getcount == 0 or getcount =='': 
                #print (">>> date")
                self.obj_StockChart.SetInputValue(1, ord('1'))  # 0: 개수, 1: 기간
                #self.obj_StockChart.SetInputValue(2, date_to)  # 종료일
                self.obj_StockChart.SetInputValue(3, date_from)  # 시작일  
                
            else:
                #print (">>>> count")
                self.obj_StockChart.SetInputValue(1, ord('2'))  # 0: ??, 1: 기간 2: 개수
                self.obj_StockChart.SetInputValue(4, getcount)
                    
            self.obj_StockChart.SetInputValue(5, self.list_field_key)  # 필드
            self.obj_StockChart.SetInputValue(6, ord('m'))  # 'D', 'W', 'M', 'm', 'T'
            self.obj_StockChart.SetInputValue(9, ord('1'))
            self.obj_StockChart.BlockRequest()


            status = self.obj_StockChart.GetDibStatus()
            msg = self.obj_StockChart.GetDibMsg1()
            print("통신상태: {} {}".format(status, msg))

            if status != 0:
                return None

            cnt = self.obj_StockChart.GetHeaderValue(3)  # 수신개수

            for i in range(cnt):
                dict_item = (
                    {name: self.obj_StockChart.GetDataValue(pos, i) 
                    for pos, name in zip(range(len(self.list_field_name)), self.list_field_name)}
                )

                for k, v in dict_item.items():
                    dict_chart[k].append(v)

            #print("차트: {} {}".format(cnt, dict_chart))
            df_code = pd.DataFrame(dict_chart, columns=self.list_field_name)
            df_code['code'] = code
            #print(df_code)
            df_return=df_return.append(df_code)
            
        return df_return
        
if __name__ == '__main__':
    creonControl = CreonControl()
    
    ## 일별 
    #today = time.strftime('%Y%m%d')

    ## chart 조회 
    # 005940
    slist =['005940', '035420']
    #slist = '005940'
    #stockdata = creonControl.creon_chart_day(slist, 3, '','')
    stockdata = creonControl.creon_chart_min(slist, 0,'20191111','20191111')

    print (stockdata)


    




