import json
import sys
import time
import numpy as np
from PyQt5.QtWidgets import *
from flask import Flask, jsonify, request, render_template
import constants
from kiwoom import Kiwoom
from threading import Thread, Event
from account.account_sender import Kiwoom_Send_Account
from order.trade import Kiwoom_Trade
from market.stick_data_sender import Kiwoom_Price
from backtesting.backtest import Kiwoom_BackTesting
from price.calculator import calculateEPS
from price.dto.eps import EPS
from realtime.trading import Kiwoom_Real_trade
from flask_restx import Api, Resource, reqparse
from flask_cors import CORS

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})

# api swagger
api = Api(app, version='1.0', title='API 문서', description='Swagger 문서', doc="/api-docs")

test_api = api.namespace('test', description='조회 API')

kiwoom = None
kiwoom_account = None
kiwoom_trade = None
kiwoom_price = None
kiwoom_backtest = None
kiwoom_real_trading = None


# socketio = SocketIO(app)

# api swagger
@test_api.route('/')
class Test(Resource):
    def get(self):
        return 'Hello World!'


@app.route("/test")
def index():
    return render_template('index.html')


# 처음 로그인 요청
@app.route("/login")
def get_login():
    global kiwoom

    if not kiwoom:
        kiwoom = Kiwoom()
    kiwoom.connect_login()
    return jsonify({'result': True})


# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# 유저 이름, 계좌, id
@app.route("/user/information", methods=['GET'])
def get_user_data():
    id = kiwoom.get_login_info("USER_ID")
    name = kiwoom.get_login_info("USER_NAME")
    account = kiwoom.get_login_info("ACCNO")

    if not name and id and account:
        return jsonify({"result": "정보를 불러오는데 실패했습니다."})
    else:
        return jsonify({"id": id, "name": name, "account": account})


# 예수금
@app.route("/user/account/info", methods=['GET'])
def get_user_money():
    result = kiwoom_account.send_detail_account_info(constants.ACCOUNT)

    if not result:
        return jsonify({"result": "정보를 불러오는데 실패했습니다."})
    else:
        return jsonify(result)


# 계좌평가잔고내역요청 - 총수익률,총 매입금액, 수익률
@app.route("/user/account/mystock", methods=['GET'])
def get_user_mystock_money():


    if kiwoom.return_list:
        time.sleep(1)

    result = kiwoom_account.send_detail_account_mystock(constants.ACCOUNT)

    result_data = result[:]

    calculation_money = kiwoom_account.send_calculation_account_money(constants.ACCOUNT)

    result_data[0]["추정예산자금"] = calculation_money[0].get("추정예상자금")


    if not result:
        return jsonify({"result": "정보를 불러오는데 실패했습니다."})
    else:
        return jsonify(result_data)


# 추정예산자금
@app.route("/user/account/total_money", methods=['GET'])
def get_user_total_money():
    result = kiwoom_account.send_calculation_account_money(constants.ACCOUNT)

    if not result:
        return jsonify({"result": "정보를 불러오는데 실패했습니다."})
    else:
        return jsonify(result[0].get("추정예상자금"))


# 계좌별주문체결내역상세요청 - 날짜별 체결내역 opw00007
@app.route("/user/account/record", methods=['POST'])
def get_user_order_history():
    # 지금기점으로 가져올 기간 / 계좌번호  / 0: 전체 1:매도 2:매수 /종목코드 : 비우면 전체
    # result = kiwoom_account.send_trading_record(1, constants.ACCOUNT, "1", "0", "")
    data = request.get_json()

    term = data['term']
    buy_or_sell = data['buy_or_sell']
    item_code = data['item_code']

    result = kiwoom_account.send_trading_record(term, constants.ACCOUNT, "1", buy_or_sell, item_code)

    if not result:
        return jsonify({"result": "정보를 불러오는데 실패했습니다."})
    else:
        return jsonify(result)


