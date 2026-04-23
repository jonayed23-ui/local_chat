import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit, join_room, leave_room
from database import (create_tables, create_room, verify_room,
                      save_message, get_recent_messages)
import socket

app = Flask(__name__)
app.secret_key = "local_chat_secret_2024"

socketio = SocketIO(app, async_mode="eventlet", cors_allowed_origins="*")

room_users = {}

create_tables()

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        if username:
            session["username"] = username
            return redirect(url_for("lobby"))
    return render_template("index.html")

@app.route("/lobby", methods=["GET", "POST"])
def lobby():
    if "username" not in session:
        return redirect(url_for("index"))
    error = None
    if request.method == "POST":
        action    = request.form.get("action")
        room_name = request.form.get("room_name", "").strip()
        password  = request.form.get("password", "").strip()
        if not room_name or not password:
            error = "Room নাম এবং Password দুটোই দিতে হবে।"
        elif action == "create":
            success = create_room(room_name, password, session["username"])
            if success:
                session["room"] = room_name
                return redirect(url_for("chat"))
            else:
                error = f'"{room_name}" নামের Room আগেই আছে। অন্য নাম দাও।'
        elif action == "join":
            result = verify_room(room_name, password)
            if result == "ok":
                session["room"] = room_name
                return redirect(url_for("chat"))
            elif result == "not_found":
                error = f'"{room_name}" নামের কোনো Room নেই।'
            else:
                error = "Password ভুল! আবার চেষ্টা করো।"
    return render_template("lobby.html", username=session["username"], error=error)

@app.route("/chat")
def chat():
    if "username" not in session or "room" not in session:
        return redirect(url_for("index"))
    messages = get_recent_messages(session["room"], 50)
    return render_template("chat.html",
                           username=session["username"],
                           room=session["room"],
                           messages=messages)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@socketio.on("user_joined")
def handle_join(data):
    username  = data.get("username")
    room_name = data.get("room")
    join_room(room_name)
    if room_name not in room_users:
        room_users[room_name] = set()
    room_users[room_name].add(username)
    emit("user_update", {
        "type":         "joined",
        "user":         username,
        "online_count": len(room_users[room_name])
    }, to=room_name)

@socketio.on("send_message")
def handle_message(data):
    username  = data.get("username")
    message   = data.get("message", "").strip()
    room_name = data.get("room")
    if not message:
        return
    save_message(room_name, username, message)
    emit("receive_message", {
        "username": username,
        "message":  message,
        "timestamp": "এইমাত্র"
    }, to=room_name)

@socketio.on("typing")
def handle_typing(data):
    emit("user_typing", {"username": data.get("username")},
         to=data.get("room"), include_self=False)

@socketio.on("stop_typing")
def handle_stop_typing(data):
    emit("user_stop_typing", {"username": data.get("username")},
         to=data.get("room"), include_self=False)

@socketio.on("disconnect")
def handle_disconnect():
    username  = session.get("username")
    room_name = session.get("room")
    if username and room_name:
        leave_room(room_name)
        if room_name in room_users:
            room_users[room_name].discard(username)
        emit("user_update", {
            "type":         "left",
            "user":         username,
            "online_count": len(room_users.get(room_name, set()))
        }, to=room_name)

if __name__ == "__main__":
    local_ip = get_local_ip()
    print("\n" + "="*50)
    print("  🚀 Local Chat App চালু হয়েছে!")
    print("="*50)
    print(f"  এই device:     http://127.0.0.1:5000")
    print(f"  WiFi তে অন্যরা: http://{local_ip}:5000")
    print("="*50 + "\n")
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)