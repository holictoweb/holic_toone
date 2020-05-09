# -*- coding: utf-8 -*-
'''

author : Lee Joon Ik
모의투자 계좌 : 8112339511


'''

import sys
import logging
import logging.config
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
import datetime

import time


import pandas as pd
import numpy as np
import sqlite3

TR_REQ_TIME_INTERVAL = 0.2
MAX_CONDITION_COUNT = 5

class Kiwoom(QAxWidget):

    def __init__(self):
        super().__init__()
        self._create_kiwoom_instance()
        self._set_signal_slots()

        self.conditionStockItem = ''


        # Loop 변수
        # 비동기 방식으로 동작되는 이벤트를 동기화(순서대로 동작) 시킬 때
        self.loginLoop = None
        self.requestTRLoop = None
        self.requestkwLoop = None
        self.orderLoop = None
        self.conditionLoop = None

        # 서버구분
        self.server = None

        # 조건식
        self.condition = None

        # 에러
        self.error = None

        # 주문번호
        self.orderNo = ""

        # 조회
        self.inquiry = 0

        # 서버에서 받은 메시지
        self.msg = ""

        # 예수금 d+2
        self.opw00001Data = 0

        # 보유종목 정보
        self.opw00018Data = {'accountEvaluation': [], 'stocks': []}

        # 타겟종목 정보
        self.condition_name_list = []

        #### 현재 모니터링이 되는 모든 stock 상세 정보
        self.automatedStockDict = dict()
        self.automatedHeader = ()

        # 로깅용 설정파일
        #logging.config.fileConfig('logging.conf')
        #self.log = logging.getLogger('Kiwoom')

    def _create_kiwoom_instance(self):
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")

    def _set_signal_slots(self): #서버쪽 이벤트에 대한 응답을 진행
        # 시스템 on
        self.OnEventConnect.connect(self._event_connect)
        self.OnReceiveMsg.connect(self._receive_Msg)
        
        # 사용자 tr 요청한 데이타를 획득 할때 이벤트가 발생
        self.OnReceiveTrData.connect(self._receive_tr_data)
        #self.OnReceiveRealData.connect(self._receive_real_data) 실시간 데이타 획득
        self.OnReceiveChejanData.connect(self._receive_chejan_data)

        # 조건 검색
        self.OnReceiveConditionVer.connect(self._recieve_condition_ver)
        self.OnReceiveTrCondition.connect(self._receive_tr_condition)
        self.OnReceiveRealCondition.connect(self._receive_real_condition)

    ###############################################################
    # 내부 메서드 정의                                               
    ###############################################################

    def logger(origin):
        def wrapper(*args, **kwargs):
            args[0].log.debug('{} args - {}, kwargs - {}'.format(origin.__name__, args, kwargs))
            return origin(*args, **kwargs)

        return wrapper

    def _get_comm_data(self, code, real_type, field_name, index, item_name): #요청에 대한 실제 데이타 획득
        '''
        개별 데이타 획득 메서드
        '''

        print("called ... ")
        ret = self.dynamicCall("GetCommData(QString, QString, QString, int, QString)", code,
                               real_type, field_name, index, item_name)
        print(ret.strip())
        return ret.strip() #strip 반환하는 데이타에 공백 존재 strip 제거함.


    def _comm_get_data(self, code, real_type, field_name, index, item_name):
        """
        depricated 추후 사용 하지 않는걸로 가이드 나옴.
        """
        ret = self.dynamicCall("CommGetData(QString, QString, QString, int, QString)", code,
                               real_type, field_name, index, item_name)
        return ret.strip()


    def _get_comm_data_ex(self, trCode, multiDataName):
        """
        멀티데이터 획득 메서드

        receiveTrData() 이벤트 메서드가 호출될 때, 그 안에서 사용해야 합니다.
        """

        if not (isinstance(trCode, str)
                and isinstance(multiDataName, str)):
            raise ParameterTypeError()

        data = self.dynamicCall("GetCommDataEx(QString, QString)", trCode, multiDataName)
        return data

    def _get_repeat_cnt(self, trcode, rqname): #반환 될 데이타의 갯수 획득
        ret = self.dynamicCall("GetRepeatCnt(QString, QString)", trcode, rqname)
        return ret
    
    @staticmethod
    def change_format(data):
        strip_data = data.lstrip('-0')
        if strip_data == '':
            strip_data = '0'

        format_data = format(int(strip_data), ',d')
        if data.startswith('-'):
            format_data = '-' + format_data

        return format_data

    @staticmethod
    def change_format2(data):
        strip_data = data.lstrip('-0')

        if strip_data == '':
            strip_data = '0'

        if strip_data.startswith('.'):
            strip_data = '0' + strip_data

        if data.startswith('-'):
            strip_data = '-' + strip_data

        return strip_data


    ###########################################################################################################
    #   사용자 호출 함수 
    ###########################################################################################################
    def get_connect_state(self):
        ret = self.dynamicCall("GetConnectState()")
        return ret

    def get_min_chart(self, s_code, duration):
        '''
        주식분봉차트조회요청
        '''
        print("[ get_min_chart ] " + s_code + '_' + duration)
        #self.ohlcv_min = {'date': [], 'open': [], 'high': [], 'low': [], 'cprice': [], 'volume': []}

        self.set_input_value("종목코드", s_code)
        self.set_input_value("틱범위", duration)
        self.set_input_value("수정주가구분", 1)
        
        self.comm_rq_data("opt10080_req", "opt10080", 0, "1021")

        return self.df_chart_minute

    def get_condition(self):
        result_yn = self.dynamicCall("GetConditionLoad()") #_recieve_condition_ver
        #print(result_yn)

        self.conditionLoop = QEventLoop()
        self.conditionLoop.exec_()

    def send_condition(self, index):
        '''
        요청 온 idx 번째 조건식에 대한 종목 코드 조회
        
        :param index: 
        :return: 
        '''

        #print ("send_condition ")
        #name_list_split = self.condition_name_list.split(";")

        name_split = self.condition_name_list[index].split("^")
        lRet_2 = self.dynamicCall("sendCondition(QString,QString,int,int)", '0156', str(name_split[1]), int(name_split[0]), 1)

        self.conditionLoop = QEventLoop()
        self.conditionLoop.exec_()

    def sendConditionStop(self, screenNo, conditionName, conditionIndex):
        """ 종목 조건검색 중지 메서드 """

        if not self.getConnectState():
            raise KiwoomConnectError()

        if not (isinstance(screenNo, str)
                and isinstance(conditionName, str)
                and isinstance(conditionIndex, int)):
            raise ParameterTypeError()

        self.dynamicCall("SendConditionStop(QString, QString, int)", screenNo, conditionName, conditionIndex)

    def get_server_gubun(self):
        """
        서버구분 정보를 반환한다.
        리턴값이 "1"이면 모의투자 서버이고, 그 외에는 실서버(빈 문자열포함).

        :return: string
        """
        ret = self.dynamicCall("KOA_Functions(QString, QString)", "GetServerGubun", "")
        return ret

    ###########################################################################################################
    #   이벤트 callback 함수 
    ###########################################################################################################
    def _recieve_condition_ver(self, lRet, sMsg):
        """
        조건검색식 이름 및 코드를 반환

        get_condition - GetConditionLoad
        """
        print("[REC] [_recieve_condition_ver]")

        if (lRet == 1):
            self.condition_name_full_list = self.dynamicCall("GetConditionNameList()").split(";")
            #print(self.condition_name_full_list)
            for condition in self.condition_name_full_list:
                #print('condition name : ' + condition)
                if condition != '':
                    condition_name = condition.split("^")
                    if condition_name[1][:3] =='PRD':
                        self.condition_name_list.append(condition)
                        #print(condition)

        else:
            print("[ERROR] 조건검색 이름 확인 오류")

        self.conditionLoop.exit()

    def _receive_tr_condition(self, sScrNo, strCodeList,  strConditionName,  nIndex,  nNext):
        '''
        조건검색에 대한 결과 코드 반환
         
        '''
        print("[REC] [_receive_tr_condition]")
        #조건식 결과를 누적
        self.conditionStockItem += strCodeList
        print("#### condition Name : "+strConditionName+"  _receive_tr_condition strCodeList : " + self.conditionStockItem)

        self.conditionLoop.exit()

    def _receive_real_condition(self):
        '''
        tr 요청 후에도 지속적으로 들어옴.
        '''
        print("[REC] [_receive_real_condition]")


        self.conditionLoop.exit()


    def _receive_Msg(self, screenNo, requestName, trCode, msg):
        """
        수신 메시지 이벤트

        서버로 어떤 요청을 했을 때(로그인, 주문, 조회 등), 그 요청에 대한 처리내용을 전달해준다.

        :param screenNo: string - 화면번호(4자리, 사용자 정의, 서버에 조회나 주문을 요청할 때 이 요청을 구별하기 위한 키값)
        :param requestName: string - TR 요청명(사용자 정의)
        :param trCode: string
        :param msg: string - 서버로 부터의 메시지
        """

        self.msg += requestName + ": " + msg + "\r\n\r\n"

    ###########################################################################################################
    #   TR 데이타 획득
    ###########################################################################################################
    
    def set_input_value(self, id, value): #입력값 셋팅
        self.dynamicCall("SetInputValue(QString, QString)", id, value)

    def comm_rq_data(self, rqname, trcode, next, screen_no): #일봉 데이타 요청
        '''
        CommRqData(
          BSTR sRQName,    // 사용자 구분명
          BSTR sTrCode,    // 조회하려는 TR이름
          long nPrevNext,  // 연속조회여부
          BSTR sScreenNo  // 화면번호
          )
        '''
        print("[ACT] [comm_rq_data] " + rqname + ' _ ' + trcode)
        self.dynamicCall("CommRqData(QString, QString, int, QString)", rqname, trcode, next, screen_no)

        self.requestTRLoop = QEventLoop()
        self.requestTRLoop.exec_()

    def comm_kw_rq_data(self, trcodelist): # codelist에 대한 정보 요청
        '''
        #CommKwRqData("03940;023590", "연속조회여부", "2", "0", "RQName", "0130");
        CommKwRqData(
          BSTR sArrCode,    // 조회하려는 종목코드 리스트
          BOOL bNext,   // 연속조회 여부 0:기본값, 1:연속조회(지원안함)
          int nCodeCount,   // 종목코드 갯수
          int nTypeFlag,    // 0:주식 관심종목, 3:선물옵션 관심종목
          BSTR sRQName,   // 사용자 구분명
          BSTR sScreenNo    // 화면번호
          )
        '''
        print("[ACT] [comm_kw_rq_data] OPTKWFID_req " + trcodelist  )

        codeCount = len(trcodelist.split(';'))

        returnCode = self.dynamicCall("CommKwRqData(QString, QString, int, int, QString, QString)", trcodelist, 0, codeCount, 0, 'OPTKWFID_req', "0130")

        if returnCode != ReturnCode.OP_ERR_NONE:
            raise KiwoomProcessingError("commKwRqData(): " + ReturnCode.CAUSE[returnCode])

        self.requestTRLoop = QEventLoop()
        self.requestTRLoop.exec_()


    def _receive_tr_data(self, screen_no, rqname, trcode, record_name, next, unused1, unused2, unused3, unused4):
        '''
        void OnReceiveTrData(
          BSTR sScrNo,       // 화면번호
          BSTR sRQName,      // 사용자 구분명
          BSTR sTrCode,      // TR이름
          BSTR sRecordName,  // 레코드 이름
          BSTR sPrevNext,    // 연속조회 유무를 판단하는 값 0: 연속(추가조회)데이터 없음, 1:연속(추가조회) 데이터 있음
          LONG nDataLength,  // 사용안함.
          BSTR sErrorCode,   // 사용안함.
          BSTR sMessage,     // 사용안함.
          BSTR sSplmMsg     // 사용안함.
          )
        '''

        print("[REC] [_receive_tr_data] : " + rqname)

        if next == '2': #900개 이상의 데이터 인경우 다음이 존재 하는지 확인 하여 다시 request
            self.remained_data = True
        else:
            self.remained_data = False

        #요청한 tr 코드에 따라 다르게 처리 진행.

        if rqname == "opt10081_req":
            #print ("#### opt10081_req is receieved....")
            self._opt10081(rqname, trcode)
        elif rqname == "opw00001_req":
            self._opw00001(rqname, trcode)
        elif rqname == "opw00018_req":
            print("request 00018.....")
            self._opw00018(rqname, trcode)
        elif rqname == "opt10001_req":
            self._opt10001(rqname, trcode)
        elif rqname == "OPTKWFID_req":
            self._OPTKWFID(trcode)
        elif rqname == "opt10080_req":
            self._opt10080(rqname, trcode)
        else:
            print("#### No TR code DATA ")
        try:
            self.requestTRLoop.exit()
        except AttributeError:
            print("[ERROR] [_receive_tr_data]")
            pass


    def _receive_real_data(self, sCode, sRealType, sRealData):
        '''
        OnReceiveRealData(
          BSTR sCode,        // 종목코드
          BSTR sRealType,    // 리얼타입
          BSTR sRealData    // 실시간 데이터 전문
          )

          실시간 데이터 수신할때마다 호출되며 SetRealReg()함수로 등록한 실시간 데이터도 이 이벤트로 전달됩니다.
          GetCommRealData()함수를 이용해서 실시간 데이터를 얻을수 있습니다.
        '''
        print('[REC] [_receive_real_data]')

        try:
            self.requestTRLoop.exit()
        except AttributeError:
            pass

    ###########################################################################################################
    #   event callback TR 데이타 획득
    ###########################################################################################################
    def _OPTKWFID(self,trCodeList):
        '''
        대상이 되는 code list 전체에 대한 정보 조회
        
        :param trCodeList: 
        :return: 
        '''
        
        print("[FUN] [_OPTKWFID] code list에 따른 전체 정보 조회 (dictionary) ")
        self.conditionStockList = self._get_comm_data_ex(trCodeList, "_OPTKWFID")
        #print(self.conditionStockList)

        automatedStockKey = ('date', 'code', 'name', 'cprice', 'updown', 'rate', 'volume')
        now = time.localtime()
        now_date = "%04d-%02d-%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)

        '''
        list 안에 개별 dict를 저장하는 방식
        [{'updown': '-25', 'price': '-1520', 'name': '동양철관', 'rate': '-1.62', 'volume': '3205680', 'code': '008970'}, ...
        
        
        self.automatedStockList = []
        for stockTmp in self.conditionStockList:
            automatedStockValue = (stockTmp[0], stockTmp[1], stockTmp[2], stockTmp[4], stockTmp[6], stockTmp[7])
            print(automatedStockKey)
            print(automatedStockValue)
            tempStock = dict(zip(automatedStockKey, automatedStockValue))
            self.automatedStockList.append(tempStock)
        print(self.automatedStockList)
        '''

        '''
        dict 안에 dict로 각 stock별 정보를 저장.
        '''

        for stockTmp in self.conditionStockList:
            # 전체 데이타 중 일부 필요한 데이타만 획득.
            automatedStockValue = (now_date, stockTmp[0], stockTmp[1], stockTmp[2], stockTmp[4], stockTmp[6], stockTmp[7])
            # print(automatedStockKey)
            # print(automatedStockValue)
            tempStock = dict(zip(automatedStockKey, automatedStockValue))
            #print(tempStock)
            self.automatedStockDict[stockTmp[0]] = tempStock

        #print(self.automatedStockDict)
        print('[FUN] [_OPTKWFID] Finished')

    def _opt10080(self, rqname, trcode):
        '''
        주식분봉차트조회요청_opt10080
        '''

        print("[FUN] [_opt10080 ] 분봉 데이타")
        data_cnt = self._get_repeat_cnt(trcode, rqname)
        self.df_chart_minute = pd.DataFrame()

        for i in range(data_cnt):
            date = self._comm_get_data(trcode, "", rqname, i, "체결시간")
            open = self._comm_get_data(trcode, "", rqname, i, "시가")
            high = self._comm_get_data(trcode, "", rqname, i, "고가")
            low = self._comm_get_data(trcode, "", rqname, i, "저가")
            close = self._comm_get_data(trcode, "", rqname, i, "현재가")
            #close = self._comm_get_data(trcode, "", rqname, i, "종가")
            volume = self._comm_get_data(trcode, "", rqname, i, "거래량")

            one_data = [date, open, high, low, close, volume]
            s_one_data = pd.Series(one_data)

            self.df_chart_minute = self.df_chart_minute.append(s_one_data, ignore_index=True)

        self.df_chart_minute.columns = ['date', 'open', 'high', 'low', 'close', 'volume']
        print(self.df_chart_minute)

        return self.df_chart_minute

    def _opt10081(self, rqname, trcode):
        data_cnt = self._get_repeat_cnt(trcode, rqname)

        for i in range(data_cnt):
            date = self._comm_get_data(trcode, "", rqname, i, "일자")
            open = self._comm_get_data(trcode, "", rqname, i, "시가")
            high = self._comm_get_data(trcode, "", rqname, i, "고가")
            low = self._comm_get_data(trcode, "", rqname, i, "저가")
            close = self._comm_get_data(trcode, "", rqname, i, "현재가")
            volume = self._comm_get_data(trcode, "", rqname, i, "거래량")
            print(date, open, high, low, close, volume)


            '''
            self.ohlcv['date'].append(date)
            self.ohlcv['open'].append(int(open))
            self.ohlcv['high'].append(int(high))
            self.ohlcv['low'].append(int(low))
            self.ohlcv['close'].append(int(close))
            self.ohlcv['volume'].append(int(volume))
            '''
            #self.db.insert_Leve_Day(day, start, end)

    def _opw00001(self, rqname, trcode):
        print("#### _opw00001 requested.")
        d2_deposit = self._comm_get_data(trcode, "", rqname, 0, "d+2추정예수금")
        self.d2_deposit = Kiwoom.change_format(d2_deposit)

    def reset_opw00018_output(self):
        self.opw00018_output = {'single': [], 'multi': []}

    def _opw00018(self, rqname, trcode):
        print("#### _opw00018 requested.")

        # single data
        total_purchase_price = self._comm_get_data(trcode, "", rqname, 0, "총매입금액")
        total_eval_price = self._comm_get_data(trcode, "", rqname, 0, "총평가금액")
        total_eval_profit_loss_price = self._comm_get_data(trcode, "", rqname, 0, "총평가손익금액")
        total_earning_rate = self._comm_get_data(trcode, "", rqname, 0, "총수익률(%)")
        estimated_deposit = self._comm_get_data(trcode, "", rqname, 0, "추정예탁자산")

        self.opw00018_output['single'].append(Kiwoom.change_format(total_purchase_price))
        self.opw00018_output['single'].append(Kiwoom.change_format(total_eval_price))
        self.opw00018_output['single'].append(Kiwoom.change_format(total_eval_profit_loss_price))

        #print("what the" + total_earning_rate)
        #total_earning_rate = Kiwoom.change_format(total_earning_rate)
        #print('total rate : ' + total_earning_rate)
        '''
        if self.get_server_gubun():
            total_earning_rate = float(total_earning_rate) / 100
            total_earning_rate = str(total_earning_rate)
        '''

        self.opw00018_output['single'].append(total_earning_rate)

        self.opw00018_output['single'].append(Kiwoom.change_format(estimated_deposit))

        self.opw00018_output['single'].append(Kiwoom.change_format(total_purchase_price))
        self.opw00018_output['single'].append(Kiwoom.change_format(total_eval_price))
        self.opw00018_output['single'].append(Kiwoom.change_format(total_eval_profit_loss_price))
        #self.opw00018_output['single'].append(Kiwoom.change_format(total_earning_rate))
        self.opw00018_output['single'].append(Kiwoom.change_format(estimated_deposit))

        # multi data
        rows = self._get_repeat_cnt(trcode, rqname)
        for i in range(rows):
            name = self._comm_get_data(trcode, "", rqname, i, "종목명")
            quantity = self._comm_get_data(trcode, "", rqname, i, "보유수량")
            purchase_price = self._comm_get_data(trcode, "", rqname, i, "매입가")
            current_price = self._comm_get_data(trcode, "", rqname, i, "현재가")
            eval_profit_loss_price = self._comm_get_data(trcode, "", rqname, i, "평가손익")
            earning_rate = self._comm_get_data(trcode, "", rqname, i, "수익률(%)")

            quantity = Kiwoom.change_format(quantity)
            purchase_price = Kiwoom.change_format(purchase_price)
            current_price = Kiwoom.change_format(current_price)
            eval_profit_loss_price = Kiwoom.change_format(eval_profit_loss_price)
            earning_rate = Kiwoom.change_format2(earning_rate)

            self.opw00018_output['multi'].append([name, quantity, purchase_price, current_price,
                                                  eval_profit_loss_price, earning_rate])

        print("#### _opw00018 FINISHED.")

    def _opt10001(self, rqname, trcode):
        print("#### kiwoom _opt10001 is requested")

        code = self._get_comm_data(trcode, "", rqname, 0, "종목코드")
        name = self._get_comm_data(trcode, "", rqname, 0, "종목명")
        current_price = self._get_comm_data(trcode, "", rqname, 0, "현재가")
        volumn = self._get_comm_data(trcode, "", rqname, 0, "거래량")
        rate = self._get_comm_data(trcode, "", rqname, 0, "등락율")


        self.opt10001_output = ([code, name, Kiwoom.change_format(current_price), volumn, rate])
        #self.opt10001_output.append(Kiwoom.change_format(current_price))

        #print("#### kiwoom _opt10001 finished ")

    ###############################################################################################################

    def send_order(self, rqname, screen_no, acc_no, order_type, code, quantity, price, hoga, order_no):
        self.dynamicCall("SendOrder(QString, QString, QString, int, QString, int, int, QString, QString)",
                         [rqname, screen_no, acc_no, order_type, code, quantity, price, hoga, order_no  ])

    def get_chejan_data(self, fid):
        ret = self.dynamicCall("GetChejanData(int)", fid)
        return ret

    def _receive_chejan_data(self, gubun, item_cnt, fid_list):
        print ("#### _receive_chejan_data.")

        print("#### order 구분 : " + gubun)
        print(self.get_chejan_data(9203))
        print(self.get_chejan_data(302))
        print(self.get_chejan_data(900))
        print(self.get_chejan_data(901))

        print('[TEST] 미체결수량: ' + self.get_chejan_data(902))

        '''
        9203       주문번호
        302        종목명
        900        주문수량
        901        주문가격
        902        미체결수량
        904        원주문번호
        905        주문구분
        908        주문 / 체결시간
        909       체결번호
        910        체결가
        911        체결량
        10        현재가, 체결가, 실시간종가
        '''

    

    ###########################################################################################################
    #   로그인 관련 함수 
    ###########################################################################################################
    def comm_connect(self):
        print("[comm_connect]")
        self.dynamicCall("CommConnect()")

        # event 발생까지 루프 돌며 대기
        self.loginLoop = QEventLoop()
        self.loginLoop.exec_()

    def _event_connect(self, err_code):
        if err_code == 0:
            print("#### OnEventConnect is connected")
        else:
            print("#### OnEventConnect is disconnected")

        self.loginLoop.exit()

    def getLoginInfo(self, tag, isConnectState=False):
        """
        사용자의 tag에 해당하는 정보를 반환한다.

        tag에 올 수 있는 값은 아래와 같다.
        ACCOUNT_CNT: 전체 계좌의 개수를 반환한다.
        ACCNO: 전체 계좌 목록을 반환한다. 계좌별 구분은 ;(세미콜론) 이다.
        USER_ID: 사용자 ID를 반환한다.
        USER_NAME: 사용자명을 반환한다.
        GetServerGubun: 접속서버 구분을 반환합니다.("1": 모의투자, 그외(빈 문자열포함): 실서버)

        :param tag: string
        :param isConnectState: bool - 접속상태을 확인할 필요가 없는 경우 True로 설정.
        :return: string
        """

        if tag == "GetServerGubun":
            info = self.getServerGubun()
        else:
            cmd = 'GetLoginInfo("%s")' % tag
            info = self.dynamicCall(cmd)

        return info

    def getServerGubun(self):
        """
        서버구분 정보를 반환한다.
        리턴값이 "1"이면 모의투자 서버이고, 그 외에는 실서버(빈 문자열포함).

        :return: string
        """

        ret = self.dynamicCall("KOA_Functions(QString, QString)", "GetServerGubun", "")
        return ret

