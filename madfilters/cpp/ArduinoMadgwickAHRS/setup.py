from setuptools import Extension, setup
#NB: import setuptools before cythonize!
from Cython.Build import cythonize
import numpy as np  

extensions = [
    Extension("Arduino", ["*.pyx"],
              language="c++",
              include_dirs=[np.get_include()])
]

setup(
    name="Arduino",
    ext_modules=cythonize(extensions)
)
