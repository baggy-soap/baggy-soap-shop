from oscar.apps.catalogue.abstract_models import AbstractProduct


class Product(AbstractProduct):

    # TODO: Test this
    @property
    def is_soap_product(self):
        product_categories = set(category.name for category in self.categories.all())
        soap_categories = {'Soap with Bag', 'Soap Refills'}
        return product_categories.intersection(soap_categories)

from oscar.apps.catalogue.models import *
