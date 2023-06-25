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
    def __init__(self, main_kiwoom, kiwoom_trade):
        self.kiwoom = main_kiwoom
        self.kiwoom_trade = kiwoom_trade
        self.connect_event()
        self.realtime_event_loop = QEventLoop()
        self.buy = False # 이미 구매를 했는지
        self.buy_price = -1 # 구매가격

        self.real_current_price = 70000

    # 이벤트 요청 연결
    def connect_event(self):
        self.kiwoom.ocx.OnReceiveRealData.connect(self.receive_realdata)

    def stop_real_trading(self):
        self.realtime_event_loop.exit()
        self.SetRealRemove("ALL","ALL")
        
    # 주식체결 받아오기
    def receive_realdata(self, sJongmokCode, sRealType, sRealData):

        if sRealType == "주식체결":
            self.real_current_price = self.get_comm_real_data(sJongmokCode, 10)

            print("----------------------------------------")
            print("현재가 : " + self.real_current_price)
            print(self.kiwoom.real_item_code)
            print(self.kiwoom.real_time_type)
            print(self.kiwoom.real_profit_ratio)
            # print(self.kiwoom.real_loss_ratio)
            # print(self.kiwoom.real_bollinger_n)
            if self.real_current_price == "+" + str(71600):
                print("asdfasdf")
            print("-----------------------------------------")


        # print("전일대비 : " + self.get_comm_real_data(sJongmokCode, 11))
        # print("등락율 : " + self.get_comm_real_data(sJongmokCode, 12))
        # print("매도호가 : " + self.get_comm_real_data(sJongmokCode, 27))
        # print("매수호가 : " + self.get_comm_real_data(sJongmokCode, 28))
        # print("누적거래량 : " + self.get_comm_real_data(sJongmokCode, 13))
        # print("시가 : " + self.get_comm_real_data(sJongmokCode, 16))
        # print("고가 : " + self.get_comm_real_data(sJongmokCode, 17))
        # print("저가 : " + self.get_comm_real_data(sJongmokCode, 18))
        # print("전일거래량대비 : " + self.get_comm_real_data(sJongmokCode, 26))
        # print("시가총액 : " + self.get_comm_real_data(sJongmokCode, 311))

    # 실시간 매매 시작
    def real_trade_start(self):
        # 몇 분봉,  익절,  손절 , 종목코드

        data = self.kiwoom.real_total_data.iloc[-1]
        print("upper : ", data['upper'])
        print("lower : ", data['lower'])
        print("current : ",  self.real_current_price)

        if self.buy == False:

            if self.real_current_price < data['lower']:

                # 매매
                self.buy = True
                self.buy_price =  self.real_current_price
                self.kiwoom_trade.send_buy_order(constants.ACCOUNT,self.kiwoom.real_item_code, 12, 0,"시장가")
        else:  # upper에 닿았을때 , 익절 퍼센트 달성   // 손절 퍼센트 달성
            if self.real_current_price >= data['upper']:
                print("볼린저밴드 익절")
                self.kiwoom_trade.send_sell_order(constants.ACCOUNT, self.kiwoom.real_item_code, 12, 0, "시장가")
                self.buy = False
            elif self.real_current_price >= self.buy_price * (1 + self.kiwoom.real_profit_ratio / 100):
                print("목표가 익절")
                self.kiwoom_trade.send_sell_order(constants.ACCOUNT, self.kiwoom.real_item_code, 12, 0, "시장가")
                self.buy = False
            elif self.real_current_price <= data['lower']:
                print("목표가 손절")
                self.kiwoom_trade.send_sell_order(constants.ACCOUNT, self.kiwoom.real_item_code, 12, 0, "시장가")
                self.buy = False




    # 실시간 등록
    def SetRealReg(self, item_code):
        self.kiwoom.ocx.dynamicCall("SetRealReg(QString, QString, QString, QString)",
                             "0111", item_code, "10", "0")

        self.realtime_event_loop.exec_()

    def setPreTrading(self, item_code, time_type, trade_parm, profit_ratio, loss_ratio, bollinger_n, bollinger_k,
                      total_data, balance):
        self.kiwoom.real_item_code = item_code  # 종목코드
        self.kiwoom.real_time_type = time_type  # 분봉, 일봉, 주봉
        self.kiwoom.real_trade_parm = trade_parm  # 시작시간 or 분봉타입
        self.kiwoom.real_profit_ratio = profit_ratio  # 익절
        self.kiwoom.real_loss_ratio = loss_ratio  # 손절
        self.kiwoom.real_bollinger_n = bollinger_n
        self.kiwoom.real_bollinger_k = bollinger_k
        self.kiwoom.real_total_data = total_data  # 이전 데이터
        self.kiwoom.real_balance = balance
        print("실시간 매매 초기 설정완료")
    def get_comm_real_data(self, item_code, fid):
        return self.kiwoom.ocx.dynamicCall("GetCommRealData(QString,int)",item_code, fid)

    def DisConnectRealData(self, screen_no):
        self.kiwoom.ocx.dynamicCall("DisConnectRealData(QString)", screen_no)

    def SetRealRemove(self,strScrNo, strDelCode):
        self.kiwoom.ocx.dynamicCall("SetRealRemove(QString, QString", strScrNo, strDelCode)



