# -*- coding:utf-8 -*-


from common.math.vector import Vector2, Vector3

EPSILON = 0.00001


class Matrix2x2:
    ELEMENT_COUNT = 4
    ROW_COUNT = 2
    COL_COUNT = 2

    def __init__(self, *args):
        self._element = [0] * self.ELEMENT_COUNT
        self.set(*args)

    def __str__(self):
        return "Matrix2x2[[%s, %s], [%s, %s]]" % (self[0],
                                                  self[1],
                                                  self[2],
                                                  self[3])

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
                raise AttributeError

    def __eq__(self, other):
        if isinstance(other, Matrix2x2):
            for i in range(self.ELEMENT_COUNT):
                if self[i] != other[i]:
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
        if x + y * self.COL_COUNT < self.ELEMENT_COUNT:
            return self[x + y * self.COL_COUNT]

    def set_row(self, index, values):
        for i in range(self.COL_COUNT):
            self._element[i + index * self.COL_COUNT] = values[i]

    def set_col(self, index, values):
        for i in range(self.ROW_COUNT):
            self._element[index + i * self.COL_COUNT] = values[i]

    def get_row(self, index):
        ret = []
        for i in range(self.COL_COUNT):
            ret.append(self[i + index * self.COL_COUNT])
        return ret

    def get_col(self, index):
        ret = []
        for i in range(self.ROW_COUNT):
            ret.append(self[index + i * self.COL_COUNT])
        return ret

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
        return self[0] * self[3] - self[1] * self[2]

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
         self._element[3]) = (inv_determinant * self[3],
                              -inv_determinant * self[1],
                              -inv_determinant * self[2],
                              inv_determinant * self[0])
        return self

    @classmethod
    def identity(cls):
        return Matrix2x2(1)


class Matrix3x3:
    ELEMENT_COUNT = 9
    ROW_COUNT = 3
    COL_COUNT = 3

    def __init__(self, *args):
        self._element = [0] * self.ELEMENT_COUNT
        self.set(*args)

    def __str__(self):
        return "Matrix3x3[[%s, %s, %s], [%s, %s, %s], [%s, %s, %s]]" % \
               (self[0], self[1], self[2],
                self[3], self[4], self[5],
                self[6], self[7], self[8])

    def __getitem__(self, item):
        if isinstance(item, int):
            return self._element[item]

    def __add__(self, other):
        if isinstance(other, Matrix3x3):
            return Matrix3x3(self[0] + other[0], self[1] + other[1], self[2] + other[2],
                             self[3] + other[3], self[4] + other[4], self[5] + other[5],
                             self[6] + other[6], self[7] + other[7], self[8] + other[8])

    def __sub__(self, other):
        if isinstance(other, Matrix3x3):
            return Matrix3x3(self[0] - other[0], self[1] - other[1], self[2] - other[2],
                             self[3] - other[3], self[4] - other[4], self[5] - other[5],
                             self[6] - other[6], self[7] - other[7], self[8] - other[8])

    def __mul__(self, other):
        if isinstance(other, Matrix3x3):
            ret = [0] * self.ELEMENT_COUNT
            for row in range(self.ROW_COUNT):
                for col in range(self.COL_COUNT):
                    sum_value = 0
                    for i in range(self.ROW_COUNT):
                        sum_value += self.get(i, row) * other.get(col, i)
                    ret[col + row * self.COL_COUNT] = sum_value
            return Matrix3x3(ret)
        elif isinstance(other, Vector3):
            return Vector3(self[0] * other.x + self[1] * other.y + self[2] * other.z,
                           self[3] * other.x + self[4] * other.y + self[5] * other.z,
                           self[6] * other.x + self[7] * other.y + self[8] * other.z)
        else:
            try:
                s = float(other)
                self._element = [x * s for x in self._element]
            except ValueError:
                raise AttributeError

    def __eq__(self, other):
        if isinstance(other, Matrix3x3):
            for i in range(self.ELEMENT_COUNT):
                if self[i] != other._element[i]:
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
                for i in range(self.ROW_COUNT):
                    self._element[i + i * self.COL_COUNT] = args[0]
        elif args_len == 3 \
                and isinstance(args[0], Vector3) \
                and isinstance(args[1], Vector3) \
                and isinstance(args[2], Vector3):
            self._element = [args[0].x, args[0].y, args[0].z,
                             args[1].x, args[1].y, args[1].z,
                             args[2].x, args[2].y, args[2].z]
        elif args_len == 9:
            self._element = list(args)
        else:
            raise AttributeError

    def get(self, x, y):
        if x + y * self.COL_COUNT < self.ELEMENT_COUNT:
            return self[x + y * self.COL_COUNT]

    def set_row(self, index, values):
        for i in range(self.COL_COUNT):
            self._element[i + index * self.COL_COUNT] = values[i]

    def set_col(self, index, values):
        for i in range(self.ROW_COUNT):
            self._element[index + i * self.COL_COUNT] = values[i]

    def get_row(self, index):
        ret = []
        for i in range(self.COL_COUNT):
            ret.append(self[i + index * self.COL_COUNT])
        return ret

    def get_col(self, index):
        ret = []
        for i in range(self.ROW_COUNT):
            ret.append(self[index + i * self.COL_COUNT])
        return ret

    def transpose(self):
        """
        转置矩阵
        """
        (self._element[1], self._element[3]) = (self._element[3], self._element[1])
        (self._element[2], self._element[6]) = (self._element[6], self._element[2])
        (self._element[5], self._element[7]) = (self._element[7], self._element[5])
        return self

    def determinant(self):
        """
        行列式
        """
        return self[0] * (self[4] * self[8] - self[5] * self[7]) - \
               self[1] * (self[3] * self[8] - self[5] * self[6]) + \
               self[2] * (self[3] * self[7] - self[4] * self[6])

    def invert(self):
        """
        逆矩阵
        """
        determinant = self.determinant()
        if determinant <= EPSILON:
            return Matrix3x3.identity()

        tmp = [0] * self.ELEMENT_COUNT
        tmp[0] = self[4] * self[8] - self[5] * self[7]
        tmp[1] = self[2] * self[7] - self[1] * self[8]
        tmp[2] = self[1] * self[5] - self[2] * self[4]
        tmp[3] = self[5] * self[6] - self[3] * self[8]
        tmp[4] = self[0] * self[8] - self[2] * self[6]
        tmp[5] = self[2] * self[3] - self[0] * self[5]
        tmp[6] = self[3] * self[7] - self[4] * self[6]
        tmp[7] = self[1] * self[6] - self[0] * self[7]
        tmp[8] = self[0] * self[4] - self[1] * self[3]

        inv_determinant = 1 / determinant
        for i in range(self.ELEMENT_COUNT):
            self._element[i] = inv_determinant * tmp[i]

        return self

    @classmethod
    def identity(cls):
        return Matrix3x3(1)


class Matrix4x4:

    def __init__(self, *args):
        pass
