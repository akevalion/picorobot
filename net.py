import network
import socket
import time

from machine import Pin
import uasyncio as asyncio

from machine import ADC

led = Pin("LED", Pin.OUT)
led.on()

#ssid = 'Freebox-46C865'
#password = 'eruatis!5-cogitur@-stimula4-calleantur.7'
ssid = 'mi 9t akevalion'
password = 'spigit123'

html ="""<!DOCTYPE html>
<html>
    <head> <title> Ok </title> </head>
    <body> <h1> Ok <h1>
        <p></p>
    <body>
</html>
"""

wlan = network.WLAN(network.STA_IF)
adc = machine.ADC(4)

def ok(writer):
    writer.write("HTTP/1.0 200 OK\r\n\Content-type: text/html\r\n\r\n")
    
def defaultSite(reader, writer):
    ok(writer)
    writer.write(html)
    

def tempSite(reader, writer):
    ADC_voltage = adc.read_u16() * (3.3 / (65536))
    temperature_celcius = 27 - (ADC_voltage - 0.706)/0.001721
    writer.write(("Temperature: {}°C".format(temperature_celcius)).encode("utf8"))
    
def invalidSite(reader, writer):
    response ="""<!DOCTYPE html>
<html>
    <head><title>Error</title></head>
    <body>
        <h1>Pagina no existe<h1>
    <body>
</html>
"""
    writer.write("HTTP/1.0 404 OK\r\n\Content-type: text/html\r\n\r\n")
    writer.write(response)


    
sites = {
    '/' : defaultSite,
    '/temp': tempSite}
def connectToNetwork():
    wlan.active(True)
    wlan.config(pm=0xa11140)
    wlan.connect(ssid, password)
    
    maxWait = 10
    while maxWait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        maxWait -= 1
        print("esperando conexion...")
        time.sleep(1)
        
    if wlan.status() != 3:
        raise RuntimeError("error de conexion")
    else:
        print('connected')
        status = wlan.ifconfig()
        print('ip = '+status[0])

async def handleRequest(reader, writer):
    requestLine = (await reader.readline()).decode('utf8')
    print("Request: ", requestLine)
    
    while await reader.readline() != b"\r\n":
        pass
    request = str(requestLine).split()
    if request[1] in sites:
        function = sites[request[1]]
        print(function)
        function(reader, writer)
    else:
        invalidSite(reader, writer)
    await writer.drain()
    await writer.wait_closed()
    
async def main():
    print("Conectando a la red...")
    connectToNetwork()
    print("iniciando servidor...")
    asyncio.create_task(asyncio.start_server(handleRequest, "0.0.0.0", 80))
    print("Esperando usuarios\n")
    while True:
        await asyncio.sleep(0.25)
        time.sleep(0.5)
    
try:
    asyncio.run(main())
finally:
    asyncio.new_event_loop()
    