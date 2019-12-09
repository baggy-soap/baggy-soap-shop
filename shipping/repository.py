from oscar.apps.shipping import repository

from shipping import methods

EUROPE_CODES = ['ES', 'FR', 'NE', 'PT']


class Repository(repository.Repository):

    def get_available_shipping_methods(self, basket, user=None, shipping_addr=None, request=None, **kwargs):
        shipping_methods = ((methods.RoyalMailInternationalStandardEurope(),)
                            if shipping_addr and shipping_addr.country.code in EUROPE_CODES
                            else (methods.RoyalMailFlatRateFirstClass(), ))
        return shipping_methods
