from django.utils.translation import ugettext_lazy as _

from oscar.apps.shipping import methods


class FreeRoyalMailFirstClass(methods.Free):
    """
    This shipping method specifies that shipping is free, using Royal Mail 1st Class.
    """
    code = 'free-shipping-royal-mail-first-class'
    name = _('Free shipping (Royal Mail 1st Class)')
