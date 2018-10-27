# -*- coding:utf-8 -*-


class Shader:

    def main(self, vertex_properties):
        pass


class VertexShader(Shader):
    pass


class PixelShader(Shader):
    pass


class _DefaultVertexShader(VertexShader):

    def main(self, vertex_properties):
        return vertex_properties['pos']


class _DefaultPixelShader(PixelShader):

    def main(self, pixel_properties):
        return pixel_properties['color']
