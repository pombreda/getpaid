from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='getpaid.vat',
      version=version,
      description="VAT add on for GetPaid",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Hannes Calitz',
      author_email='hannesc@gmail.com',
      url='http://blest.artician.com',
      license='GPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
