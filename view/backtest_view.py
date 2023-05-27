



def bollinger_backtesting_result(item_code, time_type,per, myasset, count, win_count):
    print("----------------------------------------------┐")
    print("종목 코드 :", item_code)
    print("종목 이름 : ", item_code, " 거래막대 타입 : ", time_type)
    print("퍼센트 : ", per)
    print("내 자산 : ", myasset)
    print("거래 수 :", count)
    print("이득 :", win_count, " 손해:", count - win_count)
    print("----------------------------------------------┘")