import network
import socket
import time

from machine import Pin
import uasyncio as asyncio

from machine import ADC
import uos

led = Pin("LED", Pin.OUT)
led.off()

#ssid = 'Freebox-46C865'
#password = 'eruatis!5-cogitur@-stimula4-calleantur.7'
#ssid = 'mi 9t akevalion'
#password = 'spigit123'
ssid = 'MiFibra-D3C0'
password = 'bjoV2iAp'

html ="""
<!DOCTYPE html>
<html>
    <head>
        <title>Wally Robot Control</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body{
                background: url(./bg.png) repeat fixed;
            }
            input{
                border-radius: 15px;
                height: 120px;
                width: 120px;
            }
            .grabar{
                float: left;
            }
            .pararGrabacion{
                float: right;
            }
        </style>
    </head>
    <body>
    <center><b>
        <form action="./forward">
        <input type="submit" value="Adelante"/>
        </form>
    <table><tr>
        <td><form action="./left">
        <input type="submit" value="Izquierda"/>
        </form></td>
        <td><form action="./stop">
        <input type="submit" value="Parar"/>
        </form></td>
        <td><form action="./right">
        <input type="submit" value="Derecha"/>
        </form></td>
    </tr></table>
    <form action="./back">
    <input type="submit" value="Back"/>
    </form>
    </center>

    <form action="./grabar">
    <input type="submit" value="Grabar" class="grabar"/>
    </form>

    <form action="./pararGrabacion">
    <input type="submit" value="Parar Grabacion" class="pararGrabacion"/>
    </form>
    </body>
</html>
"""

wlan = network.WLAN(network.STA_IF)
adc = machine.ADC(4)

def ok(writer):
    writer.write("HTTP/1.0 200 OK\r\n\Content-type: text/html\r\n\r\n")
    
def default_site(reader, writer):
    ok(writer)
    writer.write(html)
    

def temperature_site(reader, writer):
    ADC_voltage = adc.read_u16() * (3.3 / (65536))
    temperature_celcius = 27 - (ADC_voltage - 0.706)/0.001721
    writer.write(("Temperatura: {:.3} celcius".format(temperature_celcius)).encode("utf8"))
    
def invalid_site(reader, writer):
    response ="""
<!DOCTYPE html>
<html>
    <head><title>Error</title></head>
    <body>
        <h1>Pagina no existe<h1>
    <body>
</html>
"""
    writer.write("HTTP/1.0 404 OK\r\n\Content-type: text/html\r\n\r\n")
    writer.write(response)

def disk_size_site(reader, writer):
    res = uos.statvfs('/')
    total = res[2] * 4096/1024
    free = res[3] * 4096/1024
    used = total - free
    writer.write("Total size: {}kb\r\nFree space: {}kb\r\nUsed space: {}kb".format(total, free, used))
    

sites = {
    '/disksize': disk_size_site,
    '/': default_site,
    '/temp': temperature_site}

def connect_to_network():
    wlan.active(True)
    wlan.config(pm=0xa11140)
    wlan.connect(ssid, password)
    
    maxWait = 10
    while maxWait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        maxWait -= 1
        print("Esperando conexion...")
        time.sleep(1)
        
    if wlan.status() != 3:
        raise RuntimeError("Error de conexion")
    else:
        print('Conectado')
        status = wlan.ifconfig()
        led.on()
        print('ip = '+status[0])

async def handle_request(reader, writer):
    requestLine = (await reader.readline()).decode('utf8')
    print("Request: ", requestLine.strip())
    
    while await reader.readline() != b"\r\n":
        pass
    request = str(requestLine).split()
    if request[1] in sites:
        function = sites[request[1]]
        print(function.__name__ + "\n")
        function(reader, writer)
    else:
        invalid_site(reader, writer)
    await writer.drain()
    await writer.wait_closed()
    
async def main():
    print("Conectando a la red...")
    connect_to_network()
    print("Iniciando servidor...")
    asyncio.create_task(asyncio.start_server(handle_request, "0.0.0.0", 80))
    print("Esperando usuarios\n")
    while True:
        await asyncio.sleep(0.25)
        time.sleep(0.5)
    
try:
    asyncio.run(main())
finally:
    asyncio.new_event_loop()
    
