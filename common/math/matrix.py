# -*- coding:utf-8 -*-


from common.math.vector import *


class Matrix2x2:

    def __init__(self, *args):
        self._element = [0] * 4
        self.set(*args)

    def __str__(self):
        return "Matrix2x2[[%s, %s], [%s, %s]]" % (self._element[0],
                                                  self._element[1],
                                                  self._element[2],
                                                  self._element[3])

    def __getitem__(self, item):
        if isinstance(item, int):
            return self._element[item]

    def __mul__(self, other):
        ret = [0] * 4
        if isinstance(other, Matrix2x2):
            for row in range(2):
                for col in range(2):
                    sum_value = 0
                    for i in range(2):
                        sum_value += self.get(i, row) * other.get(col, i)
                    ret[col + row * 2] = sum_value
        return Matrix2x2(ret)

    def set(self, *args):
        args_len = len(args)
        if args_len == 0:
            pass
        elif args_len == 1:
            if isinstance(args[0], list) or isinstance(args[0], tuple):
                self._element = [_ for _ in args[0]]
            else:
                self._element = [0] * 4
                self._element[0 + 0 * 2] = args[0]
                self._element[1 + 1 * 2] = args[0]
        elif args_len == 2 and isinstance(args[0], Vector2) and isinstance(args[1], Vector2):
            self._element = [args[0].x, args[0].y,
                             args[1].x, args[1].y]
        else:
            raise AttributeError

    def get(self, x, y):
        if x + y * 2 < 4:
            return self._element[x + y * 2]

    def set_row(self, index, *args):
        pass

    def set_col(self, index, *args):
        pass

    def transpose(self):
        pass

    def invert(self):
        pass

    @classmethod
    def identity(cls):
        return Matrix2x2(1)


class Matrix3x3:

    def __init__(self, *args):
        pass


class Matrix4x4:

    def __init__(self, *args):
        pass
