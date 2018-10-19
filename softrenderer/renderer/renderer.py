# -*- coding:utf-8 -*-


from softrenderer.renderer.renderer_context import RendererContext


class Renderer:

    def __init__(self, rc):
        if not isinstance(rc, RendererContext):
            raise TypeError

        self._rc = rc

    def draw(self):
        pass
