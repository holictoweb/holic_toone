


class snipet:
    def test_creon(self):
        codemgr = win32com.client.Dispatch("CpUtil.CpCodeMgr")
        #kospi = codemgr.GetStockListByMarket(1)
        #print(kospi)
        #print(len(kospi)) 

        kosdaq = codemgr.GetStockListByMarket(2)
        print(len(kosdaq))

        #코드를 이름으로 변경
        name = codemgr.CodeToName("A005930")
        print(name)

        for code in kosdaq:
            name =codemgr.CodeToName(code)
            #print(code, name)

        # ETF이고 A900050과 A900140은 외국 주권이며 Q500001~Q500003은 ETN
        # 데이터를 쌓고자 하는 종목 선정


        ## 일봉 데이터
        instStockChart = win32com.client.Dispatch("CpSysDib.StockChart")
        # SetInputValue
        instStockChart.SetInputValue(0, "A003540")
        instStockChart.SetInputValue(1, ord('2'))
        instStockChart.SetInputValue(4, 1000)
        instStockChart.SetInputValue(5, (0, 2, 3, 4, 5, 8))
        instStockChart.SetInputValue(6, ord('D'))
        instStockChart.SetInputValue(9, ord('1'))

        # BlockRequest
        instStockChart.BlockRequest()

        # GetHeaderValue
        numData = instStockChart.GetHeaderValue(3)
        numField = instStockChart.GetHeaderValue(1)

        # GetDataValue
        for i in range(numData):
            for j in range(numField):
                print(instStockChart.GetDataValue(j, i), end=" ")
       