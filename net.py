import network
import socket
import time
import uos
import micropython
import framebuf
import random

import uasyncio as asyncio
from base import Robot
from machine import Pin, I2C, ADC
from sh1106 import SH1106_I2C

led = Pin("LED", Pin.OUT)
led.off()
i2c = I2C(1, scl = Pin( 19), sda= Pin(18))
print(i2c.scan())
oled = SH1106_I2C(128, 64, i2c)
oled.rotate(True)

#ssid = 'mi 9t akevalion'
#password = 'spigit123'
ssid = 'MiFibra-D3C0'
password = 'bjoV2iAp'

wlan = network.WLAN(network.STA_IF)
adc = machine.ADC(4)
perrito = None
robot = Robot()
ip = None

class Dog:
    def __init__(self):
        self.show()
    def right(self):
        r.right()
    def left(self):
        r.left()
    def forward(self):
        r.forward()
    def backward(self):
        r.backward()
    def stop(self):
        r.stop()
    def tick(self):
        pass

class DogInfo(Dog):  
    def show(self):
        oled.fill(0)
        oled.text('TuercasBot',25,0,1)
        oled.text('IP:'+ip, 0,20,1)
        oled.show()
        
class DogFace(Dog):
    def show(self):
        self.reset()
        self.draw_face()
    def reset(self):
        self.is_blinking = False
        self.blinking_step=0
        self.inc = None
        self.left_eye=[22,16,32,22]
        self.right_eye=[74,16,32,22]
        
    def do_blinking(self):
        self.blinking_step += self.inc
        if self.inc > 0 and self.blinking_step > 12:
            self.inc = -4
        if self.blinking_step == 0:
            self.inc = None
            self.is_blinking = False
        
        self.set_eye(self.left_eye,[22,16,32,22])
        self.set_eye(self.right_eye,[74,16,32,22])
        self.draw_face()
    def set_eye(self, eye, base):
        s = self.blinking_step
        eye[1]=base[1]+s
        eye[3]=base[3]-s
        
    def tick(self):
        if self.is_blinking:
            self.do_blinking()
        else:
            n = random.random()
            if n <= 0.05:
                self.is_blinking=True
                self.inc = 4
                self.do_blinking()
        
    def draw_face(self):
        l = self.left_eye
        r = self.right_eye
        oled.fill(0)
        oled.fill_rect(l[0],l[1], l[2],l[3],1)
        oled.fill_rect(r[0],r[1], r[2],r[3],1)
        oled.show()
        
        
    
    
def ok(writer, text):
    writer.write("HTTP/1.0 200 OK\r\n\Content-type: text/{}\r\n\r\n".format(text))

def open_file(writer, name):
    f = open(name)
    writer.write(f.read())
    f.close()
    
def default_site(reader, writer):
    ok(writer, 'html')
    open_file(writer, 'main.html')

def pico_js(reader, writer):
    ok(writer, 'javascript')
    open_file(writer, 'pico.js')
    
def pico_css(reader, writer):
    ok(writer, 'css')
    open_file(writer, 'pico.css')

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
    writer.write("HTTP/1.0 404 NOT_FOUND\r\n\Content-type: text/html\r\n\r\n")
    writer.write(response)

def disk_size_site(reader, writer):
    res = uos.statvfs('/')
    total = res[2] * 4096/1024
    free = res[3] * 4096/1024
    used = total - free
    writer.write("Total size: {}kb\r\nFree space: {}kb\r\nUsed space: {}kb\r\n{}".format(total, free, used, micropython.mem_info()))

def robot_left(reader, writer):
    perrito.left()

def robot_right(reader, writer):
    perrito.right()
    
def robot_forward(reader, writer):
    perrito.forward()
    
def robot_backward(reader, writer):
    perrito.backward()

def robot_stop(reader, writer):
    perrito.stop()
    
    
def robot_info(reader, writer):
    global perrito
    perrito = DogInfo()

def robot_face(reader, writer):
    global perrito
    perrito = DogFace()

sites = {
    '/left': robot_left,
    '/right': robot_right,
    '/showFace': robot_face,
    '/showInfo': robot_info,
    '/forward': robot_forward,
    '/backward': robot_backward,
    '/stop': robot_stop,
    '/pico.js': pico_js,
    '/pico.css': pico_css,
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
        oled.text('Esperando...',0,0,1)
        oled.show()
        print("Esperando conexion...")
        time.sleep(1)
        oled.fill(0)
        oled.show()
        time.sleep(0.5)
        
        
    if wlan.status() != 3:
        oled.fill(0)
        oled.text('Error de conexion',0,0,1)
        oled.show()
        raise RuntimeError("Error de conexion")
    else:
        print('Conectado')
        status = wlan.ifconfig()
        led.on()
        global ip
        global perrito
        ip = status[0]
        print('ip = '+ip)
        perrito = DogInfo()

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
        perrito.tick()
        time.sleep(0.1)
    
try:
    asyncio.run(main())
finally:
    asyncio.new_event_loop()
    