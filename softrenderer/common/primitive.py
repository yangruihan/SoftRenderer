# -*- coding:utf-8 -*-


from softrenderer.common.math.vector import Vector2
from softrenderer.common.types import Color


class Triangle:
    def __init__(self, *args):
        args_len = len(args)
        # vector1, vector2, vector3, color
        if args_len == 4:
            if isinstance(args[0], Vector2) \
                    and isinstance(args[1], Vector2) \
                    and isinstance(args[2], Vector2) \
                    and isinstance(args[3], Color):
                self._v1, self._v2, self._v3 = args[0], args[1], args[2]
                self._c1, self._c2, self._c3 = args[3], args[3], args[3]
            else:
                raise AttributeError
        # vector1, vector2, vector3, color1, color2, color3
        elif args_len == 6:
            if isinstance(args[0], Vector2) \
                    and isinstance(args[1], Vector2) \
                    and isinstance(args[2], Vector2) \
                    and isinstance(args[3], Color) \
                    and isinstance(args[4], Color) \
                    and isinstance(args[5], Color):
                self._v1, self._v2, self._v3 = args[0], args[1], args[2]
                self._c1, self._c2, self._c3 = args[3], args[4], args[5]
            else:
                raise AttributeError
        else:
            raise AttributeError

    def __str__(self):
        return 'Triangle(v1(p: %.5f, %.5f | c: %.5f, %.5f, %.5f, %.5f), ' \
               'v2(p: %.5f, %.5f | c: %.5f, %.5f, %.5f, %.5f), ' \
               'v3(p: %.5f, %.5f| c: %.5f, %.5f, %.5f, %.5f))' \
               % (self._v1.x, self._v1.y, self._c1.r, self._c1.g, self._c1.b, self._c1.a,
                  self._v2.x, self._v2.y, self._c2.r, self._c2.g, self._c2.b, self._c2.a,
                  self._v3.x, self._v3.y, self._c3.r, self._c3.g, self._c3.b, self._c3.a)

    def get_barycentrix(self, v):
        if not isinstance(v, Vector2):
            raise TypeError

        t = (self.v1.y - self.v3.y) * (self.v2.x - self.v3.x) + (self.v2.y - self.v3.y) * (self.v3.x - self.v1.x)
        b1 = ((v.y - self.v3.y) * (self.v2.x - self.v3.x) + (self.v2.y - self.v3.y) * (self.v3.x - v.x)) / t
        b2 = ((v.y - self.v1.y) * (self.v3.x - self.v1.x) + (self.v3.y - self.v1.y) * (self.v1.x - v.x)) / t
        b3 = ((v.y - self.v2.y) * (self.v1.x - self.v2.x) + (self.v1.y - self.v2.y) * (self.v2.x - v.x)) / t
        return b1, b2, b3

    def get_pixel_color(self, v):
        if not isinstance(v, Vector2):
            raise TypeError

        b1, b2, b3 = self.get_barycentrix(v)
        return self.c1 * b1 + self.c2 * b2 + self.c3 * b3

    @property
    def v1(self):
        return self._v1

    @property
    def v2(self):
        return self._v2

    @property
    def v3(self):
        return self._v3

    @property
    def c1(self):
        return self._c1

    @property
    def c2(self):
        return self._c2

    @property
    def c3(self):
        return self._c3
