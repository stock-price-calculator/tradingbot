import sys
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
import pythoncom


class Kiwoom:
    def __init__(self):
        self.login = False
        self.ocx = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.ocx.OnEventConnect.connect(self.OnEventConnect)

    def CommConnect(self):
        self.ocx.dynamicCall("CommConnect()")
        while not self.login:
            pythoncom.PumpWaitingMessages()

    def GetMasterCodeName(self, code):
        name = self.ocx.dynamicCall("GetMasterCodeName(QString)", code)
        return name

    def OnEventConnect(self, err_code):
        self.login = True


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.kiwoom = Kiwoom()
        self.kiwoom.CommConnect()
        name = self.kiwoom.GetMasterCodeName("005930")
        print(name)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()