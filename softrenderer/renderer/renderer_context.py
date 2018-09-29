# -*- coding:utf-8 -*-


from numpy import *


class RendererContext:

    def __init__(self, w, h):
        self._width = w
        self._height = h
        self._pixels = zeros((w + 1, h + 1), dtype=uint32)

    def clear_pixels(self):
        self._pixels.fill(0)

    def set_pixels(self, new_pixels):
        self._pixels = new_pixels

    def set_pixel(self, x, y, color):
        self._pixels[x, y] = color.hex()

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def pixels(self):
        return self._pixels
