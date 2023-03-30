import sys

import pythoncom
from PyQt5.QAxContainer import *
from PyQt5.QtWidgets import *

from kiwoom import Kiwoom

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.kiwoom = Kiwoom()
        self.kiwoom.comm_connect()

        # tr 요청
        name = self.kiwoom.get_master_code_name("005930")

        connectState = self.kiwoom.get_connect_state()
        lastPrice = self.kiwoom.get_master_last_price("005930")

        print("연결상태 : %d" %connectState)
        print("유저정보")
        print("------------------------------")
        print("계좌 수 : " + self.kiwoom.get_login_info("ACCOUNT_CNT"))
        print("계좌 번호 : " + self.kiwoom.get_login_info("ACCNO"))
        print(self.kiwoom.get_login_info("USER_ID"))
        print(self.kiwoom.get_login_info("USER_NAME"))
        print("------------------------------")
        print(name)
        print("------------------------------")
        print("전일가 : %s" %lastPrice)



        #buy_order = self.kiwoom.sendBuyOrder("8043137211", "005930", 1, 0, "시장가")
        #print(buy_order)

        sell_order = self.kiwoom.sendSellOrder("8043137211", "005930", 1, 0, "시장가")
        print(sell_order)
        #print(self.kiwoom.get_chejan_data(11))





if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()