import constants
from utility.change import *

from kiwoom import Kiwoom


class Kiwoom_Trade:
    def __init__(self, main_kiwoom):
        self.Kiwoom = main_kiwoom

    # 신규 매수 주문
    def send_buy_order(self, account, item_code, quantity, price, trading_type):
        order_params = {
            "rq_name": "신규매수주문",
            "screen_number": "2000",
            "account_number": account,
            "order_type": constants.NEW_BUY,
            "code": item_code,
            "stock_quantity": quantity,
            "price": price,
            "trading_type": changed_trading_type(trading_type),
            "origin_order_number": '',
        }
        result = Kiwoom.send_trading_data(self.Kiwoom, order_params)

        return result
    # 신규 매도 주문
    def send_sell_order(self, account, item_code, quantity, price, trading_type):
        order_params = {
            "rq_name": "신규매도주문",
            "screen_number": "2000",
            "account_number": account,
            "order_type": constants.NEW_SELL,
            "code": item_code,
            "stock_quantity": quantity,
            "price": price,
            "trading_type": changed_trading_type(trading_type),
            "origin_order_number": '',
        }
        result = Kiwoom.send_trading_data(self.Kiwoom, order_params)

        return result

    # 매수주문 취소
    def cancel_buy_order(self, account, item_code, quantity, price, trading_type, original_order_num):
        order_params = {
            "rq_name": "매수취소주문",
            "screen_number": "2000",
            "account_number": account,
            "order_type": constants.CANCEL_BUY,
            "code": item_code,
            "stock_quantity": quantity,
            "price": price,
            "trading_type": changed_trading_type(trading_type),
            "origin_order_number": original_order_num,
        }
        result = Kiwoom.send_trading_data(self.Kiwoom, order_params)

        return result

    # 매도주문 취소
    def cancel_sell_order(self, account, item_code, quantity, price, trading_type, original_order_num):
        order_params = {
            "rq_name": "매도취소주문",
            "screen_number": "2000",
            "account_number": account,
            "order_type": constants.CANCEL_BUY,
            "code": item_code,
            "stock_quantity": quantity,
            "price": price,
            "trading_type": changed_trading_type(trading_type),
            "origin_order_number": original_order_num,
        }

        result = Kiwoom.send_trading_data(self.Kiwoom, order_params)

        return result
