import sys
from PyQt5.QtWidgets import *
from kiwoom import Kiwoom
from PyQt5.QAxContainer import *
import pythoncom

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.kiwoom = Kiwoom()
        self.kiwoom.CommConnect()

        # tr 요청
        name = self.kiwoom.GetMasterCodeName("005930")

        connectState = self.kiwoom.GetConnectState()
        lastPrice = self.kiwoom.GetMasterLastPrice("005930")

        print("연결상태 : %d" %connectState)
        print("유저정보")
        print("------------------------------")
        print(self.kiwoom.GetLoginInfo("ACCOUNT_CNT"))
        print(self.kiwoom.GetLoginInfo("ACCNO"))
        print(self.kiwoom.GetLoginInfo("USER_ID"))
        print(self.kiwoom.GetLoginInfo("USER_NAME"))
        print(self.kiwoom.GetLoginInfo("KEY_BSECGB"))
        print(self.kiwoom.GetLoginInfo("FIREW_SECGB"))
        print("------------------------------")
        print(name)
        print("------------------------------")
        print("전일가 : %s" %lastPrice)






if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()