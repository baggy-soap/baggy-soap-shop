from oscar.apps.shipping import repository

from custom_apps.shipping import methods

#TODO: Verify this list against Royal Mail list and ensure they match
EUROPE_CODES = ['AL', 'AD', 'AM', 'AT', 'BY', 'BE', 'BA', 'BG', 'CH', 'CY', 'CZ', 'DE',
                'DK', 'EE', 'ES', 'FO', 'FI', 'FR', 'GE', 'GI', 'GR', 'HU', 'HR',
                'IE', 'IS', 'IT', 'LI', 'LT', 'LU', 'LV', 'MC', 'MK', 'MT', 'NO', 'NL',
                'PL', 'PT', 'RO', 'RU', 'SE', 'SI', 'SK', 'SM', 'TR', 'UA', 'VA']


class Repository(repository.Repository):

    def get_available_shipping_methods(self, basket, user=None, shipping_addr=None, request=None, **kwargs):
        shipping_methods = ((methods.RoyalMailInternationalStandardEurope(),)
                            if shipping_addr and shipping_addr.country.code in EUROPE_CODES
                            else (methods.RoyalMailFlatRateFirstClass(),))
        return shipping_methods
