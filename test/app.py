# import sys
# from flask import Flask, render_template
# from flask_socketio import SocketIO, emit
# from kiwoom import Kiwoom  # Assuming you have a Kiwoom class for interacting with Kiwoom Securities
#
# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'your-secret-key'
# socketio = SocketIO(app)
#
# kiwoom = None  # Global Kiwoom instance for handling real-time data
#
# @app.route('/')
# def index():
#     return render_template('index.html')  # HTML template for displaying real-time data
#
# @socketio.on('connect', namespace='/realtime')
# def connect_realtime():
#     global kiwoom
#
#     if not kiwoom:
#         kiwoom = Kiwoom()  # Instantiate the Kiwoom class if not already created
#     kiwoom.connect_login()
#
#     kiwoom.SetRealReg("0001", "005930", "20;10", "0")  # Register for real-time data
#
#     while True:
#         data = kiwoom.get_comm_real_data("005930", 10)  # Retrieve the real-time data for a specific stock (e.g., Samsung)
#
#         socketio.emit('realtime_data', data, namespace='/realtime')
#         socketio.sleep(1)  # Adjust the sleep duration as per your requirements
#
# if __name__ == '__main__':
#     socketio.run(app, debug=True)
from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__)
# app.config['SECRET_KEY'] = '123'  # Set a secret key for the application
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('./index.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('server_message', 'You are connected')  # Send a message to the client

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')



if __name__ == '__main__':
    socketio.run(app, debug=True)