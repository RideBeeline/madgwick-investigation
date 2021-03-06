from setuptools import Extension, setup
#NB: import setuptools before cythonize!
from Cython.Build import cythonize
import numpy as np  

extensions = [
    Extension("Adafruit", ["*.pyx"],
              language="c++",
              include_dirs=[np.get_include()])
]

setup(
    name="Adafruit",
    ext_modules=cythonize(extensions)
)
