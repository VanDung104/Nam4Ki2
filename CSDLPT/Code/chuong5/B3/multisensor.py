import paho.mqtt.client as mqtt
import json
import time
import random
import threading
from datetime import datetime

BROKER = "localhost"
PORT = 1883
TOPIC = "sensors/temperature"

# Sự kiện để dừng các cảm biến
stop_event = threading.Event()

def publish_sensor_data(sensor_id):
    client = mqtt.Client()
    client.connect(BROKER, PORT, 60)

    while not stop_event.is_set():  # Chạy đến khi có tín hiệu dừng
        temperature = round(random.uniform(20, 35), 2)
        data = {
            "sensor_id": sensor_id,
            "temperature": temperature,
            "timestamp": datetime.now().isoformat()
        }
        client.publish(TOPIC, json.dumps(data))
        print(f"Sensor {sensor_id} gửi: {data}")
        time.sleep(1)

if __name__ == "__main__":
    num_sensors = 3
    threads = []

    for i in range(1, num_sensors + 1):
        t = threading.Thread(target=publish_sensor_data, args=(i,))
        t.start()
        threads.append(t)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nDừng chương trình! Đang thoát...")
        stop_event.set()  # Báo hiệu tất cả các luồng dừng
        for t in threads:
            t.join()  # Chờ tất cả các luồng kết thúc
