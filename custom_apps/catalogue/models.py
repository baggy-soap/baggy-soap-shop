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

    @property
    def total_allocated(self):
        return sum(stockrecord.num_allocated if stockrecord.num_allocated else 0
                   for stockrecord in self.stockrecords.all())

    def get_description(self):
        """Return a product's description or it's parent's description if it is a child"""
        return self.parent.description if self.is_child else self.description

    def get_full_title(self):
        """Return a product's full title. For a child, this should be either a concatenation of it's parent's title
        and it's own title, or just the parent's title if it has no title"""
        title = self.title
        if self.is_child:
            title = "{} ({})".format(self.parent.title, self.title) if title else self.parent.title
        return title

    def __str__(self):
        if self.title:
            return self.get_full_title()
        if self.attribute_summary:
            return "%s (%s)" % (self.get_full_title(), self.attribute_summary)
        else:
            return self.get_full_title()


from oscar.apps.catalogue.models import *
