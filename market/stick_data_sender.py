from kiwoom import Kiwoom
import time
from PyQt5.QtCore import QEventLoop, QCoreApplication

class Kiwoom_Price:

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

    # 분봉차트 조회  /종목코드 , 분봉타입, 데이터 900단위로 몇개 받을지
    def send_minutes_chart_data(self, item_code, minute_type):

        Kiwoom.set_input_value(self.Kiwoom, "종목코드", item_code)
        Kiwoom.set_input_value(self.Kiwoom, "틱범위", minute_type)
        Kiwoom.set_input_value(self.Kiwoom, "수정주가구분", "0")
        Kiwoom.send_comm_rq_data(self.Kiwoom, "주식분봉차트조회요청", "opt10080", 0, "2000")

        print("요청보냈어요!")
        print(self.Kiwoom.remained_data)
        while self.Kiwoom.remained_data:
            time.sleep(0.2)
            Kiwoom.set_input_value(self.Kiwoom, "종목코드", item_code)
            Kiwoom.set_input_value(self.Kiwoom, "틱범위", minute_type)
            Kiwoom.set_input_value(self.Kiwoom, "수정주가구분", "0")
            Kiwoom.send_comm_rq_data(self.Kiwoom, "주식분봉차트조회요청", "opt10080", "2", "2000")
            print("남은 데이터 있어서 요청 더함")

        print("요청을 다보냄!!!!!!!!!!!!!!!!")

        self.wait_continuous_result()
        self.Kiwoom.continuous_data_success = False

        print(self.Kiwoom.return_list)

        if self.Kiwoom.data_success:
            return self.Kiwoom.return_list

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
