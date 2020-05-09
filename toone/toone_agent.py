from db1_data_control import *
from toone_creon_basic import * 

class TooneAgent:
    TRADING_CHARGE = 0.015  # 거래 수수료 미고려 (일반적으로 0.015%)
    TRADING_TAX = 0.3  # 거래세 미고려 (실제 0.3%)

    ACTION_BUY = 0  # 매수
    ACTION_SELL = 1  # 매도
    ACTION_HOLD = 2  # 홀딩

    # 1. Agent가 계속적으로 수행
    # 2. 전일 대비 거래량 급등 종목 조회 ( 5분 단위로 조회 ) target테이블에 저장 
    # 3.  1분 단위로 target stock에 대한 1분봉 조회 
    # 

    def __init__(self):
        self.datacontrol = DataControl()
        self.creoncontrol = CreonControl()

        self.obj_CpTdUtil = win32com.client.Dispatch("CpTrade.CpTdUtil")
        self.obj_CpTd0311 = win32com.client.Dispatch("CpTrade.CpTd0311")
        
    def reset_order(self):
        # 주문 초기화
        ret = self.obj_CpTdUtil.TradeInit(0)

    def act(self, action):
        #if action == ACTION_BUY:
        df_target = self.datacontrol.get_target_stock()
        for target in df_target.iterrows():
            if target['signal'] == 'BUY':
                status = self.order('BUY')
            elif target['signal'] == 'SELL':
                status = self.order('SELL')

    def order(self, code):
        # init
        self.reset_order()
        # 주식 매수 주문 설정
        account_number = self.obj_CpTdUtil.AccountNumber[0]       # 계좌번호 얻기
        print(account_number)
        
        self.obj_CpTd0311.SetInputValue(0, "2")                   # 1: 매도, 2: 매수
        self.obj_CpTd0311.SetInputValue(1, account_number)        # 계좌번호
        self.obj_CpTd0311.SetInputValue(2, '01')                  # '01': 주식, '02': 선물/옵션, '03': 주식 + 선물옵션
        self.obj_CpTd0311.SetInputValue(3, 'A000020')            # 동화약품
        self.obj_CpTd0311.SetInputValue(4, 10)                    # 매수수량
        self.obj_CpTd0311.SetInputValue(5, 8200)                  # 매수단가
        self.obj_CpTd0311.BlockRequest()

##############################################
# check balance


##############################################
# Agent
# data 수집

    def batch_day(self):
        print(">>> day batch ")

    def batch_min(self):   
        print(">>> 3min batch")

# database action signal check
    def data_signal(self):
        print(">>> data signal")
        # stocksignal
        # df_data = self.datacontrol()


##############################################

    def agent(self):
        
        #0. target data (from day batch )
        df_target = self.datacontrol.get_target_stock()
        print(df_target.head())

        while (1):
            curtime = time.strftime('%H%M%S')
            checktime = time.strftime('%M%S')
            print (">>> time : " + curtime)
            time.sleep(30)

        #1. Agent 시작
            if checktime % 1 == 0:
                target_list = self.datacontrol.get_target_stock()
                df_min = self.creoncontrol.creon_chart_min(target_list, 0, curtime, '')
                print(df_min.head())
                self.datacontrol.set_stock_min(df_min)
        
        #2-3. db3_analysis 
        
        #3. 종료
            

    def test_agent(self):
        slist =['005940', '035420']
        df_min = self.creoncontrol.creon_chart_min(slist, 0,'20191111','20191111')
        print(df_min.head())
        self.datacontrol.set_stock_min(df_min)

if __name__ == '__main__':
    tooneagent = TooneAgent()
    #tooneagent.agent()
    tooneagent.test_agent()






    
    

   