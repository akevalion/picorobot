
import math

class Matrix2D:
    def __init__(self):
        self.sx = self.sy = 1
        self.shx = self.shy = self.x = self.y = 0
        
    def translateBy(self, px, py):
        self.x = self.sx * px + self.shx * py + self.x
        self.y = self.shy * px + self.sy * py + self.y
        
    def rotateByRadians(self, angle):
        cos = math.cos(angle)
        sin = math.sin(angle)
        
        newSx = self.sx * cos + self.shx * sin
        newSy = self.sy * cos - self.shy * sin
        
        self.shx = self.shx * cos - self.sx * sin
        self.shy = self.shy * cos + self.sy * sin
        
        self.sx = newSx
        self.sy = newSy
    def transform(self, px, py):
        return (self.sx*px + self.shx*py + self.x,
                self.shy*px + self.sy*py + self.y)
        
        