# -*- coding:utf-8 -*-


from softrenderer.renderer.renderer import Renderer
from softrenderer.common.mesh import Mesh


class MeshRenderer(Renderer):

    def __init__(self, rc, mesh):
        Renderer.__init__(self, rc)

        if not isinstance(mesh, Mesh):
            raise TypeError

        self._mesh = Mesh

    def render(self):
        ...
