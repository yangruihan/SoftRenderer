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
            self.position = Vector3.zero()
            self.rotation = Quaternion.identity()
            self.scale = Vector3.one()
        elif args_len == 1:
            if isinstance(args[0], Transform):
                self.position = Vector3(args[0].position)
                self.rotation = Quaternion(args[0].rotation)
                self.scale = Vector3(args[0].scale)
            else:
                raise AttributeError
        elif args_len == 3 \
                and isinstance(args[0], Vector3) \
                and isinstance(args[1], Quaternion) \
                and isinstance(args[2], Vector3):
            self.position = args[0]
            self.rotation = args[1]
            self.scale = args[2]
        else:
            raise AttributeError

        self._local_to_world_matrix = Matrix4x4()

    def __str__(self):
        euler_angle = self.rotation.euler_angle()
        return 'Transform(Pos(%.5f, %.5f, %.5f), Rot(%.5f, %.5f, %.5f), Scale(%.5f, %.5f, %.5f))' % (
            self.position.x, self.position.y, self.position.z,
            euler_angle.x, euler_angle.y, euler_angle.z,
            self.scale.x, self.scale.y, self.scale.z
        )

    def get_local_to_world_matrix(self):
        if self._is_dirty:
            trans_matrix = Matrix4x4(1, 0, 0, self.position.x,
                                     0, 1, 0, self.position.y,
                                     0, 0, 1, self.position.z,
                                     0, 0, 0, 1)

            scale_matrix = Matrix4x4(self.scale.x, 0, 0, 0,
                                     0, self.scale.y, 0, 0,
                                     0, 0, self.scale.z, 0,
                                     0, 0, 0, 1)

            self._local_to_world_matrix = trans_matrix * self.rotation.get_rot_matrix() * scale_matrix
            self._is_dirty = False
        return self._local_to_world_matrix

    def translate(self, vector):
        if isinstance(vector, Vector3):
            self.position += vector
            self._is_dirty = True
        else:
            raise TypeError

    def rotate(self, x, y, z):
        self.rotation *= Quaternion.from_euler_angle(x, y, z)
        self._is_dirty = True

    def rotate_axis(self, axis, angle):
        sin_v = sin(radians(angle) / 2)
        cos_v = cos(radians(angle) / 2)
        rotate = Quaternion(axis.x * sin_v, axis.y * sin_v, axis.z * sin_v, cos_v)
        self.rotation *= rotate
        self._is_dirty = True

    def get_forward(self):
        return self.rotation * Vector3.forward()

    def get_right(self):
        return self.rotation * Vector3.right()

    def get_up(self):
        return self.rotation * Vector3.up()

    @property
    def is_dirty(self):
        return self._is_dirty