# 계좌수익률요청 - 보유 주식량 확인
@app.route("/user/account/profit", methods=['GET'])
def get_user_profit():
    result = kiwoom_account.send_price_earning_ratio(constants.ACCOUNT)

    if not result:
        return jsonify({"result": "정보를 불러오는데 실패했습니다."})
    else:
        return jsonify(result)


# 체결요청
@app.route("/user/account/conclusion", methods=['GET'])
def get_user_conclusion():
    result = kiwoom_account.send_conclude_data(constants.SAMSUNG_CODE, "1", "0", constants.ACCOUNT)
    if not result:
        return jsonify({"result": "정보를 불러오는데 실패했습니다."})
    else:
        return jsonify(result)


# 일자별실현손익요청
@app.route("/user/account/day-profit", methods=['POST'])
def get_user_day_profit():

    data = request.get_json()

    start_day = data['start_day']
    last_day = data['last_day']

    if kiwoom.return_list:
        time.sleep(1)

    result = kiwoom_account.send_day_earn_data(constants.ACCOUNT, start_day, last_day)
    if not result:
        return jsonify({"result": "정보를 불러오는데 실패했습니다."})
    else:
        return jsonify(result)


# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# 매매코드

# 매수주문 계좌번호/종목코드/수량/가격/구매타입
@app.route("/order/buy", methods=['POST'])
def send_buy_order():
    # 계좌 / 종목코드 / 수량 / 가격(시장가 = 0) / "지정가", "시장가"
    # buy_order = kiwoom_trade.send_buy_order(constants.ACCOUNT, constants.SAMSUNG_CODE, 1, 0, "시장가")
    data = request.get_json()

    item_code = data['item_code']
    quantity = data['quantity']
    price = data['price']
    trading_type = data['trading_type']

    buy_order = kiwoom_trade.send_buy_order(constants.ACCOUNT, item_code, quantity, price, trading_type)

    return jsonify(buy_order)


# 매도주문 계좌번호/종목코드/수량/가격/구매타입
@app.route("/order/sell", methods=['POST'])
def send_sell_order():
    # 계좌 / 종목코드 / 수량 / 가격(시장가 = 0) / "지정가", "시장가"
    # buy_order = kiwoom_trade.send_buy_order(constants.ACCOUNT, constants.SAMSUNG_CODE, 1, 0, "시장가")
    data = request.get_json()

    item_code = data['item_code']
    quantity = data['quantity']
    price = data['price']
    trading_type = data['trading_type']
    sell_order = kiwoom_trade.send_sell_order(constants.ACCOUNT, item_code, quantity, price, trading_type)

    return jsonify(sell_order)


# 매수주문 취소
@app.route("/order/cancel/buy", methods=['POST'])
def send_cancel_buy_order():
    data = request.get_json()
    print(data['account'], data['item_code'], data['quantity'], data['price'], data['trading_type'])

    cancel_buy_order = kiwoom_trade.cancel_buy_order(data['account'], data['item_code'], data['quantity'],
                                                     data['price'], data['trading_type'], data['original_order_num'])

    return jsonify(cancel_buy_order)


# 매도주문 취소
@app.route("/order/cancel/sell", methods=['POST'])
def send_cancel_sell_order():
    data = request.get_json()
    print(data['account'], data['item_code'], data['quantity'], data['price'], data['trading_type'])

    cancel_sell_order = kiwoom_trade.cancel_sell_order(data['account'], data['item_code'], data['quantity'],
                                                       data['price'], data['trading_type'], data['original_order_num'])

    return jsonify(cancel_sell_order)


# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# 종목명 -> 종목코드로 변환
@app.route("/market/item_code", methods=['POST'])
def send_item_list():
    data = request.get_json()

    item_name = data['item_name']

    # 모든 시장 코드 가져오기
    item_code_list = kiwoom_price.get_total_market_code()

    # 이름 입력 -> 코드 리턴
    result_name = kiwoom_price.find_item_name(item_code_list, item_name)

    if result_name == 0:
        return jsonify({"result": "정보를 불러오는데 실패했습니다."})
    else:
        return jsonify(result_name)


