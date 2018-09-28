# -*- coding:utf-8 -*-


from math import sin, cos, atan2, asin

from softrenderer.common.math.common import clamp


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
    def from_euler_angle(yaw, pitch, roll):
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
            w1 = self.w
            w2 = other.w
            v1 = Vector3(self.x, self.y, self.z)
            v2 = Vector3(self.x, self.y, self.z)
            w3 = w1 * w2 - Vector3.dot(v1, v2)
            v3 = Vector3.cross(v1, v2) + v2 * w1 + v1 * w2
            return Quaternion(v3.x, v3.y, v3.z, w3)
        elif isinstance(other, Vector3):
            u = Vector3(self.x, self.y, self.z)
            s = self.w
            return Vector3.dot(u, other) * u * 2 \
                   + other * (s * s - Vector3.dot(u, u)) \
                   + Vector3.cross(u, other) * 2 * s
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

    def euler_angle(self):
        yaw = atan2(2 * (self.w * self.x + self.z * self.y), 1 - 2 * (self.x * self.x + self.y * self.y))
        pitch = asin(clamp(2 * (self.w * self.y - self.x * self.z), -1.0, 1.0))
        roll = atan2(2 * (self.w * self.z + self.x * self.y), 1 - 2 * (self.z * self.z + self.y * self.y))
        return Vector3(degrees(yaw), degrees(pitch), degrees(roll))

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
