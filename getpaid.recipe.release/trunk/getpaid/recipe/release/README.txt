Supported options
=================

The recipe supports the following options:

eggs
    This will be the getpaid eggs

Example usage
=============

.. Note to recipe author!
   ----------------------
   zc.buildout provides a nice testing environment which makes it
   relatively easy to write doctests that both demonstrate the use of
   the recipe and test it.
   You can find examples of recipe doctests from the PyPI, e.g.
   
     http://pypi.python.org/pypi/zc.recipe.egg

   The PyPI page for zc.buildout contains documentation about the test
   environment.

     http://pypi.python.org/pypi/zc.buildout#testing-support

   Below is a skeleton doctest that you can start with when building
   your own tests.

We'll start by creating a buildout that uses the recipe::

    >>> write('buildout.cfg',
    ... """
    ... [buildout]
    ... parts = test1
    ...
    ... [test1]
    ... recipe = getpaid.recipe.release
    ...
    ... """)

Running the buildout gives us::

    >>> print 'start', system(buildout) # doctest:+ELLIPSIS
    start...
    Installing test1.


