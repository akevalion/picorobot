from machine import Pin
from time import sleep
luz = Pin('LED', Pin.OUT)
val = 1
while True:
    luz.on()
    sleep(val)
    luz.off()
    sleep(val)
    val = val * 0.9
    if val < 0.005:
        val = 1
print("done")
