# -*- coding: utf-8 -*-


from numpy import *

from softrenderer.common import utils as cu
from softrenderer.common.math.vector import Vector2


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
        return 'Color(%.5f, %.5f, %.5f, %.5f)' % (self.r, self.g, self.b, self.a)

    def __add__(self, other):
        if not isinstance(other, Color):
            raise TypeError

        return Color(self.r + other.r,
                     self.g + other.g,
                     self.b + other.b,
                     self.a + other.a)

    def __sub__(self, other):
        if not isinstance(other, Color):
            raise TypeError

        return Color(self.r - other.r,
                     self.g - other.g,
                     self.b - other.b,
                     self.a - other.a)

    def __mul__(self, other):
        try:
            s = float(other)
            return Color(self.r * s,
                         self.g * s,
                         self.b * s,
                         self.a * s)
        except Exception:
            raise TypeError

    def __truediv__(self, other):
        try:
            s = float(other)
            return Color(self.r / s,
                         self.g / s,
                         self.b / s,
                         self.a / s)
        except Exception:
            raise TypeError

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

    def __init__(self, *args):
        args_len = len(args)
        if args_len == 2:
            start = args[0]
            end = args[1]
        elif args_len == 4:
            start = Vector2(args[0], args[1])
            end = Vector2(args[2], args[3])
        else:
            raise AttributeError

        self.start = start
        self.end = end

    def __str__(self):
        return 'Line2d(start (%.5f, %.5f), end (%.5f, %.5f))' \
               % (self.start.x, self.start.y, self.end.x, self.end.y)
