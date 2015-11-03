from setuptools import setup

setup(
    name = 'Simple Search Engine',
    version = 0.001,
    description = 'Really simple search engine from HTW Berlin Students',
    author = "HTW Berlin Students",
    author_email = "None",
    scripts = ['Crowler.py'],
    packages = ['bs4'],
    install_requires = ["setuptools", "pprint"])
