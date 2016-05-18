# -*- coding: utf-8 -*-
from plone.autoform.form import AutoExtensibleForm
from Products.statusmessages.interfaces import IStatusMessage
from zope import component
from zope import interface
from zope import schema
from z3c.form import form, button

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


class OrderFormAdapter(object):
    """ This generic adapter allows to fill the form from anywhere """
    interface.implements(OrderFormSchema)
    component.adapts(interface.Interface)

    def __init__(self, context):
        self.name = None
        self.address1 = None
        self.address2 = None
        self.postcode = None
        self.telephone = None
        self.orderItems = None


class OrderForm(AutoExtensibleForm, form.Form):
    """ The form view from one of the standard base classes in plone.autoform
    (AutoExtensibleForm). It comes without any of the standard actions.
    Specialised base classes such as SchemaAddForm or SchemaEditForm have
    actions. It basically mirrors the z3c.form.form.Form base class.
    """
    # specify the schema via the schema attribute
    schema = OrderFormSchema
    form_name = 'order_form'

    # rendered as page header in standard form template
    label = _(u"Order your pizza")
    # rendered as lead-in text in standard form template
    description = _(u"We will contact you to confirm your order and delivery.")

    def update(self):
        """ update() is a good place to perform any pre-work before the
            form machinery kicks in or post-processing afterwards
        """
        # hide the editable border when rendering the form
        self.request.set('disable_border', True)

        # call the base class version - this is very important!
        super(OrderForm, self).update()

    # Define actions. The actions are rendered as button in order
    # of their definition. The argument is a (translated) string
    # that will be used as a button label. The decorated handler
    # function will be called when the button is clicked.
    @button.buttonAndHandler(_(u'Order'))
    def handleApply(self, action):
        # Extract the data from the form. self.extractData() returns a tuple
        # of the form data, which has been converted to the field’s underlying
        # type by each widget and any errors.
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        # Handle order here. For now, just print it to the console. A more
        # realistic action would be to send the order to another system, send
        # an email, or similar

        print u"Order received:"
        print u"  Customer: ", data['name']
        print u"  Telephone:", data['telephone']
        print u"  Address:  ", data['address1']
        print u"            ", data['address2']
        print u"            ", data['postcode']
        print u"  Order:    ", ', '.join(data['orderItems'])
        print u""

        # Add a cookie-tracked status message,
        # so that it can appear on the next page
        IStatusMessage(self.request).addStatusMessage(
                _(u"Thank you for your order. We will contact you shortly"),
                "info"
            )

        contextURL = self.context.absolute_url()
        # Redirect the user to the context’s default view.
        # In this case, that means the portal front page.
        self.request.response.redirect(contextURL)

    @button.buttonAndHandler(_(u"Cancel"))
    def handleCancel(self, action):
        """User cancelled. Redirect back to the front page.
        """
        contextURL = self.context.absolute_url()
        self.request.response.redirect(contextURL)