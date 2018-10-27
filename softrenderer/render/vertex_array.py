# -*- coding:utf-8 -*-


class VertexArray:
    """Array for all vertex data
    """

    def __init__(self, vertex_buffer, index_buffer):
        """Init for vertex data

        Args:
            vertex_buffer: a dictionary for vertex data
                such as:
                    {
                        "pos": []
                        "color": []
                        "normal": []
                    }

            index_buffer: a list for vertex index

        Raises:
            TypeError: if vertex_buffer is not a instance of dict or 
                index_buffer is not a instance of list

            AttributeError: if key 'pos' not in vertex_buffer

        """

        if not isinstance(vertex_buffer, dict):
            raise TypeError

        if 'pos' not in vertex_buffer:
            raise AttributeError

        if not isinstance(index_buffer, list):
            raise TypeError

        self._vertex_buffer = vertex_buffer
        self._index_buffer = index_buffer

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

    def get_vertex_pos_list(self):
        return self._vertex_buffer['pos']

    def get_vertex_properties_list_for(self, key):
        """Get vertex property list for some key

        Args:
            key: string key for property to get

        Returns:
            a flag: True if success else False
            a list: all values for some property

        Raises:
            TypeError: if key is not instance of str

        """

        if not isinstance(key, str):
            raise TypeError

        ret = []
        if key not in self._vertex_buffer:
            return False, ret

        return True, self._vertex_buffer[key]

    def get_vertex_property_at(self, key, index):
        """Get vertex property at index for some key

        Args:
            key: string key for property to get
            index: index position

        Returns:
            a flag: True if success else False
            a value: value for key in property dict

        Raises:
            TypeError: if index is not instance of int
                or key is not instance of str

        """

        if not isinstance(index, int):
            raise TypeError

        flag, ret = self.get_vertex_properties_list_for(key)

        if flag is False:
            return False, None

        if len(ret) <= index:
            return False, None

        return True, ret[index]

    def get_vertex_properties_at(self, index):
        """Get vertex properties at index

        Args:
            index: index position

        Returns:
            a dict for all vertex properties at some index

        Raises:
            TypeError: if index is not instance of int
            IndexError: if index is not valid

        """

        if not isinstance(index, int):
            raise TypeError

        ret = {}
        for k, v in self._vertex_buffer.items():
            ret[k] = v[index]

        return ret

    def get_vertex_properties_list(self):
        """Get all vertexs properties
        """

        count = len(self._vertex_buffer['pos'])
        ret = []
        for i in range(count):
            ret.append(self.get_vertex_properties_at(i))

        return ret
