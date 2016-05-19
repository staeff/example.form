# -*- coding: utf-8 -*-
from plone.supermodel import model
from plone.autoform.form import AutoExtensibleForm
from Products.statusmessages.interfaces import IStatusMessage
from zope import component
from zope import interface
from zope import schema
from z3c.form import form, button
from z3c.form import validator
from z3c.form.interfaces import ActionExecutionError
from z3c.form.interfaces import WidgetActionExecutionError
from zope.interface import invariant, Invalid

from example.form import _


def postcodeConstraint(value):
    """
    param: value (unicode)
    Check if 'value' starts with 6.
    If 'True' return 'True'
    If 'False' raise 'Invalid' exception and pass error message as the
    exception argument. Otherwise, we return True.
    """
    if not value.startswith('6'):
        raise Invalid(_(u"We can only deliver to postcodes starting with 6"))
    return True


class IOrderFormSchema(model.Schema):
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
            constraint=postcodeConstraint,
        )

    telephone = schema.ASCIILine(
            title=_(u"Telephone number"),
            description=_(u"Your phone number in international \
                            format. E.g. +44 12 123 1234"),
            required=False,
            default="+44 12 123 1234"
        )

    orderItems = schema.Set(
            title=_(u"Your order"),
            value_type=schema.Choice(values=[_(u'Margherita'),
                                             _(u'Pepperoni'),
                                             _(u'Hawaiian')])
        )

    @invariant
    def addressInvariant(data):
        if data.address1 == data.address2:
            raise Invalid(_(u"Address line 1 and 2 should not be the same!"))


class PhoneNumberValidator(validator.SimpleFieldValidator):
    """ z3c.form validator class for international phone numbers """

    def validate(self, value):
        """ Calling the superclass version of validate() to gain
            the default validation logic.
            In this method we can use variables like self.context,
            self.request, self.view, self.field and self.widget
            to access the adapted objects

            Validate international phone number on input
        """
        super(PhoneNumberValidator, self).validate(value)

        allowed_characters = "+- () / 0123456789"

        if value is not None:

            value = value.strip()

            if value == "":
                # Assume empty string = no input
                return

            # The value is not required
            for c in value:
                if c not in allowed_characters:
                    raise interface.Invalid(_(u"Phone number contains \
                                                bad characters"))

            if len(value) < 7:
                raise interface.Invalid(_(u"Phone number is too short"))

# Set conditions for which fields the validator class applies
# If we would pass a field type instead of an instance, the validator
# will be used for all fields in the form (of the given type).
validator.WidgetValidatorDiscriminators(
    PhoneNumberValidator,
    field=IOrderFormSchema['telephone']
    )

# Register the validator so it will be looked up by z3c.form machinery
component.provideAdapter(PhoneNumberValidator)


class OrderFormAdapter(object):
    """ This generic adapter allows to fill the form from anywhere """
    interface.implements(IOrderFormSchema)
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
    # specify the schema via the schema attribute, aka the schema shortcut
    # that is provided by plone.autoform.
    schema = IOrderFormSchema
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
    @button.buttonAndHandler(_(u'Order'), accessKey=u"o")
    def handleApply(self, action):
        # Extract the data from the form. self.extractData() returns a tuple
        # of the form data, which has been converted to the field’s underlying
        # type by each widget and any errors.
        data, errors = self.extractData()

        # Some additional validation
        if 'address1' in data and 'address2' in data:

            # Access values in data by index notation, because data is a dict
            if len(data['address1']) < 2 and len(data['address2']) < 2:
                raise ActionExecutionError(
                    Invalid(_(u"Please provide a valid address"))
                    )
            elif len(data['address1']) < 2 and len(data['address2']) > 10:
                raise WidgetActionExecutionError(
                    'address2',
                    Invalid(u"Please put the main part of the address \
                              in the first field")
                    )

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

    @button.buttonAndHandler(_(u"Cancel"), accessKey=u"c")
    def handleCancel(self, action):
        """User cancelled. Redirect back to the front page.
        """
        contextURL = self.context.absolute_url()
        self.request.response.redirect(contextURL)
