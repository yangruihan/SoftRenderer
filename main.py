#!/usr/bin/env python3

from OpenGL.GL import *
from OpenGL.GLUT import *

from common_types import *
from common_utils import *

WIDTH = 400
HEIGHT = 400

rc = RendererContext(WIDTH, HEIGHT)


def draw_func():
    glClearColor(1, 1, 1, 0)
    glClear(GL_COLOR_BUFFER_BIT)

    rc.clear_pixels()

    # draw_line(rc, Line2d(0, 0, 600, 600), Color.Red())
    # draw_line(rc, Line2d(0, 400, 400, 0), Color.Blue())
    # draw_line(rc, Line2d(0, 200, 400, 200), Color.Green())
    # draw_line(rc, Line2d(200, 0, 200, 400), Color.White())
    #
    # draw_line(rc, Line2d(800, 800, 900, 600), Color.White())
    # draw_line(rc, Line2d(300, 200, 500, 800), Color(255, 255, 0, 255))

    draw_triangle(rc, Vector2(200, 100), Vector2(100, 300), Vector2(300, 300), Color.blue())
    draw_triangle(rc, Vector2(200, 300), Vector2(100, 100), Vector2(300, 100), Color.red())

    glDrawPixels(WIDTH + 1, HEIGHT + 1, GL_RGBA, GL_UNSIGNED_INT_8_8_8_8, ascontiguousarray(rc.pixels.transpose()).data)
    glFlush()


glutInit()
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGBA)
glutInitWindowSize(400, 400)
glutCreateWindow("Test")
glutDisplayFunc(draw_func)
glutMainLoop()
