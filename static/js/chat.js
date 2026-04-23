const socket = io();

const messagesArea    = document.getElementById("messages-area");
const msgInput        = document.getElementById("msg-input");
const sendBtn         = document.getElementById("send-btn");
const onlineCount     = document.getElementById("online-count");
const typingIndicator = document.getElementById("typing-indicator");

let typingTimer = null;

window.addEventListener("load", () => {
  socket.emit("user_joined", { username: CURRENT_USER, room: CURRENT_ROOM });
  scrollToBottom();
  msgInput.focus();
});

function sendMessage() {
  const text = msgInput.value.trim();
  if (!text) return;
  socket.emit("send_message", { username: CURRENT_USER, message: text, room: CURRENT_ROOM });
  msgInput.value = "";
  socket.emit("stop_typing", { username: CURRENT_USER, room: CURRENT_ROOM });
  clearTimeout(typingTimer);
  msgInput.focus();
}

sendBtn.addEventListener("click", sendMessage);

msgInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); sendMessage(); }
});

msgInput.addEventListener("input", () => {
  socket.emit("typing", { username: CURRENT_USER, room: CURRENT_ROOM });
  clearTimeout(typingTimer);
  typingTimer = setTimeout(() => {
    socket.emit("stop_typing", { username: CURRENT_USER, room: CURRENT_ROOM });
  }, 1500);
});

// ── SOCKET EVENTS ────────────────────────────────────

// নতুন message আসলে
socket.on("receive_message", (data) => {
  addMessage(data.username, data.message, data.timestamp);
  scrollToBottom();

  // নিজের message না হলে notification title দেখাও
  if (data.username !== CURRENT_USER) {
    flashTitle(`💬 ${data.username}: ${data.message}`);
  }
});

// User join/leave notification
socket.on("user_update", (data) => {
  onlineCount.textContent = data.online_count;

  const action = data.type === "joined" ? "room এ ঢুকেছে 👋" : "বের হয়ে গেছে 👋";
  addSystemMessage(`${data.user} ${action}`);
  scrollToBottom();
});

// Typing দেখানো
socket.on("user_typing", (data) => {
  typingIndicator.textContent = `${data.username} লিখছে...`;
});

socket.on("user_stop_typing", () => {
  typingIndicator.textContent = "";
});

// ── HELPER FUNCTIONS ─────────────────────────────────

function addMessage(username, message, timestamp) {
  const isSelf = (username === CURRENT_USER);
  const row = document.createElement("div");
  row.className = `msg msg-new ${isSelf ? "msg-self" : "msg-other"}`;

  if (isSelf) {
    row.innerHTML = `
      <div class="msg-bubble msg-bubble-self">
        <p class="msg-text">${escapeHTML(message)}</p>
        <span class="msg-time">${timestamp}</span>
      </div>`;
  } else {
    row.innerHTML = `
      <div class="msg-avatar">${username[0].toUpperCase()}</div>
      <div>
        <div class="msg-sender">${escapeHTML(username)}</div>
        <div class="msg-bubble msg-bubble-other">
          <p class="msg-text">${escapeHTML(message)}</p>
          <span class="msg-time">${timestamp}</span>
        </div>
      </div>`;
  }

  messagesArea.appendChild(row);
}

function addSystemMessage(text) {
  const div = document.createElement("div");
  div.className = "system-msg";
  div.textContent = `📌 ${text}`;
  messagesArea.appendChild(div);
}

function scrollToBottom() {
  messagesArea.scrollTop = messagesArea.scrollHeight;
}

// XSS থেকে বাঁচার জন্য HTML escape
function escapeHTML(str) {
  const div = document.createElement("div");
  div.appendChild(document.createTextNode(str));
  return div.innerHTML;
}

// Browser tab এ notification দেখানো
let originalTitle = document.title;
function flashTitle(msg) {
  if (document.hidden) {
    document.title = msg;
    setTimeout(() => { document.title = originalTitle; }, 3000);
  }
}
