# -*- coding:utf-8 -*-


from softrenderer.render.render_context import RenderContext


class Renderer:

    def __init__(self, rc):
        if not isinstance(rc, RenderContext):
            raise TypeError

        self._rc = rc

    def draw(self):
        pass
