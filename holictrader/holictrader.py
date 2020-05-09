# -*- coding: utf-8 -*-
'''
모의투자 계좌 : 8112339511

066570 LG전자
005930 삼성전자
'''


'''
Klasa is class
from folder.file import Klasa

from folder import file
k = file.Klasa()

import folder.file as myModule
k = myModule.Klasa()
'''

import os
import pprint

print (os.environ['PATH'])
pprint.pprint(os.environ['PATH'].split(';'))

import sys, time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
''' pyqt 재 설치 오류
ERROR conda.core.link:_execute(507): An error occurred while uninstalling package 'defaults::pyqt-5.6.0-py35_2'.
FileExistsError(17, '파일이 이미 있으므로 만들 수 없습니다')
Attempting to roll back.

Rolling back transaction: done

FileExistsError(17, '파일이 이미 있으므로 만들 수 없습니다')
'''

#반복 가능 객체 확인.
import collections

# 머신러닝 관련
import pandas as pd
#import pylab

# local class
from Kiwoom import Kiwoom, ParameterTypeError, ParameterValueError, KiwoomProcessingError, KiwoomConnectError


#import holic_agent


#import settings
#import data_manager
#from policy_learner import PolicyLearner


# ui load
form_class = uic.loadUiType("holictrader.ui")[0]

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        #self.show()
   
        #########################################################################
        # Load Class
        self.kiwoom = Kiwoom()
        self.kiwoom.comm_connect()

        #self.holicAgent = holic_agent.HolicAgent()
        self.mholicstock = modelholicstock.ModelHolicStock()

        self.server = self.kiwoom.getLoginInfo("GetServerGubun")

        if len(self.server) == 0 or self.server != "1":
            self.serverGubun = "==== PROD ===="
        else:
            self.serverGubun = "DEV"

        #########################################################################
        #메인 타이머
        self.timer = QTimer(self)
        self.timer.start(1000)
        self.timer.timeout.connect(self.timeout)

        # Timer auto 실행
        self.timer_auto = QTimer(self)
        self.timer_auto.start(1000 * 10)
        self.timer_auto.timeout.connect(self.timer_auto_timeout)



        accouns_num = int(self.kiwoom.getLoginInfo("ACCOUNT_CNT"))
        accounts = self.kiwoom.getLoginInfo("ACCNO")
        accounts_list = accounts.split(';')[0:accouns_num]
        self.accountComboBox.addItems(accounts_list)

        #########################################################################
        # Event Callback connect
        self.pushButton.clicked.connect(self.send_order)
        self.lineEdit.textChanged.connect(self.code_changed)
        self.pushButton_2.clicked.connect(self.check_balance)

        self.btn_autoorder.clicked.connect(self.start_auto_order)
        self.btn_stopautoorder.clicked.connect(self.stop_auto_order)

        self.btn_start_mon.clicked.connect(self.automated_stock_mon)

        self.btn_start_analysis.clicked.connect(self.analysis_condition)

        #########################################################################
        # 메인 변수
        self.df_condition = pd.DataFrame()
        self.df_anaysis = pd.DataFrame()

    ##################################################################################################### Analisys

    def automated_stock_mon(self):
        '''
        DB에 저장된 항목 / 조건검색 항목 DB 저장.

        :return:
        '''
        print("[automated_stock_mon]")

        #df_minute_data = self.kiwoom.get_min_chart("039490", "5")
        #print(df_minute_data)

        # CONDITIN 종목에 대한 정보 확보
        self.kiwoom.get_condition()

        for idx in range(len(self.kiwoom.condition_name_list)):
            #print(self.kiwoom.condition_name_list[idx])
            if self.kiwoom.condition_name_list[idx] != '':
                self.kiwoom.send_condition(idx)
        print("#### total condition list : " + self.kiwoom.conditionStockItem)
        # 학습 대상 선정

        ''' 매수가 완료된 종목에 대한 변동이 필요함.  '''
        # stock list 획득
        #self.mystock_list = self.mholicstock.read_my_stock('buy')
        #print("#### total mystock list : " + self.mystock_list)
        # [0. 조건검색 결과 + 저장된 리스트 ]
        #for j in range(len(self.mystock_list)):
        #    self.kiwoom.conditionStockItem += str(self.mystock_list[j][0]) + ';'

        #print(self.kiwoom.conditionStockItem)

        # [1. kiwoom get DATA ]
        self.kiwoom.comm_kw_rq_data(self.kiwoom.conditionStockItem)

        # [2. 조회된 데이타에 대한 DATA 분석  ret=df ]
        self.df_condition = pd.DataFrame.from_dict(self.kiwoom.automatedStockDict, orient='index')
        print(self.df_condition)
        #print(self.df_main_list.loc[:, ['code']].to_dict() )


        # [3. Display Qt MainTableWidget ]
        dict_count = len(self.kiwoom.automatedStockDict)
        header_list = ['signal', 'weight', 'name', 'cprice', 'updown', 'rate', 'volume', 'code', 'date']
        column_idx_lookup = {header_list[i]: i for i in range(0, len(header_list))}
        #column_idx_lookup = {'date': 0, 'code': 1, 'name': 2, 'cprice': 3, 'updown': 4, 'rate': 5, 'volume': 6}
        #print(column_idx_lookup)

        self.tableAutomatedStock.setColumnCount( len(header_list) )
        self.tableAutomatedStock.setRowCount(dict_count)
        self.tableAutomatedStock.setHorizontalHeaderLabels(header_list)

        if not isinstance(self.kiwoom.automatedStockDict, collections.Iterable):
            raise ParameterTypeError()

        #print("loop start ")
        for row, stocK_value in enumerate(self.kiwoom.automatedStockDict.items()):
            #print(stocK_value[1])

            for key, value in stocK_value[1].items():
                #print("key : {}, value: {}".format(key, value))
                col = column_idx_lookup[key]

                item = QTableWidgetItem(value)

                if key == 'name':
                    item.setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
                else:
                    item.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
                self.tableAutomatedStock.setItem(row, col, item)

        self.tableAutomatedStock.resizeRowsToContents()
        self.tableAutomatedStock.resizeColumnsToContents()


    def analysis_condition(self):
        # [3. 각종목에 대한 분봉 데이타 획득 1분 / 3분 / 5분 ]
        for index, row in self.df_condition.iterrows():
            print(row['name'], row['code'])
            self.df_anaysis = self.kiwoom.get_min_chart(row['code'], '5')
            self.df_anaysis['code'] = row['code']
            #print(self.df_anaysis)
            #sself.mholicstock.insert_stock_data(self.df_anaysis)

            prep_data = data_manager.preprocess(self.df_anaysis)

            print(prep_data)
    ###############################################################
    #   자동주문   및 수동 주문                                   #
    ###############################################################

    def init_auto_order(self):
        self.selectedCondition = '' #선택된 조건식

        self.profit_Rate = '' #이익률
        self.loss_Rate = '' #손절률

        self.limit_Buying_Per_Stock = '' #종목당 매수금액
        self.limit_Buying_Stock_Number = '' #매입 제한 종목개수

        # 한번의 주문이 진행 되고 나면 다시 셋팅 하는 과정을 가져감.

        # 예수금상세현황요청을 하여야 하는지 종목 갯수에 대한 확인을 진행 해야 하는지

    def start_auto_order(self):
        # 자동 주문
        print("[ start_auto_order ]")
        print(self.df_machined_stock_item)

        # 시간에 따라 타임 아웃 나올때 마다 주문 프로세스를 호출함.
        self.isAutomaticOrder = True

    def stop_auto_order(self):
        print("[ stop_auto_order ] Finished Order... ")
        self.isAutomaticOrder = False
    
    def set_auto_order_stocks(self):
        fileList = ["buy_list.txt", "sell_list.txt"]
        automatedStocks = []

        try:
            for file in fileList:
                # utf-8로 작성된 파일을
                # cp949 환경에서 읽기위해서 encoding 지정
                with open(file, 'rt', encoding='utf-8') as f:
                    stocksList = f.readlines()
                    automatedStocks += stocksList
        except Exception as e:
            e.msg = "setAutomatedStocks() 에러"
            self.showDialog('Critical', e)
            return

        # 테이블 행수 설정
        cnt = len(automatedStocks)
        self.automatedStocksTable.setRowCount(cnt)

        # 테이블에 출력
        for i in range(cnt):
            stocks = automatedStocks[i].split(';')

            for j in range(len(stocks)):
                if j == 1:
                    name = self.kiwoom.getMasterCodeName(stocks[j].rstrip())
                    item = QTableWidgetItem(name)
                else:
                    item = QTableWidgetItem(stocks[j].rstrip())

                item.setTextAlignment(Qt.AlignVCenter | Qt.AlignCenter)
                self.automatedStocksTable.setItem(i, j, item)

        self.automatedStocksTable.resizeRowsToContents()


    def send_order(self):
        order_type_lookup = {'신규매수': 1, '신규매도': 2, '매수취소': 3, '매도취소': 4}
        hoga_lookup = {'지정가': "00", '시장가': "03"}

        account = self.accountComboBox.currentText()
        order_type = self.comboBox_2.currentText()
        code = self.lineEdit.text()
        hoga = self.comboBox_3.currentText()
        num = self.spinBox.value()
        price = self.spinBox_2.value()

        self.kiwoom.send_order("send_order_req", "0101", account, order_type_lookup[order_type], code, num, price,
                               hoga_lookup[hoga], "")
        
        # 성공 여부에 대한 확인도 필요
        self.reset_order()

    def reset_order(self):
        print("#### reset order ")
        self.accountComboBox.setCurrentIndex(0)
        self.comboBox_2.setCurrentIndex(0)
        self.lineEdit.setText('')
        self.comboBox_3.setCurrentIndex(0)
        self.spinBox.setValue(0)
        self.spinBox_2.setValue(0)


    ###############################################################
    #   예수금 및 보유 종목 정보
    ###############################################################
    def check_balance(self):
        print("#### cb_check_balance called.")

        self.kiwoom.reset_opw00018_output()
        account_number = self.kiwoom.getLoginInfo("ACCNO")
        account_number = account_number.split(';')[0]

        self.kiwoom.set_input_value("계좌번호", account_number)
        self.kiwoom.comm_rq_data("opw00018_req", "opw00018", 0, "2000")

        while self.kiwoom.remained_data:
            time.sleep(0.2)
            self.kiwoom.set_input_value("계좌번호", account_number)
            self.kiwoom.comm_rq_data("opw00018_req", "opw00018", 2, "2000")

        # opw00001
        self.kiwoom.set_input_value("계좌번호", account_number)
        self.kiwoom.comm_rq_data("opw00001_req", "opw00001", 0, "2000")

        # balance
        item = QTableWidgetItem(self.kiwoom.d2_deposit)
        item.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
        self.tableWidget.setItem(0, 0, item)

        for i in range(1, 6):
            item = QTableWidgetItem(self.kiwoom.opw00018_output['single'][i - 1])
            item.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
            self.tableWidget.setItem(0, i, item)

        self.tableWidget.resizeRowsToContents()
        self.tableWidget.resizeColumnsToContents();

        # Item list
        item_count = len(self.kiwoom.opw00018_output['multi'])
        self.tableWidget_2.setRowCount(item_count)

        for j in range(item_count):
            row = self.kiwoom.opw00018_output['multi'][j]
            for i in range(len(row)):
                item = QTableWidgetItem(row[i])
                item.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
                self.tableWidget_2.setItem(j, i, item)

        self.tableWidget_2.resizeRowsToContents()
        self.tableWidget_2.resizeColumnsToContents();


    ###############################################################
    #   공통함수                                           #
    ###############################################################
    def code_changed(self):
        code = self.lineEdit.text()
        name = self.kiwoom.get_master_code_name(code)
        self.lineEdit_2.setText(name)

    def timeout(self):
        """ 타임아웃 이벤트가 발생하면 호출되는 메서드 """
        
        current_time = QTime.currentTime()
        text_time = current_time.toString("hh:mm:ss")
        time_msg = "현재시간: " + text_time

        state = self.kiwoom.GetConnectState()
        if state == 1:
            state_msg = "server connected"
        else:
            state_msg = "not connected"

        self.statusbar.showMessage(state_msg + " | " + time_msg)

    def timer_auto_timeout(self):
        print('time_auto ---- ')

        if self.checkBox.isChecked():
            self.check_balance()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()


