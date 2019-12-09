from decimal import Decimal
from django.test import TestCase
from mock import Mock

from shipping import methods
from shipping.repository import Repository


class RepositoryTest(TestCase):

    def setUp(self):
        self.repository = Repository()
        self.mock_basket = Mock()
        self.mock_basket.total_incl_tax = Decimal('5.99')

    def test_get_available_shipping_methods_returns_royal_mail_flat_rate_first_class_if_basket_lte_5(self):
        self.mock_basket.total_incl_tax = Decimal('5.00')
        shipping_methods = self.repository.get_available_shipping_methods(self.mock_basket)
        self.assertIn(methods.RoyalMailFlatRateFirstClass.code,
                      (shipping_method.code for shipping_method in shipping_methods))

    def test_get_available_shipping_methods_returns_royal_mail_flat_rate_first_class_if_basket_gt_5(self):
        shipping_methods = self.repository.get_available_shipping_methods(self.mock_basket)
        self.assertIn(methods.RoyalMailFlatRateFirstClass.code,
                      (shipping_method.code for shipping_method in shipping_methods))

    def test_get_available_shipping_methods_returns_royal_mail_intl_std_for_europe(self):
        country_codes = ['ES', 'FR', 'PT', 'NE']
        address = Mock()
        for code in country_codes:
            address.country.code = code
            shipping_methods = self.repository.get_available_shipping_methods(self.mock_basket, shipping_addr=address)
            self.assertIn(methods.RoyalMailInternationalStandardEurope.code,
                          (shipping_method.code for shipping_method in shipping_methods))
