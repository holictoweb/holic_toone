import win32com.client
import time

from co1_creon_control import *

class SetTargetStork:


    def __init__ (self):
        self.obj_stockChart = win32com.client.Dispatch("CpSysDib.StockChart")
        self.obj_CpCodeMgr = win32com.client.Dispatch("CpUtil.CpCodeMgr")

        creoncontrol = CreonControl()


    def target_market(self):
        code_list = self.objCpCodeMgr.GetStockListByMarket(1)
        

        target_list = []
        for code in codeList:
            if CheckVolumn( code) == 1:
                target_list.append(code)
                print(code)
            time.sleep(1)

    def CheckVolumn(self, code):
        df_count = creoncontrol.creon_count(code, 60)

        # GetData
        volumes = []
        numData = df_count
        for i in range(numData):
            volume = self.objstockChart.GetDataValue(0, i)
            volumes.append(volume)


        # Calculate average volume
        averageVolume = (sum(volumes) - volumes[0]) / (len(volumes) -1)

        if(volumes[0] > averageVolume * 10):
            return 1
        else:
            return 0

if __name__ == "__main__":
    

    