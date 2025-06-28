from setuptools import setup, find_packages

setup(
    name="listener_maths_crossword",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "sympy>=1.14.0",
    ],
) 