# 주식 기본정보
@app.route("/market/information", methods=['POST'])
def send_item_information():
    data = request.get_json()

    item_code = data['item_code']

    item_information = kiwoom_price.send_market_information(item_code)

    if not item_information:
        return jsonify({"result": "정보를 불러오는데 실패했습니다."})
    else:
        return jsonify(item_information)


# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# 백테스팅 코드

# 분봉 백테스팅
@app.route("/backtest/minutes", methods=['POST'])
def send_minute_backtest():
    data = request.get_json()

    item_code = data['item_code']
    minute_type = data['minute_type']
    profit_ratio = data['profit_ratio']
    loss_ratio = data['loss_ratio']
    bollinger_n = data['bollinger_n']
    bollinger_k = data['bollinger_k']

    # result = kiwoom_backtest.bollinger_backtesting(item_code, minute_type, data, 1.02, 0.982)
    # data = kiwoom_price.send_minutes_chart_data(constants.SAMSUNG_CODE, "5")

    total_data = kiwoom_price.send_minutes_chart_data(item_code, minute_type)
    print("분봉 데이터 완료")
    result = kiwoom_backtest.bollinger_backtesting(item_code, minute_type, total_data, profit_ratio, loss_ratio,
                                                   bollinger_n, bollinger_k)
    if not result:
        return jsonify({"result": "정보를 불러오는데 실패했습니다."})
    else:
        return jsonify(result)


# 일봉 백테스팅
@app.route("/backtest/day", methods=['POST'])
def send_day_backtest():
    data = request.get_json()

    item_code = data['item_code']
    start_date = data['start_date']
    time_type = data['time_type']
    profit_ratio = data['profit_ratio']
    loss_ratio = data['loss_ratio']
    bollinger_n = data['bollinger_n']
    bollinger_k = data['bollinger_k']

    # start_date = 20230505 라면 20200101 ~ 2023.05.05 까지의 데이터를 가져옴
    total_data = kiwoom_price.send_day_chart_data(item_code, start_date)
    print("일봉 데이터 완료")
    result = kiwoom_backtest.bollinger_backtesting(item_code, time_type, total_data, profit_ratio, loss_ratio,
                                                   bollinger_n, bollinger_k)
    if not result:
        return jsonify({"result": "정보를 불러오는데 실패했습니다."})
    else:
        return jsonify(result)


# 주봉 백테스팅
@app.route("/backtest/week", methods=['POST'])
def send_week_backtest():
    data = request.get_json()

    item_code = data['item_code']
    start_date = data['start_date']
    time_type = data['time_type']
    profit_ratio = data['profit_ratio']
    loss_ratio = data['loss_ratio']
    bollinger_n = data['bollinger_n']
    bollinger_k = data['bollinger_k']

    total_data = kiwoom_price.send_week_chart_data(item_code, start_date)
    print("주봉 데이터 완료")
    result = kiwoom_backtest.bollinger_backtesting(item_code, time_type, total_data, profit_ratio, loss_ratio,
                                                   bollinger_n, bollinger_k)
    if not result:
        return jsonify({"result": "정보를 불러오는데 실패했습니다."})
    else:
        return jsonify(result)


#
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# 실시간 매매

