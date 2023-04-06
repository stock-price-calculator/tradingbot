import os
import sys
import datetime
import time
from idlelib.iomenu import errors

from PyQt5.QtCore import QEventLoop

import constants
from PyQt5.QAxContainer import *


class Kiwoom:
    def __init__(self):

        self.trading_record_loop = None
        self.plus_price_rate_loop = None
        self.detail_account_info_event_loop = None
        self.login_event_loop = None
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
        self.ocx.OnReceiveTrData.connect(self.trdata_slot)

    def create_loop_event(self):
        self.login_event_loop = QEventLoop()  # 로그인 담당 이벤트 루프
        self.detail_account_info_event_loop = QEventLoop()  # 예수금상세현황요청 담담 이벤트 루프
        self.plus_price_rate_loop = QEventLoop()  # 계좌평가잔고 루프
        self.trading_record_loop = QEventLoop()  # 체결내역 루프

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

    # 전일가
    def get_master_last_price(self, code):
        result = self.ocx.dynamicCall("GetMasterLastPrice(QString)", code)
        return result

    # SendOrder 호출
    def send_buy_order(self, account, item_code, quantity, price, trading_type):

        order_params = {
            "rq_name": "신규매수주문",
            "screen_number": "0101",
            "account_number": account,
            "order_type": constants.NEW_BUY,
            "code": item_code,
            "stock_quantity": quantity,
            "price": price,
            "trading_type": self.changed_trading_type(trading_type),
            "origin_order_number": '',
        }
        result = self.ocx.dynamicCall("SendOrder(QString, QString, QString, int, QString, int, int, QString, QString)",
                                      list(order_params.values()), )
        return result

    # SendOrder 호출
    def send_sell_order(self, account, item_code, quantity, price, trading_type):

        order_params = {
            "rq_name": "신규매도주문",
            "screen_number": "0101",
            "account_number": account,
            "order_type": constants.NEW_SELL,
            "code": item_code,
            "stock_quantity": quantity,
            "price": price,
            "trading_type": self.changed_trading_type(trading_type),
            "origin_order_number": '',
        }
        result = self.ocx.dynamicCall("SendOrder(QString, QString, QString, int, QString, int, int, QString, QString)",
                                      list(order_params.values()), )
        return result

    # SendOrder 호출
    def cancel_buy_order(self, account, item_code, quantity, price, trading_type, original_order_num):

        order_params = {
            "rq_name": "매수취소주문",
            "screen_number": "0101",
            "account_number": account,
            "order_type": constants.CANCEL_BUY,
            "code": item_code,
            "stock_quantity": quantity,
            "price": price,
            "trading_type": self.changed_trading_type(trading_type),
            "origin_order_number": original_order_num,
        }
        result = self.ocx.dynamicCall("SendOrder(QString, QString, QString, int, QString, int, int, QString, QString)",
                                      list(order_params.values()), )
        return result

    # SendOrder 호출
    def cancel_sell_order(self, account, item_code, quantity, price, trading_type, original_order_num):
        order_params = {
            "rq_name": "매도취소주문",
            "screen_number": "0101",
            "account_number": account,
            "order_type": constants.CANCEL_BUY,
            "code": item_code,
            "stock_quantity": quantity,
            "price": price,
            "trading_type": self.changed_trading_type(trading_type),
            "origin_order_number": original_order_num,
        }

        result = self.ocx.dynamicCall("SendOrder(QString, QString, QString, int, QString, int, int, QString, QString)",
                                      list(order_params.values()), )
        return result

    # 예수금상세현황요청
    def get_detail_account_info(self, account):
        print("계좌번호 및 비밀번호 등을 입력/서버에 요청")
        self.ocx.dynamicCall("SetInputValue(String,String)", "계좌번호", account)
        self.ocx.dynamicCall("SetInputValue(String,String)", "비밀번호", "0000")
        self.ocx.dynamicCall("SetInputValue(String,String)", "비밀번호입력매체구분", "00")
        self.ocx.dynamicCall("SetInputValue(String,String)", "조회구분", "2")
        self.ocx.dynamicCall("CommRqData(String,String,int,String)", "예수금상세현황요청", "opw00001", 0, "2000")
        self.detail_account_info_event_loop.exec_()

    # 계좌평가잔고내역요청
    def get_detail_account_mystock(self, account, sPrevNext="0"):
        print("계좌평가잔고내역 서버에 요청")
        # 계좌평가 잔고내역 요청
        # sPrevNext="0" : 싱글데이터 받아오기(종목합계 데이터)
        self.ocx.dynamicCall("SetInputValue(String,String)", "계좌번호", account)
        self.ocx.dynamicCall("SetInputValue(String,String)", "비밀번호", "0000")
        self.ocx.dynamicCall("SetInputValue(String,String)", "비밀번호입력매체구분", "00")
        self.ocx.dynamicCall("SetInputValue(String,String)", "조회구분", "2")
        self.ocx.dynamicCall("CommRqData(String, String, int, String)", "계좌평가잔고내역요청", "opw00018", sPrevNext, "2000")
        self.plus_price_rate_loop.exec_()

    # 오늘날짜를 기준으로 term기간만큼 날짜 가져오기
    def get_trading_record_date(self, term):
        result_date = []
        current_date = datetime.date.today()

        for i in range(0, term):
            original_date = current_date - datetime.timedelta(days=i)
            splits = str(original_date).split("-")
            conversion_date = splits[0] + splits[1] + splits[2]
            weekend_date = datetime.date(int(splits[0]), int(splits[1]), int(splits[2])).weekday()
            if weekend_date > 4:
                pass
            else:
                result_date.append(conversion_date)
        return result_date

    # 체결내역
    def get_trading_record(self, term, account, find_division, buy_or_sell, item_code=""):
        print("체결내역 서버에 요청")

        # term기간만큼 이전날짜 가져옴
        all_date = self.get_trading_record_date(term)

        for day in reversed(all_date):
            print(day)
            self.ocx.dynamicCall("SetInputValue(String,String)", "주문일자", day)
            self.ocx.dynamicCall("SetInputValue(String,String)", "계좌번호", account)
            self.ocx.dynamicCall("SetInputValue(String,String)", "비밀번호", "0000")
            self.ocx.dynamicCall("SetInputValue(String,String)", "비밀번호입력매체구분", "00")
            self.ocx.dynamicCall("SetInputValue(String,String)", "조회구분", find_division)
            self.ocx.dynamicCall("SetInputValue(String,String)", "주식채권구분", "1")
            self.ocx.dynamicCall("SetInputValue(String,String)", "매도수구분", buy_or_sell)
            self.ocx.dynamicCall("SetInputValue(String,String)", "종목코드", item_code)
            self.ocx.dynamicCall("SetInputValue(String,String)", "시작주문번호", "")
            self.ocx.dynamicCall("CommRqData(String,String,int,String)", "계좌별주문체결내역상세요청", "opw00007", 2, "2000")
            print("긑"+ day)
            self.trading_record_loop.exec_()


    def trdata_slot(self, sScrNo, sRQName, sTrCode, sRecordName, sPrevNext):
        # TR SLOT 만들기
        '''
        TR 요청을 받는 구역, slot임
        :param sScrNo: 스크린 번호
        :param sRQName: 내가 요청했을 때 지은 이름
        :param sTrCode: 요청 ID, TR코드
        :param sRecordName: 사용안함
        :param sPrevNext: 다음 페이지가 있는지
        :return:
        '''

        # 예수금 등 조회 하기
        if sRQName == "예수금상세현황요청":
            deposit = self.ocx.dynamicCall("GetCommData(String, String, int, String)", sTrCode, sRQName, 0, "예수금")
            ok_deposit = self.ocx.dynamicCall("GetCommData(String, String, int, String)", sTrCode, sRQName, 0, "출금가능금액")
            buy_deposit = self.ocx.dynamicCall("GetCommData(String, String, int, String)", sTrCode, sRQName, 0,
                                               "주문가능금액")
            print("출금가능금액 %s" % int(ok_deposit))
            print("예수금 %s" % int(deposit))
            print("주문가능금액 %s" % int(buy_deposit))

            self.detail_account_info_event_loop.exit()

        # 계좌평가 잔고
        elif sRQName == "계좌평가잔고내역요청":

            total_buy_money = self.ocx.dynamicCall("GetCommData(String, String, int, String)", sTrCode, sRQName, 0, "총매입금액")
            total_profit_loss_rate = self.ocx.dynamicCall("GetCommData(String, String, int, String)", sTrCode, sRQName, 0, "총수익률(%)")

            print("총매입금액 %s" % int(total_buy_money))
            print("총수익률 %s" % float(total_profit_loss_rate))

            self.plus_price_rate_loop.exit()

        # 체결내역
        elif sRQName == "계좌별주문체결내역상세요청":
            repeat = self.ocx.dynamicCall("GetRepeatCnt(String, String)", sTrCode, sRQName)
            print("총개수 : " + repeat)
            for i in range(repeat):
                item_code = self.ocx.dynamicCall("GetCommData(String, String, int, String)",sTrCode,sRecordName,i,"종목번호")
                trade_count = int(self.ocx.dynamicCall("GetCommData(String, String, int, String)",sTrCode,sRecordName,i,"체결수량"))
                trade_price = int(self.ocx.dynamicCall("GetCommData(String, String, int, String)",sTrCode,sRecordName,i,"체결단가"))
                order_gubun = int(self.ocx.dynamicCall("GetCommData(String, String, int, String)",sTrCode,sRecordName,i,"주문구분"))

                print("종목번호 %s" % item_code)
                print("체결수량 %s" % int(trade_count))
                print("체결단가 %s" % int(trade_price))
                print("주문구분 %s" % int(order_gubun))
            self.trading_record_loop.exit()

    def changed_trading_type(self, name):
        if (name == "지정가"):
            return constants.LIMIT_PRICE_VALUE
        else:
            return constants.MARKET_PRICE_VALUE

    def change_order_type(self, name):
        if (name == "신규매수"):
            return constants.NEW_BUY
        elif (name == "신규매도"):
            return constants.NEW_SELL
        elif (name == "매수취소"):
            return constants.CANCEL_BUY
        elif (name == "매도취소"):
            return constants.CANCEL_SELL
        elif (name == "매수정정"):
            return constants.CHANGE_BUY
        elif (name == "매도정정"):
            return constants.CHANGE_SELL
        else:
            return constants.ERROR_CODE
