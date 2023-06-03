import sys

from PyQt5.QtWidgets import *
from flask import Flask, jsonify, g
import constants
from kiwoom import Kiwoom
from threading import Thread
import asyncio

app = Flask(__name__)

kiwoom = None
@app.route("/")
def get_root():
    return jsonify("hello")

# def login_async():
#     global kiwoom
#
#     if not kiwoom:
#         kiwoom = Kiwoom()
#     kiwoom.connect_login()  # 비동기적으로 로그인 처리
#     return jsonify(0)

# @app.route("/login")
# def get_login():
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     result = loop.run_until_complete(login_async())
#     loop.close()
#     return result

@app.route("/login")
def get_login():
    global kiwoom

    if not kiwoom:
        kiwoom = Kiwoom()

    kiwoom.connect_login()

    return jsonify(0)


@app.route("/test")
def start_test():
    # tr 요청
    # kiwoom = get_kiwoom()
    global kiwoom
    name = kiwoom.get_master_code_name(constants.SAMSUNG_CODE)

    return jsonify(name)

def run_flask_app():
    app.run()

if __name__ == "__main__":

    app1 = QApplication(sys.argv)  # QApplication 인스턴스 생성
    t = Thread(target=run_flask_app)
    t.daemon = True  # 백그라운드 스레드로 실행
    t.start()
    kiwoom = Kiwoom()
    app1.exec_()


