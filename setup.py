from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'Readme.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='serius',

    version='1.0.0',

    description='Microservice Docker DNS for Local Linux',

    long_description=long_description,

    entry_points={
            "console_scripts": ['serius = serius.serius:cli']
    },

    url='https://github.com/MOXGA-OSS/gamer-serius',

    author='GAMER',

    author_email = 'oamoam@moxga.com',

    keywords='dns docker python microservices',

    packages=find_packages(),

    install_requires=['logging', 'docker'],
)