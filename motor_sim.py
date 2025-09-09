# motor_sim.py
import os
import time
import random
import socketio

URL = os.getenv("TWIN_URL", "http://localhost:5050")
sio = socketio.Client(reconnection=True, reconnection_attempts=0)

running = True  # motor state

@sio.event
def connect():
    print(f"[OK] Connected to {URL}")

@sio.event
def disconnect():
    print("[INFO] Disconnected from server")

# 👇 New event: listen for commands
@sio.on("motor_command")
def on_motor_command(data):
    global running
    cmd = data.get("action")
    if cmd == "stop":
        running = False
        print("[CMD] Motor stopped by twin")
    elif cmd == "start":
        running = True
        print("[CMD] Motor started by twin")

def ensure_connected():
    while not sio.connected:
        try:
            sio.connect(URL, wait=True, transports=["websocket", "polling"])
        except Exception as e:
            print("[WARN] Connect failed:", e)
            time.sleep(1)

def main():
    ensure_connected()
    try:
        while True:
            if running:
                motor_data = {
                    "rpm": random.randint(800, 1200),
                    "temperature": round(random.uniform(60, 100), 2),
                }
                sio.emit("motor_data", motor_data, namespace="/")
                print("Sending:", motor_data)
            else:
                print("Motor is stopped, no data...")
            time.sleep(2)
    except KeyboardInterrupt:
        pass
    finally:
        if sio.connected:
            sio.disconnect()

if __name__ == "__main__":
    main()

