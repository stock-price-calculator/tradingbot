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
        self.Kiwoom.return_list.clear()

        Kiwoom.set_input_value(self.Kiwoom, "종목코드", item_code)
        Kiwoom.set_input_value(self.Kiwoom, "틱범위", minute_type)
        Kiwoom.set_input_value(self.Kiwoom, "수정주가구분", "0")
        Kiwoom.send_comm_rq_data(self.Kiwoom, "주식분봉차트조회요청", "opt10080", 0, "2000")

        while self.Kiwoom.remained_data:
            time.sleep(0.2)
            Kiwoom.set_input_value(self.Kiwoom, "종목코드", item_code)
            Kiwoom.set_input_value(self.Kiwoom, "틱범위", minute_type)
            Kiwoom.set_input_value(self.Kiwoom, "수정주가구분", "0")
            Kiwoom.send_comm_rq_data(self.Kiwoom, "주식분봉차트조회요청", "opt10080", "2", "2000")

        self.wait_continuous_result()
        self.Kiwoom.continuous_data_success = False

        if self.Kiwoom.data_success:
            return self.Kiwoom.return_list

    # 일봉차트 조회
    def send_day_chart_data(self, item_code, start_date):
        self.Kiwoom.return_list.clear()

        Kiwoom.set_input_value(self.Kiwoom, "종목코드", item_code)
        Kiwoom.set_input_value(self.Kiwoom, "기준일자", start_date)
        Kiwoom.set_input_value(self.Kiwoom, "수정주가구분", "0")
        Kiwoom.send_comm_rq_data(self.Kiwoom, "주식일봉차트조회요청", "opt10081", 0, "2000")

        while self.Kiwoom.remained_data:
            time.sleep(0.2)
            Kiwoom.set_input_value(self.Kiwoom, "종목코드", item_code)
            Kiwoom.set_input_value(self.Kiwoom, "기준일자", start_date)
            Kiwoom.set_input_value(self.Kiwoom, "수정주가구분", "0")
            Kiwoom.send_comm_rq_data(self.Kiwoom, "주식일봉차트조회요청", "opt10081", "2", "2000")

        self.wait_continuous_result()
        self.Kiwoom.continuous_data_success = False

        if self.Kiwoom.data_success:
            return self.Kiwoom.return_list

    # 주봉차트 조회
    def send_week_chart_data(self, item_code, start_date):
        self.Kiwoom.return_list.clear()

        Kiwoom.set_input_value(self.Kiwoom, "종목코드", item_code)
        Kiwoom.set_input_value(self.Kiwoom, "기준일자", start_date)
        Kiwoom.set_input_value(self.Kiwoom, "끝일자", "")
        Kiwoom.set_input_value(self.Kiwoom, "수정주가구분", "0")
        Kiwoom.send_comm_rq_data(self.Kiwoom, "주식주봉차트조회요청", "opt10082", 0, "2000")

        while self.Kiwoom.remained_data:
            time.sleep(0.2)

            Kiwoom.set_input_value(self.Kiwoom, "종목코드", item_code)
            Kiwoom.set_input_value(self.Kiwoom, "기준일자", start_date)
            Kiwoom.set_input_value(self.Kiwoom, "끝일자", "")
            Kiwoom.set_input_value(self.Kiwoom, "수정주가구분", "0")
            Kiwoom.send_comm_rq_data(self.Kiwoom, "주식주봉차트조회요청", "opt10082", "2", "2000")

        self.wait_continuous_result()
        self.Kiwoom.continuous_data_success = False

        if self.Kiwoom.data_success:
            return self.Kiwoom.return_list


    # 주식기본정보요청
    def send_market_information(self, item_code):
        self.Kiwoom.return_list.clear()
        Kiwoom.set_input_value(self.Kiwoom, "종목코드", item_code)
        Kiwoom.send_comm_rq_data(self.Kiwoom, "주식기본정보요청", "opt10001", 0, "2000")

        self.wait_result()

        if self.Kiwoom.data_success:
            return self.Kiwoom.return_list

    # 마켓 종목코드 전부 가져오기
    def get_total_market_code(self):
        result = self.Kiwoom.GetCodeListByMarket('0').split(';')

        return result

    # 종목 코드 받아서 이름 리턴
    def convert_code_to_name(self, item_code):
        result = self.Kiwoom.GetMarsterCodeName(item_code)

        return result

    # 이름을 받아서 종목 코드 리턴
    def find_item_name(self, item_code_list,item_name):

        for code in item_code_list:
            code_name = self.convert_code_to_name(code)
            # print(code_name)
            if code_name == item_name:
                return code

        return 0



