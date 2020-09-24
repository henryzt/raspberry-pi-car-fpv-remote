from __main__ import app, socketio

def socket_emit(name, json):
    with app.test_request_context():
        socketio.emit(name, json)