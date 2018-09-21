from math import sin, cos, acos, degrees, sqrt


class Vector2:
    _Zero = None

    def __init__(self, *args):
        args_len = len(args)
        if args_len == 0:
            (self.x, self.y) = Vector2.zero()
        elif args_len == 1:
            (self.x, self.y) = (args[0], args[0])
        elif args_len == 2:
            (self.x, self.y) = (args[0], args[1])
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
            (self.x, self.y, self.z) = (args[0], args[0], args[0])
        elif args_len == 2:
            (self.x, self.y, self.z) = (args[0], args[1], 0)
        elif args_len == 3:
            (self.x, self.y, self.z) = (args[0], args[1], args[2])
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


class Quaternion:

    def __init__(self, *args):
        if len(args) == 4:
            mag = sum([x * x for x in args])
            self._x = args[0] / mag
            self._y = args[1] / mag
            self._z = args[2] / mag
            self._w = args[3] / mag
        elif len(args) == 3:
            self.set_euler_angle(*args)
        else:
            raise AttributeError

    @staticmethod
    def dot(q1, q2):
        if not isinstance(q1, Quaternion) \
                or not isinstance(q2, Quaternion):
            raise TypeError

        return q1.x * q2.x + q1.y * q2.y + q1.z * q2.z + q1.w * q2.w

    @staticmethod
    def euler_angle(yaw, pitch, roll):
        return Quaternion(yaw, pitch, roll)

    @staticmethod
    def slerp(q1, q2, t):
        if not isinstance(q1, Quaternion) \
                or not isinstance(q2, Quaternion):
            raise TypeError

        cos_theta = Quaternion.dot(q1, q2)

        if cos_theta < 0:
            cos_theta = -cos_theta
            sign = -1
        else:
            sign = 1

        if cos_theta >= 1:
            c2 = t
            c1 = 1 - t
        else:
            theta = acos(cos_theta)
            sin_theta = sin(theta)
            inv_sin_theta = 1 / sin_theta
            t_theta = t * theta
            c2 = sin(t_theta) * inv_sin_theta
            c1 = sin(theta - t_theta) * inv_sin_theta

        c2 *= sign
        return Quaternion(q1.x * c1 + q2.x * c2,
                          q1.y * c1 + q2.y * c2,
                          q1.z * c1 + q2.z * c2,
                          q1.w * c1 + q2.w * c2)

    @staticmethod
    def lerp(q1, q2, t):
        if not isinstance(q1, Quaternion) \
                or not isinstance(q2, Quaternion):
            raise TypeError

        c1 = 1 - t
        c2 = t

        return Quaternion(q1.x * c1 + q2.x * c2,
                          q1.y * c1 + q2.y * c2,
                          q1.z * c1 + q2.z * c2,
                          q1.w * c1 + q2.w * c2)

    @staticmethod
    def angle(q1, q2):
        if not isinstance(q1, Quaternion) \
                or not isinstance(q2, Quaternion):
            raise TypeError

        cos_theta = Quaternion.dot(q1, q2)
        cos_theta = -cos_theta if cos_theta < 0 else cos_theta
        theta = acos(cos_theta)
        return 2 * degrees(theta)

    def set_euler_angle(self, yaw, pitch, roll):
        sin_yaw = sin(yaw / 2)
        cos_yaw = cos(yaw / 2)

        sin_pitch = sin(pitch / 2)
        cos_pitch = cos(pitch / 2)

        sin_roll = sin(roll / 2)
        cos_roll = cos(roll / 2)

        _x = cos_roll * cos_pitch * sin_yaw - sin_roll * sin_pitch * cos_yaw
        _y = cos_roll * sin_pitch * cos_yaw + sin_roll * cos_pitch * sin_yaw
        _z = sin_roll * cos_pitch * cos_yaw - cos_roll * sin_pitch * sin_yaw
        _w = cos_roll * cos_pitch * cos_yaw + sin_roll * sin_pitch * sin_yaw

        mag = sum([_x * _x, _y * _y, _z * _z, _w * _w])
        self._x = _x / mag
        self._y = _y / mag
        self._z = _z / mag
        self._w = _w / mag

    def set(self, *args):
        if len(args) == 4:
            mag = sum([x * x for x in args])
            self._x = args[0] / mag
            self._y = args[1] / mag
            self._z = args[2] / mag
            self._w = args[3] / mag
        elif len(args) == 3:
            self.set_euler_angle(*args)
        else:
            raise AttributeError

    def __add__(self, other):
        if isinstance(other, Quaternion):
            self._x += other._x
            self._y += other._y
            self._z += other._z
            self._w += other._w
        else:
            raise TypeError

    def __sub__(self, other):
        if isinstance(other, Quaternion):
            self._x -= other._x
            self._y -= other._y
            self._z -= other._z
            self._w -= other._w
        else:
            raise TypeError

    def __mul__(self, other):
        if isinstance(other, Quaternion):
            pass
        else:
            try:
                s = float(other)
                self._x *= s
                self._y *= s
                self._z *= s
                self._w *= s
            except Exception:
                raise TypeError

    def conjugate(self):
        return Quaternion(-self.x, -self.y, -self.z, self.w)

    def inverse(self):
        return Quaternion(-self.x, -self.y, -self.z, self.w)

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def z(self):
        return self._z

    @property
    def w(self):
        return self._w
