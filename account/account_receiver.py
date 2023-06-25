import view.account_view as view
import json
import time

class Kiwoom_Receive_Account:

    def __init__(self, main_kiwoom):
        self.Kiwoom = main_kiwoom

    # 예수금상세현황요청 값 받기
    def receive_detail_account_info(self, sTrCode, sRQName):

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

    # 추청예상자금
    def receive_calculation_account_mystock(self, sTrCode, sRQName):

        calculation_value = self.Kiwoom.get_comm_data(sTrCode, sRQName, 0, "추정자산조회요청 ").strip()

         self.Kiwoom.return_list.append({
            "추정예상자금": calculation_value
        })
        
        self.Kiwoom.data_success = True

    # 계좌평가잔고내역요청 값 받기
    def receive_detail_account_mystock(self, sTrCode, sRQName):

        repeat = self.Kiwoom.get_repeat_cnt(sTrCode, sRQName)

        total_buy_money = (self.Kiwoom.get_comm_data(sTrCode, sRQName, 0, "총매입금액").strip())
        total_evaluation_money = (self.Kiwoom.get_comm_data(sTrCode, sRQName, 0, "총평가금액").strip())
        total_profit_money = (self.Kiwoom.get_comm_data(sTrCode, sRQName, 0, "총평가손익금액").strip())
        total_profit_loss_rate = (self.Kiwoom.get_comm_data(sTrCode, sRQName, 0, "총수익률(%)").strip())


        self.Kiwoom.return_list.append({
            "총매입금액": (total_buy_money),
            "총수익률": (total_profit_loss_rate),
            "총평가금액" : (total_evaluation_money),
            "총평가손익금액" :(total_profit_money),
        })

        # view.계좌평가잔고내역요청출력(total_buy_money,total_profit_loss_rate)
        # print(total_evaluation_money,total_profit_money)


        for i in range(repeat):
            item_code = self.Kiwoom.get_comm_data(sTrCode, sRQName, i, "종목코드").strip()
            item_name = self.Kiwoom.get_comm_data(sTrCode, sRQName, i, "종목명").strip()
            evaluation_profit_money = self.Kiwoom.get_comm_data(sTrCode, sRQName, i, "평가손익").strip()
            profit_ratio = self.Kiwoom.get_comm_data(sTrCode, sRQName, i, "수익률").strip()
            buy_price = self.Kiwoom.get_comm_data(sTrCode, sRQName, i, "매입가").strip()
            buy_count = self.Kiwoom.get_comm_data(sTrCode, sRQName, i, "보유수량").strip()
            current_price = self.Kiwoom.get_comm_data(sTrCode, sRQName, i, "현재가").strip()
            buy_total_money = self.Kiwoom.get_comm_data(sTrCode, sRQName, i, "매입금액").strip()
            total_tax = self.Kiwoom.get_comm_data(sTrCode, sRQName, i, "수수료합").strip()
            tax = self.Kiwoom.get_comm_data(sTrCode, sRQName, i, "세금").strip()
            buy_evaluation_total_money = self.Kiwoom.get_comm_data(sTrCode, sRQName, i, "평가금액").strip()
            my_total_percentage = self.Kiwoom.get_comm_data(sTrCode, sRQName, i, "보유비중(%)").strip()

            if item_code != "" or item_code is not None:
                list = []

                list.append({
                    "종목코드": item_code,
                    "종목명": item_name,
                    "평가손익": evaluation_profit_money,
                    "수익률": profit_ratio,
                    "매입가": buy_price,
                    "보유수량": buy_count,
                    "현재가": current_price,
                    "매입금액": buy_total_money,
                    "수수료합": total_tax,
                    "세금": tax,
                    "평가금액": buy_evaluation_total_money,
                    "보유비중(%)": my_total_percentage,
                })
                self.Kiwoom.return_list.append(list)
        self.Kiwoom.data_success = True


    # 계좌별주문체결내역상세요청 값 받기
    def receive_trading_record(self, sTrCode, sRQName, sRecordName):
        # self.Kiwoom.return_list.clear()  # 결과리스트 초기화
        repeat = self.Kiwoom.get_repeat_cnt(sTrCode, sRQName)
        cnt = 0
        for i in range(repeat):
            order_number = self.Kiwoom.get_comm_data(sTrCode, sRecordName, i, "주문번호").strip()
            item_code = self.Kiwoom.get_comm_data(sTrCode, sRecordName, i, "종목번호").strip()
            item_name = self.Kiwoom.get_comm_data(sTrCode, sRecordName, i, "종목명").strip()
            trade_time = self.Kiwoom.get_comm_data(sTrCode, sRecordName, i, "주문시간").strip()
            trade_count = self.Kiwoom.get_comm_data(sTrCode, sRecordName, i, "체결수량").strip()
            trade_price = self.Kiwoom.get_comm_data(sTrCode, sRecordName, i, "체결단가").strip()
            order_type = self.Kiwoom.get_comm_data(sTrCode, sRecordName, i, "매매구분").strip()

            if order_number != "" and order_number is not None:
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
            time.sleep(0.3)
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

            if trade_time != "" and trade_time is not None:
                view.계좌수익률요청(trade_time, item_code, item_name, trade_price, trade_buy_price, trade_total_price, item_buy_count)
                self.Kiwoom.return_list.append({
                    "일자": trade_time,
                    "종목코드": item_code,
                    "종목명": item_name,
                    "현재가": trade_price,
                    "매입가": trade_buy_price,
                    "매입금액": trade_total_price,
                    "보유수량": item_buy_count
                })

        self.Kiwoom.data_success = True

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

            self.Kiwoom.return_list.append({
                "주문번호": order_number,
                "종목명": item_name,
                "시간": time,
            })
        self.Kiwoom.data_success = True


    # opt10074 일자별실현손익요청
    def receive_day_earn_data(self,sTrCode, sRQName, sRecordName):
        repeat = self.Kiwoom.get_repeat_cnt(sTrCode, sRQName)

        total_buy_money = self.Kiwoom.get_comm_data(sTrCode, sRecordName, 0, "총매수금액").strip()
        total_sell_money = self.Kiwoom.get_comm_data(sTrCode, sRecordName, 0, "총매도금액").strip()
        profit_money = self.Kiwoom.get_comm_data(sTrCode, sRecordName, 0, "실현손익").strip()
        trade_charge = self.Kiwoom.get_comm_data(sTrCode, sRecordName, 0, "매매수수료").strip()
        trade_tax = self.Kiwoom.get_comm_data(sTrCode, sRecordName, 0, "매매세금").strip()

        self.Kiwoom.return_list.append({
            "총매수금액": total_buy_money,
            "총매도금액": total_sell_money,
            "실현손익": profit_money,
            "매매수수료": trade_charge,
            "매매세금": trade_tax,
        })

        for i in range(repeat):
            date = self.Kiwoom.get_comm_data(sTrCode, sRecordName, i, "일자").strip()
            buy_total_price = self.Kiwoom.get_comm_data(sTrCode, sRecordName, i, "매수금액").strip()
            sell_total_price = self.Kiwoom.get_comm_data(sTrCode, sRecordName, i, "매도금액").strip()
            day_profit_money = self.Kiwoom.get_comm_data(sTrCode, sRecordName, i, "당일매도손익").strip()
            day_trade_charge = self.Kiwoom.get_comm_data(sTrCode, sRecordName, i, "당일매매수수료").strip()
            day_trade_tax = self.Kiwoom.get_comm_data(sTrCode, sRecordName, i, "당일매매세금").strip()

            if date != "" and date is not None:
                list =[]

                list.append({
                    "일자": date,
                    "매수금액": buy_total_price,
                    "매도금액": sell_total_price,
                    "당일매도손익": day_profit_money,
                    "당일매매수수료": day_trade_charge,
                    "당일매매세금": day_trade_tax,
                })
                self.Kiwoom.return_list.append(list)
        self.Kiwoom.data_success = True
