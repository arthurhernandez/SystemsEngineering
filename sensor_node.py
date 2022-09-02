
#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import time
from Ips331_class import lps331
from adx import adxl343

# White Bar Code Label Number on Each Raspberry Pi
sensor_id = 986293
temperature = 21
pressure = 31
x_acceleration = 0.001
y_acceleration = 0.002
z_acceleration = 1.001

def on_message(client, userdata, message):
#    print("topic:", message.topic)
    print("message:", message.payload.decode('UTF-8'))

def on_connect(client,userdata,flags,rc):
	client.subscribe("sensors/986293/temperature")
	pass

client = mqtt.Client()
client.on_message=on_message
client.on_connect=on_connect
client.connect("pivot.iuiot.org")
client.loop_start()
while(1):
    adxx = adxl343()
    ips = lps331()
    print("Publish Temperature, Pressure, and Accelerometer Data")
    temp = ips.read_temperature()
    press = ips.read_pressure()
    x = adxx.read_x_axis()
    y = adxx.read_y_axis()
    z = adxx.read_z_axis()
    client.publish(f"sensors/{sensor_id}/temperature",f"{temp}")
    client.publish(f"sensors/{sensor_id}/pressure",f"{press}")
    client.publish(f"sensors/{sensor_id}/accel/x",f"{x}")
    client.publish(f"sensors/{sensor_id}/accel/y",f"{y}")
    client.publish(f"sensors/{sensor_id}/accel/z",f"{z}")
    time.sleep(5)
