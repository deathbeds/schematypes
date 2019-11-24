import json
from pathlib import Path
import setuptools

name = "schematypes"

__version__ = None

here = Path(__file__).parent

# This should be replaced with proper pathlib business

with (here/ name / '_version.py').open('r') as file:
    exec(file.read())

with open(str(here/'readme.md'),'r') as f:
    description = f.read()

import sys

from setuptools.command.test import test as TestCommand
class PyTest(TestCommand):
    def run_tests(self): sys.exit(__import__('pytest').main([]))

install_requires = []

setup_args = dict(
    name=name,
    version=__version__,
    author="deathbeds",
    author_email="tony.fast@gmail.com",
    description="An extended Python type system using jsonschemas.",
    long_description=description,
    long_description_content_type='text/markdown',
    url="https://github.com/deathbeds/schematypes",
    python_requires=">=3.5",
    license="BSD-3-Clause",
    setup_requires=[
        'pytest-runner',
    ] + ([] if sys.version_info.minor == 4 else ['wheel>=0.31.0']),
    tests_require=['pytest', 'nbformat'],
    install_requires=install_requires,
    include_package_data=True,
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: IPython",
        "Framework :: Jupyter",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: BSD License",
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',],
    zip_safe=False,
    cmdclass={'test': PyTest,},
    entry_points = {},
)

if __name__ == "__main__":
    setuptools.setup(**setup_args)
