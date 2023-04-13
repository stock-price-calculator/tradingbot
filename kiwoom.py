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


def changed_trading_type(name):
    if (name == "지정가"):
        return constants.LIMIT_PRICE_VALUE
    else:
        return constants.MARKET_PRICE_VALUE


def change_order_type(name):
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


class Kiwoom:
    def __init__(self):

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
            "trading_type": changed_trading_type(trading_type),
            "origin_order_number": '',
        }
        result = self.send_trading_data(order_params)

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
            "trading_type": changed_trading_type(trading_type),
            "origin_order_number": '',
        }
        result = self.send_trading_data(order_params)

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
            "trading_type": changed_trading_type(trading_type),
            "origin_order_number": original_order_num,
        }
        result = self.send_trading_data(order_params)

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
            "trading_type": changed_trading_type(trading_type),
            "origin_order_number": original_order_num,
        }

        result = self.send_trading_data(order_params)

        return result

    # 예수금상세현황요청
    def get_detail_account_info(self, account):
        self.set_input_value("계좌번호", account)
        self.set_input_value("비밀번호", "0000")
        self.set_input_value("비밀번호입력매체구분", "00")
        self.set_input_value("조회구분", "2")
        self.send_comm_rq_data("예수금상세현황요청", "opw00001", 0, "2000")

    # 계좌평가잔고내역요청
    def get_detail_account_mystock(self, account, sPrevNext="0"):

        # sPrevNext="0" : 싱글데이터 받아오기(종목합계 데이터)
        self.set_input_value("계좌번호", account)
        self.set_input_value("비밀번호", "0000")
        self.set_input_value("비밀번호입력매체구분", "00")
        self.set_input_value("조회구분", "2")
        self.send_comm_rq_data("계좌평가잔고내역요청", "opw00018", sPrevNext, "2000")

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
    def get_trading_record(self, term, account, find_division, buy_or_sell, item_code):
        print("체결내역 서버에 요청")

        # term기간만큼 이전날짜 가져옴
        all_date = self.get_trading_record_date(term)

        print(all_date)
        for day in reversed(all_date):
            self.set_input_value("주문일자", day)
            self.set_input_value("계좌번호", account)
            self.set_input_value("비밀번호", "0000")
            self.set_input_value("비밀번호입력매체구분", "00")
            self.set_input_value("조회구분", find_division)
            self.set_input_value("주식채권구분", "1")
            self.set_input_value("매도수구분", buy_or_sell)
            self.set_input_value("종목코드", item_code)
            self.set_input_value("시작주문번호", "")
            self.send_comm_rq_data("계좌별주문체결내역상세요청", "opw00007", 0, "2000")
            time.sleep(0.3)

    # 분봉차트 조회
    def get_minutes_chart_data(self, item_code, minute_type):
        self.set_input_value("종목코드", item_code)
        self.set_input_value("틱범위", minute_type)
        self.set_input_value("수정주가구분", "0")
        self.send_comm_rq_data("주식분봉차트조회요청", "opt10080", 0, "2000")

    # 일봉차트 조회
    def get_day_chart_data(self, item_code, start_date):
        self.set_input_value("종목코드", item_code)
        self.set_input_value("기준일자", start_date)
        self.set_input_value("수정주가구분", "0")
        self.send_comm_rq_data("주식일봉차트조회요청", "opt10081", 0, "2000")

    # 주봉차트 조회
    def get_week_chart_data(self, item_code, start_date, last_date):
        self.set_input_value("종목코드", item_code)
        self.set_input_value("기준일자", start_date)
        self.set_input_value("끝일자", last_date)
        self.set_input_value("수정주가구분", "0")
        self.send_comm_rq_data("주식주봉차트조회요청", "opt10082", 0, "2000")

    def receive_trdata(self, sScrNo, sRQName, sTrCode, sRecordName, sPrevNext):
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

        # print("--------------------")
        # print(sScrNo)
        # print(sRQName)
        # print(sTrCode)
        # print(sRecordName)
        # print(sPrevNext)
        # print("--------------------")

        # 예수금 등 조회 하기
        if sRQName == "예수금상세현황요청":

            deposit = self.get_comm_data(sTrCode, sRQName, 0, "예수금")
            ok_deposit = self.get_comm_data(sTrCode, sRQName, 0, "출금가능금액")
            buy_deposit = self.get_comm_data(sTrCode, sRQName, 0, "주문가능금액")
            view.예수금상세현황요청출력(ok_deposit, deposit, buy_deposit)
            self.tr_event_loop.exit()

        # 계좌평가 잔고
        elif sRQName == "계좌평가잔고내역요청":
            total_buy_money = self.get_comm_data(sTrCode, sRQName, 0, "총매입금액")
            total_profit_loss_rate = self.get_comm_data(sTrCode, sRQName, 0, "총수익률(%)")
            view.계좌평가잔고내역요청출력(total_buy_money, total_profit_loss_rate)
            self.tr_event_loop.exit()

        # 체결내역
        elif sRQName == "계좌별주문체결내역상세요청":

            repeat = self.get_repeat_cnt(sTrCode, sRQName)

            for i in range(repeat):
                order_number = self.get_comm_data(sTrCode, sRecordName, i, "주문번호")
                item_code = self.get_comm_data(sTrCode, sRecordName, i, "종목번호")
                item_name = self.get_comm_data(sTrCode, sRecordName, i, "종목명")
                trade_count = self.get_comm_data(sTrCode, sRecordName, i, "체결수량")
                trade_price = self.get_comm_data(sTrCode, sRecordName, i, "체결단가")
                order_type = self.get_comm_data(sTrCode, sRecordName, i, "매매구분")

                if order_number != "":
                    view.계좌별주문체결내역상세요청출력(order_number, item_code, item_name, trade_count, trade_price, order_type)
            self.tr_event_loop.exit()

        elif sRQName == "주식분봉차트조회요청":

            repeat = self.get_repeat_cnt(sTrCode, sRQName)

            for i in range(repeat):
                current_price = self.get_comm_data(sTrCode, sRecordName, i, "현재가")
                volume = self.get_comm_data(sTrCode, sRecordName, i, "거래량")
                open_price = self.get_comm_data(sTrCode, sRecordName, i, "시가")
                high_price = self.get_comm_data(sTrCode, sRecordName, i, "고가")
                low_price = self.get_comm_data(sTrCode, sRecordName, i, "저가")
                standard_minute = self.get_comm_data(sTrCode, sRecordName, i, "체결시간")

                view.주식분봉차트조회요청(standard_minute, current_price, open_price, high_price, low_price, volume)
            self.tr_event_loop.exit()

        elif sRQName == "주식일봉차트조회요청":
            repeat = self.get_repeat_cnt(sTrCode, sRQName)

            for i in range(repeat):
                current_price = self.get_comm_data(sTrCode, sRecordName, i, "현재가")
                volume = self.get_comm_data(sTrCode, sRecordName, i, "거래량")
                open_price = self.get_comm_data(sTrCode, sRecordName, i, "시가")
                high_price = self.get_comm_data(sTrCode, sRecordName, i, "고가")
                low_price = self.get_comm_data(sTrCode, sRecordName, i, "저가")
                standard_day = self.get_comm_data(sTrCode, sRecordName, i, "일자")

                view.주식일봉차트조회요청(standard_day, current_price, open_price, high_price, low_price, volume)
            self.tr_event_loop.exit()

        elif sRQName == "주식주봉차트조회요청":
            repeat = self.get_repeat_cnt(sTrCode, sRQName)

            for i in range(repeat):
                current_price = self.get_comm_data(sTrCode, sRecordName, i, "현재가")
                volume = self.get_comm_data(sTrCode, sRecordName, i, "거래량")
                open_price = self.get_comm_data(sTrCode, sRecordName, i, "시가")
                high_price = self.get_comm_data(sTrCode, sRecordName, i, "고가")
                low_price = self.get_comm_data(sTrCode, sRecordName, i, "저가")
                standard_day = self.get_comm_data(sTrCode, sRecordName, i, "일자")

                view.주식주봉차트조회요청(standard_day, current_price, open_price, high_price, low_price, volume)
            self.tr_event_loop.exit()





    # tr요청 기본 함수
    # tr 데이터 정보 입력
    def set_input_value(self, id, value):
        self.ocx.dynamicCall("SetInputValue(String, String)", id, value)

    # tr데이터 전송
    def send_comm_rq_data(self, rqname, trcode, next, screen_number):
        self.ocx.dynamicCall("CommRqData(String,String,int,String)", rqname, trcode, next, screen_number)
        self.tr_event_loop = QEventLoop()
        self.tr_event_loop.exec_()

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
        return trade_data

    def get_comm_data(self, trcode, record_name, next, rqname):
        comm_data = self.ocx.dynamicCall("GetCommData(String, String, int, String)", trcode, record_name, next, rqname)
        return comm_data
