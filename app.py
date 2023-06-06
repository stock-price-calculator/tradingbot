import sys
from PyQt5.QtWidgets import *
from flask import Flask, jsonify
from flask_restful import Api, Resource
import constants
from kiwoom import Kiwoom
from threading import Thread

app = Flask(__name__)
api = Api(app)

kiwoom = None



class Login(Resource):
    def get(self):
        global kiwoom

        if not kiwoom:
            kiwoom = Kiwoom()

        kiwoom.connect_login()

        return 0

# 처음 로그인 요청
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

    if not kiwoom:
        return jsonify(0)
    name = kiwoom.get_master_code_name(constants.SAMSUNG_CODE)

    if not name:
        return jsonify(0)
    else:
        return jsonify(name)

# Flask 서버 실행
def run_flask_app():
    app.run(debug=True)

# Kiwoom 서버 실행
def run_kiwoom_app():
    global kiwoom

    app1 = QApplication(sys.argv)  # QApplication 인스턴스 생성
    kiwoom = Kiwoom()
    app1.exec_()

api.add_resource(Login, '/login')

if __name__ == "__main__":

    # app1 = QApplication(sys.argv)  # QApplication 인스턴스 생성
    # t = Thread(target=run_flask_app)
    # t.daemon = True  # 백그라운드 스레드로 실행
    # t.start()
    # kiwoom = Kiwoom()
    # app1.exec_()

    t = Thread(target=run_kiwoom_app)
    t.daemon = True  # 백그라운드 스레드로 실행
    t.start()

    run_flask_app()


