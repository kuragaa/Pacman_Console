from setuptools import setup, find_packages

setup(
    name='pacman',
    version='14.0',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'pacman = pacman.game:main'
        ]
    }
) 

