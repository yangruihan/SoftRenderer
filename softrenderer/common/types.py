# -*- coding: utf-8 -*-


from softrenderer.common import utils as cu


class Color:
    _Red = None
    _Green = None
    _Blue = None
    _White = None
    _Black = None

    def __init__(self, r, g, b, a):
        self._r = r
        self._g = g
        self._b = b
        self._a = a

    def __str__(self):
        return 'Color(%.5f, %.5f, %.5f, %.5f)' % (self.r, self.g, self.b, self.a)

    @property
    def r(self):
        return self._r

    @r.setter
    def r(self, r):
        self._r = r

    @property
    def g(self):
        return self._g

    @g.setter
    def g(self, g):
        self._g = g

    @property
    def b(self):
        return self._b

    @b.setter
    def b(self, b):
        self._b = b

    @property
    def a(self):
        return self._a

    @a.setter
    def a(self, a):
        self._a = a

    @staticmethod
    def _check_valid(value):
        if value < 0  or value > 1:
            return False
        return True

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

    def is_valid(self):
        return self.r >= 0 and self.g >= 0 and self.b >= 0 and self.a >= 0

    @classmethod
    def red(cls):
        if cls._Red is None:
            cls._Red = Color(1.0, 0.0, 0.0, 1.0)
        return cls._Red

    @classmethod
    def green(cls):
        if cls._Green is None:
            cls._Green = Color(0, 1.0, 0, 1.0)
        return cls._Green

    @classmethod
    def blue(cls):
        if cls._Blue is None:
            cls._Blue = Color(0, 0, 1.0, 1.0)
        return cls._Blue

    @classmethod
    def white(cls):
        if cls._White is None:
            cls._White = Color(1.0, 1.0, 1.0, 1.0)
        return cls._White

    @classmethod
    def black(cls):
        if cls._Black is None:
            cls._Black = Color(0, 0, 0, 1.0)
        return cls._Black

    def hex(self):
        return cu.rgb2hex(int(self.r * 255),
                          int(self.g * 255),
                          int(self.b * 255),
                          int(self.a * 255))

    def hex_str(self):
        return cu.rgb2hex_str(int(self.r * 255),
                              int(self.g * 255),
                              int(self.b * 255),
                              int(self.a * 255))
