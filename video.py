# This code allows to the pico w connect to a local area server with some images
# you should used on server with pbm files because pico memory is small
# python3 -m http.server
import network
import socket
import time
import framebuf

import uasyncio as asyncio
from machine import Pin, I2C, ADC
from sh1106 import SH1106_I2C

import network
import socket
import time
import framebuf

import uasyncio as asyncio
from machine import Pin, I2C, ADC
from sh1106 import SH1106_I2C

# Connect to network

i2c = I2C(1, scl = Pin( 19), sda= Pin(18))

print(i2c.scan())
pin = Pin(1, Pin.OUT)
pin.on()
width = 128
height = 64

oled = SH1106_I2C(width, height, i2c)

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
print("Conecting to router")
wlan.connect('MiFibra-D3C0', 'bjoV2iAp')

while not wlan.isconnected() and wlan.status() >= 0:
    print("Waiting to connect:")
    time.sleep(1)
print("Connected!")
print("ip: "+ wlan.ifconfig()[0])

# Get IP address for google.com

ai = socket.getaddrinfo("192.168.1.17", 8000)
addr = ai[0][-1]

# Create a socket and make a HTTP request

print("renderizando")
oled.rotate(True)
k = 1
while True:
    print("fotograma: "+str(k))
    s = socket.socket()
    s.connect(addr)
    s.send(b"GET /"+str(k)+".pbm HTTP/1.0\r\n\r\n")
    # Print the response
    s.recv(500)
    data = s.recv(1500)
    icon = bytearray(data[10:len(data)-1])
    data = bytearray(s.recv(1000))
    for bit in data:
        icon.append(bit)
    s.close()
    image = framebuf.FrameBuffer(icon, 128, 64, framebuf.MONO_HLSB)
    oled.blit(image, 0, 0)
    oled.show()
    k=k+1