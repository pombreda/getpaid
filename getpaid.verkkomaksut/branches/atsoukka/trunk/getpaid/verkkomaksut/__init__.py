"""
Verkkomaksut.fi payment processor for GetPaid
"""

__version__ = "$Revision$"
# $Id$
# $URL$

from zope.i18nmessageid import MessageFactory
_ = MessageFactory('getpaid.verkkomaksut')

NAME = "getpaid.verkkomaksut" # must be <type 'str'> (!)
TITLE = _(u"Verkkomaksut Processor")
DESCRIPTION = _(u"An offline payment processor for Verkkomaksut.fi")
