💬 Local Chat App

A real-time chat app that works entirely on your local WiFi network — no internet, no servers, just pure local communication.

✨ Features
🔒 Password-Protected Rooms — Keep chats private with secure room access
⚡ Real-Time Messaging — Instant communication using Socket.IO
✍️ Typing Indicator — See when someone is typing
🟢 Online Users Count — Track active participants in a room
💾 Persistent Chat History — Messages stored using SQLite
🌑 Dark Theme UI — Clean and eye-friendly interface
📱 Multi-Device Support — Works on mobile, PC, or laptop
🛠️ Tech Stack
Layer	Technology
Backend	Python + Flask
Real-Time	Flask-SocketIO + Eventlet
Database	SQLite
Frontend	HTML + CSS + JavaScript
Security	Werkzeug Password Hashing
🚀 Getting Started
1️⃣ Clone the Repository
git clone https://github.com/yourUsername/local-chat.git
cd local-chat
2️⃣ Create Virtual Environment
python -m venv .venv
3️⃣ Activate Environment
# Windows
.venv\Scripts\activate

# Mac / Linux
source .venv/bin/activate
4️⃣ Install Dependencies
pip install -r requirements.txt
5️⃣ Run the App
python app.py
6️⃣ Open in Browser
http://127.0.0.1:5000
📡 Connect with Friends (Same WiFi)

After running the app, you’ll see something like:

http://192.168.x.x:5000

👉 Share this link with your friends
👉 They can join instantly from their browser

🔐 How It Works
You (Host)	Your Friend
Enter your name	Enter their name
Create Room	Join Room
Set password	Enter password
Start chatting	Start chatting
📁 Project Structure
local_chat/
│
├── app.py
├── database.py
├── requirements.txt
│
├── templates/
│   ├── index.html
│   ├── lobby.html
│   └── chat.html
│
└── static/
    ├── css/
    │   └── style.css
    └── js/
        └── chat.js
⚙️ Requirements
Python 3.8+
pip
📝 License

This project is open-source and available under the MIT License.

💡 Why This Project?

No internet? No problem.
This app is perfect for:

Classroom communication
Office/local team chats
Offline LAN messaging
