import smbus2
import bme280
import json
import time
import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion
import yaml
import os
import datetime


def load_config():
    try:
        config_path = "/usr/bin/app/config.yaml"
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        return config
    except FileNotFoundError:
        print("Błąd: Plik konfiguracyjny 'config.yaml' nie został znaleziony.")
        return None

def read_sample():
    data = bme280.sample(bus, I2C_ADDRESS, calibration_params)
    return {
	"timestamp": datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
	"temperature": round(data.temperature, 1),
	"humidity": int(data.humidity),
	"pressure": int(data.pressure)
	}


def on_connect(client, userdata, flags, rc, properties):
    global REQUEST_TOPIC
    if rc == 0:
        print("Połączono z brokerem MQTT!")
        client.subscribe(REQUEST_TOPIC)
        print(f"Nasłuchuję na temacie: {REQUEST_TOPIC}")
        print(f'Aktualny czas: {datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")}')
    else:
        print(f"Błąd połączenia, kod: {rc}")

def on_message(client, userdata, msg):
    global REQUEST_TOPIC
    print(f"Otrzymano wiadomość na temacie: {msg.topic}")
    
    if msg.topic == REQUEST_TOPIC:
        print("Otrzymano żądanie odczytu danych. Odczytuję i wysyłam...")
        
        data = read_sample()
        payload = json.dumps(data)
        
        client.publish(DATA_TOPIC, payload)
        print(f"Wysłano dane na temat {DATA_TOPIC}: {payload}")

if __name__ == "__main__":
    
    full_config = load_config()
    
    config = full_config["weather_sensor"]
    
    if config:
        global DATA_TOPIC, REQUEST_TOPIC
        I2C_PORT = config.get("i2c_port")
        print(I2C_PORT)
        I2C_ADDRESS = config.get("i2c_address")

        BROKER_ADDRESS = config.get("broker_address")
        BROKER_PORT = config.get("broker_port")
        DATA_TOPIC = config.get("data_topic")
        REQUEST_TOPIC = config.get("request_topic")
    
    
    bus = smbus2.SMBus(I2C_PORT)

    calibration_params = bme280.load_calibration_params(bus, I2C_ADDRESS)
    
    client = mqtt.Client(CallbackAPIVersion.VERSION2, "weather-sensor")
    client.on_connect = on_connect

    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(BROKER_ADDRESS, BROKER_PORT)

    print("Uruchamiam klienta MQTT w trybie nasłuchiwania...")
    client.loop_forever()


