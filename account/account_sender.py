import datetime
import time

from kiwoom import Kiwoom
from PyQt5.QtCore import QEventLoop, QCoreApplication


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


class Kiwoom_Send_Account:

    def __init__(self, main_kiwoom):
        self.Kiwoom = main_kiwoom

    def wait_continuous_result(self):
        while not self.Kiwoom.data_success:
            QCoreApplication.processEvents()
            time.sleep(0.2)
            if self.Kiwoom.continuous_data_success:
                self.Kiwoom.data_success = True

    # 단일정보 요청 - 예수금. 계좌평가
    def wait_result(self):
        while not self.Kiwoom.data_success:
            QCoreApplication.processEvents()
            time.sleep(0.2)
            if self.Kiwoom.return_list:
                self.Kiwoom.data_success = True

    # 예수금상세현황요청
    def send_detail_account_info(self, account):
        Kiwoom.set_input_value(self.Kiwoom, "계좌번호", account)
        Kiwoom.set_input_value(self.Kiwoom, "비밀번호", "0000")
        Kiwoom.set_input_value(self.Kiwoom, "비밀번호입력매체구분", "00")
        Kiwoom.set_input_value(self.Kiwoom, "조회구분", "2")
        Kiwoom.send_comm_rq_data(self.Kiwoom, "예수금상세현황요청", "opw00001", 0, "2000")

        self.wait_result()

        if self.Kiwoom.data_success:
            return self.Kiwoom.return_list

    # 계좌평가잔고내역요청 - 총수익률
    def send_detail_account_mystock(self, account, sPrevNext="2"):

        Kiwoom.set_input_value(self.Kiwoom, "계좌번호", account)
        Kiwoom.set_input_value(self.Kiwoom, "비밀번호", "0000")
        Kiwoom.set_input_value(self.Kiwoom, "비밀번호입력매체구분", "00")
        Kiwoom.set_input_value(self.Kiwoom, "조회구분", "2")
        Kiwoom.send_comm_rq_data(self.Kiwoom, "계좌평가잔고내역요청", "opw00018", 0, "2000")

        self.wait_continuous_result()
        self.Kiwoom.continuous_data_success = False

        if self.Kiwoom.data_success:
            return self.Kiwoom.return_list

    # 오늘날짜를 기준으로 term기간만큼 날짜 가져오기

    # 계좌별주문체결내역상세요청
    def send_trading_record(self, term, account, find_division, buy_or_sell, item_code):
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

        self.wait_continuous_result()
        self.Kiwoom.continuous_data_success = False

        if self.Kiwoom.data_success:
            return self.Kiwoom.return_list

    # opt10085 계좌수익률 요청
    def send_price_earning_ratio(self, account):
        Kiwoom.set_input_value(self.Kiwoom, "계좌번호", account)
        Kiwoom.send_comm_rq_data(self.Kiwoom, "계좌수익률요청", "opt10085", 0, "2000")

        self.wait_continuous_result()

        self.Kiwoom.continuous_data_success = False

        if self.Kiwoom.data_success:
            return self.Kiwoom.return_list

    # opt10076 체결요청
    def send_conclude_data(self, item_code, gubun, buy_or_sell, account):
        Kiwoom.set_input_value(self.Kiwoom, "종목코드", item_code)
        Kiwoom.set_input_value(self.Kiwoom, "조회구분", gubun)
        Kiwoom.set_input_value(self.Kiwoom, "매도수구분", buy_or_sell)
        Kiwoom.set_input_value(self.Kiwoom, "계좌번호", account)
        Kiwoom.set_input_value(self.Kiwoom, "비밀번호", "")
        Kiwoom.set_input_value(self.Kiwoom, "주문번호", "")
        Kiwoom.set_input_value(self.Kiwoom, "체결구분", "0")

        Kiwoom.send_comm_rq_data(self.Kiwoom, "체결요청", "opt10076", 0, "2000")

        self.wait_continuous_result()
        self.Kiwoom.continuous_data_success = False
        if self.Kiwoom.data_success:
            return self.Kiwoom.return_list

    # opt10074 일자별실현손익요청
    def send_day_earn_data(self, account, start_day, last_day):
        Kiwoom.set_input_value(self.Kiwoom, "계좌번호", account)
        Kiwoom.set_input_value(self.Kiwoom, "시작일자", start_day)
        Kiwoom.set_input_value(self.Kiwoom, "종료일자", last_day)
        Kiwoom.send_comm_rq_data(self.Kiwoom, "일자별실현손익요청", "opt10074", 0, "2000")

        self.wait_continuous_result()
        self.Kiwoom.continuous_data_success = False
        if self.Kiwoom.data_success:
            return self.Kiwoom.return_list
