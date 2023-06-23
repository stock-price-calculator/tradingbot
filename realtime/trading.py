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
    def __init__(self, main_kiwoom):
        self.kiwoom = main_kiwoom
        self.connect_event()
        self.realtime_event_loop = QEventLoop()

    # 이벤트 요청 연결
    def connect_event(self):
        self.kiwoom.ocx.OnReceiveRealData.connect(self.receive_realdata)

    def stop_real_trading(self):
        self.realtime_event_loop.exit()
        self.SetRealRemove("ALL","ALL")
        
    # 주식체결 받아오기
    def receive_realdata(self, sJongmokCode, sRealType, sRealData):

        if sRealType == "주식체결":
            print("-----------------------------------------")
            print("현재가 : " + self.get_comm_real_data(sJongmokCode, 10))
            print("전일대비 : " + self.get_comm_real_data(sJongmokCode, 11))
            print("등락율 : " + self.get_comm_real_data(sJongmokCode, 12))
            print("매도호가 : " + self.get_comm_real_data(sJongmokCode, 27))
            print("매수호가 : " + self.get_comm_real_data(sJongmokCode, 28))
            print("누적거래량 : " + self.get_comm_real_data(sJongmokCode, 13))
            print("시가 : " + self.get_comm_real_data(sJongmokCode, 16))
            print("고가 : " + self.get_comm_real_data(sJongmokCode, 17))
            print("저가 : " + self.get_comm_real_data(sJongmokCode, 18))
            print("전일거래량대비 : " + self.get_comm_real_data(sJongmokCode, 26))
            print("시가총액 : " + self.get_comm_real_data(sJongmokCode, 311))
            print("-----------------------------------------")


    # 실시간 매매 시작
    def real_trade_start(self, current_price):
        # 몇 분봉,  익절,  손절,  볼린저밴드 값1, 볼린저밴드 값2, 종목코드


    # 실시간 등록
    def SetRealReg(self, screen_no, code_list, fid_list, real_type, time_type, profit_ratio, loss_ratio, bollinger_n, bollinger_k):
        self.kiwoom.ocx.dynamicCall("SetRealReg(QString, QString, QString, QString)",
                             screen_no, code_list, fid_list, real_type)

        self.real_item_code = code_list # 종목코드
        self.real_time_type = time_type # 몇 분봉
        self.real_profit_ratio = profit_ratio # 익절
        self.reale_loss_ratio = loss_ratio # 손절
        self.real_bollinger_n = bollinger_n
        self.real_bollinger_k = bollinger_k

        self.realtime_event_loop.exec_()

    def get_comm_real_data(self, item_code, fid):
        return self.kiwoom.ocx.dynamicCall("GetCommRealData(QString,int)",item_code, fid)

    def DisConnectRealData(self, screen_no):
        self.kiwoom.ocx.dynamicCall("DisConnectRealData(QString)", screen_no)

    def SetRealRemove(self,strScrNo, strDelCode):
        self.kiwoom.ocx.dynamicCall("SetRealRemove(QString, QString", strScrNo, strDelCode)



