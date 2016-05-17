# -*- coding: utf-8 -*-
from zope import interface
from zope import schema

from example.form import _


class OrderFormSchema(interface.Interface):
    """ A schema that describes the form’s fields """

    name = schema.TextLine(
            title=_(u"Your full name"),
        )

    address1 = schema.TextLine(
            title=_(u"Address line 1"),
        )

    address2 = schema.TextLine(
            title=_(u"Address line 2"),
            required=False,
        )

    postcode = schema.TextLine(
            title=_(u"Postcode"),
        )

    telephone = schema.ASCIILine(
            title=_(u"Telephone number"),
            description=_(u"We prefer a mobile number"),
        )

    orderItems = schema.Set(
            title=_(u"Your order"),
            value_type=schema.Choice(values=[_(u'Margherita'),
                                             _(u'Pepperoni'),
                                             _(u'Hawaiian')])
        )
