import win32com.client

inCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")

print (inCpCybos.IsConnect)


if inCpCybos.IsConnect == 1:
    print("연결 정상")
else:
    print("연결 끊김") 