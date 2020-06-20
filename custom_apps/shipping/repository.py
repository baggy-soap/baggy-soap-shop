from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import gettext_lazy as _
from oscar.apps.shipping import repository
from custom_apps.shipping.models import WeightBased


class Repository(repository.Repository):

    def get_available_shipping_methods(self, basket, user=None, shipping_addr=None, request=None, **kwargs):
        country_code = shipping_addr.country.code if shipping_addr else "GB"
        weightbased_dict = {method: method.calculate(basket).excl_tax
                            for method in WeightBased.objects.all().filter(countries=country_code)}
        if weightbased_dict:
            chargeable_methods_dict = {method: charge for method, charge in weightbased_dict.items() if charge > 0}
            shipping_methods = sorted(chargeable_methods_dict, key=chargeable_methods_dict.get)
        else:
            shipping_methods = []

        return shipping_methods

    def get_default_shipping_method(self, basket, shipping_addr=None, **kwargs):
        """
        Return a 'default' shipping method to show on the basket page to give
        the customer an indication of what their order will cost.
        """
        shipping_methods = self.get_shipping_methods(basket, shipping_addr=shipping_addr, **kwargs)
        if len(shipping_methods) == 0:
            raise ImproperlyConfigured(_("You need to define some shipping methods"))

        # Assume first returned method is default
        return shipping_methods[0]
