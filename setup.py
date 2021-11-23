from setuptools import setup, find_packages

setup(
    name='fonext',
    version="0.1.dev",
    author='derwind',
    license="MIT License",
    packages=find_packages("Lib"),
    package_dir={'': 'Lib'},
    description='font manipulation tools',
    install_requires=[],
)
