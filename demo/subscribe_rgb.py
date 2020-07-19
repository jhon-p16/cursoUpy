from machine import Pin
import machine, neopixel
from urandom import getrandbits
import network
import time
from umqtt.robust import MQTTClient
import os
import sys

num_leds=50
pin_salida=17
np = neopixel.NeoPixel(machine.Pin(pin_salida), num_leds)

    
def neopixel(msg):
    cadena = msg.decode('utf-8').lstrip('#') 
    
    rgb = (tuple(int(cadena[i:i+2], 16) for i in (2, 0, 4)))
    print(rgb)
    for led in range(num_leds):
        np[led]=rgb
    np.write()


#RECIBIR EL DATO DEL SERVIDOR PARA ENCENDER LOS 
#########################
# la siguiente función es la devolución de llamada que es
# llamada cuando se reciben los datos suscritos
def cb(topic, msg):
    print((msg))    
    
    neopixel(msg)

#CONEXION A LA RED WIFI

# Informacion de la red WiFi

WIFI_SSID = ''
WIFI_PASSWORD = ''


# apagar el punto de acceso WiFi
ap_if = network.WLAN(network.AP_IF)
ap_if.active(False)

# conecta el dispositivo a la red WiFi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(WIFI_SSID, WIFI_PASSWORD)

# esperar hasta que el dispositivo esté conectado a la red WiFi
MAX_ATTEMPTS = 20
attempt_count = 0

while not wifi.isconnected() and attempt_count < MAX_ATTEMPTS:
    attempt_count += 1
    time.sleep(1)
    print('conectando a la red WiFi...')
    
if attempt_count == MAX_ATTEMPTS:
    print('no se pudo conectar a la red WiFi')
    sys.exit()
    
print('conectado a la red WiFi')
print ("Configuracion de red: ", wifi.ifconfig())

#CONEXION AL SERVIDOR CONECTATEGT
#########################       

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
MQTT_TOPIC = b'rgb'

client = MQTTClient(client_id=mqtt_client_id, server=MQTT_URL,               
                    ssl=False)
print('conectado al servidor MQTT')

try:      
    client.connect()
except Exception as e:
    print('no se pudo conectar al servidor MQTT {}{}'.format(type(e).__name__, e))
    sys.exit()


mqtt_feedname = bytes('/{:s}/{:s}'.format(MQTT_USER, MQTT_TOPIC), 'utf-8')  
client.set_callback(cb)                    
client.subscribe(mqtt_feedname)  


# espere hasta que se hayan publicado los datos en la fuente IO de Adafruit
while True:
    try:
        client.wait_msg()
        
        
    except KeyboardInterrupt:
        print('Ctrl-C pressed...exiting')
        client.disconnect()
        sys.exit()
