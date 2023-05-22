import sys

from PyQt5.QAxContainer import *
from PyQt5.QtCore import QEventLoop
from PyQt5.QtWidgets import *
import constants
from kiwoom import Kiwoom
from account.transmission import Kiwoom_Send_Account
from order.trade import Kiwoom_Trade
from market.stick_data_sender import Kiwoom_Price

class TradingBot():
    def __init__(self):
        super().__init__()
        self.kiwoom = Kiwoom()
        self.kiwoom_account = Kiwoom_Send_Account(self.kiwoom)
        self.kiwoom_trade = Kiwoom_Trade(self.kiwoom)
        self.kiwoom_price = Kiwoom_Price(self.kiwoom)

        while True:
            n = int(input("메뉴번호를 선택하세요 : "))
            if n == 1:  # 시장가 매수
                buy_order = self.kiwoom_trade.send_buy_order(constants.ACCOUNT, constants.SAMSUNG_CODE, 1, 0, "시장가")
                print("결과값 : ", buy_order)
            elif n == 2: # 시장가 매도
                sell_order = self.kiwoom_trade.send_sell_order(constants.ACCOUNT, constants.SAMSUNG_CODE, 1, 0, "시장가")
                print("결과값 : ", sell_order)
            if n == 3: # 테스트
                self.start_test()
            elif n == 4: # 예수금
                self.kiwoom_account.get_detail_account_info(constants.ACCOUNT)
            elif n == 5: #총수익률
                self.kiwoom_account.get_detail_account_mystock(constants.ACCOUNT)
            elif n == 6: # 계좌별주문체결내역상세요청
                self.kiwoom_account.get_trading_record(30, constants.ACCOUNT, "1", "0", "")
            elif n == 7: # 주식분봉차트조회요청
                self.kiwoom_price.send_minutes_chart_data(constants.SAMSUNG_CODE, "5", 3)
            elif n == 8:  # 주식일봉차트조회요청
                self.kiwoom_price.send_day_chart_data(constants.SAMSUNG_CODE, "20230413")
            elif n == 9: # 주식주봉차트조회요청
                self.kiwoom_price.send_week_chart_data(constants.SAMSUNG_CODE,"20160101","20230413")

    def start_test(self):
        # tr 요청
        name = self.kiwoom.get_master_code_name(constants.SAMSUNG_CODE)
        connectState = self.kiwoom.get_connect_state()
        lastPrice = self.kiwoom.get_master_last_price(constants.SAMSUNG_CODE)

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
    window = TradingBot()
    #window.show()
    app.exec_()