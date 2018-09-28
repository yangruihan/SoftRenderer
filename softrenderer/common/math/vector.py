# -*- coding: utf-8 -*-


from math import acos, degrees, sqrt
from softrenderer.common.math.matrix import *


class Vector2:
    _Zero = None

    def __init__(self, *args):
        args_len = len(args)
        if args_len == 0:
            (self.x, self.y) = Vector2.zero()
        elif args_len == 1:
            (self.x, self.y) = [args[0]] * 2
        elif args_len == 2:
            (self.x, self.y) = args
        else:
            raise AttributeError

    def __str__(self):
        return 'Vector2(%s, %s)' % (self.x, self.y)

    def __getitem__(self, item):
        if isinstance(item, int):
            if item == 0:
                return self.x
            elif item == 1:
                return self.y
            else:
                raise IndexError
        elif isinstance(item, str):
            if item.lower() == 'x':
                return self.x
            elif item.lower() == 'y':
                return self.y
            else:
                raise AttributeError
        else:
            raise AttributeError

    def __add__(self, other):
        assert isinstance(other, Vector2)

        return Vector2(self.x + other.x,
                       self.y + other.y)

    def __sub__(self, other):
        assert isinstance(other, Vector2)

        return Vector2(self.x - other.x,
                       self.y - other.y)

    def __mul__(self, other):
        try:
            s = float(other)
            return Vector2(self.x * s,
                           self.y * s)
        except Exception:
            raise TypeError

    def __truediv__(self, other):
        try:
            s = float(other)
            return Vector2(self.x / s,
                           self.y / s)
        except Exception:
            raise TypeError

    @staticmethod
    def angle(from_v, to_v):
        if not isinstance(from_v, Vector2) \
                or not isinstance(to_v, Vector2):
            raise TypeError

        # cos(Theta) = (a * b) / ||a|| * ||b||
        c = Vector2.dot(from_v, to_v)
        d = from_v.magnitude() * to_v.magnitude()
        return degrees(acos(c / d))

    @staticmethod
    def dot(v1, v2):
        if not isinstance(v1, Vector2) \
                or not isinstance(v2, Vector2):
            raise TypeError

        return v1.x * v2.x + v1.y * v2.y

    @staticmethod
    def cross(v1, v2):
        if not isinstance(v1, Vector2) \
                or not isinstance(v2, Vector2):
            raise TypeError

        return (v1.x * v2.y) - (v1.y * v2.x)

    def magnitude(self):
        return sqrt(self.x * self.x + self.y * self.y)

    def sqr_magnitude(self):
        return self.x * self.x + self.y * self.y

    def normalized(self):
        tmp = 1 / self.magnitude()
        return Vector2(self.x * tmp,
                       self.y * tmp)

    def normalize(self):
        tmp = 1 / self.magnitude()
        self.x *= tmp
        self.y *= tmp

    @classmethod
    def zero(cls):
        if cls._Zero is None:
            cls._Zero = Vector2(0)
        return cls._Zero


class Vector3:
    _Zero = None

    def __init__(self, *args):
        args_len = len(args)
        if args_len == 0:
            (self.x, self.y, self.z) = Vector3.zero()
        elif args_len == 1:
            (self.x, self.y, self.z) = [args[0]] * 3
        elif args_len == 2:
            if isinstance(args[0], Vector2):
                (self.x, self.y, self.z) = (args[0].x, args[0].y, args[1])
            else:
                (self.x, self.y, self.z) = (args[0], args[1], 0)
        elif args_len == 3:
            (self.x, self.y, self.z) = args
        else:
            raise AttributeError

    def __str__(self):
        return 'Vector3(%s, %s, %s)' % (self.x, self.y, self.z)

    def __getitem__(self, item):
        if isinstance(item, int):
            if item == 0:
                return self.x
            elif item == 1:
                return self.y
            elif item == 2:
                return self.z
            else:
                raise IndexError
        elif isinstance(item, str):
            if item.lower() == 'x':
                return self.x
            elif item.lower() == 'y':
                return self.y
            elif item.lower() == 'z':
                return self.z
            else:
                raise AttributeError
        else:
            raise AttributeError

    def __add__(self, other):
        assert isinstance(other, Vector3)

        return Vector3(self.x + other.x,
                       self.y + other.y,
                       self.z + other.z)

    def __sub__(self, other):
        assert isinstance(other, Vector3)

        return Vector3(self.x - other.x,
                       self.y - other.y,
                       self.z - other.z)

    def __mul__(self, other):
        if isinstance(other, Matrix4x4):
            pass
        try:
            s = float(other)
            return Vector3(self.x * s,
                           self.y * s,
                           self.z * s)
        except Exception:
            raise TypeError

    def __truediv__(self, other):
        try:
            s = float(other)
            return Vector3(self.x / s,
                           self.y / s,
                           self.z / s)
        except Exception:
            raise TypeError

    @staticmethod
    def angle(from_v, to_v):
        if not isinstance(from_v, Vector3) \
                or not isinstance(to_v, Vector3):
            raise TypeError

        # cos(Theta) = (a * b) / ||a|| * ||b||
        c = Vector3.dot(from_v, to_v)
        d = from_v.magnitude() * to_v.magnitude()
        return degrees(acos(c / d))

    @staticmethod
    def dot(v1, v2):
        if not isinstance(v1, Vector3) \
                or not isinstance(v2, Vector3):
            raise TypeError

        return v1.x * v2.x + v1.y * v2.y + v1.z * v2.z

    @staticmethod
    def cross(v1, v2):
        if not isinstance(v1, Vector3) \
                or not isinstance(v2, Vector3):
            raise TypeError

        return Vector3((v1.y * v2.z) - (v1.z * v2.y),
                       (v1.z * v2.x) - (v1.x * v2.z),
                       (v1.x * v2.y) - (v1.y * v2.x))

    @staticmethod
    def lerp(v1, v2, t):
        if not isinstance(v1, Vector3) \
                or not isinstance(v2, Vector3):
            raise TypeError

        return v1 + (v2 - v1) * t

    def magnitude(self):
        return sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def sqr_magnitude(self):
        return self.x * self.x + self.y * self.y + self.z * self.z

    def normalized(self):
        tmp = 1 / self.magnitude()
        return Vector3(self.x * tmp,
                       self.y * tmp,
                       self.z * tmp)

    def normalize(self):
        tmp = 1 / self.magnitude()
        self.x *= tmp
        self.y *= tmp
        self.z *= tmp

    @classmethod
    def zero(cls):
        if cls._Zero is None:
            cls._Zero = Vector3(0)
        return cls._Zero