class ParameterTypeError(Exception):
    """ 파라미터 타입이 일치하지 않을 경우 발생하는 예외 """

    def __init__(self, msg="파라미터 타입이 일치하지 않습니다."):
        self.msg = msg

    def __str__(self):
        return self.msg


class ParameterValueError(Exception):
    """ 파라미터로 사용할 수 없는 값을 사용할 경우 발생하는 예외 """

    def __init__(self, msg="파라미터로 사용할 수 없는 값 입니다."):
        self.msg = msg

    def __str__(self):
        return self.msg


class KiwoomProcessingError(Exception):
    """ 키움에서 처리실패에 관련된 리턴코드를 받았을 경우 발생하는 예외 """

    def __init__(self, msg="처리 실패"):
        self.msg = msg

    def __str__(self):
        return self.msg

    def __repr__(self):
        return self.msg


class KiwoomConnectError(Exception):
    """ 키움서버에 로그인 상태가 아닐 경우 발생하는 예외 """

    def __init__(self, msg="로그인 여부를 확인하십시오"):
        self.msg = msg

    def __str__(self):
        return self.msg


class ReturnCode(object):
    """ 키움 OpenApi+ 함수들이 반환하는 값 """

    OP_ERR_NONE = 0 # 정상처리
    OP_ERR_FAIL = -10   # 실패
    OP_ERR_LOGIN = -100 # 사용자정보교환실패
    OP_ERR_CONNECT = -101   # 서버접속실패
    OP_ERR_VERSION = -102   # 버전처리실패
    OP_ERR_FIREWALL = -103  # 개인방화벽실패
    OP_ERR_MEMORY = -104    # 메모리보호실패
    OP_ERR_INPUT = -105 # 함수입력값오류
    OP_ERR_SOCKET_CLOSED = -106 # 통신연결종료
    OP_ERR_SISE_OVERFLOW = -200 # 시세조회과부하
    OP_ERR_RQ_STRUCT_FAIL = -201    # 전문작성초기화실패
    OP_ERR_RQ_STRING_FAIL = -202    # 전문작성입력값오류
    OP_ERR_NO_DATA = -203   # 데이터없음
    OP_ERR_OVER_MAX_DATA = -204 # 조회가능한종목수초과
    OP_ERR_DATA_RCV_FAIL = -205 # 데이터수신실패
    OP_ERR_OVER_MAX_FID = -206  # 조회가능한FID수초과
    OP_ERR_REAL_CANCEL = -207   # 실시간해제오류
    OP_ERR_ORD_WRONG_INPUT = -300   # 입력값오류
    OP_ERR_ORD_WRONG_ACCTNO = -301  # 계좌비밀번호없음
    OP_ERR_OTHER_ACC_USE = -302 # 타인계좌사용오류
    OP_ERR_MIS_2BILL_EXC = -303 # 주문가격이20억원을초과
    OP_ERR_MIS_5BILL_EXC = -304 # 주문가격이50억원을초과
    OP_ERR_MIS_1PER_EXC = -305  # 주문수량이총발행주수의1%초과오류
    OP_ERR_MIS_3PER_EXC = -306  # 주문수량이총발행주수의3%초과오류
    OP_ERR_SEND_FAIL = -307 # 주문전송실패
    OP_ERR_ORD_OVERFLOW = -308  # 주문전송과부하
    OP_ERR_MIS_300CNT_EXC = -309    # 주문수량300계약초과
    OP_ERR_MIS_500CNT_EXC = -310    # 주문수량500계약초과
    OP_ERR_ORD_WRONG_ACCTINFO = -340    # 계좌정보없음
    OP_ERR_ORD_SYMCODE_EMPTY = -500 # 종목코드없음

    CAUSE = {
        0: '정상처리',
        -10: '실패',
        -100: '사용자정보교환실패',
        -102: '버전처리실패',
        -103: '개인방화벽실패',
        -104: '메모리보호실패',
        -105: '함수입력값오류',
        -106: '통신연결종료',
        -200: '시세조회과부하',
        -201: '전문작성초기화실패',
        -202: '전문작성입력값오류',
        -203: '데이터없음',
        -204: '조회가능한종목수초과',
        -205: '데이터수신실패',
        -206: '조회가능한FID수초과',
        -207: '실시간해제오류',
        -300: '입력값오류',
        -301: '계좌비밀번호없음',
        -302: '타인계좌사용오류',
        -303: '주문가격이20억원을초과',
        -304: '주문가격이50억원을초과',
        -305: '주문수량이총발행주수의1%초과오류',
        -306: '주문수량이총발행주수의3%초과오류',
        -307: '주문전송실패',
        -308: '주문전송과부하',
        -309: '주문수량300계약초과',
        -310: '주문수량500계약초과',
        -340: '계좌정보없음',
        -500: '종목코드없음'
    }


