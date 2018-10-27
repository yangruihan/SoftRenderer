#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from OpenGL.GL import *
from OpenGL.GLUT import *
from numpy import *

import logging
import time

from softrenderer.render.render_context import RenderContext
from softrenderer.render.triangle_renderer import TriangleRenderer
from softrenderer.common.types import Color
from softrenderer.common.primitive import Triangle2d, Line2d
from softrenderer.common.transform import Transform
from softrenderer.common.math.vector import Vector2, Vector3

WIDTH = 400
HEIGHT = 400

rc = RenderContext(WIDTH, HEIGHT)

pre_frame_time = 0
timer = 0

tr = TriangleRenderer(Vector3(0, 0.25, 0),
                      Vector3(-0.25, -0.25, 0),
                      Vector3(0.25, -0.25, 0),
                      Color.red(),
                      Color.green(),
                      Color.blue())


def draw_func():
    global pre_frame_time, timer, tr

    now_time = time.time()
    delta_time = now_time - pre_frame_time
    logging.info("Time span %f, fps %f", delta_time, 1 / delta_time)
    pre_frame_time = now_time

    glClearColor(1, 1, 1, 0)
    glClear(GL_COLOR_BUFFER_BIT)

    rc.clear()

    rc.draw_line(Line2d(Vector2(0, 200), Vector2(400, 200)),
                 Color.red(), Color.red())
    rc.draw_line(Line2d(Vector2(200, 0), Vector2(200, 400)),
                 Color.green(), Color.green())

    timer += delta_time

#    v1, v2, v3 = Vector3(0, 100, 0), Vector3(-100, -
#                                             100, 0), Vector3(100, -100, 0)

    tf = Transform()
    tf.translate(Vector3(0, 0, 0))
    tf.rotate_axis(Vector3.forward(), 45 * timer)
    tf.scale = Vector3(2, 2, 1)
#    world_mat = tf.get_local_to_world_matrix()
#    v1, v2, v3 = world_mat * v1, world_mat * v2, world_mat * v3

#    rc.draw_triangle(Triangle2d(Vector2(v1.x, v1.y),
#                                Vector2(v2.x, v2.y),
#                                Vector2(v3.x, v3.y),
#                                Color.red(),
#                                Color.green(),
#                                Color.blue()))

    tr.tf(tf)

    rc.draw(tr)

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
