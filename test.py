#!/usr/bin/env python3

import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from numpy import *

WIDTH = 400
HEIGHT = 400

class RendererContext():
    
    def __init__(self, w, h):
        self.__width = w
        self.__height = h
        self.__pixels = zeros((WIDTH, HEIGHT), dtype=uint32)

    def clear_pixels(self):
        self.__pixels.fill(0)

    def set_pixels(self, new_pixels):
        self.__pixels = new_pixels

    def set_pixel(self, x, y, color):
        self.__pixels[x, y] = color

    def width(self):
        return self.__width

    def height(self):
        return self.__height

    def pixels(self):
        return self.__pixels


rc = RendererContext(WIDTH, HEIGHT)

def rgb2Hex(r, g, b, a):
    return int('%02x%02x%02x%02x' % (r, g, b, a), 16)
 
def drawFunc():
    glClearColor(1, 1, 1, 0)
    glClear(GL_COLOR_BUFFER_BIT)

    rc.clear_pixels()

    for i in range(50, 100):
        for j in range(50, 100):
            rc.set_pixel(i, j, rgb2Hex(255, 0, 0, 255))
    
    glDrawPixels(WIDTH, HEIGHT, GL_RGBA, GL_UNSIGNED_INT_8_8_8_8, ascontiguousarray(rc.pixels().transpose()).data)
    glFlush()
 
glutInit()
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGBA)
glutInitWindowSize(400, 400)
glutCreateWindow("Test")
glutDisplayFunc(drawFunc)
glutMainLoop()
