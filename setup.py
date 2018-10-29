from distutils.core import setup, Extension

setup(
    name='softrenderer',
    version='0.0.1',
    description='A software renderer by python',
    author='Yang Ruihan',
    author_email='coderyrh9236@gmail.com',
    url='https://www.github.com/yangruihan/SoftRenderer',
    packages=[
        'softrenderer',
        'softrenderer.common',
        'softrenderer.debug',
        'softrenderer.render',
    ],
    ext_package='softrenderer.cython',
    ext_modules=[
        Extension('render_utils', sources=['softrenderer/cython/render_utils.c'])
    ]
)
