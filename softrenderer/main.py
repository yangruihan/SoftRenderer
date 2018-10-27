#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from OpenGL.GL import *
from OpenGL.GLUT import *
from numpy import *

import logging
import time
import threading

from softrenderer.render.render_context import RenderContext
from softrenderer.render.triangle_renderer import TriangleRenderer
from softrenderer.common.types import Color
from softrenderer.common.primitive import Triangle2d, Line2d
from softrenderer.common.transform import Transform
from softrenderer.common.math.vector import Vector2, Vector3

WIDTH = 400
HEIGHT = 400

RC = RenderContext(WIDTH, HEIGHT)

PRE_FRAME_TIME = 0
TIMER = 0

TR = TriangleRenderer(Vector3(0, 0.25, 0),
                      Vector3(-0.25, -0.25, 0),
                      Vector3(0.25, -0.25, 0),
                      Color.red(),
                      Color.green(),
                      Color.blue())

TF = Transform()
TF.translate(Vector3(0, 0, 0))
TF.scale = Vector3(1, 1, 1)

TR.set_tf(TF)

RUNNING = False


def on_glut_draw():
    global RC

    glClearColor(1, 1, 1, 0)
    glClear(GL_COLOR_BUFFER_BIT)

    glDrawPixels(WIDTH + 1, HEIGHT + 1, GL_RGBA, GL_UNSIGNED_INT_8_8_8_8,
                 ascontiguousarray(RC.color_buffer.transpose()).data)
    glFlush()


def on_glut_close():
    global RUNNING
    RUNNING = False


def render_thread_job():
    global PRE_FRAME_TIME, TIMER, TR, TF, RC

    while RUNNING:
        now_time = time.time()
        delta_time = now_time - PRE_FRAME_TIME
        logging.info("Render Thread: Time span %f, fps %f", delta_time, 9999 if delta_time == 0 else 1 / delta_time)
        PRE_FRAME_TIME = now_time

        RC.clear()

        RC.draw_line(Line2d(Vector2(0, 200), Vector2(400, 200)),
                     Color.red(), Color.red())
        RC.draw_line(Line2d(Vector2(200, 0), Vector2(200, 400)),
                     Color.green(), Color.green())

        TIMER += delta_time

        TF.rotate_axis(Vector3.forward(), 10)

        RC.draw(TR)


RENDER_THREAD = threading.Thread(target=render_thread_job, name='render_thread')


def main():
    global PRE_FRAME_TIME, RENDER_THREAD, RUNNING

    # init logging
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    # init glut
    glutInit()
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGBA)
    glutInitWindowSize(400, 400)
    glutCreateWindow("Software Render")
    glutDisplayFunc(on_glut_draw)
    glutIdleFunc(on_glut_draw)
    glutCloseFunc(on_glut_close)

    RUNNING = True

    # record start time
    PRE_FRAME_TIME = time.time()

    # start render thread
    RENDER_THREAD.start()

    # start glut main loop
    glutMainLoop()


if __name__ == '__main__':
    main()
