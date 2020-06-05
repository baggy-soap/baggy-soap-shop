from oscar.apps.shipping import repository
from custom_apps.shipping.models import WeightBased


class Repository(repository.Repository):

    def get_available_shipping_methods(self, basket, user=None, shipping_addr=None, request=None, **kwargs):
        def is_chargeable_method(method):
            return method.calculate(basket).excl_tax > 0

        if shipping_addr:
            weightbased_set = WeightBased.objects.all().filter(countries=shipping_addr.country.code)

            if weightbased_set:
                shipping_methods = list(filter(is_chargeable_method, weightbased_set))
            else:
                shipping_methods = []
        else:
            shipping_methods = []

        return shipping_methods
