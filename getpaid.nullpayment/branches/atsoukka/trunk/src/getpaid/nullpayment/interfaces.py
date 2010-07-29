# Copyright (c) 2010 ifPeople, Kapil Thangavelu, and Contributors
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

"""
NullPaymentProcessor Options
"""

__version__ = "$Revision$"
# $Id$
# $URL$                                                                                                            

from zope import schema

from getpaid.core import interfaces

from getpaid.nullpayment import _


class INullPaymentOptions(interfaces.IPaymentProcessorOptions):

    accepted_credit_cards = schema.List(
        title    = _(u"Accepted Credit Cards"),
        required = False,
        default  = [],
        description = _(u"Credit cards accepted for payment"),
        value_type  = schema.Choice(title=u"credit_card_types",
                                    source="getpaid.core.credit_card_types"))
    
    allow_authorization = schema.Choice(
        title   = _(u"Allow Authorizations"),
        values  =  (u"allow_authorization", u"no_authorization"),
        default =   u"allow_authorization")

    allow_capture = schema.Choice(
        title   = _(u"Allow Captures"),
        values  =  (u"allow_capture", u"no_capture"),
        default =   u"allow_capture")

    allow_refunds = schema.Choice(
        title   = _(u"Allow Refunds"),
        values  =  (u"allow_refund", u"no_refund"),
        default =   u"allow_refund")
