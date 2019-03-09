from decimal import Decimal
from oscar.apps.shipping import repository

from shipping import methods


class Repository(repository.Repository):

    def get_available_shipping_methods(self, basket, user=None, shipping_addr=None, request=None, **kwargs):
        shipping_methods = ((methods.RoyalMailLargeLetterFirstClass(), )
                            if basket.total_incl_tax <= Decimal('5.00')
                            else (methods.FreeRoyalMailFirstClass(), ))
        if shipping_addr and shipping_addr.country.code == 'ES':
            shipping_methods = (methods.RoyalMailInternationalStandard(), )
        return shipping_methods
