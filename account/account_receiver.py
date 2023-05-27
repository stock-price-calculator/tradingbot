import view.account_view as view


class Kiwoom_Receive_Account:

    def __init__(self, main_kiwoom):
        self.Kiwoom = main_kiwoom

    # 예수금상세현황요청 값 받기
    def receive_detail_account_info(self, sTrCode, sRQName):
        deposit = self.Kiwoom.get_comm_data(sTrCode, sRQName, 0, "예수금").strip()
        ok_deposit = self.Kiwoom.get_comm_data(sTrCode, sRQName, 0, "출금가능금액").strip()
        buy_deposit = self.Kiwoom.get_comm_data(sTrCode, sRQName, 0, "주문가능금액").strip()
        view.예수금상세현황요청출력(ok_deposit, deposit, buy_deposit)

    # 계좌평가잔고내역요청 값 받기
    def receive_detail_account_mystock(self, sTrCode, sRQName):
        total_buy_money = self.Kiwoom.get_comm_data(sTrCode, sRQName, 0, "총매입금액").strip()
        total_profit_loss_rate = self.Kiwoom.get_comm_data(sTrCode, sRQName, 0, "총수익률(%)").strip()
        view.계좌평가잔고내역요청출력(total_buy_money, total_profit_loss_rate)

    # 계좌별주문체결내역상세요청 값 받기
    def receive_trading_record(self, sTrCode, sRQName, sRecordName):
        repeat = self.Kiwoom.get_repeat_cnt(sTrCode, sRQName)

        for i in range(repeat):
            order_number = self.Kiwoom.get_comm_data(sTrCode, sRecordName, i, "주문번호").strip()
            item_code = self.Kiwoom.get_comm_data(sTrCode, sRecordName, i, "종목번호").strip()
            item_name = self.Kiwoom.get_comm_data(sTrCode, sRecordName, i, "종목명").strip()
            trade_time = self.Kiwoom.get_comm_data(sTrCode, sRecordName, i, "주문시간").strip()
            trade_count = self.Kiwoom.get_comm_data(sTrCode, sRecordName, i, "체결수량").strip()
            trade_price = self.Kiwoom.get_comm_data(sTrCode, sRecordName, i, "체결단가").strip()
            order_type = self.Kiwoom.get_comm_data(sTrCode, sRecordName, i, "매매구분").strip()

            if order_number != "":
                view.계좌별주문체결내역상세요청출력(order_number, item_code, item_name, trade_time, trade_count, trade_price,
                                     order_type)

    # 10085 계좌수익률요청
    def receive_price_earning_ratio(self, sTrCode, sRecordName):

        trade_time = self.Kiwoom.get_comm_data(sTrCode, sRecordName, 0, "일자").strip()
        item_code = self.Kiwoom.get_comm_data(sTrCode, sRecordName, 0, "종목코드").strip()
        item_name = self.Kiwoom.get_comm_data(sTrCode, sRecordName,0, "종목명").strip()
        trade_price = self.Kiwoom.get_comm_data(sTrCode, sRecordName, 0, "현재가").strip()
        trade_buy_price = self.Kiwoom.get_comm_data(sTrCode, sRecordName, 0, "매입가").strip()
        trade_total_price = self.Kiwoom.get_comm_data(sTrCode, sRecordName,0, "매입금액").strip()
        item_buy_count = self.Kiwoom.get_comm_data(sTrCode, sRecordName, 0, "보유수량").strip()


