from setuptools import setup, find_packages
import os

version = '0.2'

setup(name='getpaid.verkkomaksut',
      version=version,
      description="Verkkomaksut payment processor for getpaid.",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='plone getpaid processor',
      author='Taito Horiuchi',
      author_email='taito.horiuchi@gmail.com',
      url='http://pypi.python.org/pypi/getpaid.verkkomaksut',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['getpaid'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- PloneGetPaid: -*-
          'getpaid.core',
      ],
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )