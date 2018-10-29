from distutils.core import setup
from Cython.Build import cythonize
from distutils.extension import Extension

sourcefiles = [
    'test_c_dict.pyx',
    'test_c_list.pyx',
]

setup(
    ext_modules=cythonize(sourcefiles)
)
