from Products.CMFCore.utils import getToolByName

def addCatalogIndexes(context):
    index_data = context.readDataFile('catalog_noclobber.txt')
    if index_data is None:
        return
    portal = context.getSite()
    pct = getToolByName(portal, 'portal_catalog')
    existing_indexes = pct.indexes()
    existing_columns = pct.schema()
    for line in index_data.split('\n'):
        if line:
            index, type = line.split()
            if index not in existing_indexes:
                pct.addIndex(index, type)
            if index not in existing_columns:
                pct.addColumn(index)

def importVarious(context):
    """Miscellanous steps import handle
    """

    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a 
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.

    if context.readDataFile('getpaid.creditpublish_various.txt') is None:
        return

    addCatalogIndexes(context)
