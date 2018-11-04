from django.test import TestCase
from mock import Mock

from shipping import methods
from shipping.repository import Repository


class RepositoryTest(TestCase):

    def setUp(self):
        self.repository = Repository()

    def test_get_available_shipping_methods_returns_free_royal_mail_first_class_for_uk(self):
        shipping_methods = self.repository.get_available_shipping_methods(Mock())
        self.assertIn(methods.FreeRoyalMailFirstClass.code,
                      (shipping_method.code for shipping_method in shipping_methods))

    def test_get_available_shipping_methods_returns_royal_mail_intl_std_for_spain(self):
        address = Mock()
        address.country.code = 'ES'
        shipping_methods = self.repository.get_available_shipping_methods(Mock(), shipping_addr=address)
        self.assertIn(methods.RoyalMailInternationalStandard.code,
                      (shipping_method.code for shipping_method in shipping_methods))
