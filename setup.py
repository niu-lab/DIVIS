#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='DIVIS',
    version="0.1",
    license='MIT',
    author='ZhangYu',
    author_email='zhangy@sccas.cn',
    description='Integrated Somatic and Germline Pipelines for WES, WGS and Panel.',
    packages=['divis'],
    include_package_data=True,
    zip_safe=False,
    platforms='linux',
    python_requires='>=3.5',
    install_requires=[
        'GPyFlow>=0.1',
        'click==5.1',
    ],
    entry_points={
        'console_scripts': [
            'divis = divis.cli:main',
        ],
    }
)
