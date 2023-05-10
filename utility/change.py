import constants



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