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
        name1 = self.kiwoom.SetInputValue("종목코드", "005930")
        name2 = self.kiwoom.CommRqData("opt10001", "opt10001", 0, "0101")

        print(name)
        print(name1)
        print(name2)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()