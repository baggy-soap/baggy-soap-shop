
from oscar.apps.dashboard.catalogue import views


class ProductListView(views.ProductListView):

    # TODO: Test
    def get_queryset(self):
        """
        Build the queryset for this list, returning as a list to prevent tables2 from passing
        ordering to the database (we want a Python list sort using the appropriate key)
        """
        queryset = views.Product.objects.browsable_dashboard().base_queryset()
        queryset = self.filter_queryset(queryset)
        queryset = self.apply_search(queryset)
        return list(queryset)