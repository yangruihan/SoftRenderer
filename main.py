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

def draw_func():
    glClearColor(1, 1, 1, 0)
    glClear(GL_COLOR_BUFFER_BIT)

    rc.clear_pixels()

    draw_line(rc, 0, 0, 399, 399, Color.Red())
    draw_line(rc, 0, 399, 399, 0, Color.Blue())

    glDrawPixels(WIDTH, HEIGHT, GL_RGBA, GL_UNSIGNED_INT_8_8_8_8, ascontiguousarray(rc.pixels().transpose()).data)
    glFlush()
 
glutInit()
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGBA)
glutInitWindowSize(400, 400)
glutCreateWindow("Test")
glutDisplayFunc(draw_func)
glutMainLoop()
