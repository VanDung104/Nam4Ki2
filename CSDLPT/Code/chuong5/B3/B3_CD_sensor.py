import paho.mqtt.client as mqtt
import json
import time
import random
import threading
from datetime import datetime

BROKER = "localhost"  # Thay bằng IP nếu Broker chạy trên máy khác
PORT = 1883
TOPIC = "sensors/temperature"
DELAY = 5  # Gửi dữ liệu mỗi 5 giây

def publish_sensor_data(sensor_id):
    client = mqtt.Client()
    client.connect(BROKER, PORT, 60)

    while True:
        temperature = round(random.uniform(20, 35), 2)  # Giả lập nhiệt độ
        data = {
            "sensor_id": sensor_id,
            "temperature": temperature,
            "timestamp": datetime.now().isoformat()
        }
        client.publish(TOPIC, json.dumps(data))
        print(f"Sensor {sensor_id} gửi: {data}\n")
        time.sleep(DELAY)  # Chờ 5 giây trước khi gửi tiếp

if __name__ == "__main__":
    num_sensors = 3  # Số lượng cảm biến
    threads = []

    for i in range(1, num_sensors + 1):
        t = threading.Thread(target=publish_sensor_data, args=(i,), daemon=True)
        t.start()
        threads.append(t)

    try:
        while True:
            time.sleep(1)  # Giữ chương trình chạy
    except KeyboardInterrupt:
        print("\nDừng chương trình! Đang thoát...")
