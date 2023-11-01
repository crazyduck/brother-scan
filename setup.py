""" Create a python module from folder brscan """
import setuptools

with open('README.md', 'r', encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='brscan',
    version='0.1.0',
    author='Esben Haabendal',
    author_email='esben@haabendal.dk',
    description='Service for (some) network scanners from Brother Inc.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/esben/brother-scan',
    packages=setuptools.find_packages(),
    classifiers=(
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
    ),
    entry_points={
        'console_scripts': [
            'brscand=brscan.brscand:main',
        ]
    }
)
