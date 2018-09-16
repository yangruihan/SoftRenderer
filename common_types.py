from numpy import *

from common_utils import *

class RendererContext():
    
    def __init__(self, w, h):
        self._width = w
        self._height = h
        self._pixels = zeros((w, h), dtype=uint32)

    def clear_pixels(self):
        self._pixels.fill(0)

    def set_pixels(self, new_pixels):
        self._pixels = new_pixels

    def set_pixel(self, x, y, color):
        self._pixels[x, y] = color.hex()

    def width(self):
        return self._width

    def height(self):
        return self._height

    def pixels(self):
        return self._pixels

class Color():

    _Red = None
    _Green = None
    _Blue = None
    _White = None
    _Black = None

    def __init__(self, r, g, b, a):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    @classmethod
    def Red(cls):
        if cls._Red is None:
            cls._Red = Color(255, 0, 0, 255)
        return cls._Red

    @classmethod
    def Green(cls):
        if cls._Green is None:
            cls._Green = Color(0, 255, 0, 255)
        return cls._Green

    @classmethod
    def Blue(cls):
        if cls._Blue is None:
            cls._Blue = Color(0, 0, 255, 255)
        return cls._Blue

    @classmethod
    def White(cls):
        if cls._White is None:
            cls._White = Color(255, 255, 255, 255)
        return cls._White

    @classmethod
    def Black(cls):
        if cls._Black is None:
            cls._Black = Color(0, 0, 0, 255)
        return cls._Black

    def hex(self):
        return rgb2Hex(self.r, self.g, self.b, self.a)

    def hex_str(self):
        return rgb2HexStr(self.r, self.g, self.b, self.a)
