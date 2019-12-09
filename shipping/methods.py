from decimal import Decimal
from django.utils.translation import ugettext_lazy as _

from oscar.apps.shipping import methods


class FreeRoyalMailFirstClass(methods.Free):
    """
    This shipping method specifies that shipping is free, using Royal Mail 1st Class.
    """
    code = 'free-shipping-royal-mail-first-class'
    name = _('Free UK shipping (Royal Mail 1st Class)')
    description = _('Orders over £5 qualify for free UK shipping')


class RoyalMailLargeLetterFirstClass(methods.FixedPrice):
    """
    This is fixed price shipping method, using Royal Mail Large Letter 1st Class.
    """
    code = 'royal-mail-large-letter-first-class'
    name = _('Royal Mail Large Letter 1st Class')
    description = _('Spend over £5 to qualify for free UK shipping')
    charge_excl_tax = Decimal('1.50')
    charge_incl_tax = Decimal('1.50')


class RoyalMailFlatRateFirstClass(methods.FixedPrice):
    """
    This is a fixed price shipping method, using Royal Mail 1st Class.
    """
    code = 'royal-mail-flat-rate-first-class'
    name = _('Flat rate postage and packing (Royal Mail 1st Class)')
    charge_excl_tax = Decimal('2.99')
    charge_incl_tax = Decimal('2.99')


class RoyalMailInternationalStandardEurope(methods.FixedPrice):
    """
    This is fixed price shipping method, using Royal Mail International Standard in Europe.
    """
    code = 'royal-mail-international-standard-europe'
    name = _('Royal Mail International Standard Europe (3 to 5 working days)')
    charge_excl_tax = Decimal('4.99')
    charge_incl_tax = Decimal('4.99')


class RoyalMailInternationalStandardWorldZone1(methods.FixedPrice):
    """
    This is fixed price shipping method, using Royal Mail International Standard in World Zone 1.
    """
    code = 'royal-mail-international-standard-world-zone-1'
    name = _('Royal Mail International Standard World Zone 1 (3 to 5 working days)')
    charge_excl_tax = Decimal('6.99')
    charge_incl_tax = Decimal('6.99')



class RoyalMailInternationalStandardWorldZone2(methods.FixedPrice):
    """
    This is fixed price shipping method, using Royal Mail International Standard in World Zone 2.
    """
    code = 'royal-mail-international-standard-world-zone-1'
    name = _('Royal Mail International Standard World Zone 2 (3 to 5 working days)')
    charge_excl_tax = Decimal('7.99')
    charge_incl_tax = Decimal('7.99')
