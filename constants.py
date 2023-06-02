
import sys

class _constant:
    def __setattr__(self, name, value):
        if (name in self.__dict__):
            raise Exception('변수에 값을 할당할 수 없습니다.')
            self.__dict__[name] = value

    def __delattr__(self, name):
        if name in self.__dict__:
            raise Exception('변수를 삭제할 수 없습니다.')


sys.modules[__name__] = _constant()

_constant.ERROR_CODE = -1
_constant.LIMIT_PRICE = "지정가"
_constant.LIMIT_PRICE_VALUE = "00"

_constant.MARKET_PRICE = "시장가"
_constant.MARKET_PRICE_VALUE = "03"

_constant.NEW_BUY = 1
_constant.NEW_SELL = 2
_constant.CANCEL_BUY = 3
_constant.CANCEL_SELL = 4
_constant.CHANGE_BUY = 5
_constant.CHANGE_SELL = 6

# app.py

_constant.ACCOUNT = "8051014511"
_constant.SAMSUNG_CODE = "005930"
_constant.LG_CODE ="066570"

#backtest.py
_constant.TRADE_CHARGE = 0.015
