from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='getpaid.creditregistry',
      version=version,
      description="A credit registry that is hooked into GetPaid",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='getpaid credit registry',
      author='Darryl Dixon (Winterhouse Consulting Ltd)',
      author_email='darryl.dixon@winterhouseconsulting.com',
      url='https://getpaid.googlecode.com/svn/getpaid.creditregistry/trunk',
      license='GPL',
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
