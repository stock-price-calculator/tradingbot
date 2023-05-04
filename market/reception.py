import view.market_view as view


class Kiwoom_Receive_Market_price:

    def __init__(self, main_kiwoom):
        self.Kiwoom = main_kiwoom
    #분봉차트 값 받기
    def receive_minutes_chart_data(self,sTrCode, sRQName, sRecordName):
        repeat = self.Kiwoom.get_repeat_cnt(sTrCode, sRQName)

        received_data = []
        for i in range(1):
            current_price = self.Kiwoom.get_comm_data(sTrCode, sRecordName, i, "현재가").strip()
            volume = self.Kiwoom.get_comm_data(sTrCode, sRecordName, i, "거래량").strip()
            open_price = self.Kiwoom.get_comm_data(sTrCode, sRecordName, i, "시가").strip()
            high_price = self.Kiwoom.get_comm_data(sTrCode, sRecordName, i, "고가").strip()
            low_price = self.Kiwoom.get_comm_data(sTrCode, sRecordName, i, "저가").strip()
            standard_minute = self.Kiwoom.get_comm_data(sTrCode, sRecordName, i, "체결시간").strip()
            received_data.append([standard_minute,current_price,open_price,high_price,low_price,volume])
            print(received_data)
            #view.주식분봉차트조회요청(standard_minute, current_price, open_price, high_price, low_price, volume)

    # 일봉차트 값 받기
    def receive_day_chart_data(self,sTrCode, sRQName, sRecordName):
        repeat = self.Kiwoom.get_repeat_cnt(sTrCode, sRQName)

        for i in range(repeat):
            current_price = self.Kiwoom.get_comm_data(sTrCode, sRecordName, i, "현재가").strip()
            volume = self.Kiwoom.get_comm_data(sTrCode, sRecordName, i, "거래량").strip()
            open_price = self.Kiwoom.get_comm_data(sTrCode, sRecordName, i, "시가").strip()
            high_price = self.Kiwoom.get_comm_data(sTrCode, sRecordName, i, "고가").strip()
            low_price = self.Kiwoom.get_comm_data(sTrCode, sRecordName, i, "저가").strip()
            standard_day = self.Kiwoom.get_comm_data(sTrCode, sRecordName, i, "일자").strip()

            view.주식일봉차트조회요청(standard_day, current_price, open_price, high_price, low_price, volume)

    # 주봉차트 값 받기
    def receive_week_chart_data(self, sTrCode, sRQName, sRecordName):
        repeat = self.Kiwoom.get_repeat_cnt(sTrCode, sRQName)

        for i in range(repeat):
            current_price = self.Kiwoom.get_comm_data(sTrCode, sRecordName, i, "현재가").strip()
            volume = self.Kiwoom.get_comm_data(sTrCode, sRecordName, i, "거래량").strip()
            open_price = self.Kiwoom.get_comm_data(sTrCode, sRecordName, i, "시가").strip()
            high_price = self.Kiwoom.get_comm_data(sTrCode, sRecordName, i, "고가").strip()
            low_price = self.Kiwoom.get_comm_data(sTrCode, sRecordName, i, "저가").strip()
            standard_day = self.Kiwoom.get_comm_data(sTrCode, sRecordName, i, "일자").strip()

            view.주식주봉차트조회요청(standard_day, current_price, open_price, high_price, low_price, volume)
