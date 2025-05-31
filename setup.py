#!/usr/bin/env python3
import setuptools


def setup():
    setuptools.setup(
        name='deb-resolve',
        version='1.0',
        author='igrekus',
        description='All your apt dependencies resolving needs',
        package_dir={'': 'src'},
        packages=setuptools.find_packages(where='src'),
        install_requires=[],
        python_requires='>=3.7',
        entry_points={'console_scripts': ['deb-resolve=deb_resolve.main:main']}
    )


if __name__ == '__main__':
    setup()
