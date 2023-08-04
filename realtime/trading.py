import os
import sys
import datetime
import time
import view
import traceback
from idlelib.iomenu import errors

from PyQt5.QtCore import QEventLoop

import constants
from PyQt5.QAxContainer import *
from account.account_receiver import Kiwoom_Receive_Account
from market.stick_data_receiver import Kiwoom_Receive_Market_price
from backtesting.backtest import *

import sys

from PyQt5.QAxContainer import *
from PyQt5.QtCore import QEventLoop
from PyQt5.QtWidgets import *
import constants
from kiwoom import Kiwoom
from account.account_sender import Kiwoom_Send_Account
from order.trade import Kiwoom_Trade
from market.stick_data_sender import Kiwoom_Price


class Kiwoom_Real_trade:
    def __init__(self, main_kiwoom, kiwoom_trade, kiwoom_account):
        self.kiwoom = main_kiwoom
        self.kiwoom_trade = kiwoom_trade
        self.kiwoom_account = kiwoom_account
        self.connect_event()
        self.realtime_event_loop = QEventLoop()
        self.buy = False  # 이미 구매를 했는지
        self.buy_price = -1  # 구매가격
        self.real_current_price = 70000
        self.real_buy_quantity = 0


    # 이벤트 요청 연결
    def connect_event(self):
        print("실시간 이벤트 연결")
        self.kiwoom.ocx.OnReceiveRealData.connect(self.receive_realdata)

    def stop_real_trading(self):
        self.realtime_event_loop.exit()
        self.SetRealRemove("ALL", "ALL")

    # 주식체결 받아오기
    def receive_realdata(self, sJongmokCode, sRealType, sRealData):
        print(self.kiwoom.real_start)
        if sRealType == "주식체결" and self.kiwoom.real_start == True:
            self.real_current_price = str(self.get_comm_real_data(sJongmokCode, 10))
            print("----------------------------------------")
            print("현재가 : " + (self.real_current_price))
            # print(self.kiwoom.real_item_code)
            # print(self.kiwoom.real_time_type)
            # print(self.kiwoom.real_profit_ratio)
            # # print(self.kiwoom.real_loss_ratio)
            # # print(self.kiwoom.real_bollinger_n)
            print("-----------------------------------------")

            self.real_trade_start(int(self.real_current_price))

    # 실시간 매매 시작
    def real_trade_start(self, current_price):
        # 몇 분봉,  익절,  손절 , 종목코드

        data = self.kiwoom.real_total_data.iloc[-1]
        print("upper : ", data['upper'])
        print("lower : ", data['lower'])
        print("current : ", current_price)

        if self.buy == False:

            if current_price < data['lower']:
                # 매매
                self.buy = True
                self.buy_price = current_price  # 현재가

                self.real_buy_quantity = int(self.kiwoom.real_can_buy_money // current_price)  # 매수 가능 수량
                self.kiwoom_trade.send_buy_order(constants.ACCOUNT, self.kiwoom.real_item_code, self.real_buy_quantity,
                                                 0, "시장가")

                # 매수가능 금액 업데이트
                self.kiwoom.real_can_buy_money = self.kiwoom_account.send_detail_account_info(constants.ACCOUNT)

        else:  # upper에 닿았을때 , 익절 퍼센트 달성   // 손절 퍼센트 달성

            if current_price >= data['upper'] or \
                    current_price >= self.buy_price * (1 + self.kiwoom.real_profit_ratio / 100) or \
                    current_price <= data['lower']:

                if current_price >= data['upper']:
                    print("볼린저밴드 익절")
                elif current_price >= self.buy_price * (1 + self.kiwoom.real_profit_ratio / 100):
                    print("목표가 익절")
                elif current_price <= data['lower']:
                    print("목표가 손절")
                # 매도
                self.kiwoom_trade.send_sell_order(constants.ACCOUNT, self.kiwoom.real_item_code, self.real_buy_quantity,
                                                  0, "시장가")
                self.buy = False
                self.buy_price = -1
                # 매수 가능 금액 수정
                self.kiwoom.real_can_buy_money = self.kiwoom_account.send_detail_account_info(constants.ACCOUNT)

    # 실시간 등록
    def SetRealReg(self, item_code):
        print("실시간 연결 시작")
        self.kiwoom.ocx.dynamicCall("SetRealReg(QString, QString, QString, QString)",
                                    "0111", item_code, "10", 0)

        self.realtime_event_loop.exec_()

    def setPreTrading(self, item_code, time_type, trade_parm, profit_ratio, loss_ratio, bollinger_n, bollinger_k,
                      total_data, balance, can_buy_money):
        self.kiwoom.real_item_code = item_code  # 종목코드
        self.kiwoom.real_time_type = time_type  # 분봉, 일봉, 주봉
        self.kiwoom.real_trade_parm = trade_parm  # 시작시간 or 분봉타입
        self.kiwoom.real_profit_ratio = profit_ratio  # 익절
        self.kiwoom.real_loss_ratio = loss_ratio  # 손절
        self.kiwoom.real_bollinger_n = bollinger_n
        self.kiwoom.real_bollinger_k = bollinger_k
        self.kiwoom.real_total_data = total_data  # 이전 데이터
        self.kiwoom.real_balance = balance
        self.kiwoom.real_can_buy_money = can_buy_money
        print("실시간 매매 초기 설정완료")

    def get_comm_real_data(self, item_code, fid):
        return self.kiwoom.ocx.dynamicCall("GetCommRealData(QString,int)", item_code, fid)

    def DisConnectRealData(self, screen_no):
        self.kiwoom.ocx.dynamicCall("DisConnectRealData(QString)", screen_no)

    def SetRealRemove(self, strScrNo, strDelCode):
        self.kiwoom.ocx.dynamicCall("SetRealRemove(QString, QString", strScrNo, strDelCode)
