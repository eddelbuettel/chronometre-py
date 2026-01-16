from setuptools import setup, Extension
import pybind11

ext_modules = [
    Extension(
        "chronometre",  # Module name
        ["chronometre.cpp"],  # Source files
        include_dirs=[pybind11.get_include()],  # Include pybind11 headers
        language="c++",  # Specify C++ as the language
    )
]

setup(
    name="chronometre",
    version="0.0.1",
    ext_modules=ext_modules,
)
