"""
Setup-Script for LingPy
"""
from setuptools import setup, find_packages, Extension
import sys
from os.path import join

# check for specific features
with_c = False
for i, arg in enumerate(sys.argv):
    if arg.lower() == '--with-c':
        del sys.argv[i]
        with_c = True
        break


# set up extension modules
extension_modules = []
if 'install' in sys.argv or 'bdist_egg' in sys.argv or 'develop' in sys.argv:
    if with_c:
        ext_path = ['lingpy3', 'algorithm', 'cython']
        extension_modules = [
            Extension('.'.join(ext_path + [mod]), [join(*ext_path + [mod + '.c'])])
            for mod in ['calign', 'malign', 'talign', 'cluster', 'misc']]

requires = [
    'networkx',
    'attrs',
    'six',
    'appdirs',
    'clldutils>=1.5.1',
    'tqdm',
    'zope.interface>=4.3',
]


setup(
    name='lingpy3',
    version="1.0",
    packages=find_packages(),
    install_requires=requires,
    tests_require=['nose', 'coverage', 'mock'],
    test_suite="lingpy3.tests",
    author="Johann-Mattis List and Robert Forkel",
    author_email="info@lingpy.org",
    entry_points={
        'console_scripts': ['lingpy=lingpy.cli:main'],
    },
    keywords=[
        "historical linguistics",
        "sequence alignment",
        "computational linguistics",
        "dialectology"
    ],
    classifiers=[
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
    url="http://lingpy.org",
    description="Python library for automatic tasks in historical linguistics",
    license="gpl-3.0",
    platforms=["unix", "linux", "windows"],
    ext_modules=extension_modules,
    include_package_data=True,
    zip_safe=False,
)
