import pythoncom
import constants
from PyQt5.QAxContainer import *


class Kiwoom:
    def __init__(self):
        self.login = False
        self.ocx = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.ocx.OnEventConnect.connect(self.on_event_connect)

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

    def get_chejan_data(self, value):
        result = self.ocx.dynamicCall("GetChejanData(int)", value)
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
