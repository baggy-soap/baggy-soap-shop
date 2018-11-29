from oscar.apps.catalogue.abstract_models import AbstractProduct


class Product(AbstractProduct):

    @property
    def is_soap_product(self):
        product_categories = set(category.name for category in self.categories.all())
        soap_categories = {'Soap with Bag', 'Soap Refills', 'Shampoo with Bag', 'Shampoo Refills'}
        return product_categories.intersection(soap_categories)

    @property
    def total_stock_count(self):
        return sum(stockrecord.num_in_stock for stockrecord in self.stockrecords.all())


from oscar.apps.catalogue.models import *
