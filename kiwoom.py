import pythoncom
from PyQt5.QtCore import QEventLoop

import constants
from PyQt5.QAxContainer import *


class Kiwoom:
    def __init__(self):
        self.login = False
        self.ocx = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.ocx.OnEventConnect.connect(self.on_event_connect)
        self.ocx.OnReceiveTrData.connect(self.trdata_slot)

        self.detail_account_info_event_loop = None


    # 로그인 메서드 호출
    def comm_connect(self):
        self.ocx.dynamicCall("CommConnect()")
        while not self.login:
            pythoncom.PumpWaitingMessages()

    # 로그인 성공 여부
    def on_event_connect(self, err_code):
        if err_code == 0:
            print("로그인 성공")
            self.login = True
        else:
            print("로그인 실패")

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

    def get_detail_account_info(self, deposit_name, pw, pw_mc, search5):
        print("계좌번호 및 비밀번호 등을 입력/서버에 요청")
        self.ocx.dynamicCall("SetInputValue(QString,QString)", "계좌번호", "8043137211")
        self.ocx.dynamicCall("SetInputValue(QString,QString)", "비밀번호", "0000")
        self.ocx.dynamicCall("SetInputValue(QString,QString)", "비밀번호입력매체구분", "00")
        self.ocx.dynamicCall("SetInputValue(QString,QString)", "조회구분", "2")
        self.ocx.dynamicCall("CommRqData(QString,QString,int,QString)", "예수금상세현황요청", "opw00001", 0, "2000")
        #self.detail_account_info_event_loop = QEventLoop()
        #self.detail_account_info_event_loop.exec_()

    def event_slots(self):
        self.OnEventConnect.connect(self.login_slot)
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
            deposit = self.dynamicCall("GetCommData(String, String, int, String)", sTrCode, sRQName, 0, "예수금")
            print("예수금 %s" % int(deposit))

            ok_deposit = self.dynamicCall("GetCommData(String, String, int, String)", sTrCode, sRQName, 0, "출금가능금액")
            print("출금가능금액 %s" % int(ok_deposit))
            #self.detail_account_info_event_loop.exit()
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



