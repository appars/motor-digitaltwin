from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
# Logging helps during debugging; keep or set to False later
socketio = SocketIO(app, cors_allowed_origins="*", logger=True, engineio_logger=True)

motor_state = {"rpm": 0, "temperature": 0, "running": True}

@app.route("/")
def index():
    return render_template("index.html", motor=motor_state)

@socketio.on("connect")
def on_connect():
    print("[WS] Dashboard connected")

@socketio.on("disconnect")
def on_disconnect():
    print("[WS] Dashboard disconnected")

# Telemetry from simulator -> push to dashboards
@socketio.on("motor_data")
def handle_motor_data(data):
    global motor_state
    motor_state.update(data)
    print(f"[TELEMETRY] {motor_state}")
    # NOTE: no 'broadcast' kwarg on v5
    socketio.emit("update_dashboard", motor_state)

# Dashboard control -> relay to simulator(s)
@socketio.on("motor_command")
def handle_motor_command(data):
    action = (data or {}).get("action")
    if action in ("start", "stop"):
        motor_state["running"] = (action == "start")
        print(f"[CTRL] Relayed motor command: {action}")
        socketio.emit("motor_command", {"action": action})
        socketio.emit("update_dashboard", motor_state)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5050, debug=True)