class FidList(object):
    """ receiveChejanData() 이벤트 메서드로 전달되는 FID 목록 """

    CHEJAN = {
        9201: '계좌번호',
        9203: '주문번호',
        9205: '관리자사번',
        9001: '종목코드',
        912: '주문업무분류',
        913: '주문상태',
        302: '종목명',
        900: '주문수량',
        901: '주문가격',
        902: '미체결수량',
        903: '체결누계금액',
        904: '원주문번호',
        905: '주문구분',
        906: '매매구분',
        907: '매도수구분',
        908: '주문/체결시간',
        909: '체결번호',
        910: '체결가',
        911: '체결량',
        10: '현재가',
        27: '(최우선)매도호가',
        28: '(최우선)매수호가',
        914: '단위체결가',
        915: '단위체결량',
        938: '당일매매수수료',
        939: '당일매매세금',
        919: '거부사유',
        920: '화면번호',
        921: '921',
        922: '922',
        923: '923',
        949: '949',
        10010: '10010',
        917: '신용구분',
        916: '대출일',
        930: '보유수량',
        931: '매입단가',
        932: '총매입가',
        933: '주문가능수량',
        945: '당일순매수수량',
        946: '매도/매수구분',
        950: '당일총매도손일',
        951: '예수금',
        307: '기준가',
        8019: '손익율',
        957: '신용금액',
        958: '신용이자',
        959: '담보대출수량',
        924: '924',
        918: '만기일',
        990: '당일실현손익(유가)',
        991: '당일신현손익률(유가)',
        992: '당일실현손익(신용)',
        993: '당일실현손익률(신용)',
        397: '파생상품거래단위',
        305: '상한가',
        306: '하한가'
    }


