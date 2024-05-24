import struct
import zlib
import array

class SDRData:
    def __init__(self,x,y,minf,maxf, miny, maxy):
        self.coordinates = list(zip(x, y))
        self.x = x
        self.y = y
        self.minf = minf 
        self.maxf = maxf  
        self.miny = miny
        self.maxy = maxy
    def getCoordinates(self):
        return self.coordinates
    def getMax(self):
        return self.maxf
    def getMin(self):
        return self.minf
    def getMinY(self):
        return self.miny
    def getMaxY(self):
        return self.maxy