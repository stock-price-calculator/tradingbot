import sys


import constants
from kiwoom import Kiwoom
# from account.account_sender import Kiwoom_Send_Account
# from order.trade import Kiwoom_Trade
# from market.stick_data_sender import Kiwoom_Price

from flask import Flask, jsonify
from PyQt5.QtWidgets import QApplication
from PyQt5.QAxContainer import QAxWidget
import sys
from PyQt5.QAxContainer import *
from PyQt5.QtCore import QEventLoop
from PyQt5.QtWidgets import *

# class TradingBot():
#     def __init__(self):
#
#         self.kiwoom = Kiwoom()
#         # self.kiwoom_account = Kiwoom_Send_Account(self.kiwoom)
#         # self.kiwoom_trade = Kiwoom_Trade(self.kiwoom)
#         # self.kiwoom_price = Kiwoom_Price(self.kiwoom)
#
#         while True:
#             n = int(input("메뉴번호를 선택하세요 : "))
#             if n == 1:  # 시장가 매수
#                 buy_order = self.kiwoom_trade.send_buy_order(constants.ACCOUNT, constants.LG_CODE, 1, 0, "시장가")
#                 print("결과값 : ", buy_order)
#             elif n == 2: # 시장가 매도
#                 sell_order = self.kiwoom_trade.send_sell_order(constants.ACCOUNT, constants.LG_CODE, 1, 0, "시장가")
#                 print("결과값 : ", sell_order)
#             if n == 3: # 테스트
#                 self.start_test()
#             elif n == 4: # 예수금
#                 self.kiwoom_account.send_detail_account_info(constants.ACCOUNT)
#             elif n == 5: #총수익률 - 총 매입금액, 수익률
#                 self.kiwoom_account.send_detail_account_mystock(constants.ACCOUNT)
#             elif n == 6: # 계좌별주문체결내역상세요청 - 날짜별 체결내역
#                 self.kiwoom_account.send_trading_record(150, constants.ACCOUNT, "1", "0", "")
#             elif n == 7: # 주식분봉차트조회요청
#                 self.kiwoom_price.send_minutes_chart_data(constants.SAMSUNG_CODE, "5")
#             elif n == 8:  # 주식일봉차트조회요청
#                 self.kiwoom_price.send_day_chart_data(constants.SAMSUNG_CODE, "20230413")
#             elif n == 9: # 주식주봉차트조회요청
#                 self.kiwoom_price.send_week_chart_data(constants.SAMSUNG_CODE,"20160101","20230413")
#             elif n == 10: # 계좌수익률요청 - 보유 주식량 확인 가능
#                 self.kiwoom_account.send_price_earning_ratio(constants.ACCOUNT)
#             elif n == 11: # 체결요청
#                 self.kiwoom_account.send_conclude_data(constants.SAMSUNG_CODE,"1","0",constants.ACCOUNT)
#             elif n == 12: # 일자별실현손익요청
#                 self.kiwoom_account.send_day_earn_data(constants.ACCOUNT, "20230101", "20230531")


app = Flask(__name__)


@app.route("/")
def home():
    return "Welcome to Auto Trading!"

@app.route("/buy")
def buy_stock():
    # 자동매매 로직에서 매수 작업을 수행하는 함수
    # ...

    return jsonify({"result": "Buy order placed"})

@app.route("/sell")
def sell_stock():
    # 자동매매 로직에서 매도 작업을 수행하는 함수
    # ...

    return jsonify({"result": "Sell order placed"})

def start_auto_trading():
    global kiwoom

    # PyQt5 애플리케이션 실행
    app = QApplication(sys.argv)

    # 키움증권 API OCX(ActiveX) 컨트롤 생성
    kiwoom = Kiwoom()
    # start_test(kiwoom)
    sys.exit(app.exec_())

def start_test(kiwoom):
    # tr 요청
    name = kiwoom.get_master_code_name(kiwoom, constants.SAMSUNG_CODE)
    connectState = kiwoom.get_connect_state()
    lastPrice = kiwoom.get_master_last_price(constants.SAMSUNG_CODE)

    print("연결상태 : %d" % connectState)
    print("유저정보")
    print("------------------------------")
    print("계좌 수 : " + kiwoom.get_login_info("ACCOUNT_CNT"))
    print("계좌 번호 : " + kiwoom.get_login_info("ACCNO"))
    print(kiwoom.get_login_info("USER_ID"))
    print(kiwoom.get_login_info("USER_NAME"))
    print("------------------------------")
    print(name)
    print("------------------------------")
    print("전일가 : %s" % lastPrice)

if __name__ == "__main__":
    # 자동매매를 위한 PyQt5 애플리케이션 실행
    start_auto_trading()

    # Flask 서버 실행
    app.run()




# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = TradingBot()
#     #window.show()
#     app.exec_()