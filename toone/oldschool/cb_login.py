import win32com.client
from pywinauto import application
import os, time


class Creon:
    def __init__(self):
        self.obj_CpUtil_CpCybos = win32com.client.Dispatch('CpUtil.CpCybos')

    def kill_client(self):
        os.system('taskkill /IM coStarter* /F /T')
        os.system('taskkill /IM CpStart* /F /T')
        os.system('taskkill /IM DibServer* /F /T')
        os.system('wmic process where "name like \'%coStarter%\'" call terminate')
        os.system('wmic process where "name like \'%CpStart%\'" call terminate')
        os.system('wmic process where "name like \'%DibServer%\'" call terminate')

    def connect(self, id_, pwd, pwdcert):
        if not self.connected():
            self.disconnect()
            self.kill_client()
            app = application.Application()
            app.start(
                'C:\CREON\STARTER\coStarter.exe /prj:cp /id:{id} /pwd:{pwd} /pwdcert:{pwdcert} /autostart'.format(
                    id=id_, pwd=pwd, pwdcert=pwdcert
                )
            )
        while not self.connected():
            time.sleep(1)
        return True

    def connected(self):
        b_connected = self.obj_CpUtil_CpCybos.IsConnect
        if b_connected == 0:
            return False
        return True

    def disconnect(self):
        if self.connected():
            self.obj_CpUtil_CpCybos.PlusDisconnect()
