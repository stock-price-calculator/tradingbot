import datetime
import time


from kiwoom import Kiwoom


# term기간만큼 이전날짜 가져옴
def get_trading_record_date(term):
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


class Kiwoom_Account:

    def __init__(self, main_kiwoom):
        self.Kiwoom = main_kiwoom

    # 예수금상세현황요청
    def get_detail_account_info(self, account):
        Kiwoom.set_input_value(self.Kiwoom, "계좌번호", account)
        Kiwoom.set_input_value(self.Kiwoom, "비밀번호", "0000")
        Kiwoom.set_input_value(self.Kiwoom, "비밀번호입력매체구분", "00")
        Kiwoom.set_input_value(self.Kiwoom, "조회구분", "2")
        Kiwoom.send_comm_rq_data(self.Kiwoom, "예수금상세현황요청", "opw00001", 0, "2000")

    # 계좌평가잔고내역요청
    def get_detail_account_mystock(self, account, sPrevNext="0"):

        # sPrevNext="0" : 싱글데이터 받아오기(종목합계 데이터)
        Kiwoom.set_input_value(self.Kiwoom, "계좌번호", account)
        Kiwoom.set_input_value(self.Kiwoom, "비밀번호", "0000")
        Kiwoom.set_input_value(self.Kiwoom, "비밀번호입력매체구분", "00")
        Kiwoom.set_input_value(self.Kiwoom, "조회구분", "2")
        Kiwoom.send_comm_rq_data(self.Kiwoom, "계좌평가잔고내역요청", "opw00018", sPrevNext, "2000")

    # 오늘날짜를 기준으로 term기간만큼 날짜 가져오기

    # 체결내역
    def get_trading_record(self, term, account, find_division, buy_or_sell, item_code):
        print("체결내역 서버에 요청")

        # term기간만큼 이전날짜 가져옴
        all_date = get_trading_record_date(term)

        for day in reversed(all_date):
            Kiwoom.set_input_value(self.Kiwoom, "주문일자", day)
            Kiwoom.set_input_value(self.Kiwoom, "계좌번호", account)
            Kiwoom.set_input_value(self.Kiwoom, "비밀번호", "0000")
            Kiwoom.set_input_value(self.Kiwoom, "비밀번호입력매체구분", "00")
            Kiwoom.set_input_value(self.Kiwoom, "조회구분", find_division)
            Kiwoom.set_input_value(self.Kiwoom, "주식채권구분", "1")
            Kiwoom.set_input_value(self.Kiwoom, "매도수구분", buy_or_sell)
            Kiwoom.set_input_value(self.Kiwoom, "종목코드", item_code)
            Kiwoom.set_input_value(self.Kiwoom, "시작주문번호", "")
            Kiwoom.send_comm_rq_data(self.Kiwoom, "계좌별주문체결내역상세요청", "opw00007", 0, "2000")
            time.sleep(0.3)
