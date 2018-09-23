# -*- coding:utf-8 -*-


from math import fabs, cos, sin, radians
from common.math.vector import Vector2, Vector3, Vector4

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

    @property
    def elements(self):
        return self._element

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
        if fabs(determinant) <= EPSILON:
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

    @property
    def elements(self):
        return self._element

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
        if fabs(determinant) <= EPSILON:
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
    ELEMENT_COUNT = 16
    ROW_COUNT = 4
    COL_COUNT = 4

    def __init__(self, *args):
        self._element = [0] * self.ELEMENT_COUNT
        self.set(*args)

    def __str__(self):
        return "Matrix4x4[[%s, %s, %s, %s], [%s, %s, %s, %s], [%s, %s, %s, %s], [%s, %s, %s, %s]]" % \
               (self[0], self[1], self[2], self[3],
                self[4], self[5], self[6], self[7],
                self[8], self[9], self[10], self[11],
                self[12], self[13], self[14], self[15])

    def __getitem__(self, item):
        if isinstance(item, int):
            return self._element[item]

    def __add__(self, other):
        if isinstance(other, Matrix4x4):
            return Matrix4x4(self[0] + other[0], self[1] + other[1], self[2] + other[2], self[3] + other[3],
                             self[4] + other[4], self[5] + other[5], self[6] + other[6], self[7] + other[7],
                             self[8] + other[8], self[9] + other[9], self[10] + other[10], self[11] + other[11],
                             self[12] + other[12], self[13] + other[13], self[14] + other[14], self[15] + other[15])

    def __sub__(self, other):
        if isinstance(other, Matrix4x4):
            return Matrix4x4(self[0] - other[0], self[1] - other[1], self[2] - other[2], self[3] - other[3],
                             self[4] - other[4], self[5] - other[5], self[6] - other[6], self[7] - other[7],
                             self[8] - other[8], self[9] - other[9], self[10] - other[10], self[11] - other[11],
                             self[12] - other[12], self[13] - other[13], self[14] - other[14], self[15] - other[15])

    def __mul__(self, other):
        if isinstance(other, Matrix4x4):
            ret = [0] * self.ELEMENT_COUNT
            for row in range(self.ROW_COUNT):
                for col in range(self.COL_COUNT):
                    sum_value = 0
                    for i in range(self.ROW_COUNT):
                        sum_value += self.get(i, row) * other.get(col, i)
                    ret[col + row * self.COL_COUNT] = sum_value
            return Matrix4x4(ret)
        elif isinstance(other, Vector4):
            return Vector4(self[0] * other.x + self[1] * other.y + self[2] * other.z + self[3] * other.w,
                           self[4] * other.x + self[5] * other.y + self[6] * other.z + self[7] * other.w,
                           self[8] * other.x + self[9] * other.y + self[10] * other.z + self[11] * other.w,
                           self[12] * other.x + self[13] * other.y + self[14] * other.z + self[15] * other.w, )
        else:
            try:
                s = float(other)
                self._element = [x * s for x in self._element]
            except ValueError:
                raise AttributeError

    def __eq__(self, other):
        if isinstance(other, Matrix4x4):
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
            elif isinstance(args[0], Matrix4x4):
                self._element = [args[0][i] for i in range(self.ELEMENT_COUNT)]
            else:
                self._element = [0] * self.ELEMENT_COUNT
                for i in range(self.ROW_COUNT):
                    self._element[i + i * self.COL_COUNT] = args[0]
        elif args_len == 4 \
                and isinstance(args[0], Vector4) \
                and isinstance(args[1], Vector4) \
                and isinstance(args[2], Vector4) \
                and isinstance(args[3], Vector4):
            self._element = [args[0].x, args[0].y, args[0].z, args[0].w,
                             args[1].x, args[1].y, args[1].z, args[1].w,
                             args[2].x, args[2].y, args[2].z, args[2].w,
                             args[3].x, args[3].y, args[3].z, args[3].w]
        elif args_len == 16:
            self._element = list(args)
        else:
            raise AttributeError

    def get(self, x, y):
        if x + y * self.COL_COUNT < self.ELEMENT_COUNT:
            return self[x + y * self.COL_COUNT]

    @property
    def elements(self):
        return self._element

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
        (self._element[1], self._element[4]) = (self._element[4], self._element[1])
        (self._element[2], self._element[8]) = (self._element[8], self._element[2])
        (self._element[3], self._element[12]) = (self._element[12], self._element[3])
        (self._element[6], self._element[9]) = (self._element[9], self._element[6])
        (self._element[7], self._element[13]) = (self._element[13], self._element[7])
        (self._element[11], self._element[14]) = (self._element[14], self._element[11])
        return self

    def determinant(self):
        """
        行列式
        """
        return self[0] * Matrix4x4._get_co_factor(self[5], self[6], self[7], self[9], self[10],
                                                  self[11], self[13], self[14], self[15]) - \
               self[1] * Matrix4x4._get_co_factor(self[4], self[6], self[7], self[8], self[10],
                                                  self[11], self[12], self[14], self[15]) + \
               self[2] * Matrix4x4._get_co_factor(self[4], self[5], self[7], self[8], self[9],
                                                  self[11], self[12], self[13], self[15]) - \
               self[3] * Matrix4x4._get_co_factor(self[4], self[5], self[6], self[8], self[9],
                                                  self[10], self[12], self[13], self[14])

    @staticmethod
    def _get_co_factor(m0, m1, m2, m3, m4, m5, m6, m7, m8):
        return m0 * (m4 * m8 - m5 * m7) - m1 * (m3 * m8 - m5 * m6) + m2 * (m3 * m7 - m4 * m6)

    def invert(self):
        """
        逆矩阵
        """
        if self[3] == 0 and self[7] == 0 and self[11] == 0 and self[15] == 1:
            self.invert_affine()
        else:
            self.invert_general()

        return self

    def inverted(self):
        tmp = Matrix4x4(self)
        if tmp[3] == 0 and tmp[7] == 0 and tmp[11] == 0 and tmp[15] == 1:
            tmp.invert_affine()
        else:
            tmp.invert_general()

        return tmp

    def invert_euclidean(self):
        (self._element[1], self._element[4]) = (self._element[4], self._element[1])
        (self._element[2], self._element[8]) = (self._element[8], self._element[2])
        (self._element[6], self._element[9]) = (self._element[9], self._element[6])

        i = self[12]
        j = self[13]
        k = self[14]
        self._element[12] = -(self[0] * i + self[4] * j + self[8] * k)
        self._element[13] = -(self[1] * i + self[5] * j + self[9] * k)
        self._element[14] = -(self[2] * i + self[6] * j + self[10] * k)

        return self

    def invert_affine(self):
        r = Matrix3x3(self[0], self[1], self[2],
                      self[4], self[5], self[6],
                      self[8], self[9], self[10])
        r.invert()
        (self._element[0], self._element[1], self._element[2]) = (r[0], r[1], r[2])
        (self._element[4], self._element[5], self._element[6]) = (r[3], r[4], r[5])
        (self._element[8], self._element[9], self._element[10]) = (r[6], r[7], r[8])

        i = self[12]
        j = self[13]
        k = self[14]
        self._element[12] = -(self[0] * i + self[4] * j + self[8] * k)
        self._element[13] = -(self[1] * i + self[5] * j + self[9] * k)
        self._element[14] = -(self[2] * i + self[6] * j + self[10] * k)

        return self

    def invert_projective(self):
        a = Matrix2x2(self[0], self[1], self[4], self[5])
        b = Matrix2x2(self[8], self[9], self[12], self[13])
        c = Matrix2x2(self[2], self[3], self[6], self[7])
        d = Matrix2x2(self[10], self[11], self[14], self[15])

        a.invert()
        ab = a * b
        ca = c * a
        cab = ca * b
        dcab = d - cab

        determinant = dcab[0] * dcab[3] - dcab[1] * dcab[2]
        if fabs(determinant) < EPSILON:
            return Matrix4x4.identity()

        d1 = dcab
        d1.invert()
        d2 = -dcab

        c1 = d2 * ca
        b1 = ab * d2
        a1 = a - (ab * c1)

        self.set(a1[0], a1[2], b1[0], b1[2],
                 a1[1], a1[3], b1[1], b1[3],
                 c1[0], c1[2], d1[0], d1[2],
                 c1[1], c1[3], d1[1], d1[3])

        return self

    def invert_general(self):
        co_factor0 = Matrix4x4._get_co_factor(self[5], self[6], self[7], self[9], self[10],
                                              self[11], self[13], self[14], self[15])
        co_factor1 = Matrix4x4._get_co_factor(self[4], self[6], self[7], self[8], self[10],
                                              self[11], self[12], self[14], self[15])
        co_factor2 = Matrix4x4._get_co_factor(self[4], self[5], self[7], self[8], self[9],
                                              self[11], self[12], self[13], self[15])
        co_factor3 = Matrix4x4._get_co_factor(self[4], self[5], self[6], self[8], self[9],
                                              self[10], self[12], self[13], self[14])

        determinant = self[0] * co_factor0 - self[1] * co_factor1 + self[2] * co_factor2 - self[3] * co_factor3
        if fabs(determinant) <= EPSILON:
            return Matrix4x4.identity()

        co_factor4 = Matrix4x4._get_co_factor(self[1], self[2], self[3], self[9], self[10],
                                              self[11], self[13], self[14], self[15])
        co_factor5 = Matrix4x4._get_co_factor(self[0], self[2], self[3], self[8], self[10],
                                              self[11], self[12], self[14], self[15])
        co_factor6 = Matrix4x4._get_co_factor(self[0], self[1], self[3], self[8], self[9],
                                              self[11], self[12], self[13], self[15])
        co_factor7 = Matrix4x4._get_co_factor(self[0], self[1], self[2], self[8], self[9],
                                              self[10], self[12], self[13], self[14])

        co_factor8 = Matrix4x4._get_co_factor(self[1], self[2], self[3], self[5], self[6],
                                              self[7], self[13], self[14], self[15])
        co_factor9 = Matrix4x4._get_co_factor(self[0], self[2], self[3], self[4], self[6],
                                              self[7], self[12], self[14], self[15])
        co_factor10 = Matrix4x4._get_co_factor(self[0], self[1], self[3], self[4], self[5],
                                               self[7], self[12], self[13], self[15])
        co_factor11 = Matrix4x4._get_co_factor(self[0], self[1], self[2], self[4], self[5],
                                               self[6], self[12], self[13], self[14])

        co_factor12 = Matrix4x4._get_co_factor(self[1], self[2], self[3], self[5], self[6],
                                               self[7], self[9], self[10], self[11])
        co_factor13 = Matrix4x4._get_co_factor(self[0], self[2], self[3], self[4], self[6],
                                               self[7], self[8], self[10], self[11])
        co_factor14 = Matrix4x4._get_co_factor(self[0], self[1], self[3], self[4], self[5],
                                               self[7], self[8], self[9], self[11])
        co_factor15 = Matrix4x4._get_co_factor(self[0], self[1], self[2], self[4], self[5],
                                               self[6], self[8], self[9], self[10])

        inv_determinant = 1 / determinant

        self._element[0] = inv_determinant * co_factor0
        self._element[1] = -inv_determinant * co_factor4
        self._element[2] = inv_determinant * co_factor8
        self._element[3] = -inv_determinant * co_factor12

        self._element[4] = -inv_determinant * co_factor1
        self._element[5] = inv_determinant * co_factor5
        self._element[6] = -inv_determinant * co_factor9
        self._element[7] = inv_determinant * co_factor13

        self._element[8] = inv_determinant * co_factor2
        self._element[9] = -inv_determinant * co_factor6
        self._element[10] = inv_determinant * co_factor10
        self._element[11] = -inv_determinant * co_factor14

        self._element[12] = -inv_determinant * co_factor3
        self._element[13] = inv_determinant * co_factor7
        self._element[14] = -inv_determinant * co_factor11
        self._element[15] = inv_determinant * co_factor15

        return self

    def translate(self, *args):
        args_len = len(args)
        if args_len == 1 and isinstance(args[0], Vector3):
            return self.translate(args[0].x, args[0].y, args[0].z)
        elif args_len == 3:
            (x, y, z) = args

            self._element[0] += self[3] * x
            self._element[1] += self[3] * y
            self._element[2] += self[3] * z

            self._element[4] += self[7] * x
            self._element[5] += self[7] * y
            self._element[6] += self[7] * z

            self._element[8] += self[11] * x
            self._element[9] += self[11] * y
            self._element[10] += self[11] * z

            self._element[12] += self[15] * x
            self._element[13] += self[15] * y
            self._element[14] += self[15] * z

            return self
        else:
            raise AttributeError

    def scale(self, *args):
        args_len = len(args)
        if args_len == 1:
            return self.scale(*([args[0]] * 3))
        elif args_len == 3:
            (x, y, z) = args

            self._element[0] *= x
            self._element[1] *= y
            self._element[2] *= z

            self._element[4] *= x
            self._element[5] *= y
            self._element[6] *= z

            self._element[8] *= x
            self._element[9] *= y
            self._element[10] *= z

            self._element[12] *= x
            self._element[13] *= y
            self._element[14] *= z

            return self
        else:
            raise AttributeError

    def rotate(self, *args):
        args_len = len(args)
        if args_len == 2 and isinstance(args[1], Vector3):
            return self.rotate(args[0], args[1].x, args[1].y, args[1].z)
        elif args_len == 4:
            (angle, x, y, z) = args
            c = cos(radians(angle))
            s = sin(radians(angle))
            c1 = 1 - c
            (m0, m1, m2, _,
             m4, m5, m6, _,
             m8, m9, m10, _,
             m12, m13, m14, _) = self.elements

            r0 = x * x * c1 + c
            r1 = x * y * c1 + z * s
            r2 = x * z * c1 - y * s
            r4 = x * y + c1 - z * s
            r5 = y * y * c1 + c
            r6 = y * z * c1 + x * s
            r8 = x * z * c1 + y * s
            r9 = y * z * c1 - x * s
            r10 = z * z * c1 + c

            self._element[0] = r0 * m0 + r4 * m1 + r8 * m2
            self._element[1] = r1 * m0 + r5 * m1 + r9 * m2
            self._element[2] = r2 * m0 + r6 * m1 + r10 * m2
            self._element[4] = r0 * m4 + r4 * m5 + r8 * m6
            self._element[5] = r1 * m4 + r5 * m5 + r9 * m6
            self._element[6] = r2 * m4 + r6 * m5 + r10 * m6
            self._element[8] = r0 * m8 + r4 * m9 + r8 * m10
            self._element[9] = r1 * m8 + r5 * m9 + r9 * m10
            self._element[10] = r2 * m8 + r6 * m9 + r10 * m10
            self._element[12] = r0 * m12 + r4 * m13 + r8 * m14
            self._element[13] = r1 * m12 + r5 * m13 + r9 * m14
            self._element[14] = r2 * m12 + r6 * m13 + r10 * m14

            return self
        else:
            raise AttributeError

    def rotate_x(self, angle):
        c = cos(radians(angle))
        s = sin(radians(angle))
        (m1, m2,
         m5, m6,
         m9, m10,
         m13, m14) = (self[1], self[2],
                      self[5], self[6],
                      self[9], self[10],
                      self[13], self[14])

        self._element[1] = m1 * c + m2 * -s
        self._element[2] = m1 * s + m2 * c
        self._element[5] = m5 * c + m6 * -s
        self._element[6] = m5 * s + m6 * c
        self._element[9] = m9 * c + m10 * -s
        self._element[10] = m9 * s + m10 * c
        self._element[13] = m13 * c + m14 * -s
        self._element[14] = m13 * s + m14 * c

        return self

    def rotate_y(self, angle):
        c = cos(radians(angle))
        s = sin(radians(angle))
        (m0, m2,
         m4, m6,
         m8, m10,
         m12, m14) = (self[0], self[2],
                      self[4], self[6],
                      self[8], self[10],
                      self[12], self[14])

        self._element[0] = m0 * c + m2 * s
        self._element[2] = m0 * -s + m2 * c
        self._element[4] = m4 * c + m6 * s
        self._element[6] = m4 * -s + m6 * c
        self._element[8] = m8 * c + m10 * s
        self._element[10] = m8 * -s + m10 * c
        self._element[12] = m12 * c + m14 * s
        self._element[14] = m12 * -s + m14 * c

        return self

    def rotate_z(self, angle):
        c = cos(radians(angle))
        s = sin(radians(angle))
        (m0, m1,
         m4, m5,
         m8, m9,
         m12, m13) = (self[0], self[1],
                      self[4], self[5],
                      self[8], self[9],
                      self[12], self[13])

        self._element[0] = m0 * c + m1 * -s
        self._element[1] = m0 * s + m1 * c
        self._element[4] = m4 * c + m5 * -s
        self._element[5] = m4 * s + m5 * c
        self._element[8] = m8 * c + m9 * -s
        self._element[9] = m8 * s + m9 * c
        self._element[12] = m12 * c + m13 * -s
        self._element[13] = m12 * s + m13 * c

        return self

    @classmethod
    def identity(cls):
        return Matrix4x4(1)
