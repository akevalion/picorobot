import network
import socket
import time

from machine import Pin
import uasyncio as asyncio

led = Pin("LED", Pin.OUT)
led.on()

#ssid = 'Freebox-46C865'
#password = 'eruatis!5-cogitur@-stimula4-calleantur.7'
ssid = 'mi 9t akevalion'
password = 'spigit123'

html ="""<!DOCTYPE html>
<html>
    <head> <title> Pi mierda </title> </head>
    <body> <h1> Pico carajo <h1>
        <p>%s</p>
    <body>
</html>
"""

wlan = network.WLAN(network.STA_IF)

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
    print("Cliente connectado")
    requestLine = await reader.readline()
    print("Request: ", requestLine)
    
    while await reader.readline() != b"\r\n":
        pass
    
    request = str(requestLine)
    
    status = ""
    if request.find("prender") != -1:
        print("led on")
        led.on()
        status = "luz prendida"
    if request.find("apagar") != -1:
        print("led off")
        led.off()
        status = "luz apagada"
    response = html % status
    writer.write("HTTP/1.0 200 OK\r\n\Content-type: text/html\r\n\r\n")
    writer.write(response)
    await writer.drain()
    await writer.wait_closed()
    print("Client disconnected")
    
async def main():
    print("Conectando a la red...")
    connectToNetwork()
    print("iniciando servidor...")
    asyncio.create_task(asyncio.start_server(handleRequest, "0.0.0.0", 80))
    while True:
        print("esperando")
        await asyncio.sleep(0.25)
        time.sleep(0.5)
    
try:
    asyncio.run(main())
finally:
    asyncio.new_event_loop()
    
