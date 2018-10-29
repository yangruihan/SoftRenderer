#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import logging
import time
import platform as pl

from OpenGL.GL import *
from OpenGL.GLUT import *
from numpy import *

from softrenderer.common.math.vector import Vector2, Vector3
from softrenderer.common.primitive import Line2d
from softrenderer.common.transform import Transform
from softrenderer.common.types import Color
from softrenderer.debug.profiler import Profiler
from softrenderer.render.render_context import RenderContext
from softrenderer.render.triangle_renderer import TriangleRenderer

WIDTH = 400
HEIGHT = 400

RC = RenderContext(WIDTH, HEIGHT)

PRE_FRAME_TIME = 0
TIMER = 0

TR = TriangleRenderer(Vector3(0, 0.5, 0),
                      Vector3(-0.5, -0.5, 0),
                      Vector3(0.5, -0.5, 0),
                      Color.blue(),
                      Color.green(),
                      Color.red())

TF = Transform()
TF.translate(Vector3(0, 0, 0))
TF.scale = Vector3(1, 1, 1)

TR.set_tf(TF)

RUNNING = False


def on_glut_main_loop():
    global PRE_FRAME_TIME

    Profiler.before_update()

    now_time = time.time()
    delta_time = now_time - PRE_FRAME_TIME
    PRE_FRAME_TIME = now_time

    render(delta_time)

    Profiler.after_update()


def on_glut_close():
    global RUNNING
    RUNNING = False


def render(delta_time):
    global TIMER, TR, TF, RC

    # gl clear
    glClearColor(1, 1, 1, 0)
    glClear(GL_COLOR_BUFFER_BIT)

    RC.clear()

    RC.draw_line(Line2d(Vector2(0, 200), Vector2(400, 200)),
                 Color.red(), Color.red())
    RC.draw_line(Line2d(Vector2(200, 0), Vector2(200, 400)),
                 Color.green(), Color.green())

    TIMER += delta_time

    #    TF.rotate_axis(Vector3.up(), 10)

    RC.draw(TR)

    # gl flush
    glDrawPixels(WIDTH + 1, HEIGHT + 1, GL_RGBA, GL_UNSIGNED_INT_8_8_8_8,
                 ascontiguousarray(RC.color_buffer.transpose()).data)
    glFlush()


def main():
    global PRE_FRAME_TIME, RUNNING

    # init logging
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    # init profiler
    Profiler.config(Profiler.ENABLE)

    # init glut
    glutInit()
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGBA)
    glutInitWindowSize(400, 400)
    glutCreateWindow("Real-Time Software Rendering")
    glutDisplayFunc(on_glut_main_loop)
    glutIdleFunc(on_glut_main_loop)

    if 'Darwin' not in pl.platform():
        glutCloseFunc(on_glut_close)

    RUNNING = True

    # record start time
    PRE_FRAME_TIME = time.time()

    # start glut main loop
    glutMainLoop()


if __name__ == '__main__':
    main()
