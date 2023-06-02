import sys

from PyQt5.QtWidgets import *
from flask import Flask, jsonify, g

import constants
from kiwoom import Kiwoom

app = Flask(__name__)

@app.route("/buy")
def buy_stock():
    # 자동매매 로직에서 매수 작업을 수행하는 함수
    # ...
    result = start_test()
    return jsonify({"result": result})


@app.route("/sell")
def sell_stock():
    # 자동매매 로직에서 매도 작업을 수행하는 함수
    # ...

    return jsonify(3)


@app.route("/login")
def get_login():
    app1 = QApplication(sys.argv)
    if not app1:
        app1 = QApplication(sys.argv)  # QApplication 인스턴스 생성

    g.kiwoom = Kiwoom()

    if not app1:
        return jsonify(0)
    else:
        return jsonify(1)


@app.route("/sell1")
def start_auto_trading():
    result = start_test()

    return result


def start_test():
    # tr 요청
    name = g.kiwoom.get_master_code_name(constants.SAMSUNG_CODE)
    connectState = g.kiwoom.get_connect_state()
    lastPrice = g.kiwoom.get_master_last_price(constants.SAMSUNG_CODE)

    print("연결상태 : %d" % connectState)
    print("유저정보")
    print("------------------------------")
    print("계좌 수 : " + g.kiwoom.get_login_info("ACCOUNT_CNT"))
    print("계좌 번호 : " + g.kiwoom.get_login_info("ACCNO"))
    print(g.kiwoom.get_login_info("USER_ID"))
    print(g.kiwoom.get_login_info("USER_NAME"))
    print("------------------------------")
    print(name)
    print("------------------------------")
    print("전일가 : %s" % lastPrice)

    return name


if __name__ == "__main__":
    # 자동매매를 위한 PyQt5 애플리케이션 실행
    # start_auto_trading()

    # Flask 서버 실행
    app.run()
