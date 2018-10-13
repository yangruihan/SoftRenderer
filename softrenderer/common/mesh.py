# -*- coding:utf-8 -*-


class Mesh:

    def __init__(self, *args):
        args_len = len(args)
        if args_len == 2:
            if not isinstance(args[0], list) or not isinstance(args[1], list):
                raise TypeError

            self._vertex_list = args[0]
            self._index_list = args[1]
        else:
            raise AttributeError

    def __str__(self):
        return 'Mesh(Vertex(%s), Index(%s))' % (self._vertex_list, self._index_list)

    @property
    def vertex_list(self):
        return self._vertex_list

    @vertex_list.setter
    def vertex_list(self, value):
        if not isinstance(value, list):
            raise TypeError

        self._vertex_list = value

    @property
    def index_list(self):
        return self._index_list

    @index_list.setter
    def index_list(self, value):
        if not isinstance(value, list):
            raise TypeError

        self._index_list = value
