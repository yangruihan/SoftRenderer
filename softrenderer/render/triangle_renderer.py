# -*- coding:utf-8 -*-


from softrenderer.render.renderer import Renderer
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

    def set_tf(self, tf):
        self._tf = tf
        world_mat = tf.get_local_to_world_matrix()
        self._nv1, self._nv2, self._nv3 = (world_mat * self._v1,
                                           world_mat * self._v2,
                                           world_mat * self._v3)

    def draw(self):
        if self._tf.is_dirty:
            world_mat = self._tf.get_local_to_world_matrix()
            self._nv1, self._nv2, self._nv3 = (world_mat * self._v1,
                                               world_mat * self._v2,
                                               world_mat * self._v3)

        vertex_buffer = {'pos': [self._nv1, self._nv2, self._nv3], 'color': [self._c1, self._c2, self._c3]}
        index_buffer = [0, 1, 2]

        return VertexArray(vertex_buffer, index_buffer)
