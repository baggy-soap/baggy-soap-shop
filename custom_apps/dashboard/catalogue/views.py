
from oscar.apps.dashboard.catalogue import views


class ProductListView(views.ProductListView):

    def get_queryset(self):
        """
        Build the queryset for this list, returning as a list to prevent tables2 from passing
        ordering to the database (we want a Python list sort using the appropriate key)
        """
        # Get all products, including children (i.e. don't use browsable_dashboard queryset)
        queryset = views.Product.objects.base_queryset()
        queryset = self.filter_queryset(queryset)
        queryset = self.apply_search(queryset)
        return list(queryset)