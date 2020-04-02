from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
# with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    # long_description = f.read()
long_description="it's comming"

setup(
    name='covap-backend',

    version='0.1',

    description='COVAP Backend',
    long_description=long_description,

    url='https://github.com/tariqdaouda/covap-backend',

    author='Tariq Daouda',
    author_email='look for me on the internet',

    license='ApacheV2',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        # 'Development Status :: 5 - Production/Stable',
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',
        # 'Intended Audience :: System Administrators',
        # 'Topic :: Software Development :: Libraries',
        # 'Topic :: Database',
        # 'Topic :: Database :: Database Engines/Servers',

        'License :: OSI Approved :: Apache Software License',

        # 'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],

    install_requires=['pyArango', 'pandas', 'click', 'numpy', ],

    keywords='database ORM nosql arangodb driver validation',

    packages=find_packages(),

    entry_points={
        'console_scripts': [
            'sample=sample:main',
        ],
    },
)
