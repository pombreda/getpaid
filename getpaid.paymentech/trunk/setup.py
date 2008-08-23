"""
$Id: setup.py 1868 2008-08-22 22:00:38Z fairwinds.dp $

Copyright (c) 2007 - 2008 ifPeople, Kapil Thangavelu, and Contributors
All rights reserved. Refer to LICENSE.txt for details of distribution and use.

Distutils setup
 
"""

import os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(
    name='getpaid.paymentech',
    version='0.3dev',
    license = 'ZPL2.1',
    author='Six Feet Up, Inc.',
    author_email='getpaid-dev@googlegroups.com',
    description='Get paid paymentech payment processor functionality',
    long_description = (
        read('README.txt')
        + '\n' +
        read('CHANGES.txt')
        + '\n' +
        'Detailed Documentation\n'
        '**********************\n'
        + '\n' +
        read('src', 'getpaid', 'paymentech', 'README.txt')
        + '\n' +
        'Download\n'
        '**********************\n'
        ),
Ê Ê classifiers=[
Ê Ê Ê Ê "Framework :: Plone",
Ê Ê Ê Ê "Programming Language :: Python",
Ê Ê Ê Ê "Framework :: Zope3",
Ê Ê Ê Ê "Intended Audience :: Developers",
Ê Ê Ê Ê "License :: OSI Approved :: Zope Public License",
Ê Ê Ê Ê "Operating System :: OS Independent",
Ê Ê Ê Ê "Topic :: Office/Business :: Financial",
Ê Ê Ê Ê "Topic :: Software Development :: Libraries",
Ê Ê Ê Ê ],
    url='http://code.google.com/p/getpaid',
    packages=find_packages('src'),
    package_dir={'':'src'},
    namespace_packages=['getpaid'],
    include_package_data=True,
    install_requires = ['setuptools',
                        'getpaid.core',
                        'zc.ssl',
                        'zope.app.annotation',
                       ],
    zip_safe = False,
    )