@app.route("/real_trading_start", methods=['POST'])
def start1_real_trading():
    # 화면번호, 종목코드, 등록할 FID, 종목코드, 시간타입, 익절, 손절, 볼린저n , k
    # kiwoom_real_trading.SetRealReg("0111", item_code, "10", "0", time_type, 2.03, 0.982, 20, 2)

    data = request.get_json()

    item_code = data['item_code']
    time_type = data['time_type']  # 분봉, 일봉, 주봉
    profit_ratio = data['profit_ratio']
    loss_ratio = data['loss_ratio']
    bollinger_n = data['bollinger_n']
    bollinger_k = data['bollinger_k']
    get_parm = data['get_time']  # 분봉일때는 분봉타입, 일봉, 주봉일 때는 start_date
    balance = data['balance']  # 투자할 총 금액

    # time_type마다 분리
    if time_type == "minute":
        total_data = kiwoom_price.send_minutes_chart_data(item_code, get_parm)
    elif time_type == "day":
        total_data = kiwoom_price.send_day_chart_data(item_code, get_parm)
    else:
        total_data = kiwoom_price.send_week_chart_data(item_code, get_parm)

    # result = kiwoom_backtest.bollinger_backtesting(item_code, "5", total_data, profit_ratio, loss_ratio,
    #                                                bollinger_n, bollinger_k)

    # 볼린저값 리스트
    result_list = kiwoom_backtest.plot_bollinger_bands(total_data, bollinger_n, bollinger_k)

    # 그래프로 만들기
    # kiwoom_backtest.set_graph(result_list, bollinger_n)

    # 매수 가능 금액
    can_buy_money = kiwoom_account.send_detail_account_info(constants.ACCOUNT)

    kiwoom.real_item_code = item_code  # 종목코드
    kiwoom.real_time_type = time_type  # 분봉, 일봉, 주봉
    kiwoom.real_trade_parm = get_parm  # 시작시간 or 분봉타입
    kiwoom.real_profit_ratio = profit_ratio  # 익절
    kiwoom.real_loss_ratio = loss_ratio  # 손절
    kiwoom.real_bollinger_n = bollinger_n
    kiwoom.real_bollinger_k = bollinger_k
    kiwoom.real_total_data = result_list  # 이전 데이터
    kiwoom.real_balance = balance
    kiwoom.real_can_buy_money = abs(int(can_buy_money[0]["주문가능금액"]))


    result = 1
    if not result:
        return jsonify({"result": "정보를 불러오는데 실패했습니다."})
    else:
        return jsonify({"result": "자동매매 시작"})

@app.route("/start", methods=['POST'])
def start():
    data = request.get_json()

    item_code = data['item_code']
    kiwoom.real_start = True

    # kiwoom_real_trading.SetRealReg(item_code)
    return jsonify({"result": "자동매매 시작"})

@app.route("/real_trading_current_price", methods=['POST'])
def set_real_trading_current_price():
    data = request.get_json()

    current_price = data['current_price']

    kiwoom_trade.real_current_price = current_price
    kiwoom_real_trading.real_trade_start()

    return jsonify({"result": "현재값 변경 완료"})

# 실시간 매매 종료
@app.route("/real_trading_stop", methods=['GET'])
def stop_real_trading():
    kiwoom_real_trading.stop_real_trading()  # Set up real-time data subscription

    return jsonify({"result": "실시간 매매 종료"})



@app.route("/price", methods=['GET'])
def get_price():
    code = request.args.get("code")
    results: [EPS] = calculateEPS(code)
    price = results[len(results) - 1].sp_eps * 10
    price = np.round(price, -1)
    return jsonify({
        "result": price
    })


# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# Flask 서버 실행
def run_flask_app():
    # socketio.init_app(app)
    app.run(host='0.0.0.0', port=5000, debug=True)
    # socketio.run(app, debug=True)


# Kiwoom 서버 실행
def run_kiwoom_app():
    global kiwoom
    global kiwoom_account
    global kiwoom_trade
    global kiwoom_price
    global kiwoom_backtest
    global kiwoom_real_trading

    app1 = QApplication(sys.argv)  # QApplication 인스턴스 생성
    kiwoom = Kiwoom()
    kiwoom_account = Kiwoom_Send_Account(kiwoom)
    kiwoom_trade = Kiwoom_Trade(kiwoom)
    kiwoom_price = Kiwoom_Price(kiwoom)
    kiwoom_backtest = Kiwoom_BackTesting(kiwoom)
    kiwoom_real_trading = Kiwoom_Real_trade(kiwoom, kiwoom_trade, kiwoom_account)
    app1.exec_()


if __name__ == "__main__":
    t = Thread(target=run_kiwoom_app)
    t.daemon = True  # 백그라운드 스레드로 실행
    t.start()

    run_flask_app()
