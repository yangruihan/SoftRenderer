# -*- coding:utf-8 -*-


from softrenderer.render.renderer import Renderer
from softrenderer.render import render_context as rc
from softrenderer.render.vertex_array import VertexArray


class TriangleRenderer(Renderer):

    def __init__(self, v1, v2, v3, c1, c2, c3):
        self._v1 = v1
        self._v2 = v2
        self._v3 = v3
        self._c1 = c1
        self._c2 = c2
        self._c3 = c3

        self._nv1 = v1
        self._nv2 = v2
        self._nv3 = v3

        self._tf = None

        self._vertex_buffer = [
            self._nv1.x, self._nv1.y, self._nv1.z, self._nv1.w, self._c1.r, self._c1.g, self._c1.b, self._c1.a,
            self._nv2.x, self._nv2.y, self._nv2.z, self._nv2.w, self._c2.r, self._c2.g, self._c2.b, self._c2.a,
            self._nv3.x, self._nv3.y, self._nv3.z, self._nv3.w, self._c3.r, self._c3.g, self._c3.b, self._c3.a,
        ]
        self._layout_buffer = [4, 4]  # x, y, z, w, r, g, b, a
        self._index_buffer = [0, 1, 2]
        self._vertex_array = VertexArray(self._vertex_buffer, self._layout_buffer, self._index_buffer)

    def set_tf(self, tf):
        self._tf = tf
        world_mat = tf.get_local_to_world_matrix()
        self._nv1, self._nv2, self._nv3 = (world_mat * self._v1,
                                           world_mat * self._v2,
                                           world_mat * self._v3)

    def draw(self, render_context):
        if self._tf.is_dirty:
            world_mat = self._tf.get_local_to_world_matrix()
            self._nv1, self._nv2, self._nv3 = (world_mat * self._v1,
                                               world_mat * self._v2,
                                               world_mat * self._v3)
        self._vertex_buffer = [
            self._nv1.x, self._nv1.y, self._nv1.z, self._nv1.w, self._c1.r, self._c1.g, self._c1.b, self._c1.a,
            self._nv2.x, self._nv2.y, self._nv2.z, self._nv2.w, self._c2.r, self._c2.g, self._c2.b, self._c2.a,
            self._nv3.x, self._nv3.y, self._nv3.z, self._nv3.w, self._c3.r, self._c3.g, self._c3.b, self._c3.a,
        ]

        rc.RenderContext.buffer_data(rc.RenderContext.BufferType.ARRAY_BUFFER, self._vertex_buffer)

        self._vertex_array.bind()
        render_context.draw()
        self._vertex_array.un_bind()