class RealType(object):

    REALTYPE = {
        '주식시세': {
            10: '현재가',
            11: '전일대비',
            12: '등락율',
            27: '최우선매도호가',
            28: '최우선매수호가',
            13: '누적거래량',
            14: '누적거래대금',
            16: '시가',
            17: '고가',
            18: '저가',
            25: '전일대비기호',
            26: '전일거래량대비',
            29: '거래대금증감',
            30: '거일거래량대비',
            31: '거래회전율',
            32: '거래비용',
            311: '시가총액(억)'
        },

        '주식체결': {
            20: '체결시간(HHMMSS)',
            10: '체결가',
            11: '전일대비',
            12: '등락율',
            27: '최우선매도호가',
            28: '최우선매수호가',
            15: '체결량',
            13: '누적체결량',
            14: '누적거래대금',
            16: '시가',
            17: '고가',
            18: '저가',
            25: '전일대비기호',
            26: '전일거래량대비',
            29: '거래대금증감',
            30: '전일거래량대비',
            31: '거래회전율',
            32: '거래비용',
            228: '체결강도',
            311: '시가총액(억)',
            290: '장구분',
            691: 'KO접근도'
        },

        '주식호가잔량': {
            21: '호가시간',
            41: '매도호가1',
            61: '매도호가수량1',
            81: '매도호가직전대비1',
            51: '매수호가1',
            71: '매수호가수량1',
            91: '매수호가직전대비1',
            42: '매도호가2',
            62: '매도호가수량2',
            82: '매도호가직전대비2',
            52: '매수호가2',
            72: '매수호가수량2',
            92: '매수호가직전대비2',
            43: '매도호가3',
            63: '매도호가수량3',
            83: '매도호가직전대비3',
            53: '매수호가3',
            73: '매수호가수량3',
            93: '매수호가직전대비3',
            44: '매도호가4',
            64: '매도호가수량4',
            84: '매도호가직전대비4',
            54: '매수호가4',
            74: '매수호가수량4',
            94: '매수호가직전대비4',
            45: '매도호가5',
            65: '매도호가수량5',
            85: '매도호가직전대비5',
            55: '매수호가5',
            75: '매수호가수량5',
            95: '매수호가직전대비5',
            46: '매도호가6',
            66: '매도호가수량6',
            86: '매도호가직전대비6',
            56: '매수호가6',
            76: '매수호가수량6',
            96: '매수호가직전대비6',
            47: '매도호가7',
            67: '매도호가수량7',
            87: '매도호가직전대비7',
            57: '매수호가7',
            77: '매수호가수량7',
            97: '매수호가직전대비7',
            48: '매도호가8',
            68: '매도호가수량8',
            88: '매도호가직전대비8',
            58: '매수호가8',
            78: '매수호가수량8',
            98: '매수호가직전대비8',
            49: '매도호가9',
            69: '매도호가수량9',
            89: '매도호가직전대비9',
            59: '매수호가9',
            79: '매수호가수량9',
            99: '매수호가직전대비9',
            50: '매도호가10',
            70: '매도호가수량10',
            90: '매도호가직전대비10',
            60: '매수호가10',
            80: '매수호가수량10',
            100: '매수호가직전대비10',
            121: '매도호가총잔량',
            122: '매도호가총잔량직전대비',
            125: '매수호가총잔량',
            126: '매수호가총잔량직전대비',
            23: '예상체결가',
            24: '예상체결수량',
            128: '순매수잔량(총매수잔량-총매도잔량)',
            129: '매수비율',
            138: '순매도잔량(총매도잔량-총매수잔량)',
            139: '매도비율',
            200: '예상체결가전일종가대비',
            201: '예상체결가전일종가대비등락율',
            238: '예상체결가전일종가대비기호',
            291: '예상체결가',
            292: '예상체결량',
            293: '예상체결가전일대비기호',
            294: '예상체결가전일대비',
            295: '예상체결가전일대비등락율',
            13: '누적거래량',
            299: '전일거래량대비예상체결률',
            215: '장운영구분'
        },

        '장시작시간': {
            215: '장운영구분(0:장시작전, 2:장종료전, 3:장시작, 4,8:장종료, 9:장마감)',
            20: '시간(HHMMSS)',
            214: '장시작예상잔여시간'
        },

        '업종지수': {
            20: '체결시간',
            10: '현재가',
            11: '전일대비',
            12: '등락율',
            15: '거래량',
            13: '누적거래량',
            14: '누적거래대금',
            16: '시가',
            17: '고가',
            18: '저가',
            25: '전일대비기호',
            26: '전일거래량대비(계약,주)'
        },

        '업종등락': {
            20: '체결시간',
            252: '상승종목수',
            251: '상한종목수',
            253: '보합종목수',
            255: '하락종목수',
            254: '하한종목수',
            13: '누적거래량',
            14: '누적거래대금',
            10: '현재가',
            11: '전일대비',
            12: '등락율',
            256: '거래형성종목수',
            257: '거래형성비율',
            25: '전일대비기호'
        },

        '주문체결': {
            9201: '계좌번호',
            9203: '주문번호',
            9205: '관리자사번',
            9001: '종목코드',
            912: '주문분류(jj:주식주문)',
            913: '주문상태(10:원주문, 11:정정주문, 12:취소주문, 20:주문확인, 21:정정확인, 22:취소확인, 90,92:주문거부)',
            302: '종목명',
            900: '주문수량',
            901: '주문가격',
            902: '미체결수량',
            903: '체결누계금액',
            904: '원주문번호',
            905: '주문구분(+:현금매수, -:현금매도)',
            906: '매매구분(보통, 시장가등)',
            907: '매도수구분(1:매도, 2:매수)',
            908: '체결시간(HHMMSS)',
            909: '체결번호',
            910: '체결가',
            911: '체결량',
            10: '체결가',
            27: '최우선매도호가',
            28: '최우선매수호가',
            914: '단위체결가',
            915: '단위체결량',
            938: '당일매매수수료',
            939: '당일매매세금'
        },

        '잔고': {
            9201: '계좌번호',
            9001: '종목코드',
            302: '종목명',
            10: '현재가',
            930: '보유수량',
            931: '매입단가',
            932: '총매입가',
            933: '주문가능수량',
            945: '당일순매수량',
            946: '매도매수구분',
            950: '당일총매도손익',
            951: '예수금',
            27: '최우선매도호가',
            28: '최우선매수호가',
            307: '기준가',
            8019: '손익율'
        },

        '주식시간외호가': {
            21: '호가시간(HHMMSS)',
            131: '시간외매도호가총잔량',
            132: '시간외매도호가총잔량직전대비',
            135: '시간외매수호가총잔량',
            136: '시간외매수호가총잔량직전대비'
        }
    }

