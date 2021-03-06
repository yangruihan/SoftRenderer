# -*- coding:utf-8 -*-


from math import floor
from joblib import Parallel, delayed
import multiprocessing

from softrenderer.common.math.vector import Vector2, Vector3
from softrenderer.common.types import Color
from softrenderer.render import shader
from softrenderer.render import render_context as rc

from softrenderer.cython import render_utils as ru

from softrenderer.debug import profiler

CORE_NUM = multiprocessing.cpu_count()


class Primitive:
    pass


class Point(Primitive):
    """Point primitive
    """

    def __init__(self, start_pos, array_buffer):
        super().__init__()

        self._start_pos = start_pos
        self._properties = array_buffer

    def __str__(self):
        return 'Point(%.5f, %.5f, %.5f)' % (self.x, self.y, self.z)

    def __setitem__(self, index, value):
        self._properties[self._start_pos + index] = value

    def __getitem__(self, index):
        return self._properties[self._start_pos + index]

    def rasterize(self):
        self[0] = floor(self.x)
        self[1] = floor(self.y)

    @property
    def x(self):
        return self[0]

    @x.setter
    def x(self, x):
        self[0] = x

    @property
    def y(self):
        return self[1]

    @y.setter
    def y(self, y):
        self[1] = y

    @property
    def z(self):
        return self[2]

    @z.setter
    def z(self, z):
        self[2] = z

    @property
    def w(self):
        return self[3]

    @w.setter
    def w(self, w):
        self[3] = w


class Line(Primitive):
    """Line primitive
    """

    def __init__(self, start, end):
        if not isinstance(start, Point) or \
                not isinstance(end, Point):
            raise TypeError

        super().__init__()

        self._start = start
        self._end = end

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, start):
        if not isinstance(start, Point):
            raise TypeError

        self._start = start

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, end):
        if not isinstance(end, Point):
            raise TypeError

        self._end = end


class Triangle(Primitive):
    """Triangle Primitive
    """

    def __init__(self, v1, v2, v3):
        if not isinstance(v1, Point) or \
                not isinstance(v2, Point) or \
                not isinstance(v3, Point):
            raise TypeError

        super().__init__()

        self._v1 = v1
        self._v2 = v2
        self._v3 = v3
        self._scan_buffer = None
        self._pixels = None
        self._properties_gradient = {}

    @property
    def v1(self):
        return self._v1

    @v1.setter
    def v1(self, v1):
        if not isinstance(v1, Point):
            raise TypeError

        self._v1 = v1

    @property
    def v2(self):
        return self._v2

    @v2.setter
    def v2(self, v2):
        if not isinstance(v2, Point):
            raise TypeError

        self._v2 = v2

    @property
    def v3(self):
        return self._v3

    @v3.setter
    def v3(self, v3):
        if not isinstance(v3, Point):
            raise TypeError

        self._v3 = v3

    @property
    def pixels(self):
        return self._pixels

    def rasterize(self):
        self.v1.rasterize()
        self.v2.rasterize()
        self.v3.rasterize()

        # sorted by y axis
        self._v1, self._v2, self._v3 = sorted([self._v1, self._v2, self._v3], key=lambda vertex: vertex.y)

        # init scan buffer
        self._scan_buffer = [[None, None] for _ in range(self._v3.y - self._v1.y + 1)]

        # calculate properties gradient
        self._properties_gradient = []

        try:
            one_over_dx = 1.0 / ((self.v2.x - self.v3.x) * (self.v1.y - self.v3.y)
                                 - (self.v1.x - self.v3.x) * (self.v2.y - self.v3.y))

            for i in range(rc.RenderContext.instance().each_vertex_properties_count):
                gx = one_over_dx * ((self.v2[i] - self.v3[i]) * (self.v1.y - self.v3.y)
                                    - (self.v1[i] - self.v3[i]) * (self.v2.y - self.v3.y))
                gy = -one_over_dx * ((self.v2[i] - self.v3[i]) * (self.v1.x - self.v3.x)
                                     - (self.v1[i] - self.v3[i]) * (self.v2.x - self.v3.x))
                self._properties_gradient.append((gx, gy))

        except ZeroDivisionError:
            if self.v1.x == self.v2.x == self.v3.x:
                if self.v1.y >= self.v2.y:
                    for i in range(rc.RenderContext.instance().each_vertex_properties_count):
                        self._properties_gradient.append((0,
                                                          ((self.v3[i] - self.v1[i]) / (self.v3.y - self.v1.y))))
                else:
                    for i in range(rc.RenderContext.instance().each_vertex_properties_count):
                        self._properties_gradient.append((0,
                                                          ((self.v3[i] - self.v2[i]) / (self.v3.y - self.v2.y))))
            else:
                # sorted by x axis
                self._v1, self._v2, self._v3 = sorted([self._v1, self._v2, self._v3], key=lambda vertex: vertex.x)
                if self.v1.y >= self.v2.y:
                    for i in range(rc.RenderContext.instance().each_vertex_properties_count):
                        self._properties_gradient.append((0,
                                                          ((self.v3[i] - self.v1[i]) / (self.v3.x - self.v1.x))))
                else:
                    for i in range(rc.RenderContext.instance().each_vertex_properties_count):
                        self._properties_gradient.append((0,
                                                          ((self.v3[i] - self.v2[i]) / (self.v3.x - self.v2.x))))

        # calculate handedness
        vector1 = Vector2(self._v3.x - self._v1.x, self._v3.y - self._v1.y)
        vector2 = Vector2(self._v2.x - self._v1.x, self._v2.y - self._v1.y)
        handedness = 0 if Vector2.cross(vector1, vector2) < 0 else 1

        # scan edge
        self._refresh_scan_buffer(self._v1, self._v3, handedness)
        self._refresh_scan_buffer(self._v1, self._v2, 1 - handedness)
        self._refresh_scan_buffer(self._v2, self._v3, 1 - handedness)

    def _refresh_scan_buffer(self, min_y_v, max_y_v, handedness):
        len_y = max_y_v.y - min_y_v.y
        if len_y == 0:
            return

        slope = (max_y_v.x - min_y_v.x) / len_y
        x = min_y_v.x
        t_slope = 1 / (len_y + 1)
        t = 0

        for i, y in enumerate(range(min_y_v.y, max_y_v.y + 1)):
            vertex_properties = []
            for index in range(2, rc.RenderContext.instance().each_vertex_properties_count):
                gx, gy = self._properties_gradient[index]
                value = min_y_v[index] + (gy + gx * slope) * i
                vertex_properties.append(value)

            vertex_properties[0] = floor(x)
            vertex_properties[1] = y

            self._scan_buffer[y - self._v1.y][handedness] = vertex_properties
            x += slope
            t += t_slope

    def pixel_shading(self, pixel_shader):
        if not isinstance(pixel_shader, shader.PixelShader):
            raise TypeError

        self._properties_gradient = self._properties_gradient[:2] + self._properties_gradient[4:]

        self._pixels = []
        scan_len = len(self._scan_buffer)
        pixel_info = Parallel(n_jobs=CORE_NUM)(
            delayed(Triangle._scan_line_pixel_shading_job2)(*self._scan_buffer[i], self._properties_gradient,
                                                            pixel_shader) for i in range(0, scan_len))
        self._pixels += sum(pixel_info, [])

    @staticmethod
    def _scan_line_pixel_shading_job2(start, end, properties_gradient, pixel_shader):
        if start is None or end is None:
            return []

        profiler.Profiler.begin('pixel_stage.pixel_shading.scan_x')
        pixel_info = ru.scan_line_pixel_shading_job(start, end[0], properties_gradient, pixel_shader)
        pixel_info.append((start[0],
                           start[1],
                           start[2],
                           pixel_shader.main(start).hex()))
        pixel_info.append((end[0],
                           end[1],
                           end[2],
                           pixel_shader.main(end).hex()))

        profiler.Profiler.end()

        return pixel_info

    @staticmethod
    def _scan_line_pixel_shading_job(start, end, properties_gradient, pixel_shader, pixels):
        y = start['pos'].y
        start_x = start['pos'].x
        end_x = end['pos'].x

        for index, pos in enumerate(range(start_x + 1, end_x)):
            Triangle._pixel_shading_job(start, properties_gradient, index, pos, y, pixel_shader, pixels)

    @staticmethod
    def _pixel_shading_job(start, properties_gradient, index, x, y, pixel_shader, pixels):
        profiler.Profiler.begin('pixel_stage.pixel_shading.scan_x.interpolation')
        pixel_properties = {}
        #        ru.linear_interpolation(index, start, properties_gradient, pixel_properties)
        for i, v in start.items():
            gx, _ = properties_gradient[i]
            pixel_properties[i] = v + gx * index

        profiler.Profiler.end()

        pixel_properties['pos'].x = x
        pixel_properties['pos'].y = y

        color = pixel_shader.main(pixel_properties)

        profiler.Profiler.begin('pixel_stage.pixel_shading.scan_x.append')
        pixels.append((pixel_properties['pos'], color))
        profiler.Profiler.end()

    @staticmethod
    def _linear_interpolation(vp1, vp2, t):
        vertex_properties = {}
        for i, v in vp1.items():
            vp2_value = vp2[i]
            vertex_properties[i] = v * (1 - t) + vp2_value * t

        return vertex_properties


class Line2d:

    def __init__(self, *args):
        args_len = len(args)
        if args_len == 2:
            start = args[0]
            end = args[1]
        elif args_len == 4:
            start = Vector2(args[0], args[1])
            end = Vector2(args[2], args[3])
        else:
            raise AttributeError

        self.start = start
        self.end = end

    def __str__(self):
        return 'Line2d(start (%.5f, %.5f), end (%.5f, %.5f))' \
               % (self.start.x, self.start.y, self.end.x, self.end.y)


class Triangle2d:

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
        return 'Triangle2d(' \
               'v1(p: %.5f, %.5f | c: %.5f, %.5f, %.5f, %.5f), ' \
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

    def get_sorted_vector_by_y(self):
        ret = [(self.v1, self.c1), (self.v2, self.c2), (self.v3, self.c3)]
        return sorted(ret, iey=lambda x: x[0].y)

    @property
    def v1(self):
        return self._v1

    @v1.setter
    def v1(self, v1):
        if not isinstance(v1, Vector3):
            raise TypeError

        self._v1 = v1

    @property
    def v2(self):
        return self._v2

    @v2.setter
    def v2(self, v2):
        if not isinstance(v2, Vector3):
            raise TypeError

        self._v2 = v2

    @property
    def v3(self):
        return self._v3

    @v3.setter
    def v3(self, v3):
        if not isinstance(v3, Vector3):
            raise TypeError

        self._v3 = v3

    @property
    def c1(self):
        return self._c1

    @c1.setter
    def c1(self, c1):
        if not isinstance(c1, Color):
            raise TypeError

        self._c1 = c1

    @property
    def c2(self):
        return self._c2

    @c2.setter
    def c2(self, c2):
        if not isinstance(c2, Color):
            raise TypeError

        self._c2 = c2

    @property
    def c3(self):
        return self._c3

    @c3.setter
    def c3(self, c3):
        if not isinstance(c3, Color):
            raise TypeError

        self._c3 = c3
