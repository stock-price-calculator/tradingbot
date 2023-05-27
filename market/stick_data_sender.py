from kiwoom import Kiwoom
import time


class Kiwoom_Price:

    def __init__(self, main_kiwoom):
        self.Kiwoom = main_kiwoom

    # 분봉차트 조회  /종목코드 , 분봉타입, 데이터 900단위로 몇개 받을지
    def send_minutes_chart_data(self, item_code, minute_type, data_count):
        Kiwoom.set_input_value(self.Kiwoom, "종목코드", item_code)
        Kiwoom.set_input_value(self.Kiwoom, "틱범위", minute_type)
        Kiwoom.set_input_value(self.Kiwoom, "수정주가구분", "0")
        Kiwoom.send_comm_rq_data(self.Kiwoom, "주식분봉차트조회요청", "opt10080", 0, "2000")
        data_count -= 1
        print("첫번째 보냄")
        if data_count == 0:
            print("wnat값 0설정")
            self.Kiwoom.want_data_count = 0  # count가 0일경우 또는 remain_data가 0일때 종료해야함
        while self.Kiwoom.remained_data and data_count > 0:
            print("두번째 보냄")
            time.sleep(0.2)
            data_count -= 1
            Kiwoom.set_input_value(self.Kiwoom, "종목코드", item_code)
            Kiwoom.set_input_value(self.Kiwoom, "틱범위", minute_type)
            Kiwoom.set_input_value(self.Kiwoom, "수정주가구분", "0")
            Kiwoom.send_comm_rq_data(self.Kiwoom, "주식분봉차트조회요청", "opt10080", 2, "2000")
            self.Kiwoom.want_data_count = data_count


    # 일봉차트 조회
    def send_day_chart_data(self, item_code, start_date):
        Kiwoom.set_input_value(self.Kiwoom, "종목코드", item_code)
        Kiwoom.set_input_value(self.Kiwoom, "기준일자", start_date)
        Kiwoom.set_input_value(self.Kiwoom, "수정주가구분", "0")
        Kiwoom.send_comm_rq_data(self.Kiwoom, "주식일봉차트조회요청", "opt10081", 0, "2000")

    # 주봉차트 조회
    def send_week_chart_data(self, item_code, start_date, last_date):
        Kiwoom.set_input_value(self.Kiwoom, "종목코드", item_code)
        Kiwoom.set_input_value(self.Kiwoom, "기준일자", start_date)
        Kiwoom.set_input_value(self.Kiwoom, "끝일자", last_date)
        Kiwoom.set_input_value(self.Kiwoom, "수정주가구분", "0")
        Kiwoom.send_comm_rq_data(self.Kiwoom, "주식주봉차트조회요청", "opt10082", 0, "2000")
