from setuptools import setup, find_packages

version = "0.2"

setup(
    name="getpaid.paymentech",
    version=version,
    description="package for plone getpaid to hook up the checkout with Paymentech",
    long_description=open(os.path.join("src", "getpaid", "paymentech", "readme.txt")).read(),
    classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Framework :: Zope3",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Zope Public License",
        "Operating System :: OS Independent",
        "Topic :: Office/Business :: Financial"
        "Topic :: Software Development :: Libraries",
        ],
    keywords='',
    author='Six Feet Up, Inc.',
    author_email='info@sixfeetup.com',
    url='http://code.google.com/p/getpaid',
    packages=find_packages('src'),
    package_dir={'':'src'},
    namespace_packages=['getpaid'],
    include_package_data=True,
    install_requires = [ 'setuptools',
                         'getpaid.core',
                         'zc.ssl'
                         ],
    zip_safe = False,
    )

