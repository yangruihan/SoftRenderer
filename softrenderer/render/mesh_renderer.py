# -*- coding:utf-8 -*-


from softrenderer.render.renderer import Renderer
from softrenderer.common.mesh import Mesh


class MeshRenderer(Renderer):

    def __init__(self, mesh):
        self._mesh = Mesh
        self._material = None

    def draw(self):
        ...
