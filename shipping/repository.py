from oscar.apps.shipping import repository

from shipping import methods


class Repository(repository.Repository):

    def get_available_shipping_methods(self, basket, user=None, shipping_addr=None, request=None, **kwargs):
        shipping_methods = ((methods.RoyalMailInternationalStandardEurope(),)
                            if shipping_addr and shipping_addr.country.code == 'ES'
                            else (methods.RoyalMailFlatRateFirstClass(), ))
        return shipping_methods
