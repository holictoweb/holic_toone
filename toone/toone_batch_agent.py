from toone_creon_basic import * 
from toone_azuresql import *

class TooneBatchAgent:
    
    def __init__(self):
        self.tooneAzuresql = TooneAzuresql()
        self.creoncontrol = CreonControl()

        self.obj_CpTdUtil = win32com.client.Dispatch("CpTrade.CpTdUtil")
        self.obj_CpTd0311 = win32com.client.Dispatch("CpTrade.CpTd0311")
        

#############################################
    
    def agent_batch(self, stock_type):
        target_list = self.creoncontrol.get_kosdaq_code()
        #print(target_list)
        
        if stock_type == 'D':
            #target_list =['005940', '035420']
            df_day = pd.DataFrame( self.creoncontrol.creon_chart_day(target_list, 0,'20180101','20201231') ) 
            self.tooneAzuresql.set_chart_day(df_day)
        elif stock_type == 'M':
            df_min = pd.DataFrame( self.creoncontrol.creon_chart_min(target_list, 0,'20191111','20191111') ) 
            self.tooneAzuresql.set_chart_min(df_min)
        else:    
            target_list =['005940', '035420']
            df_min = pd.DataFrame( self.creoncontrol.creon_chart_min(target_list, 0,'20191111','20191111') ) 
            print(df_min)
            self.tooneAzuresql.set_chart_min(df_min)
        

if __name__ == '__main__':
    tooneBatchAgent = TooneBatchAgent()

    
    #tooneagent.agent()
    stock_df = tooneBatchAgent.agent_batch('D')
    #print (stock_df.header())






    
    

   