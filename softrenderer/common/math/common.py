# -*- coding:utf-8 -*-


from math import atan2, asin, degrees, radians, cos, sin
from softrenderer.common.math import matrix as mt
from softrenderer.common.math import vector as vt


def clamp(value, left, right):
    return max(left, min(value, right))


def euler2matrix(euler):
    if not isinstance(euler, vt.Vector3):
        raise TypeError

    h, p, r = radians(euler.x), radians(euler.y), radians(euler.z)

    ret = mt.Matrix3x3()

    ret.set(0, 0, cos(r) * cos(h) - sin(r) * sin(p) * sin(h))
    ret.set(1, 0, -sin(r) * cos(p))
    ret.set(2, 0, cos(r) * sin(h) + sin(r) * sin(p) * cos(h))

    ret.set(0, 1, sin(r) * cos(h) + cos(r) * sin(p) * sin(h))
    ret.set(1, 1, cos(r) * cos(p))
    ret.set(2, 1, sin(r) * sin(h) - cos(r) * sin(p) * cos(h))

    ret.set(0, 2, -cos(p) * sin(h))
    ret.set(1, 2, sin(p))
    ret.set(2, 2, cos(p) * cos(h))

    return ret


def matrix2euler(matrix):
    if isinstance(matrix, mt.Matrix3x3):
        mt3 = matrix
    elif isinstance(matrix, mt.Matrix4x4):
        mt3 = matrix.left_up()
    else:
        raise TypeError

    ret = vt.Vector3()

    if mt3.get(1, 0) == mt3.get(1, 1) == 0:
        ret.x = degrees(0)
        ret.y = degrees(asin(mt3.get(1, 2)))
        ret.z = degrees(atan2(mt3.get(0, 1), mt3.get(0, 0)))
    else:
        ret.x = degrees(atan2(-mt3.get(0, 2), mt3.get(2, 2)))
        ret.y = degrees(asin(mt3.get(1, 2)))
        ret.z = degrees(atan2(-mt3.get(1, 0), mt3.get(1, 1)))

    return ret


if __name__ == '__main__':
    v = vt.Vector3(130, 100, 150)
    mat = euler2matrix(v)
    print(mat)
    print('----')
    v = matrix2euler(mat)
    print(v)
