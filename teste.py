from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return "OIIIIIIIIIII"

@socketio.on('my event', namespace='/test')
def test_message(message):
    emit('my response', {'data': message['data']})


@socketio.on('connect', namespace='/test')
def test_connect():
    print("Cliente conectou")
    emit('my response', {'data': 'Connected'})

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app)