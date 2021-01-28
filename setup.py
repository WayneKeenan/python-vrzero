__author__ = 'Wayne Keenan'
import os
from setuptools import setup, find_packages

install_requires = ['pi3d', 'numpy']
tests_require = []

base_dir = os.path.dirname(os.path.abspath(__file__))

version = "0.0.2"

setup(
    name='vrzero',
    version=version,
    description="A library that makes Virtual Reality easier",
    long_description="\n\n".join([
        open(os.path.join(base_dir, "README.md"), "r").read(),
    ]),
    url='https://www.thebubbleworks.com/',
    author='Wayne Keenan',
    author_email='wayne@thebubbleworks.com',
    maintainer='Wayne Keenan',
    maintainer_email='wayne@thebubbleworks.com',
    packages=find_packages(),
    zip_safe=False,
    install_requires=install_requires,
    tests_require=tests_require,
    test_suite="tests.get_tests",
)