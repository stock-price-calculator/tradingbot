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


class Kiwoom:
    def __init__(self):

        self.remained_data = False  # 차트데이터 요청할때 sPrevNext가 2이면 계속
        self.login_event_loop = None
        self.tr_event_loop = None
        self.ocx = None
        self.create_loop_event()
        self.create_kiwoom_instance()
        self.connect_event()
        self.connect_login()


    # 레지스트리에 저장된 키움 openAPI 모듈 불러오기
    def create_kiwoom_instance(self):
        self.ocx = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")

    # 이벤트 요청 연결
    def connect_event(self):
        self.ocx.OnEventConnect.connect(self.login_slot)
        self.ocx.OnReceiveTrData.connect(self.receive_trdata)

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


 # 요청한 tr값 수신
    def receive_trdata(self, sScrNo, sRQName, sTrCode, sRecordName, sPrevNext):

        # view.print_receive_trdata_element( sScrNo, sRQName, sTrCode, sRecordName, sPrevNext)

        # 예수금 등 조회 하기
        if sRQName == "예수금상세현황요청":
            self.receive_account.receive_detail_account_info(sTrCode, sRQName)

        self.tr_event_loop.exit()