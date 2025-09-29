import streamlit as st
import paho.mqtt.client as mqtt
import json
import time
import yaml


def load_config():
    try:
        config_path = "/usr/bin/app/config.yaml"
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        return config
    except FileNotFoundError:
        print("Błąd: Plik konfiguracyjny 'config.yaml' nie został znaleziony.")
        return None

config = load_config()
weather_sensor = config["weather_sensor"]
broker_config = config["broker"]

MQTT_BROKER = broker_config.get("broker_address")
MQTT_PORT = broker_config.get("broker_port")
MQTT_TOPIC = weather_sensor.get("data_topic")
MQTT_TOPIC_REQUEST = weather_sensor.get("request_topic")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

data = {
    "timestamp": "Connecting...",
    "temperature": "Connecting...",
    "humidity": "Connecting...",
    "pressure": "Connecting..."
}

def on_connect(client, userdata, flags, reason_code, properties):
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    global data
    try:
        data = json.loads(msg.payload.decode("utf-8"))
    except json.JSONDecodeError:
        print("Błąd: Nieprawidłowy format JSON")


client.on_message = on_message
client.on_connect = on_connect
try:
    client.connect(MQTT_BROKER)
    client.loop_start()
    st.success("Connected to MQTT Broker!")
except Exception as e:
    st.error(f"Nie udało się połączyć z brokerem MQTT: {e}")

st.title("Dane z czujnika pogody 🌡️🍃")
st.subheader("Automatyczne odświeżanie co 1 sekundę")

placeholder_timestamp = st.empty()
placeholder_temp = st.empty()
placeholder_hum = st.empty()
placeholder_press = st.empty()

while True:
    client.publish(MQTT_TOPIC_REQUEST)
    with placeholder_timestamp.container():
        st.metric(label="Timestamp", value=f"{data['timestamp']}")
    
    with placeholder_temp.container():
        st.metric(label="Temperatura", value=f"{data['temperature']} °C")
    
    with placeholder_hum.container():
        st.metric(label="Wilgotność", value=f"{data['humidity']} %")
        
    with placeholder_press.container():
        st.metric(label="Ciśnienie", value=f"{data['pressure']} hPa")

    time.sleep(1)
    