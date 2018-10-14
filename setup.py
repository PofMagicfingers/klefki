#!/usr/bin/env python

from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

version = '0.1.1'

print find_packages()

setup(
    name='klefki',
    version=version,
    install_requires=requirements,
    author='Pof Magicfingers',
    author_email='pof@pof.pm',
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    description='Connect to cotizasso',
    entry_points={
        'console_scripts': [
            'klefki = klefki.__main__:main',
        ]
    },
    classifiers=[
        'Operating System :: OS Independent',
        'Topic :: Internet',
        'Topic :: Utilities',
    ]
)
