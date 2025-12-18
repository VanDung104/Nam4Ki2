import paho.mqtt.client as mqtt
import json
import time
import random
from datetime import datetime

BROKER = "localhost"  # Đổi IP nếu Broker chạy trên máy khác
PORT = 1883
TOPIC = "sensors/temperature2"

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
        print(f"Sensor {sensor_id} published: {data}")
        time.sleep(1)

if __name__ == "__main__":
    publish_sensor_data(sensor_id=2)
