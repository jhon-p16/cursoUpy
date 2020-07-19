import network
import time
from umqtt.robust import MQTTClient
import os
import gc
import sys

from machine import Pin, I2C
#from time import sleep
import BME280

i2c = I2C(scl=Pin(22), sda=Pin(23), freq=10000)
bme = BME280.BME280(i2c=i2c)



# WiFi connection information
WIFI_SSID = ''
WIFI_PASSWORD = ''
# turn off the WiFi Access Point
ap_if = network.WLAN(network.AP_IF)
ap_if.active(False)

# connect the device to the WiFi network
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(WIFI_SSID, WIFI_PASSWORD)

# wait until the device is connected to the WiFi network
MAX_ATTEMPTS = 20
attempt_count = 0
while not wifi.isconnected() and attempt_count < MAX_ATTEMPTS:
    attempt_count += 1
    time.sleep(1)

if attempt_count == MAX_ATTEMPTS:
    print('could not connect to the WiFi network')
    sys.exit()


# Cliente MQTT aleatorio
random_num = int.from_bytes(os.urandom(3), 'little')
mqtt_client_id = bytes('client_'+str(random_num), 'utf-8')

# conectar con el BROKER CONECTATE-GT usando TCP no seguro (puerto 1883)
# 
# Para usar una conexión segura (encriptada) con TLS:
#    establece el parámetro de inicializador MQTTClient a "ssl = True"
#    Advertencia: una conexión segura usa aproximadamente 9k bytes de la pila
#          (aproximadamente 1/4 de la pila de micropython en la plataforma ESPXX)


MQTT_URL = b'galiot.galileo.edu' 
MQTT_USER = b'node' #cambiar el node
MQTT_TOPIC = b'temp'

client = MQTTClient(client_id=mqtt_client_id, server=MQTT_URL,               
                    ssl=False)
print('conectado al servidor MQTT')

try:      
    client.connect()
except Exception as e:
    print('no se pudo conectar al servidor MQTT {}{}'.format(type(e).__name__, e))
    sys.exit()


mqtt_feedname = bytes('/{:s}/{:s}'.format(MQTT_USER, MQTT_TOPIC), 'utf-8')  
PUBLISH_PERIOD_IN_SEC = 3

while True:
	
    try:
    
		temp = bme.temperature
		client.publish(mqtt_feedname,bytes(str(temp), 'utf-8'),qos=0)
		print('Publish:  Temperatura = {}C'.format(temp))
		time.sleep(PUBLISH_PERIOD_IN_SEC)
    except KeyboardInterrupt:
        print('Ctrl-C pressed...exiting')
        client.disconnect()
        sys.exit()
