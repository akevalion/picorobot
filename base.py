from machine import Pin

class Robot:
    def __init__(self):
        self.pleftF = 21
        self.pleftB = 22
        self.prightF = 26
        self.prightB = 27
        self.leftF= Pin(self.pleftF, Pin.OUT)
        self.leftB= Pin(self.pleftB, Pin.OUT)
        self.rightF= Pin(self.prightF, Pin.OUT)
        self.rightB= Pin(self.prightB, Pin.OUT)
        self.stop()

    def leftFOn(self):
        self.pleftF.on()

    def leftFOff(self):
        self.leftF.off()

    def leftBOn(self):
        self.leftB.on()

    def leftBOff(self):
        self.leftB.off()

    def rightFOn(self):
        self.rightF.on()
    
    def rightFOff(self):
        self.rightF.off()
    
    def rightBOn(self):
        self.rightB.on()

    def rightBOff(self):
        self.rightB.off()
    
        
    def forward(self):
        self.rightBOff()
        self.leftBOff()
        self.rightFOn()
        self.leftFOn()
        
    def backward(self):
        self.rightFOff()
        self.leftFOff()
        self.rightBOn()
        self.leftBOn()
        
    def left(self):
        self.rightBOff()
        self.leftFOff()
        self.rightFOn()
        self.leftBOn()
        
    def right(self):
        self.leftBOff()
        self.rightFOff()
        self.leftFOn()
        self.rightBOn()
        
    def stop(self):
        self.rightFOff()
        self.rightBOff()
        self.leftFOff()
        self.leftBOff()
