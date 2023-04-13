import sys

from PyQt5.QAxContainer import *
from PyQt5.QtCore import QEventLoop
from PyQt5.QtWidgets import *

from kiwoom import Kiwoom

class MyWindow():
    def __init__(self):
        super().__init__()
        self.kiwoom = Kiwoom()

        while True:
            n = int(input("메뉴번호를 선택하세요 : "))
            if n == 1:  # 시장가 매수
                buy_order = self.kiwoom.send_buy_order("8043137211", "005930", 1, 0, "시장가")
                print("결과값 : ", buy_order)
            elif n == 2: # 시장가 매도
                sell_order = self.kiwoom.send_sell_order("8043137211", "005930", 1, 0, "시장가")
                print("결과값 : ", sell_order)
            elif n == 3: # 테스트
                self.start_test()
            elif n == 4: # 예수금
                self.kiwoom.get_detail_account_info("8043137211")
            elif n == 5: #총수익률
                self.kiwoom.get_detail_account_mystock("8043137211")
            elif n == 6: # 계좌별주문체결내역상세요청
                self.kiwoom.get_trading_record(20, "8043137211", "1", "0", "")
            elif n == 7: # 주식분봉차트조회요청
                self.kiwoom.get_minutes_data("005930", "5")

    def start_test(self):
        # tr 요청
        name = self.kiwoom.get_master_code_name("005930")

        connectState = self.kiwoom.get_connect_state()
        lastPrice = self.kiwoom.get_master_last_price("005930")

        print("연결상태 : %d" % connectState)
        print("유저정보")
        print("------------------------------")
        print("계좌 수 : " + self.kiwoom.get_login_info("ACCOUNT_CNT"))
        print("계좌 번호 : " + self.kiwoom.get_login_info("ACCNO"))
        print(self.kiwoom.get_login_info("USER_ID"))
        print(self.kiwoom.get_login_info("USER_NAME"))
        print("------------------------------")
        print(name)
        print("------------------------------")
        print("전일가 : %s" % lastPrice)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    #window.show()
    app.exec_()