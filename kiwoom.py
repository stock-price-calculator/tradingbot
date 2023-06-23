import os
import sys
import datetime
import time
import view
import traceback
from idlelib.iomenu import errors

from PyQt5.QtCore import QEventLoop, QCoreApplication

import constants
from PyQt5.QAxContainer import *
from account.account_receiver import Kiwoom_Receive_Account
from market.stick_data_receiver import Kiwoom_Receive_Market_price
from backtesting.backtest import Kiwoom_BackTesting



class Kiwoom:
    _instance = None
    def __new__(cls, *args, **kwargs):
        # 인스턴스가 없는 경우에만 인스턴스를 생성
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):

        self.remained_data = False  #차트데이터 요청할때 sPrevNext가 2이면 계속
        self.login_event_loop = None # login요청값을 받을 때 exit
        self.tr_event_loop = None # tr요청값을 받을 때 exit
        self.ocx = None
        self.create_loop_event()
        self.create_kiwoom_instance()
        self.connect_event()

        self.login_success = False  # loop못사용해서 변수 설정
        self.data_success = False # loop못사용해서 변수 설정
        self.continuous_data_success = False
        self.receive_account = Kiwoom_Receive_Account(self)
        self.receive_market_price = Kiwoom_Receive_Market_price(self)
        self.receive_backtest = Kiwoom_BackTesting(self)
        self.result_list = []

        self.return_list = []  #결과값 리턴할 리스트

        self.real_item_code =None  # 종목코드
        self.real_time_type = None  # 분봉, 일봉, 주봉
        self.real_trade_parm = None  # 시작시간 or 분봉타입
        self.real_profit_ratio = None  # 익절
        self.real_loss_ratio = None  # 손절
        self.real_bollinger_n = None
        self.real_bollinger_k = None
        self.real_total_data = None  # 이전 데이터

    # 레지스트리에 저장된 키움 openAPI 모듈 불러오기
    def create_kiwoom_instance(self):
        self.ocx = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")

    # 이벤트 요청 연결
    def connect_event(self):
        self.ocx.OnEventConnect.connect(self.login_slot)
        self.ocx.OnReceiveTrData.connect(self.receive_trdata)
        # self.ocx.OnReceiveRealData.connect(self.receive_realdata)

    # 이벤트 루프 생성
    def create_loop_event(self):
        self.login_event_loop = QEventLoop()  # 로그인 담당 이벤트 루프

    # 로그인 메서드 호출
    def connect_login(self):
        self.ocx.dynamicCall("CommConnect()")

        while not self.login_success:
            QCoreApplication.processEvents()
            time.sleep(0.2)

        if self.login_success:
            return 0

    # 로그인 성공 여부
    def login_slot(self, err_code):
        if err_code == 0:
            print("로그인에 성공하였습니다.")
            self.login_success = True
            self.login_event_loop.exit(1)
        else:
            print("로그인에 실패하였습니다.")
            self.login_event_loop.exit(0)

    # 종목코드의 종목명을 반환
    def get_master_code_name(self, code):
        name = self.ocx.dynamicCall("GetMasterCodeName(QString)", code)
        return name

    # 통신 접속 상태 반환
    def get_connect_state(self):
        result = self.ocx.dynamicCall("GetConnectState()")
        return result

    # ACCOUNT_CNT - 전체 계좌 개수를 반환
    # ACCNO - 전체 계좌를 반환, 계좌별 구분은 ';'이다
    # USER_ID - 사용자의 ID를 반환
    # USER_NAME - 사용자명을 반환한다
    # KEY_BSECGB - 키보드보안 해지여부 0:정상 1:해지
    # FIREW_SECGB - 방화벽 설정 여부 0:미설정 1:설정 2:해지

    # 사용자 정보 및 계좌 정보
    def get_login_info(self, tag):
        result = self.ocx.dynamicCall("GetLoginInfo(QString)", tag)
        return result

    # 요청한 tr값 수신
    def receive_trdata(self, sScrNo, sRQName, sTrCode, sRecordName, sPrevNext):

        '''
        TR 요청을 받는 구역, slot임
        :param sScrNo: 스크린 번호
        :param sRQName: 내가 요청했을 때 지은 이름
        :param sTrCode: 요청 ID, TR코드
        :param sRecordName: 사용안함
        :param sPrevNext: 다음 페이지가 있는지
        :return:
        '''

        # view.print_receive_trdata_element( sScrNo, sRQName, sTrCode, sRecordName, sPrevNext)
        #
        if sPrevNext == "2":
            self.remained_data = True
        else:
            self.remained_data = False

        # 예수금 등 조회 하기
        if sRQName == "예수금상세현황요청":
            self.receive_account.receive_detail_account_info(sTrCode, sRQName)
        # 계좌평가 잔고
        elif sRQName == "계좌평가잔고내역요청":
            self.receive_account.receive_detail_account_mystock(sTrCode, sRQName)
            self.continuous_data_success = True
        # 체결내역
        elif sRQName == "계좌별주문체결내역상세요청":
            self.receive_account.receive_trading_record(sTrCode, sRQName, sRecordName)
            self.continuous_data_success = True
        elif sRQName == "계좌수익률요청":
            self.receive_account.receive_price_earning_ratio(sTrCode,sRQName, sRecordName)
            self.continuous_data_success = True
        elif sRQName == "체결요청":
            self.receive_account.receive_conclude_data(sTrCode,sRQName,sRecordName)
            self.continuous_data_success = True
        elif sRQName == "일자별실현손익요청":
            self.receive_account.receive_day_earn_data(sTrCode,sRQName,sRecordName)
            self.continuous_data_success = True
        elif sRQName == "신규매수주문" or sRQName == "신규매도주문":
            print("주문 완료")
        elif sRQName == "주식기본정보요청":
            self.receive_market_price.receive_market_information(sTrCode, sRQName, sRecordName)
        elif sRQName == "주식분봉차트조회요청":
            data_list = self.receive_market_price.receive_minutes_chart_data(sTrCode, sRQName, sRecordName)
            self.return_list += data_list

            if not self.remained_data:
                time.sleep(0.5)
                print("끝남")
                self.continuous_data_success = True

        elif sRQName == "주식일봉차트조회요청":
            data_list = self.receive_market_price.receive_day_chart_data(sTrCode, sRQName, sRecordName)
            self.return_list += data_list

            if not self.remained_data:
                time.sleep(0.5)
                self.continuous_data_success = True

        elif sRQName == "주식주봉차트조회요청":
            data_list = self.receive_market_price.receive_week_chart_data(sTrCode, sRQName, sRecordName)

            self.return_list += data_list

            if not self.remained_data:
                time.sleep(0.5)
                self.continuous_data_success = True

        self.tr_event_loop.exit()

    # 실시간 데이터 받아오기
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


    # tr요청 기본 함수
    # tr 데이터 정보 입력
    def set_input_value(self, id, value):
        self.ocx.dynamicCall("SetInputValue(String, String)", id, value)

    # tr데이터 전송
    def send_comm_rq_data(self, rqname, trcode, next, screen_number):
        self.ocx.dynamicCall("CommRqData(String,String,int,String)", rqname, trcode, next, screen_number)
        self.tr_event_loop = QEventLoop()
        self.tr_event_loop.exec_()
        self.data_success = False
        # self.continuous_data_success = False


    # tr 반복수 받음
    def get_repeat_cnt(self, trcode, rqname):
        repeat_cnt = self.ocx.dynamicCall("GetRepeatCnt(String, String)", trcode, rqname)
        if repeat_cnt == 0:
            repeat_cnt = 1
        return repeat_cnt

    # 매수 매도 데이터 전송
    def send_trading_data(self, order_params):
        trade_data = self.ocx.dynamicCall(
            "SendOrder(QString, QString, QString, int, QString, int, int, QString, QString)",
            list(order_params.values()), )
        self.tr_event_loop = QEventLoop()
        self.tr_event_loop.exec_()
        return trade_data

    # 시장종목 리스트를 가져오기 (종목코드 가져오기)
    def GetCodeListByMarket(self,market):
        item_code_list = self.ocx.dynamicCall("GetCodeListByMarket(QString)",market)

        return item_code_list

    # 종목코드 -> 종목이름
    def GetMarsterCodeName(self, item_code):
        item_name = self.ocx.dynamicCall("GetMasterCodeName(QString)", item_code)

        return item_name

    def get_comm_data(self, trcode, record_name, next, rqname):
        comm_data = self.ocx.dynamicCall("GetCommData(String, String, int, String)", trcode, record_name, next, rqname)
        return comm_data

    # 실시간
    def get_comm_real_data(self, item_code, fid):
        return self.ocx.dynamicCall("GetCommRealData(QString,int)",item_code, fid)

    # 실시간 요청 등록
    def SetRealReg(self, screen_no, code_list, fid_list, real_type):
        self.ocx.dynamicCall("SetRealReg(QString, QString, QString, QString)",
                             screen_no, code_list, fid_list, real_type)