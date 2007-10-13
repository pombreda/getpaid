from StringIO import StringIO
from Products.PloneGetPaid.Extensions.install import install_dependencies

def setupVarious(context):
    """Import steps that are not handled by GS import/export handlers can be
    defined in the setupVarious() function.
    See Products.GenericSetup.context.BaseContext to see what you can do with
    ``context`` (the function argument).
    For instance, it is possible to get the Plone Site object:
    ``site = context.getSite()``
    """
    if context.readDataFile('PloneGetPaid.setupVarious.txt') is None:
        return

    # Now do something useful
    site = context.getSite()

    logger = context.getLogger("PloneGetPaid")
    out = StringIO()

    print >> out, "Installing Dependencies"
    install_dependencies(site)

    logger.info(out.getvalue())

