# -*- coding:utf-8 -*-


from softrenderer.render import render_context as rc


class VertexArray:
    """Array for all vertex data
    """

    def __init__(self, vertex_buffer, layout_buffer, index_buffer):
        self._vertex_buffer = vertex_buffer
        self._layout_buffer = layout_buffer
        self._index_buffer = index_buffer

        self._renderer_id = rc.RenderContext.gen_vertex_array(1)
        self.bind()
        self._vertex_buffer_id, self._index_buffer_id = rc.RenderContext.gen_buffers(2)
        rc.RenderContext.bind_buffer(rc.RenderContext.BufferType.ARRAY_BUFFER, self._vertex_buffer_id)
        rc.RenderContext.buffer_data(rc.RenderContext.BufferType.ARRAY_BUFFER, vertex_buffer)
        rc.RenderContext.bind_buffer(rc.RenderContext.BufferType.ELEMENT_ARRAY_BUFFER, self._index_buffer_id)
        rc.RenderContext.buffer_data(rc.RenderContext.BufferType.ELEMENT_ARRAY_BUFFER, index_buffer)
        rc.RenderContext.bind_array_buffer_layout(layout_buffer)

        self.un_bind()

    def bind(self):
        rc.RenderContext.bind_vertex_array(self._renderer_id)

    def un_bind(self):
        rc.RenderContext.bind_vertex_array(0)

    def delete(self):
        rc.RenderContext.delete_buffers(self._vertex_buffer_id, self._index_buffer_id)
        rc.RenderContext.delete_vertex_array(self._vertex_buffer_id)
        rc.RenderContext.delete_array_buffer_layout()

    @property
    def vertex_buffer(self):
        return self._vertex_buffer

    @vertex_buffer.setter
    def vertex_buffer(self, vertex_buffer):
        if not isinstance(vertex_buffer, dict):
            raise TypeError

        if 'pos' not in vertex_buffer:
            raise AttributeError

        self._vertex_buffer = vertex_buffer

    @property
    def index_buffer(self):
        return self._index_buffer

    @index_buffer.setter
    def index_buffer(self, index_buffer):
        if not isinstance(index_buffer, list):
            raise TypeError

        self._index_buffer = index_buffer

    @property
    def layout_buffer(self):
        return self._layout_buffer

    @layout_buffer.setter
    def layout_buffer(self, layout_buffer):
        if not isinstance(layout_buffer, list):
            raise TypeError

        self._layout_buffer = layout_buffer
