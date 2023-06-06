import view.account_view as view
import json


class Kiwoom_Receive_Account:

    def __init__(self, main_kiwoom):
        self.Kiwoom = main_kiwoom


    # 예수금상세현황요청 값 받기
    def receive_detail_account_info(self, sTrCode, sRQName):
        self.Kiwoom.return_list.clear()

        deposit = self.Kiwoom.get_comm_data(sTrCode, sRQName, 0, "예수금").strip()
        ok_deposit = self.Kiwoom.get_comm_data(sTrCode, sRQName, 0, "출금가능금액").strip()
        buy_deposit = self.Kiwoom.get_comm_data(sTrCode, sRQName, 0, "주문가능금액").strip()

        self.Kiwoom.return_list.append({
            "예수금": deposit,
            "출금가능금액" :ok_deposit,
            "주문가능금액" :buy_deposit
        })
        view.예수금상세현황요청출력(ok_deposit, deposit, buy_deposit)
        self.Kiwoom.data_success = True



    # 계좌평가잔고내역요청 값 받기
    def receive_detail_account_mystock(self, sTrCode, sRQName):
        self.Kiwoom.return_list.clear()  # 결과리스트 초기화

        total_buy_money = self.Kiwoom.get_comm_data(sTrCode, sRQName, 0, "총매입금액").strip()
        total_profit_loss_rate = self.Kiwoom.get_comm_data(sTrCode, sRQName, 0, "총수익률(%)").strip()

        self.Kiwoom.return_list.append({
            "총매입금액": total_buy_money,
            "총수익률(%)": total_profit_loss_rate,
        })
        view.계좌평가잔고내역요청출력(total_buy_money, total_profit_loss_rate)
        self.Kiwoom.data_success = True



    # 계좌별주문체결내역상세요청 값 받기
    def receive_trading_record(self, sTrCode, sRQName, sRecordName):
        self.Kiwoom.return_list.clear()  # 결과리스트 초기화
        repeat = self.Kiwoom.get_repeat_cnt(sTrCode, sRQName)

        for i in range(repeat):
            order_number = self.Kiwoom.get_comm_data(sTrCode, sRecordName, i, "주문번호").strip()
            item_code = self.Kiwoom.get_comm_data(sTrCode, sRecordName, i, "종목번호").strip()
            item_name = self.Kiwoom.get_comm_data(sTrCode, sRecordName, i, "종목명").strip()
            trade_time = self.Kiwoom.get_comm_data(sTrCode, sRecordName, i, "주문시간").strip()
            trade_count = self.Kiwoom.get_comm_data(sTrCode, sRecordName, i, "체결수량").strip()
            trade_price = self.Kiwoom.get_comm_data(sTrCode, sRecordName, i, "체결단가").strip()
            order_type = self.Kiwoom.get_comm_data(sTrCode, sRecordName, i, "매매구분").strip()

            if order_number != "" or order_number is None:
                view.계좌별주문체결내역상세요청출력(order_number, item_code, item_name, trade_time, trade_count, trade_price,
                                     order_type)
            self.Kiwoom.return_list.append({
                "주문번호": order_number,
                "종목번호": item_code,
                "종목명": item_name,
                "주문시간": trade_time,
                "체결수량": trade_count,
                "체결단가": trade_price,
                "매매구분": order_type
            })

        self.Kiwoom.data_success = True

    # 10085 계좌수익률요청
    def receive_price_earning_ratio(self, sTrCode, sRQName, sRecordName):

        repeat = self.Kiwoom.get_repeat_cnt(sTrCode, sRQName)

        for i in range(repeat):
            trade_time = self.Kiwoom.get_comm_data(sTrCode, sRecordName, i, "일자").strip()
            item_code = self.Kiwoom.get_comm_data(sTrCode, sRecordName, i, "종목코드").strip()
            item_name = self.Kiwoom.get_comm_data(sTrCode, sRecordName, i, "종목명").strip()
            trade_price = abs(int(self.Kiwoom.get_comm_data(sTrCode, sRecordName, i, "현재가").strip()))
            trade_buy_price = self.Kiwoom.get_comm_data(sTrCode, sRecordName, i, "매입가").strip()
            trade_total_price = self.Kiwoom.get_comm_data(sTrCode, sRecordName,i, "매입금액").strip()
            item_buy_count = self.Kiwoom.get_comm_data(sTrCode, sRecordName, i, "보유수량").strip()

            view.계좌수익률요청(trade_time, item_code, item_name, trade_price, trade_buy_price, trade_total_price, item_buy_count)

    # opt10076 체결요청
    def receive_conclude_data(self, sTrCode, sRQName, sRecordName):
        repeat = self.Kiwoom.get_repeat_cnt(sTrCode, sRQName)

        for i in range(repeat):
            order_number = self.Kiwoom.get_comm_data(sTrCode, sRecordName, i, "주문번호").strip()
            item_name = self.Kiwoom.get_comm_data(sTrCode, sRecordName, i, "종목명").strip()
            time = self.Kiwoom.get_comm_data(sTrCode, sRecordName, i, "시간").strip()

            print(order_number)
            print(item_name)
            print(time)

    # opt10074 일자별실현손익요청
    def receive_day_earn_data(self,sTrCode, sRQName, sRecordName):
        repeat = self.Kiwoom.get_repeat_cnt(sTrCode, sRQName)

        total_buy_money = self.Kiwoom.get_comm_data(sTrCode, sRecordName, 0, "총매수금액").strip()
        total_sell_money = self.Kiwoom.get_comm_data(sTrCode, sRecordName, 0, "총매도금액").strip()
        profit_money = self.Kiwoom.get_comm_data(sTrCode, sRecordName, 0, "실현손익").strip()
        trade_charge = self.Kiwoom.get_comm_data(sTrCode, sRecordName, 0, "매매수수료").strip()
        trade_tax = self.Kiwoom.get_comm_data(sTrCode, sRecordName, 0, "매매세금").strip()

        print("총매수금액 : " + total_buy_money)
        print("총매도금액 : " + total_sell_money)
        print("실현손익 : " + profit_money)
        print("매매수수료 : " + trade_charge)
        print("매매세금 : " + trade_tax)

        for i in range(repeat):
            date = self.Kiwoom.get_comm_data(sTrCode, sRecordName, i, "일자").strip()
            buy_total_price = self.Kiwoom.get_comm_data(sTrCode, sRecordName, i, "매수금액").strip()
            sell_total_price = self.Kiwoom.get_comm_data(sTrCode, sRecordName, i, "매도금액").strip()
            day_profit_money = self.Kiwoom.get_comm_data(sTrCode, sRecordName, i, "당일매도손익").strip()
            day_trade_charge = self.Kiwoom.get_comm_data(sTrCode, sRecordName, i, "당일매매수수료").strip()
            day_trade_tax = self.Kiwoom.get_comm_data(sTrCode, sRecordName, i, "당일매매세금").strip()

            print("-------------------------------------")
            print("일자 : " + date)
            print("매수금액 : " + buy_total_price)
            print("매도금액 : " + sell_total_price)
            print("당일매도손익 : " + day_profit_money)
            print("당일매매수수료 : " + day_trade_charge)
            print("당일매매세금 : " + day_trade_charge)
            print("-------------------------------------")