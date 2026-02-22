import os
from flask import Flask, send_file
from flask_socketio import SocketIO
import pyautogui

pyautogui.PAUSE = 0 

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLIENT_DIR = os.path.join(BASE_DIR, 'client')

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    html_path = os.path.join(CLIENT_DIR, 'index.html')
    return send_file(html_path)

@socketio.on('move')
def handle_move(data):
    try:
        pyautogui.move(int(data.get('dx', 0)), int(data.get('dy', 0)))
    except pyautogui.FailSafeException:
        pass

@socketio.on('click')
def handle_click(data):
    button_type = data.get('button', 'left') 
    pyautogui.click(button=button_type)

if __name__ == '__main__':
    print("🚀 Magic Trackpad Server is running!")
    print("Ensure your phone is on the same Wi-Fi network.")
    socketio.run(app, host='0.0.0.0', port=3000)
