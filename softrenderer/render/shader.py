# -*- coding:utf-8 -*-


from softrenderer.common.types import Color


class Shader:

    def main(self, vertex_properties):
        pass


class VertexShader(Shader):
    pass


class PixelShader(Shader):
    pass


class _DefaultVertexShader(VertexShader):

    def main(self, vertex_properties):
        return vertex_properties


class _DefaultPixelShader(PixelShader):

    def main(self, pixel_properties):
        return Color(pixel_properties[2], pixel_properties[3], pixel_properties[4], pixel_properties[5])
