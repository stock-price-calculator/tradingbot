

def 예수금상세현황요청출력(ok_deposit, deposit, buy_deposit):
    print("--------------------------")
    print("출금가능금액 %s" % int(ok_deposit))
    print("예수금 %s" % int(deposit))
    print("주문가능금액 %s" % int(buy_deposit))
    print("--------------------------")

def 계좌평가잔고내역요청출력(total_buy_money, total_profit_loss_rate):
    print("--------------------------")
    print("총매입금액 %s" % int(total_buy_money))
    print("총수익률 %s" % float(total_profit_loss_rate))
    print("--------------------------")

def 계좌별주문체결내역상세요청출력(order_number, item_code, item_name, trade_count, trade_price, order_type):
    print("--------------------------")
    print("주문번호 :  %s" % order_number)
    print("종목번호 : %s" % item_code)
    print("종목명   : %s" % item_name)
    print("체결수량 : %s" % (trade_count))
    print("체결단가 : %s" % (trade_price))
    print("매매구분 : %s" % (order_type))
    print("--------------------------")

def 주식분봉차트조회요청(standard_minute, current_price, open_price, high_price, low_price, volume):
    print("--------------------------")
    print("분봉기준시간 : %s" % standard_minute)
    print("현재가 : %s" % current_price)
    print("시가   : %s" % open_price)
    print("고가 : %s" % high_price)
    print("저가 : %s" % low_price)
    print("거래량 : %s" % volume)
    print("--------------------------")

def 주식일봉차트조회요청(standard_day, current_price, open_price, high_price, low_price, volume):
    print("--------------------------")
    print("일봉기준날짜 : %s" % standard_day)
    print("현재가 : %s" % current_price)
    print("시가   : %s" % open_price)
    print("고가 : %s" % high_price)
    print("저가 : %s" % low_price)
    print("거래량 : %s" % volume)
    print("--------------------------")

def 주식주봉차트조회요청(standard_day, current_price, open_price, high_price, low_price, volume):
    print("--------------------------")
    print("주봉기준날짜 : %s" % standard_day)
    print("현재가 : %s" % current_price)
    print("시가   : %s" % open_price)
    print("고가 : %s" % high_price)
    print("저가 : %s" % low_price)
    print("거래량 : %s" % volume)
    print("--------------------------")

# receive_trdata 인자값들 출력
def print_receive_trdata_element(sScrNo, sRQName, sTrCode, sRecordName, sPrevNext):
    print(sScrNo)
    print(sRQName)
    print(sTrCode)
    print(sRecordName)
    print(sPrevNext)


