from oscar.apps.catalogue import search_handlers
from oscar.core.loading import get_model

Product = get_model('catalogue', 'Product')


class SimpleProductSearchHandler(search_handlers.SimpleProductSearchHandler):
    ordering = 'categories'

    def get_queryset(self):
        qs = Product.browsable.base_queryset()

        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, str):
                ordering = (ordering,)
            qs = qs.order_by(*ordering)

        if self.categories:
            qs = qs.filter(categories__in=self.categories).distinct()
        return qs
