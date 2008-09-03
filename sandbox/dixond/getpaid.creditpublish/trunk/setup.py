from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='getpaid.creditpublish',
      version=version,
      description="A suite of tools to control publishing content with credit",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='getpaid credit publish',
      author='Darryl Dixon (Winterhouse Consulting Ltd)',
      author_email='darryl.dixon@winterhouseconsulting.com',
      url='https://getpaid.googlecode.com/svn/getpaid.creditpublish',
      license='ZPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['getpaid'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
