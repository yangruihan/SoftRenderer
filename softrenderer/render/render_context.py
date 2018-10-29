# -*- coding:utf-8 -*-


import logging
from enum import Enum

from numpy import *

from softrenderer.common import primitive as pr
from softrenderer.common.exceptions import IndexBufferCountError
from softrenderer.common.math.vector import Vector2
from softrenderer.cython import render_utils as ru
from softrenderer.debug import profiler
from softrenderer.render import renderer as rd
from softrenderer.render.shader import VertexShader, PixelShader
from softrenderer.render.shader import _DefaultPixelShader
from softrenderer.render.shader import _DefaultVertexShader


class RenderContext:
    E_LEFT = 1
    E_TOP = 1 << 1
    E_RIGHT = 1 << 2
    E_BOTTOM = 1 << 3
    E_IN = 0

    _Width = 0
    _Height = 0

    class BufferType(Enum):
        ARRAY_BUFFER = 1
        ELEMENT_ARRAY_BUFFER = 2

    _instance = None

    def __init__(self):
        self._color_buffer = None

        # shader
        self._vertex_shader = _DefaultVertexShader()
        self._pixel_shader = _DefaultPixelShader()

        # init vertex array buffer
        self._vertex_array = {}
        self._vertex_array_id_set = [_ for _ in range(1, 257)]
        self._current_bind_vertex_array_id = -1

        # init buffer
        self._buffers = {}
        self._bind_buffer_id_map = {}
        self._buffers_id_set = [_ for _ in range(1, 257)]

        # array buffer layout
        self._array_buffer_layout = None

        self._vertex_count = 0
        self._each_vertex_properties_count = 0

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = RenderContext()
        return cls._instance

    @classmethod
    def set_screen_size(cls, width, height):
        RenderContext._Width = width
        RenderContext._Height = height

        cls.instance()._color_buffer = zeros((width + 1, height + 1), dtype=uint32)
        cls.instance()._color_buffer2 = zeros((width + 1, height + 1), dtype=uint32)

    @classmethod
    def gen_buffers(cls, count):
        if count <= 0:
            raise AttributeError('count cannot be zero')
        else:
            if count > len(cls.instance()._buffers_id_set):
                raise AttributeError('no enough buffers')

            if count == 1:
                return cls.instance()._buffers_id_set.pop()
            else:
                return [cls.instance()._buffers_id_set.pop() for _ in range(count)]

    @classmethod
    def delete_buffers(cls, *args):
        if len(args) == 0:
            raise AttributeError('id list cannot be empty')

        for buffer_id in args:
            if buffer_id in cls.instance()._buffers:
                del cls.instance()._buffers[buffer_id]
                cls.instance()._buffers_id_set.append(buffer_id)

    @classmethod
    def bind_buffer(cls, buffer_type, buffer_id):
        if buffer_id < 0:
            raise AttributeError('id invalid')

        # set current bind buffer id
        if not isinstance(buffer_type, RenderContext.BufferType):
            raise TypeError

        cls.instance()._bind_buffer_id_map[buffer_type] = buffer_id

        # bind buffer for vertex array
        if cls.instance()._current_bind_vertex_array_id >= 0:
            if cls.instance()._current_bind_vertex_array_id not in cls.instance()._vertex_array:
                cls.instance()._vertex_array[cls.instance()._current_bind_vertex_array_id] = {buffer_type: buffer_id}
            else:
                cls.instance()._vertex_array[cls.instance()._current_bind_vertex_array_id][buffer_type] = buffer_id

    @classmethod
    def buffer_data(cls, buffer_type, data):
        if not isinstance(buffer_type, RenderContext.BufferType):
            raise TypeError

        cls.instance()._buffers[buffer_type] = data

    @classmethod
    def gen_vertex_array(cls, count):
        if count <= 0:
            raise AttributeError('count cannot be zero')
        else:
            if count > len(cls.instance()._vertex_array_id_set):
                raise AttributeError('no enough buffers')

            if count == 1:
                return cls.instance()._vertex_array_id_set.pop()
            else:
                return [cls.instance()._vertex_array_id_set.pop() for _ in range(count)]

    @classmethod
    def delete_vertex_array(cls, *args):
        if len(args) == 0:
            raise AttributeError('id list cannot be empty')

        for vertex_array_id in args:
            if vertex_array_id in cls.instance()._vertex_array:
                del cls.instance()._vertex_array[vertex_array_id]
                cls.instance()._vertex_array_id_set.append(vertex_array_id)

    @classmethod
    def bind_vertex_array(cls, vertex_array_id):
        if vertex_array_id < 0:
            raise AttributeError('id invalid')

        cls._current_bind_vertex_array_id = vertex_array_id

    @classmethod
    def bind_array_buffer_layout(cls, layout):
        cls.instance()._array_buffer_layout = layout

    @classmethod
    def delete_array_buffer_layout(cls):
        cls.instance()._array_buffer_layout = None

    @classmethod
    def clear(cls):
        cls.instance()._clear_color_buffer()

    @classmethod
    def bind_vertex_shader(cls, shader=None):
        if shader is not None and not isinstance(shader, VertexShader):
            raise TypeError

        cls.instance()._vertex_shader = shader

    @classmethod
    def bind_pixel_shader(cls, shader=None):
        if shader is not None and not isinstance(shader, PixelShader):
            raise TypeError

        cls.instance()._pixel_shader = shader

    @classmethod
    def draw(cls, *args):
        cls.instance()._draw(*args)

    @classmethod
    def draw_pixel(cls, x, y, color):
        cls.instance()._draw_pixel(x, y, color)

    @classmethod
    def draw_line(cls, line, start_color, end_color):
        cls.instance()._draw_line(line, start_color, end_color)

    @classmethod
    def draw_triangle(cls, triangle):
        cls.instance()._draw_triangle(triangle)

    @classmethod
    def color_buffer(cls):
        return cls.instance()._get_color_buffer()

    @property
    def vertex_count(self):
        return self._vertex_count

    @property
    def each_vertex_properties_count(self):
        return self._each_vertex_properties_count

    def _get_color_buffer(self):
        return self._color_buffer

    def _draw(self, *args):
        argv_len = len(args)
        if argv_len == 1:
            if isinstance(args[0], rd.Renderer):
                renderer = args[0]
                renderer.draw(self)
            else:
                raise TypeError
        elif argv_len == 0:
            if self._vertex_shader is None:
                logging.error("[Render Error] vertex_shader is None")
                return

            if self._pixel_shader is None:
                logging.error("[Render Error] fragment_shader is None")
                return

            # geometry stage
            profiler.Profiler.begin("geometry_stage")
            array_buffer = self._geometry_stage()
            profiler.Profiler.end()

            # rasterizer stage
            profiler.Profiler.begin("pixel_stage")
            self._rasterizer_stage(array_buffer)
            profiler.Profiler.end()
        else:
            raise TypeError('takes 0 or 1 positional argument but %d were given' % argv_len)

    def _draw_pixel(self, x, y, color):
        if color.is_valid():
            self._set_pixel(x, y, color)

    def _draw_line(self, line, color1, color2):
        logging.debug('[Log]Draw Line Call: (line: %s, color1: %s, color2: %s)' % (line,
                                                                                   color1,
                                                                                   color2))

        (ret, line) = self._cohen_sutherland_line_clip(line, Vector2.zero(),
                                                       Vector2(RenderContext._Width, RenderContext._Height))

        if not ret:
            logging.debug('[Log]Line was aborted')
            return
        else:
            logging.debug('[Log]Will draw line %s' % line)

        (x1, y1) = (line.start.x, line.start.y)
        (x2, y2) = (line.end.x, line.end.y)

        # draw a pixel
        if x1 == x2 and y1 == y2:
            self._draw_pixel(x1, y1, color1)
        # draw a vertical line
        elif x1 == x2:
            inc = 1 if y1 <= y2 else -1
            t = 0 if y1 <= y2 else 1
            t_span = 1 / (y2 - y1) * inc
            for y in range(y1, y2 + inc, inc):
                if color1 == color2:
                    color = color1
                else:
                    color = color1 * (1 - t) + color2 * t
                self._draw_pixel(x1, y, color)
                t += t_span

        # draw a horizontal line
        elif y1 == y2:
            inc = 1 if x1 <= x2 else -1
            t = 0 if x1 <= x2 else 1
            t_span = 1 / (x2 - x1) * inc
            for x in range(x1, x2 + inc, inc):
                if color1 == color2:
                    color = color1
                else:
                    color = color1 * (1 - t) + color2 * t
                self._draw_pixel(x, y1, color)
                t += t_span
        else:
            dx = x2 - x1 if x1 < x2 else x1 - x2
            dy = y2 - y1 if y1 < y2 else y1 - y2

            if dx >= dy:
                if x2 < x1:
                    x1, x2 = x2, x1
                    y1, y2 = y2, y1

                y = y1
                rem = 0
                t = 0
                t_span = 1 / (x2 - x1)
                for x in range(x1, x2 + 1):
                    if color1 == color2:
                        color = color1
                    else:
                        color = color1 * (1 - t) + color2 * t
                    self._draw_pixel(x, y, color)
                    t += t_span
                    rem += dy
                    if rem >= dx:
                        rem -= dx
                        y += 1 if y2 >= y1 else -1
                self._draw_pixel(x2, y2, color2)
            else:
                if y2 < y1:
                    x1, x2 = x2, x1
                    y1, y2 = y2, y1

                x = x1
                rem = 0
                t = 0
                t_span = 1 / (y2 - y1)
                for y in range(y1, y2 + 1):
                    if color1 == color2:
                        color = color1
                    else:
                        color = color1 * (1 - t) + color2 * t
                    self._draw_pixel(x, y, color)
                    t += t_span
                    rem += dx
                    if rem >= dy:
                        rem -= dy
                        x += 1 if x2 >= x1 else -1
                self._draw_pixel(x2, y2, color2)

    def _draw_triangle(self, triangle):
        if not isinstance(triangle, pr.Triangle2d):
            raise TypeError

        (v1, c1), (v2, c2), (v3, c3) = triangle.get_sorted_vector_by_y()
        v1.rasterization()
        v2.rasterization()
        v3.rasterization()

        if v2.y == v3.y:
            self._fill_top_flat_triangle(pr.Triangle2d(v1, v2, v3, c1, c2, c3))
        elif v2.y == v1.y:
            self._fill_bottom_flat_triangle(
                pr.Triangle2d(v3, v1, v2, c3, c1, c2))
        else:
            v4 = Vector2(int(v1.x + (v2.y - v1.y) *
                             (v3.x - v1.x) / (v3.y - v1.y)), v2.y)
            v4.rasterization()
            b1, b2, b3 = pr.Triangle2d(
                v1, v2, v3, c1, c2, c3).get_barycentrix(v4)
            c4 = c1 * b1 + c2 * b2 + c3 * b3

            self._fill_top_flat_triangle(pr.Triangle2d(v1, v2, v4, c1, c2, c4))
            self._fill_bottom_flat_triangle(
                pr.Triangle2d(v3, v2, v4, c3, c2, c4))

    def _geometry_stage(self):
        """Geometry stage for rendering pipeline
        """
        ret = []

        array_buffer = self._buffers[RenderContext.BufferType.ARRAY_BUFFER]

        # vertex shading
        self._each_vertex_properties_count = sum(self._array_buffer_layout)
        self._vertex_count = int(len(array_buffer) / self._each_vertex_properties_count)

        for i in range(self._vertex_count):
            start_pos = i * self._each_vertex_properties_count
            ret += self._vertex_shader.main(array_buffer[start_pos: start_pos + self._each_vertex_properties_count])

        # clipping
        ...

        # screen mapping
        half_width = RenderContext._Width * 0.5
        half_height = RenderContext._Height * 0.5
        self._each_vertex_properties_count = int(len(ret) / self._vertex_count)
        for i in range(self._vertex_count):
            start_pos = i * self._each_vertex_properties_count
            inv_ndc_w = 1.0 / ret[start_pos + 3]
            ret[start_pos] = (ret[start_pos] * inv_ndc_w + 1) * half_width
            ret[start_pos + 1] = (ret[start_pos + 1] * inv_ndc_w + 1) * half_height
            ret[start_pos + 2] = (ret[start_pos + 2] * inv_ndc_w)

        return ret

    def _rasterizer_stage(self, array_buffer):
        """Rasterizer stage
        """
        # triangle setup
        profiler.Profiler.begin('pixel_stage.triangle_setup')
        index_buffer = self._buffers[RenderContext.BufferType.ELEMENT_ARRAY_BUFFER]
        if len(index_buffer) % 3 != 0:
            raise IndexBufferCountError

        triangles = []
        for i1, i2, i3 in zip(*[iter(index_buffer)] * 3):
            start_1 = i1 * self._each_vertex_properties_count
            start_2 = i2 * self._each_vertex_properties_count
            start_3 = i3 * self._each_vertex_properties_count
            triangles.append(pr.Triangle(pr.Point(start_1, array_buffer),
                                         pr.Point(start_2, array_buffer),
                                         pr.Point(start_3, array_buffer)))
        profiler.Profiler.end()

        # triangle traversal
        profiler.Profiler.begin('pixel_stage.triangle_traversal')
        for triangle in triangles:
            triangle.rasterize()
        profiler.Profiler.end()

        # pixel shading
        profiler.Profiler.begin('pixel_stage.pixel_shading')
        for triangle in triangles:
            triangle.pixel_shading(self._pixel_shader)
        profiler.Profiler.end()

        # merging
        profiler.Profiler.begin('pixel_stage.merging')
        for triangle in triangles:
            ru.merging(triangle.pixels, self._color_buffer)
        profiler.Profiler.end()

    def _clear_color_buffer(self):
        self._color_buffer.fill(0)

    def _set_pixels(self, new_pixels):
        self._color_buffer = new_pixels

    def _set_pixel(self, x, y, color):
        if x > RenderContext._Width or x < 0 or y > RenderContext._Height or y < 0:
            return

        self._color_buffer[x, y] = color.hex()

    def _cohen_sutherland_line_clip(self, line, min_pos, max_pos):
        def encode(pos, _min_pos, _max_pos):
            _code = self.E_IN

            if pos.x < _min_pos.x:
                _code |= self.E_LEFT
            elif pos.x > _max_pos.x:
                _code |= self.E_RIGHT

            if pos.y < _min_pos.y:
                _code |= self.E_BOTTOM
            elif pos.y > _max_pos.y:
                _code |= self.E_TOP

            return _code

        (x1, y1) = (line.start.x, line.start.y)
        (x2, y2) = (line.end.x, line.end.y)

        code1 = encode(Vector2(x1, y1), min_pos, max_pos)
        code2 = encode(Vector2(x2, y2), min_pos, max_pos)

        accept = False

        while True:
            if code1 | code2 == 0:
                accept = True
                break

            elif code1 & code2 != 0:
                break

            else:
                code = code1 if code1 != 0 else code2
                (x, y) = (0, 0)
                if code & self.E_TOP != 0:
                    x = x1 + (x2 - x1) * (max_pos.y - y1) / (y2 - y1)
                    y = max_pos.y
                elif code & self.E_BOTTOM != 0:
                    x = x1 + (x2 - x1) * (min_pos.y - y1) / (y2 - y1)
                    y = min_pos.y
                elif code & self.E_LEFT != 0:
                    x = min_pos.x
                    y = y1 + (y2 - y1) * (min_pos.x - x1) / (x2 - x1)
                elif code & self.E_RIGHT != 0:
                    x = max_pos.x
                    y = y1 + (y2 - y1) * (max_pos.x - x1) / (x2 - x1)

                if code == code1:
                    (x1, y1) = (int(x), int(y))
                    code1 = encode(Vector2(x1, y1), min_pos, max_pos)
                else:
                    (x2, y2) = (int(x), int(y))
                    code2 = encode(Vector2(x2, y2), min_pos, max_pos)

        if accept:
            return True, pr.Line2d(x1, y1, x2, y2)
        else:
            return False, None

    def _fill_bottom_flat_triangle(self, triangle):
        if not isinstance(triangle, pr.Triangle2d):
            raise TypeError

        inv_slope1 = (triangle.v2.x - triangle.v1.x) / \
                     (triangle.v2.y - triangle.v1.y)
        inv_slope2 = (triangle.v3.x - triangle.v1.x) / \
                     (triangle.v3.y - triangle.v1.y)
        if inv_slope1 < inv_slope2:
            inv_slope1, inv_slope2 = inv_slope2, inv_slope1
            triangle.c2, triangle.c3 = triangle.c3, triangle.c2

        cx1, cx2 = triangle.v1.x, triangle.v1.x
        rate_span = 1 / (triangle.v1.y - triangle.v3.y)
        t = 0

        for y in range(triangle.v1.y, triangle.v2.y - 1, -1):
            # x1, x2 = int(cx1), int(cx2)
            # c1, c2 = triangle.get_pixel_color(Vector2(x1, y)),
            # triangle.get_pixel_color(Vector2(x2, y))
            temp_c = triangle.c1 * (1 - t)
            c1, c2 = temp_c + triangle.c2 * t, temp_c + triangle.c3 * t
            self._draw_line(pr.Line2d(int(cx1), y, int(cx2), y), c1, c2)
            cx1 -= inv_slope1
            cx2 -= inv_slope2
            t += rate_span

    def _fill_top_flat_triangle(self, triangle):
        if not isinstance(triangle, pr.Triangle2d):
            raise TypeError

        inv_slope1 = (triangle.v2.x - triangle.v1.x) / \
                     (triangle.v2.y - triangle.v1.y)
        inv_slope2 = (triangle.v3.x - triangle.v1.x) / \
                     (triangle.v3.y - triangle.v1.y)
        if inv_slope1 > inv_slope2:
            inv_slope1, inv_slope2 = inv_slope2, inv_slope1
            triangle.c2, triangle.c3 = triangle.c3, triangle.c2

        cx1, cx2 = triangle.v1.x, triangle.v1.x
        rate_span = 1 / (triangle.v3.y - triangle.v1.y)
        t = 0

        for y in range(triangle.v1.y, triangle.v2.y + 1):
            # x1, x2 = int(cx1), int(cx2)
            # c1, c2 = triangle.get_pixel_color(Vector2(x1, y)),
            # triangle.get_pixel_color(Vector2(x2, y))
            temp_c = triangle.c1 * (1 - t)
            c1, c2 = temp_c + triangle.c2 * t, temp_c + triangle.c3 * t
            self._draw_line(pr.Line2d(int(cx1), y, int(cx2), y), c1, c2)
            cx1 += inv_slope1
            cx2 += inv_slope2
            t += rate_span
