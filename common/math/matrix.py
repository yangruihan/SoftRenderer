# -*- coding:utf-8 -*-


from common.math.vector import *

EPSILON = 0.00001


class Matrix2x2:
    ELEMENT_COUNT = 4
    ROW_COUNT = 2
    COL_COUNT = 2

    def __init__(self, *args):
        self._element = [0] * self.ELEMENT_COUNT
        self.set(*args)

    def __str__(self):
        return "Matrix2x2[[%s, %s], [%s, %s]]" % (self._element[0],
                                                  self._element[1],
                                                  self._element[2],
                                                  self._element[3])

    def __getitem__(self, item):
        if isinstance(item, int):
            return self._element[item]

    def __add__(self, other):
        if isinstance(other, Matrix2x2):
            return Matrix2x2(self[0] + other[0],
                             self[1] + other[1],
                             self[2] + other[2],
                             self[3] + other[3])

    def __sub__(self, other):
        if isinstance(other, Matrix2x2):
            return Matrix2x2(self[0] - other[0],
                             self[1] - other[1],
                             self[2] - other[2],
                             self[3] - other[3])

    def __mul__(self, other):
        if isinstance(other, Matrix2x2):
            ret = [0] * self.ELEMENT_COUNT
            for row in range(self.ROW_COUNT):
                for col in range(self.COL_COUNT):
                    sum_value = 0
                    for i in range(self.ROW_COUNT):
                        sum_value += self.get(i, row) * other.get(col, i)
                    ret[col + row * self.COL_COUNT] = sum_value
            return Matrix2x2(ret)
        elif isinstance(other, Vector2):
            return Vector2(self[0] * other.x + self[1] * other.y,
                           self[2] * other.x + self[3] * other.y)
        else:
            try:
                s = float(other)
                self._element = [x * s for x in self._element]
            except ValueError:
                pass

    def __eq__(self, other):
        if isinstance(other, Matrix2x2):
            for i in range(self.ELEMENT_COUNT):
                if self._element[i] != other._element[i]:
                    return False
            return True
        else:
            return False

    def set(self, *args):
        args_len = len(args)
        if args_len == 0:
            pass
        elif args_len == 1:
            if isinstance(args[0], list) or isinstance(args[0], tuple):
                self._element = [_ for _ in args[0]]
            else:
                self._element = [0] * self.ELEMENT_COUNT
                self._element[0 + 0 * 2] = args[0]
                self._element[1 + 1 * 2] = args[0]
        elif args_len == 2 and isinstance(args[0], Vector2) and isinstance(args[1], Vector2):
            self._element = [args[0].x, args[0].y,
                             args[1].x, args[1].y]
        elif args_len == 4:
            self._element = [args[0], args[1], args[2], args[3]]
        else:
            raise AttributeError

    def get(self, x, y):
        if x + y * 2 < self.ELEMENT_COUNT:
            return self._element[x + y * 2]

    def set_row(self, index, *args):
        pass

    def set_col(self, index, *args):
        pass

    def transpose(self):
        """
        转置矩阵
        """
        (self._element[1], self._element[2]) = (self._element[2], self._element[1])
        return self

    def determinant(self):
        """
        行列式
        """
        return self._element[0] * self._element[3] - self._element[1] * self._element[2]

    def invert(self):
        """
        逆矩阵
        """
        determinant = self.determinant()
        if determinant <= EPSILON:
            return Matrix2x2.identity()
        inv_determinant = 1 / determinant
        (self._element[0],
         self._element[1],
         self._element[2],
         self._element[3]) = (inv_determinant * self._element[3],
                              -inv_determinant * self._element[1],
                              -inv_determinant * self._element[2],
                              inv_determinant * self._element[0])
        return self

    @classmethod
    def identity(cls):
        return Matrix2x2(1)


class Matrix3x3:

    def __init__(self, *args):
        pass


class Matrix4x4:

    def __init__(self, *args):
        pass
