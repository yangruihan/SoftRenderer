#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from OpenGL.GL import *
from OpenGL.GLUT import *
from numpy import *

import logging
import time

from softrenderer.renderer.renderer_context import RendererContext
from softrenderer.common.types import Color
from softrenderer.common.primitive import Triangle2d
from softrenderer.common.transform import Transform
from softrenderer.common.math.vector import Vector2, Vector3

WIDTH = 400
HEIGHT = 400

rc = RendererContext(WIDTH, HEIGHT)

pre_frame_time = 0


def draw_func():
    global pre_frame_time

    now_time = time.time()
    time_span = now_time - pre_frame_time
    logging.info("Time span %f, fps %f", time_span, 1 / time_span)
    pre_frame_time = now_time

    glClearColor(1, 1, 1, 0)
    glClear(GL_COLOR_BUFFER_BIT)

    rc.clear()

    # draw_line(rc, Line2d(0, 0, 600, 600), Color.Red())
    # draw_line(rc, Line2d(0, 400, 400, 0), Color.Blue())
    # draw_line(rc, Line2d(0, 200, 400, 200), Color.Green())
    # draw_line(rc, Line2d(200, 0, 200, 400), Color.White())
    #
    # draw_line(rc, Line2d(800, 800, 900, 600), Color.White())
    # draw_line(rc, Line2d(300, 200, 500, 800), Color(255, 255, 0, 255))

    # draw_triangle(rc, Triangle2d(Vector2(200, 100),
    #                              Vector2(100, 300),
    #                              Vector2(300, 300),
    #                              Color.red(),
    #                              Color.green(),
    #                              Color.blue()))

    v1, v2, v3 = Vector3(0, 100, 0), Vector3(-100, -100, 0), Vector3(100, -100, 0)
    tf = Transform()
    tf.translate(Vector3(200, 200, 0))
    tf.rotate_axis(Vector3.forward(), 45)
    tf.scale = Vector3(0.5, 0.5, 1)
    world_mat = tf.get_local_to_world_matrix()
    v1, v2, v3 = world_mat * v1, world_mat * v2, world_mat * v3

    rc.draw_triangle(Triangle2d(Vector2(v1.x, v1.y),
                                Vector2(v2.x, v2.y),
                                Vector2(v3.x, v3.y),
                                Color.red(),
                                Color.green(),
                                Color.blue()))

    glDrawPixels(WIDTH + 1, HEIGHT + 1, GL_RGBA, GL_UNSIGNED_INT_8_8_8_8,
                 ascontiguousarray(rc.color_buffer.transpose()).data)
    glFlush()


def main():
    global pre_frame_time

    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    pre_frame_time = time.time()

    glutInit()
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGBA)
    glutInitWindowSize(400, 400)
    glutCreateWindow("Test")
    glutDisplayFunc(draw_func)
    glutIdleFunc(draw_func)
    glutMainLoop()


if __name__ == '__main__':
    main()