if __name__ == "__main__":
    app = QApplication(sys.argv)
    kiwoom = Kiwoom()
    kiwoom.comm_connect()

    kiwoom.reset_opw00018_output()
    account_number = kiwoom.getLoginInfo("ACCNO")
    account_number = account_number.split(';')[0]


    # opt10081 TR 요청
    '''
    kiwoom.set_input_value("종목코드", "039490")
    kiwoom.set_input_value("틱범위", "10")
    kiwoom.set_input_value("수정주가구분", 1)

    kiwoom.comm_rq_data("opt10080_req", "opt10080", 0, "0101")
    '''

    df_minute_data = kiwoom.get_min_chart("039490", "5")
    #print(df_minute_data)

    '''
    kiwoom.set_input_value("계좌번호", account_number)
    kiwoom.comm_rq_data("opw00018_req", "opw00018", 0, "2000")
    print(kiwoom.opw00018_output['single'])
    print(kiwoom.opw00018_output['multi'])
    '''


    '''
    code_list = kiwoom.get_code_list_by_market('10')

    print(kiwoom.get_master_code_name("039490"))
    print("#### Get the code list.... ")
    for code in code_list:
        print(code, end=" ")
    print("#### finished....")

    
    print("#### opt10081 TR 요청")
    # opt10081 TR 요청
    kiwoom.set_input_value("종목코드", "039490")
    kiwoom.set_input_value("기준일자", "20190124")
    kiwoom.set_input_value("수정주가구분", 1)

    kiwoom.comm_rq_data("opt10081_req", "opt10081", 0, "0101")
    
    
    while kiwoom.remained_data == True:
        time.sleep(TR_REQ_TIME_INTERVAL)
        kiwoom.set_input_value("종목코드", "039490")
        kiwoom.set_input_value("기준일자", "20170224")
        kiwoom.set_input_value("수정주가구분", 1)
        kiwoom.comm_rq_data("opt10081_req", "opt10081", 2, "0101")
    

    print("#### D+2 계정 확인....")
    kiwoom.set_input_value("계좌번호", "8112339511")
    kiwoom.set_input_value("비밀번호", "1004")
    kiwoom.comm_rq_data("opw00001_req", "opw00001", 0, "2000")

    print(kiwoom.d2_deposit)

    print("#### opw00018_req....")
    account_number = kiwoom.get_login_info("ACCNO")
    account_number = account_number.split(';')[0]

    kiwoom.set_input_value("계좌번호", account_number)
    kiwoom.comm_rq_data("opw00018_req", "opw00018", 0, "2000")
    '''
