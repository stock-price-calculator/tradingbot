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

        # if sRealType == "잔고":
        #     print("-----------------------------------------")
        #     print("계좌번호 : " + self.get_comm_real_data(sJongmokCode, 9201))
        #     print("종목코드, 업종코드 : " + self.get_comm_real_data(sJongmokCode, 9001))
        #     print("종목명 : " + self.get_comm_real_data(sJongmokCode, 302))
        #     print("현재가 : " + self.get_comm_real_data(sJongmokCode, 10))
        #     print("보유수량 : " + self.get_comm_real_data(sJongmokCode, 930))
        #     print("매입단가 : " + self.get_comm_real_data(sJongmokCode, 931))
        #     print("총매입가 : " + self.get_comm_real_data(sJongmokCode, 932))
        #     print("주문가능수량 : " + self.get_comm_real_data(sJongmokCode, 933))
        #     print("당일순매수량 : " + self.get_comm_real_data(sJongmokCode, 945))
        #     print("매도/매수구분 : " + self.get_comm_real_data(sJongmokCode, 946))
        #     print("손익율 : " + self.get_comm_real_data(sJongmokCode, 8019))
        #     print("당일실현손익(유가) : " + self.get_comm_real_data(sJongmokCode, 990))
        #     print("-----------------------------------------")
        #

    # 실시간 등록
    def SetRealReg(self, screen_no, code_list, fid_list, real_type):
        self.kiwoom.ocx.dynamicCall("SetRealReg(QString, QString, QString, QString)",
                             screen_no, code_list, fid_list, real_type)
        self.realtime_event_loop.exec_()

    def get_comm_real_data(self, item_code, fid):
        return self.kiwoom.ocx.dynamicCall("GetCommRealData(QString,int)",item_code, fid)

    def DisConnectRealData(self, screen_no):
        self.kiwoom.ocx.dynamicCall("DisConnectRealData(QString)", screen_no)

    def SetRealRemove(self,strScrNo, strDelCode):
        self.kiwoom.ocx.dynamicCall("SetRealRemove(QString, QString", strScrNo, strDelCode)