class Vector4:
    _Zero = None

    def __init__(self, *args):
        args_len = len(args)
        if args_len == 0:
            (self.x, self.y, self.z, self.w) = Vector4.zero()
        elif args_len == 1:
            (self.x, self.y, self.z, self.w) = [args[0]] * 4
        elif args_len == 2:
            if isinstance(args[0], Vector3):
                (self.x, self.y, self.z, self.w) = (args[0].x, args[0].y, args[0].z, args[1])
            else:
                (self.x, self.y, self.z, self.w) = (args[0], args[1], 0, 0)
        elif args_len == 3:
            (self.x, self.y, self.z, self.w) = (args[0], args[1], args[2], 0)
        elif args_len == 4:
            (self.x, self.y, self.z, self.w) = args
        else:
            raise AttributeError

    def __str__(self):
        return 'Vector4(%s, %s, %s, %s)' % (self.x, self.y, self.z, self.w)

    def __getitem__(self, item):
        if isinstance(item, int):
            if item == 0:
                return self.x
            elif item == 1:
                return self.y
            elif item == 2:
                return self.z
            elif item == 3:
                return self.w
            else:
                raise IndexError
        elif isinstance(item, str):
            if item.lower() == 'x':
                return self.x
            elif item.lower() == 'y':
                return self.y
            elif item.lower() == 'z':
                return self.z
            elif item.lower() == 'w':
                return self.w
            else:
                raise AttributeError
        else:
            raise AttributeError

    def __add__(self, other):
        assert isinstance(other, Vector4)

        return Vector4(self.x + other.x,
                       self.y + other.y,
                       self.z + other.z,
                       self.w + other.w)

    def __sub__(self, other):
        assert isinstance(other, Vector4)

        return Vector3(self.x - other.x,
                       self.y - other.y,
                       self.z - other.z,
                       self.w - other.w)

    def __mul__(self, other):
        try:
            s = float(other)
            return Vector4(self.x * s,
                           self.y * s,
                           self.z * s,
                           self.w * s)
        except Exception:
            raise TypeError

    def __truediv__(self, other):
        try:
            s = float(other)
            return Vector4(self.x / s,
                           self.y / s,
                           self.z / s,
                           self.w / s)
        except Exception:
            raise TypeError

    @staticmethod
    def dot(v1, v2):
        if not isinstance(v1, Vector4) \
                or not isinstance(v2, Vector4):
            raise TypeError

        return v1.x * v2.x + v1.y * v2.y + v1.z * v2.z + v1.w * v2.w

    def magnitude(self):
        return sqrt(self.x * self.x + self.y * self.y + self.z * self.z + self.w * self.w)

    def sqr_magnitude(self):
        return self.x * self.x + self.y * self.y + self.z * self.z + self.w * self.w

    def normalized(self):
        tmp = 1 / self.magnitude()
        return Vector3(self.x * tmp,
                       self.y * tmp,
                       self.z * tmp,
                       self.w * tmp)

    def normalize(self):
        tmp = 1 / self.magnitude()
        self.x *= tmp
        self.y *= tmp
        self.z *= tmp
        self.w *= tmp

    @classmethod
    def zero(cls):
        if cls._Zero is None:
            cls._Zero = Vector4(0)
        return cls._Zero
