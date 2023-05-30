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


class Kiwoom:
    def __init__(self):


        self.login_event_loop = None # login요청값을 받을 때 exit
        self.tr_event_loop = None # tr요청값을 받을 때 exit
        self.ocx = None
        self.create_loop_event()
        self.create_kiwoom_instance()
        self.connect_event()
        self.connect_login() # 로그인 요청

        self.SetRealReg("0101", "005930", "10", "0")

    # 레지스트리에 저장된 키움 openAPI 모듈 불러오기
    def create_kiwoom_instance(self):
        self.ocx = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")

    # 이벤트 요청 연결
    def connect_event(self):
        self.ocx.OnEventConnect.connect(self.login_slot)
        self.ocx.OnReceiveRealData.connect(self.receive_realdata)

    # 이벤트 루프 생성
    def create_loop_event(self):
        self.login_event_loop = QEventLoop()  # 로그인 담당 이벤트 루프

    # 로그인 메서드 호출
    def connect_login(self):
        self.ocx.dynamicCall("CommConnect()")
        self.login_event_loop.exec_()

    # 로그인 성공 여부
    def login_slot(self, err_code):
        if err_code == 0:
            print("로그인에 성공하였습니다.")
        else:
            print("로그인에 실패하였습니다.")
            sys.exit(0)
        self.login_event_loop.exit()




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
            print("상한가발생시간 : " + self.get_comm_real_data(sJongmokCode, 567))
            print("하한가발생시간 : " + self.get_comm_real_data(sJongmokCode, 568))
            print("-----------------------------------------")

    def SetRealReg(self, screen_no, code_list, fid_list, real_type):
        self.ocx.dynamicCall("SetRealReg(QString, QString, QString, QString)",
                             screen_no, code_list, fid_list, real_type)

    def get_comm_real_data(self, item_code, fid):
        return self.ocx.dynamicCall("GetCommRealData(QString,int)",item_code, fid)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Kiwoom()
    #window.show()
    app.exec_()