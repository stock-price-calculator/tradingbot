


# 분봉차트 조회
def get_minutes_chart_data(self, item_code, minute_type):
    self.set_input_value("종목코드", item_code)
    self.set_input_value("틱범위", minute_type)
    self.set_input_value("수정주가구분", "0")
    self.send_comm_rq_data("주식분봉차트조회요청", "opt10080", 0, "2000")


# 일봉차트 조회
def get_day_chart_data(self, item_code, start_date):
    self.set_input_value("종목코드", item_code)
    self.set_input_value("기준일자", start_date)
    self.set_input_value("수정주가구분", "0")
    self.send_comm_rq_data("주식일봉차트조회요청", "opt10081", 0, "2000")


# 주봉차트 조회
def get_week_chart_data(self, item_code, start_date, last_date):
    self.set_input_value("종목코드", item_code)
    self.set_input_value("기준일자", start_date)
    self.set_input_value("끝일자", last_date)
    self.set_input_value("수정주가구분", "0")
    self.send_comm_rq_data("주식주봉차트조회요청", "opt10082", 0, "2000")


