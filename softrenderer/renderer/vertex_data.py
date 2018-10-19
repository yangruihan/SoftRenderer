# -*- coding:utf-8 -*-


class VertexData:

    def __init__(self, vertex_buffer=None, index_buffer=None, **kwargs):
        if vertex_buffer is None:
            vertex_buffer = []

        if index_buffer is None:
            index_buffer = []

        self.data = kwargs
        self.data = {'vertex_buffer': vertex_buffer,
                     'index_buffer': index_buffer}

    def __setitem__(self, key, value):
        pass

    def __getitem__(self, item):
        pass
