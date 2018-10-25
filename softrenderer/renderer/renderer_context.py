# -*- coding:utf-8 -*-


import logging

from numpy import *

from softrenderer.common.math.vector import Vector2, Vector3
from softrenderer.common.primitive import Line2d, Triangle2d
from softrenderer.renderer import renderer as rd
from softrenderer.renderer.shader import VertexShader, PixelShader


class RendererContext:
    E_LEFT = 1
    E_TOP = 1 << 1
    E_RIGHT = 1 << 2
    E_BOTTOM = 1 << 3
    E_IN = 0

    def __init__(self, w, h):
        self._width = w
        self._height = h
        self._color_buffer = zeros((w + 1, h + 1), dtype=uint32)
        self._vertex_shader = None
        self._pixel_shader = None

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

        vertex_data_list = renderer.draw()

        # geometry stage
        vertex_data_list = self._geometry_stage(vertex_data_list)

        # rasterizer stage
        self._rasterizer_stage(vertex_data_list)

    def _geometry_stage(self, vertex_data_list):
        ret = []

        # vertex shading
        for vertex_data in vertex_data_list:
            ret.append(self._vertex_shader.main(vertex_data))

        # clipping
        ...

        # screen mapping
        for i in range(len(ret)):
            ndc = ret[i]['position']
            screen_pos = Vector3((ndc.x + 1) * self.width / 2,
                                 (ndc.y + 1) * self.height / 2,
                                 ndc.z)
            ret[i]['position'] = screen_pos

        return ret

    def _rasterizer_stage(self, vertex_data_list):
        pass

    def _clear_color_buffer(self):
        self._color_buffer.fill(0)

    def _set_pixels(self, new_pixels):
        self._color_buffer = new_pixels

    def _set_pixel(self, x, y, color):
        self._color_buffer[x, y] = color.hex()

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
            return True, Line2d(x1, y1, x2, y2)
        else:
            return False, None

    def draw_triangle(self, triangle):
        if not isinstance(triangle, Triangle2d):
            raise TypeError

        (v1, c1), (v2, c2), (v3, c3) = triangle.get_sorted_vector_by_y()
        v1.rasterization()
        v2.rasterization()
        v3.rasterization()

        if v2.y == v3.y:
            self._fill_top_flat_triangle(Triangle2d(v1, v2, v3, c1, c2, c3))
        elif v2.y == v1.y:
            self._fill_bottom_flat_triangle(Triangle2d(v3, v1, v2, c3, c1, c2))
        else:
            v4 = Vector2(int(v1.x + (v2.y - v1.y) * (v3.x - v1.x) / (v3.y - v1.y)), v2.y)
            v4.rasterization()
            c4 = triangle.get_pixel_color(v4)

            self._fill_top_flat_triangle(Triangle2d(v1, v2, v4, c1, c2, c4))
            self._fill_bottom_flat_triangle(Triangle2d(v3, v2, v4, c3, c2, c4))

    def _fill_bottom_flat_triangle(self, triangle):
        if not isinstance(triangle, Triangle2d):
            raise TypeError

        inv_slope1 = (triangle.v2.x - triangle.v1.x) / (triangle.v2.y - triangle.v1.y)
        inv_slope2 = (triangle.v3.x - triangle.v1.x) / (triangle.v3.y - triangle.v1.y)

        cx1, cx2 = triangle.v1.x, triangle.v1.x
        rate_span = 1 / (triangle.v1.y - triangle.v3.y)
        t = 0

        for y in range(triangle.v1.y, triangle.v2.y - 1, -1):
            # x1, x2 = int(cx1), int(cx2)
            # c1, c2 = triangle.get_pixel_color(Vector2(x1, y)), triangle.get_pixel_color(Vector2(x2, y))
            temp_c = triangle.c1 * (1 - t)
            c1, c2 = temp_c + triangle.c2 * t, temp_c + triangle.c3 * t
            self.draw_line(Line2d(int(cx1), y, int(cx2), y), c1, c2)
            cx1 -= inv_slope1
            cx2 -= inv_slope2
            t += rate_span

    def _fill_top_flat_triangle(self, triangle):
        if not isinstance(triangle, Triangle2d):
            raise TypeError

        inv_slope1 = (triangle.v2.x - triangle.v1.x) / (triangle.v2.y - triangle.v1.y)
        inv_slope2 = (triangle.v3.x - triangle.v1.x) / (triangle.v3.y - triangle.v1.y)

        cx1, cx2 = triangle.v1.x, triangle.v1.x
        rate_span = 1 / (triangle.v3.y - triangle.v1.y)
        t = 0

        for y in range(triangle.v1.y, triangle.v2.y + 1):
            # x1, x2 = int(cx1), int(cx2)
            # c1, c2 = triangle.get_pixel_color(Vector2(x1, y)), triangle.get_pixel_color(Vector2(x2, y))
            temp_c = triangle.c1 * (1 - t)
            c1, c2 = temp_c + triangle.c2 * t, temp_c + triangle.c3 * t
            self.draw_line(Line2d(int(cx1), y, int(cx2), y), c1, c2)
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
        return self._color_buffer
