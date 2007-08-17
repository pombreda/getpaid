from zope.schema import TextLine
from zope.schema.interfaces import ValidationError


class InvalidPhoneNumber(ValidationError):
    __doc__ = u"Only digit character allowed."


class InvalidCreditCardNumber(ValidationError):
    __doc__ = u"Only digit character allowed."


class PhoneNumber(TextLine):

    def _validate(self, value):
        super(PhoneNumber, self)._validate(value)
        if value and not value.isdigit():
            raise InvalidPhoneNumber(value)


class CreditCardNumber(TextLine):

    def _validate(self, value):
        super(CreditCardNumber, self)._validate(value)
        if value and not value.isdigit():
            raise InvalidCreditCardNumber(value)