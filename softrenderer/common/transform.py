# -*- coding:utf-8 -*-


from math import sin, cos, radians

from softrenderer.common.math.vector import Vector3
from softrenderer.common.math.quaternion import Quaternion
from softrenderer.common.math.matrix import Matrix4x4


class Transform:

    def __init__(self, *args):
        self._is_dirty = True

        args_len = len(args)
        if args_len == 0:
            self._position = Vector3.zero()
            self._rotation = Quaternion.identity()
            self._scale = Vector3.one()
        elif args_len == 1:
            if isinstance(args[0], Transform):
                self._position = Vector3(args[0].position)
                self._rotation = Quaternion(args[0].rotation_quaternion)
                self._scale = Vector3(args[0].scale)
            else:
                raise AttributeError
        elif args_len == 3 \
                and isinstance(args[0], Vector3) \
                and isinstance(args[1], Quaternion) \
                and isinstance(args[2], Vector3):
            self._position = args[0]
            self._rotation = args[1]
            self._scale = args[2]
        else:
            raise AttributeError

        self._local_to_world_matrix = Matrix4x4()

    def __str__(self):
        euler_angle = self._rotation.euler_angle()
        return 'Transform(Pos(%.5f, %.5f, %.5f), Rot(%.5f, %.5f, %.5f), Scale(%.5f, %.5f, %.5f))' % (
            self._position.x, self._position.y, self._position.z,
            euler_angle.x, euler_angle.y, euler_angle.z,
            self._scale.x, self._scale.y, self._scale.z
        )

    def get_local_to_world_matrix(self):
        if self._is_dirty:
            trans_matrix = Matrix4x4(1, 0, 0, self._position.x,
                                     0, 1, 0, self._position.y,
                                     0, 0, 1, self._position.z,
                                     0, 0, 0, 1)

            scale_matrix = Matrix4x4(self._scale.x, 0, 0, 0,
                                     0, self._scale.y, 0, 0,
                                     0, 0, self._scale.z, 0,
                                     0, 0, 0, 1)

            self._local_to_world_matrix = trans_matrix * self._rotation.get_rot_matrix() * scale_matrix
            self._is_dirty = False
        return self._local_to_world_matrix

    def translate(self, vector):
        if isinstance(vector, Vector3):
            self._position += vector
            self._is_dirty = True
        else:
            raise TypeError

    def rotate(self, x, y, z):
        self._rotation *= Quaternion.from_euler_angle(x, y, z)
        self._is_dirty = True

    def rotate_axis(self, axis, angle):
        sin_v = sin(radians(angle) / 2)
        cos_v = cos(radians(angle) / 2)
        rotate = Quaternion(axis.x * sin_v, axis.y * sin_v, axis.z * sin_v, cos_v)
        self._rotation *= rotate
        self._is_dirty = True

    def get_forward(self):
        return self._rotation * Vector3.forward()

    def get_right(self):
        return self._rotation * Vector3.right()

    def get_up(self):
        return self._rotation * Vector3.up()

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position):
        self._position = position

    @property
    def rotation(self):
        return self._rotation.euler_angle()

    @rotation.setter
    def rotation(self, euler_angle):
        self._rotation = Quaternion.from_euler_angle(euler_angle)

    @property
    def rotation_quaternion(self):
        return self._rotation

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, scale):
        self._scale = scale

    @property
    def is_dirty(self):
        return self._is_dirty
