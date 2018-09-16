#!/usr/bin/env python3

import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from numpy import *

from common_types import *
from common_utils import *

WIDTH = 400
HEIGHT = 400

rc = RendererContext(WIDTH, HEIGHT)

def drawFunc():
    glClearColor(1, 1, 1, 0)
    glClear(GL_COLOR_BUFFER_BIT)

    rc.clear_pixels()

    for i in range(0, 200):
        for j in range(0, 200):
            rc.set_pixel(i, j, Color.Red())

    for i in range(200, 400):
        for j in range(0, 200):
            rc.set_pixel(i, j, Color.Green())

    for i in range(0, 200):
        for j in range(200, 400):
            rc.set_pixel(i, j, Color.Blue())

    for i in range(200, 400):
        for j in range(200, 400):
            rc.set_pixel(i, j, Color.White())

    glDrawPixels(WIDTH, HEIGHT, GL_RGBA, GL_UNSIGNED_INT_8_8_8_8, ascontiguousarray(rc.pixels().transpose()).data)
    glFlush()
 
glutInit()
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGBA)
glutInitWindowSize(400, 400)
glutCreateWindow("Test")
glutDisplayFunc(drawFunc)
glutMainLoop()
