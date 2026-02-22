import os
from socket import socket
from flask import Flask, send_file
from flask_socketio import SocketIO
import pyautogui
import socket
import qrcode

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

@socketio.on('scroll')
def handle_scroll(data):
    dy = float(data.get('dy', 0)) * 0.5
    pyautogui.scroll(dy)

@socketio.on('click')
def handle_click(data):
    button_type = data.get('button', 'left') 
    pyautogui.click(button=button_type)


if __name__ == '__main__':
    print("🚀 Magic Trackpad Server is running!")
    print("Ensure your phone is on the same Wi-Fi network.")

    ip_addresses = socket.gethostbyname_ex(socket.gethostname())[2]
    filtered_ips = [ip for ip in ip_addresses if not ip.startswith("127.")]

    img = qrcode.make(filtered_ips[0])
    qr = qrcode.QRCode()

    qr.add_data('http://' + filtered_ips[0] + ':3000')

    qr.print_ascii()
    
    socketio.run(app, host='0.0.0.0', port=3000)
