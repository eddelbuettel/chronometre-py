from setuptools import setup, Extension


class Pybind11Include:
    def __str__(self):
        import pybind11
        return pybind11.get_include()

ext_modules = [
    Extension(
        "chronometre._chronometre",  # Module name
        ["src/chronometre/_chronometre.cpp"],  # Source files
        include_dirs=[Pybind11Include()],  # Include pybind11 headers
        language="c++",  # Specify C++ as the language
    )
]

setup(
    name="chronometre",
    version="0.0.1",
    packages=["chronometre"],
    package_dir={"": "src"},
    ext_modules=ext_modules,
)
