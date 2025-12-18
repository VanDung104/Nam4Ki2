import paho.mqtt.client as mqtt
import json

BROKER = "localhost"
PORT = 1883
TOPIC = "sensors/temperature"

def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode())
    print(f"Nhận dữ liệu từ Sensor {data['sensor_id']}: {data['temperature']}°C tại {data['timestamp']}")

def subscribe_monitor():
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(BROKER, PORT, 60)
    client.subscribe(TOPIC)
    client.loop_forever()

if __name__ == "__main__":
    subscribe_monitor()
