from machine import Pin
import network, machine, neopixel, time

numero_leds = 10
np = neopixel.NeoPixel(machine.Pin(15), numero_leds)


    
ssid = 'RumboalaExcelenciaUG'
password = ''

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)
while station.isconnected() == False:
    pass
print('Connection successful')
print(station.ifconfig())

rele1 = Pin(12, Pin.OUT)
#ROJO
def colorROJO():
    for led in range(0,numero_leds,1):
        np[led]=(0,255,0)
        np.write()
        time.sleep_ms(100)
    print("ROJO")

def colorAPAGO():
    for led in range(0,numero_leds,1):
        np[led]=(0,0,0)
        np.write()
        time.sleep_ms(100)
    print("ROJO")    
##################

def web_page():
    html ="""
    <html>
        <head>
        <title>Control de reles</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="icon" href="data:,">
        <style>
            html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
            h1{color: #0F3376; padding: 2vh;}p{font-size: 1.5rem;}
            .button{display: inline-block; background-color: #31ad00; border: none;
            border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
            .button2{background-color: #f30c0c;}
            .button3{background-color: #f30c0c;}
            .button4{background-color: #f30c0c;}
        </style>
        </head>
        <body>
        <h1>Control de reles</h1>
        <p><a href="/?rele1=on"><button class="button">RELE1 ON</button></a></p>
        <p><a href="/?rele1=off"><button class="button button2">RELE2 OFF</button></a></p>
        <p><a href="/?color=rojo"><button class="button button3">LuzRoja</button></a></p>
        <p><a href="/?color=null"><button class="button button4">APAGAR</button></a></p>
        </body>
    </html>
    """
    return html
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:
    conn, addr = s.accept()
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    request = str(request)
    print('Content = %s' % request)

    rele1_on = request.find('/?rele1=on')
    rele1_off = request.find('/?rele1=off')
    color_rojo = request.find('/?color=rojo')
    apagar = request.find('/?color=null')
    

    if rele1_on == 6:
        print('on')
        rele1.value(1)    
    if rele1_off == 6:
        print('off')
        rele1.value(0)
    if rele1_off == 6:
        print('rojo')
        colorROJO()
    if rele1_off == 6:
        print('apagado')
        colorAPAGO()       
        
    response = web_page()
    conn.send(response)
    conn.close()