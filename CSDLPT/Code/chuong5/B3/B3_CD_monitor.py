import paho.mqtt.client as mqtt
import json
import threading

BROKER = "localhost"
PORT = 1883
TOPIC = "sensors/temperature"
THRESHOLD = 30  # Ngưỡng cảnh báo nhiệt độ

def on_message(client, userdata, msg):
    monitor_id = userdata  # Nhận ID của Monitor từ userdata
    data = json.loads(msg.payload.decode())

    sensor_id = data["sensor_id"]
    temperature = data["temperature"]
    timestamp = data["timestamp"]

    # Kiểm tra ngưỡng nhiệt độ
    if temperature > THRESHOLD:
        print(f"Monitor {monitor_id} CẢNH BÁO! Sensor {sensor_id} quá nóng: {temperature}°C tại {timestamp}\n")
    else:
        print(f"Monitor {monitor_id} nhận dữ liệu từ Sensor {sensor_id}: {temperature}°C tại {timestamp}\n")

def subscribe_monitor(monitor_id):
    client = mqtt.Client(userdata=monitor_id)  # Gán monitor_id vào userdata
    client.on_message = on_message
    client.connect(BROKER, PORT, 60)
    client.subscribe(TOPIC)

    print(f"Monitor {monitor_id} đang lắng nghe dữ liệu...")
    client.loop_forever()

if __name__ == "__main__":
    num_monitors = 2  # Số lượng Monitor

    threads = []
    for i in range(1, num_monitors + 1):
        t = threading.Thread(target=subscribe_monitor, args=(i,), daemon=True)
        t.start()
        threads.append(t)

    try:
        while True:
            pass  # Giữ chương trình chạy
    except KeyboardInterrupt:
        print("\nDừng Monitor! Đang thoát...")
