from oscar.apps.catalogue import managers


class ProductQuerySet(managers.ProductQuerySet):

    #TODO: Maybe remove this and change call in get_queryset?
    def browsable_dashboard(self):
        """
        Products that should be browsable in the dashboard.

        Excludes non-canonical products, but includes non-public products.
        """
        return self