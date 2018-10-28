# -*- coding:utf-8 -*-


import logging

from numpy import *

from softrenderer.common.math.vector import Vector2, Vector3
from softrenderer.common import primitive as pr
from softrenderer.render import renderer as rd
from softrenderer.render.shader import VertexShader, PixelShader
from softrenderer.render.shader import _DefaultVertexShader
from softrenderer.render.shader import _DefaultPixelShader

from softrenderer.common.exceptions import IndexBufferCountValid

from softrenderer.cython import render_utils as ru

from softrenderer.debug import profiler


class RenderContext:
    E_LEFT = 1
    E_TOP = 1 << 1
    E_RIGHT = 1 << 2
    E_BOTTOM = 1 << 3
    E_IN = 0

    def __init__(self, w, h):
        self._width = w
        self._height = h
        self._current_use_color_buffer = 0
        self._color_buffer = zeros((w + 1, h + 1), dtype=uint32)
        self._color_buffer2 = zeros((w + 1, h + 1), dtype=uint32)
        self._vertex_shader = _DefaultVertexShader()
        self._pixel_shader = _DefaultPixelShader()

    def clear(self):
        self._clear_color_buffer()

    def bind_vertex_shader(self, shader=None):
        if shader is not None and not isinstance(shader, VertexShader):
            raise TypeError

        self._vertex_shader = shader

    def bind_pixel_shader(self, shader=None):
        if shader is not None and not isinstance(shader, PixelShader):
            raise TypeError

        self._pixel_shader = shader

    def draw(self, renderer):
        if not isinstance(renderer, rd.Renderer):
            raise TypeError

        if self._vertex_shader is None:
            logging.debug("[Render Error] vertex_shader is None")
            return

        if self._pixel_shader is None:
            logging.debug("[Render Error] fragment_shader is None")
            return

        vertex_data = renderer.draw()

        # geometry stage
        profiler.Profiler.begin("geometry_stage")
        vertex_property_list = self._geometry_stage(vertex_data)
        profiler.Profiler.end()

        # rasterizer stage
        profiler.Profiler.begin("pixel_stage")
        self._rasterizer_stage(vertex_property_list, vertex_data.index_buffer)
        profiler.Profiler.end()

        # swap color buffer
        self._current_use_color_buffer = (
            self._current_use_color_buffer + 1) % 2

    def _geometry_stage(self, vertex_data):
        """Geometry stage for rendering pipeline

        Args:
            vertex_data: contains index buffer and vertex properties
                for calculate

        Returns:
            vertex_properties_list: vertex property data through
                vertex shading, clipping and screen mapping

        """
        ret = []

        # vertex shading
        vertex_properties_list = vertex_data.get_vertex_properties_list()

        for vertex_properties in vertex_properties_list:
            vertex_properties['pos'] = self._vertex_shader.main(
                vertex_properties)
            ret.append(vertex_properties)

        # clipping
        ...

        # screen mapping
        half_width = self.width * 0.5
        half_height = self.height * 0.5
        for vertex_property in ret:
            ndc = vertex_property['pos']
            inv_ndc_w = 1 / ndc.w
            screen_pos = Vector3((ndc.x * inv_ndc_w + 1) * half_width,
                                 (ndc.y * inv_ndc_w + 1) * half_height,
                                 ndc.z * inv_ndc_w)

            vertex_property['pos'] = screen_pos

        return ret

    def _rasterizer_stage(self, vertex_properties_list, index_buffer):
        """Rasterizer stage

        Args:
            vertex_properties_list: vertex data for rendering
            index_buffer: index data for vertex

        """
        # triangle setup
        profiler.Profiler.begin('pixel_stage.triangle_setup')
        if len(index_buffer) % 3 != 0:
            raise IndexBufferCountValid

        triangles = []
        for i1, i2, i3 in zip(*[iter(index_buffer)] * 3):
            triangles.append(pr.Triangle(pr.Point(vertex_properties_list[i1]),
                                         pr.Point(vertex_properties_list[i2]),
                                         pr.Point(vertex_properties_list[i3])))
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
        if self._current_use_color_buffer == 0:
            for triangle in triangles:
                ru.merging(triangle.pixels, self._color_buffer)
        else:
            for triangle in triangles:
                ru.merging(triangle.pixels, self._color_buffer2)

#            for pixel in triangle.pixels:
#                pos, color = pixel
#                self._set_pixel(pos.x, pos.y, color)
        profiler.Profiler.end()

    def _clear_color_buffer(self):
        if self._current_use_color_buffer == 0:
            self._color_buffer.fill(0)
        else:
            self._color_buffer2.fill(0)

    def _set_pixels(self, new_pixels):

        if self._current_use_color_buffer == 0:
            self._color_buffer = new_pixels
        else:
            self._color_buffer2 = new_pixels

    def _set_pixel(self, x, y, color):
        if x > self.width or x < 0 or y > self.height or y < 0:
            return

        if self._current_use_color_buffer == 0:
            self._color_buffer[x, y] = color.hex()
        else:
            self._color_buffer2[x, y] = color.hex()

    def draw_pixel(self, x, y, color):
        if color.is_valid():
            self._set_pixel(x, y, color)

    def draw_line(self, line, color1, color2):
        logging.debug('[Log]Draw Line Call: (line: %s, color1: %s, color2: %s)' % (line,
                                                                                   color1,
                                                                                   color2))

        (ret, line) = self._cohen_sutherland_line_clip(line, Vector2.zero(),
                                                       Vector2(self.width, self.height))

        if not ret:
            logging.debug('[Log]Line was aborted')
            return
        else:
            logging.debug('[Log]Will draw line %s' % line)

        (x1, y1) = (line.start.x, line.start.y)
        (x2, y2) = (line.end.x, line.end.y)

        # draw a pixel
        if x1 == x2 and y1 == y2:
            self.draw_pixel(x1, y1, color1)
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
                self.draw_pixel(x1, y, color)
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
                self.draw_pixel(x, y1, color)
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
                    self.draw_pixel(x, y, color)
                    t += t_span
                    rem += dy
                    if rem >= dx:
                        rem -= dx
                        y += 1 if y2 >= y1 else -1
                self.draw_pixel(x2, y2, color2)
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
                    self.draw_pixel(x, y, color)
                    t += t_span
                    rem += dx
                    if rem >= dy:
                        rem -= dy
                        x += 1 if x2 >= x1 else -1
                self.draw_pixel(x2, y2, color2)

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

    def draw_triangle(self, triangle):
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
            self.draw_line(pr.Line2d(int(cx1), y, int(cx2), y), c1, c2)
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
            self.draw_line(pr.Line2d(int(cx1), y, int(cx2), y), c1, c2)
            cx1 += inv_slope1
            cx2 += inv_slope2
            t += rate_span

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def color_buffer(self):
        if self._current_use_color_buffer == 0:
            return self._color_buffer2
        else:
            return self._color_buffer
