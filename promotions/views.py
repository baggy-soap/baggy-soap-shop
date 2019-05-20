from oscar.apps.catalogue.views import CatalogueView


class HomeView(CatalogueView):
    template_name = 'promotions/home.html'
