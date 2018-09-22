# -*- coding:utf-8 -*-


import unittest
from common.math.matrix import Matrix2x2
from common.math.vector import Vector2


class TestMatrix2x2Methods(unittest.TestCase):

    def setUp(self):
        self.m = Matrix2x2()
        self.m1 = Matrix2x2([1, 2, 3, 4])
        self.m2 = Matrix2x2((5, 6, 7, 8))
        self.m3 = Matrix2x2(5)
        self.m4 = Matrix2x2(Vector2(1, 2), Vector2(3, 4))
        self.m5 = Matrix2x2(1, 2, 3, 4)

    def test_init(self):
        self.assertEqual(self.m[0], 0)
        self.assertEqual(self.m[1], 0)
        self.assertEqual(self.m[2], 0)
        self.assertEqual(self.m[3], 0)
        self.assertEqual(str(self.m), 'Matrix2x2[[0, 0], [0, 0]]')
        self.assertEqual(str(self.m1), 'Matrix2x2[[1, 2], [3, 4]]')
        self.assertEqual(str(self.m2), 'Matrix2x2[[5, 6], [7, 8]]')
        self.assertEqual(str(self.m3), 'Matrix2x2[[5, 0], [0, 5]]')
        self.assertEqual(str(self.m4), 'Matrix2x2[[1, 2], [3, 4]]')
        self.assertEqual(str(self.m5), 'Matrix2x2[[1, 2], [3, 4]]')

    def test_get(self):
        self.assertEqual(self.m1.get(0, 1), 3)
        self.assertEqual(self.m3.get(1, 1), 5)

    def test_identity(self):
        self.assertEqual(str(Matrix2x2.identity()), 'Matrix2x2[[1, 0], [0, 1]]')

    def test_get_item(self):
        self.assertEqual(self.m1[0], 1)
        self.assertEqual(self.m5[3], 4)

    def test_add(self):
        tmp = self.m1 + self.m2
        self.assertEqual(str(tmp), 'Matrix2x2[[6, 8], [10, 12]]')

    def test_sub(self):
        tmp = self.m2 - self.m1
        self.assertEqual(str(tmp), 'Matrix2x2[[4, 4], [4, 4]]')

    def test_mul(self):
        tmp = self.m1 * self.m2
        self.assertEqual(str(tmp), 'Matrix2x2[[19, 22], [43, 50]]')

    def test_eq(self):
        self.assertTrue(self.m1 == self.m5)

    def test_transpose(self):
        tmp = Matrix2x2([1, 2, 3, 4])
        tmp.transpose()
        self.assertEqual(str(tmp), 'Matrix2x2[[1, 3], [2, 4]]')


if __name__ == '__main__':
    pass
