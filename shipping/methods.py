from decimal import Decimal
from django.utils.translation import ugettext_lazy as _

from oscar.apps.shipping import methods


class FreeRoyalMailFirstClass(methods.Free):
    """
    This shipping method specifies that shipping is free, using Royal Mail 1st Class.
    """
    code = 'free-shipping-royal-mail-first-class'
    name = _('Free UK shipping (Royal Mail 1st Class)')


class RoyalMailInternationalStandard(methods.FixedPrice):
    """
    This is fixed price shipping method, using Royal Mail International Standard.
    """
    code = 'royal-mail-international-standard'
    name = _('Royal Mail International Standard (3 to 5 working days)')
    charge_excl_tax = Decimal('3.85')
    charge_incl_tax = Decimal('3.85')
