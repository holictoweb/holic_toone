from pywinauto import application
from pywinauto import timings
import time
import os
'''
swapy를 통해 윈도우 창의 각각의 항목들 정보를 확인 가능함. 
https://github.com/pywinauto/SWAPY
'''
app = application.Application()
app.start("C:\\KiwoomFlash3\\Bin\\NKMiniStarter.exe")

title = "번개3 Login"
dlg = timings.WaitUntilPasses(20, 0.5, lambda: app.window_(title=title))

pass_ctrl = dlg.Edit2
pass_ctrl.SetFocus()
pass_ctrl.TypeKeys('1004cjst')

cert_ctrl = dlg.Edit3
cert_ctrl.SetFocus()
cert_ctrl.TypeKeys('!1004cjstk')

btn_ctrl = dlg.Button0
btn_ctrl.Click()


'''일정 시간 후에 프로세스 킬 '''
time.sleep(50)
os.system("taskkill /im nkmini.exe")