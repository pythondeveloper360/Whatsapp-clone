from flask import Flask, request
from flask_socketio import SocketIO
import database

app = Flask(__name__)
app.config['SECRET_KEY'] = database.tokenGenerator()
socketio = SocketIO(app=app)

@app.route('/authUserLogin', methods=['POST'])
def authUserLogin():
    username, token, client_id = request.headers.get(
        'username'), request.headers.get('token'), request.headers.get('client_id')
    response = database.authUserLogin(
        username=username, token=token, client_id=client_id)
    if response:
        return {"auth": True}
    return {"auth": False}


@app.route('/authUser', methods=['POST'])
def loginUser():
    username, password,date = request.headers.get(
        'username'), request.headers.get('password'),request.headers.get('date')
    response = database.loginUser(username=username, password=password,date = date)
    if response:
        return response
    return {'auth': False}


if __name__ == '__main__':
    socketio.run(app,debug=True, host='0.0.0.0', port=8000)
