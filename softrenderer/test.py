# -*- coding:utf-8 -*-


import unittest
from softrenderer.common.math.matrix import Matrix2x2, Matrix3x3
from softrenderer.common.math.vector import Vector2, Vector3, Vector4
from softrenderer.common.math.quaternion import Quaternion
from softrenderer.common.transform import Transform


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
        self.assertEqual(str(self.m), 'Matrix2x2[[0.00000, 0.00000], [0.00000, 0.00000]]')
        self.assertEqual(str(self.m1), 'Matrix2x2[[1.00000, 2.00000], [3.00000, 4.00000]]')
        self.assertEqual(str(self.m2), 'Matrix2x2[[5.00000, 6.00000], [7.00000, 8.00000]]')
        self.assertEqual(str(self.m3), 'Matrix2x2[[5.00000, 0.00000], [0.00000, 5.00000]]')
        self.assertEqual(str(self.m4), 'Matrix2x2[[1.00000, 2.00000], [3.00000, 4.00000]]')
        self.assertEqual(str(self.m5), 'Matrix2x2[[1.00000, 2.00000], [3.00000, 4.00000]]')

    def test_get(self):
        self.assertEqual(self.m1.get(0, 1), 3)
        self.assertEqual(self.m3.get(1, 1), 5)

    def test_identity(self):
        self.assertEqual(str(Matrix2x2.identity()), 'Matrix2x2[[1.00000, 0.00000], [0.00000, 1.00000]]')

    def test_get_item(self):
        self.assertEqual(self.m1[0], 1)
        self.assertEqual(self.m5[3], 4)

    def test_add(self):
        tmp = self.m1 + self.m2
        self.assertEqual(str(tmp), 'Matrix2x2[[6.00000, 8.00000], [10.00000, 12.00000]]')

    def test_sub(self):
        tmp = self.m2 - self.m1
        self.assertEqual(str(tmp), 'Matrix2x2[[4.00000, 4.00000], [4.00000, 4.00000]]')

    def test_mul(self):
        tmp = self.m1 * self.m2
        self.assertEqual(str(tmp), 'Matrix2x2[[19.00000, 22.00000], [43.00000, 50.00000]]')

    def test_eq(self):
        self.assertTrue(self.m1 == self.m5)

    def test_transpose(self):
        tmp = Matrix2x2([1, 2, 3, 4])
        tmp.transpose()
        self.assertEqual(str(tmp), 'Matrix2x2[[1.00000, 3.00000], [2.00000, 4.00000]]')


class TestMatrix3x3Methods(unittest.TestCase):

    def setUp(self):
        self.m = Matrix3x3()
        self.m1 = Matrix3x3([1, 2, 3, 4, 5, 6, 7, 8, 9])
        self.m2 = Matrix3x3((5, 6, 7, 8, 9, 10, 11, 12, 13))
        self.m3 = Matrix3x3(5)
        self.m4 = Matrix3x3(Vector3(1, 2, 3), Vector3(4, 5, 6), Vector3(7, 8, 9))
        self.m5 = Matrix3x3(1, 2, 3, 4, 5, 6, 7, 8, 9)

    def test_init(self):
        self.assertEqual(self.m[0], 0)
        self.assertEqual(self.m[1], 0)
        self.assertEqual(self.m[2], 0)
        self.assertEqual(self.m[3], 0)
        self.assertEqual(str(self.m),
                         'Matrix3x3[[0.00000, 0.00000, 0.00000],'
                         ' [0.00000, 0.00000, 0.00000],'
                         ' [0.00000, 0.00000, 0.00000]]')
        self.assertEqual(str(self.m1),
                         'Matrix3x3[[1.00000, 2.00000, 3.00000],'
                         ' [4.00000, 5.00000, 6.00000],'
                         ' [7.00000, 8.00000, 9.00000]]')
        self.assertEqual(str(self.m2),
                         'Matrix3x3[[5.00000, 6.00000, 7.00000],'
                         ' [8.00000, 9.00000, 10.00000],'
                         ' [11.00000, 12.00000, 13.00000]]')
        self.assertEqual(str(self.m3),
                         'Matrix3x3[[5.00000, 0.00000, 0.00000],'
                         ' [0.00000, 5.00000, 0.00000],'
                         ' [0.00000, 0.00000, 5.00000]]')
        self.assertEqual(str(self.m4),
                         'Matrix3x3[[1.00000, 2.00000, 3.00000],'
                         ' [4.00000, 5.00000, 6.00000],'
                         ' [7.00000, 8.00000, 9.00000]]')
        self.assertEqual(str(self.m5),
                         'Matrix3x3[[1.00000, 2.00000, 3.00000],'
                         ' [4.00000, 5.00000, 6.00000],'
                         ' [7.00000, 8.00000, 9.00000]]')

    def test_get(self):
        self.assertEqual(self.m1.get(0, 1), 4)
        self.assertEqual(self.m3.get(1, 1), 5)

    def test_identity(self):
        self.assertEqual(str(Matrix3x3.identity()),
                         'Matrix3x3[[1.00000, 0.00000, 0.00000],'
                         ' [0.00000, 1.00000, 0.00000],'
                         ' [0.00000, 0.00000, 1.00000]]')

    def test_get_item(self):
        self.assertEqual(self.m1[0], 1)
        self.assertEqual(self.m5[3], 4)

    def test_add(self):
        tmp = self.m1 + self.m2
        self.assertEqual(str(tmp),
                         'Matrix3x3[[6.00000, 8.00000, 10.00000],'
                         ' [12.00000, 14.00000, 16.00000],'
                         ' [18.00000, 20.00000, 22.00000]]')

    def test_sub(self):
        tmp = self.m2 - self.m1
        self.assertEqual(str(tmp),
                         'Matrix3x3[[4.00000, 4.00000, 4.00000],'
                         ' [4.00000, 4.00000, 4.00000],'
                         ' [4.00000, 4.00000, 4.00000]]')

    def test_mul(self):
        tmp = self.m1 * self.m2
        self.assertEqual(str(tmp),
                         'Matrix3x3[[54.00000, 60.00000, 66.00000],'
                         ' [126.00000, 141.00000, 156.00000],'
                         ' [198.00000, 222.00000, 246.00000]]')

    def test_eq(self):
        self.assertTrue(self.m1 == self.m5)

    def test_transpose(self):
        tmp = Matrix3x3([1, 2, 3, 4, 5, 6, 7, 8, 9])
        tmp.transpose()
        self.assertEqual(str(tmp),
                         'Matrix3x3[[1.00000, 4.00000, 7.00000],'
                         ' [2.00000, 5.00000, 8.00000],'
                         ' [3.00000, 6.00000, 9.00000]]')


class TestTransformMethods(unittest.TestCase):
    def setUp(self):
        self._tf = Transform()

    def test_init(self):
        self.assertEqual(self._tf.position, Vector3.zero())
        self.assertEqual(self._tf.rotation, Quaternion.identity())
        self.assertEqual(self._tf.scale, Vector3.one())

    def test_transform(self):
        tmp = Transform(self._tf)
        tmp.translate(Vector3.right())
        self.assertEqual(tmp.position, Vector3(1, 0, 0))
        print(tmp)
        tmp.rotate_axis(Vector3.forward(), -90)
        print(tmp)
        tmp.scale = Vector3(2, 2, 2)

        print(tmp.get_local_to_world_matrix() * Vector4(Vector3.right(), 1))


if __name__ == '__main__':
    pass
