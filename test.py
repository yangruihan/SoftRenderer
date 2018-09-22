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

    def test_get(self):
        self.assertEqual(self.m1.get(0, 1), 3)
        self.assertEqual(self.m3.get(1, 1), 5)

    def test_identity(self):
        self.assertEqual(str(Matrix2x2.identity()), 'Matrix2x2[[1, 0], [0, 1]]')


if __name__ == '__main__':
    pass
