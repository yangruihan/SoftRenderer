from numpy import *

import common_utils as cu
from Common.math import *


class RendererContext:

    def __init__(self, w, h):
        self._width = w
        self._height = h
        self._pixels = zeros((w + 1, h + 1), dtype=uint32)

    def clear_pixels(self):
        self._pixels.fill(0)

    def set_pixels(self, new_pixels):
        self._pixels = new_pixels

    def set_pixel(self, x, y, color):
        self._pixels[x, y] = color.hex()

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def pixels(self):
        return self._pixels


class Color:
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

    def __str__(self):
        return 'Color(%s, %s, %s, %s)' % (self.r, self.g, self.b, self.a)

    @classmethod
    def red(cls):
        if cls._Red is None:
            cls._Red = Color(255, 0, 0, 255)
        return cls._Red

    @classmethod
    def green(cls):
        if cls._Green is None:
            cls._Green = Color(0, 255, 0, 255)
        return cls._Green

    @classmethod
    def blue(cls):
        if cls._Blue is None:
            cls._Blue = Color(0, 0, 255, 255)
        return cls._Blue

    @classmethod
    def white(cls):
        if cls._White is None:
            cls._White = Color(255, 255, 255, 255)
        return cls._White

    @classmethod
    def black(cls):
        if cls._Black is None:
            cls._Black = Color(0, 0, 0, 255)
        return cls._Black

    def hex(self):
        return cu.rgb2hex(self.r, self.g, self.b, self.a)

    def hex_str(self):
        return cu.rgb2hex_str(self.r, self.g, self.b, self.a)


class Line2d:

    def __init__(self, x1, y1, x2, y2):
        if isinstance(x1, Vector2):
            start = x1
        else:
            start = Vector2(x1, y1)

        if isinstance(y1, Vector2):
            end = y1
        else:
            end = Vector2(x2, y2)

        self.start = start
        self.end = end

    def __str__(self):
        return 'Line2d(start (%s, %s), end (%s, %s))' \
               % (self.start.x, self.start.y, self.end.x, self.end.y)
