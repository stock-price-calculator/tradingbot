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
        # userInfo = self.kiwoom.GetLoginInfo()
        print(self.kiwoom.GetLoginInfo("ACCOUNT_CNT"))
        print(self.kiwoom.GetLoginInfo("ACCNO"))
        print(self.kiwoom.GetLoginInfo("USER_ID"))
        print(self.kiwoom.GetLoginInfo("USER_NAME"))
        print(self.kiwoom.GetLoginInfo("KEY_BSECGB"))
        print(self.kiwoom.GetLoginInfo("FIREW_SECGB"))
        print(name)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()