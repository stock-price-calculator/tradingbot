

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

def 계좌별주문체결내역상세요청출력(order_number, item_code,  item_name, trade_time, trade_count, trade_price, order_type):
    print("--------------------------")
    print("주문시간 : %s" %trade_time)
    print("주문번호 : %s" % order_number)
    print("종목번호 : %s" % item_code)
    print("종목명   : %s" % item_name)
    print("체결수량 : %s" % (trade_count))
    print("체결단가 : %s" % (trade_price))
    print("매매구분 : %s" % (order_type))
    print("--------------------------")

def 계좌수익률요청(trade_time, item_code, item_name, trade_price, trade_buy_price, trade_total_price, item_buy_count):
    print("--------------------------")
    print("일자 : %s" % trade_time)
    print("종목코드 : %s" % item_code)
    print("종목명   : %s" % item_name)
    print("현재가 : %s" % (trade_price))
    print("매입가 : %s" % (trade_buy_price))
    print("매입총금액 : %s" % (trade_total_price))
    print("보유수량 : %s" % (item_buy_count))
    print("--------------------------")

# receive_trdata 인자값들 출력
def print_receive_trdata_element(sScrNo, sRQName, sTrCode, sRecordName, sPrevNext):
    print(sScrNo)
    print(sRQName)
    print(sTrCode)
    print(sRecordName)
    print(sPrevNext)


