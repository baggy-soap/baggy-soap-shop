from decimal import Decimal
from django.test import TestCase

from shipping.methods import RoyalMailInternationalStandard


class RoyalMailInternationalStandardTest(TestCase):

    def test_charge_excl_tax_gives_correct_price(self):
        shipping_method = RoyalMailInternationalStandard()
        self.assertEqual(Decimal('3.85'), shipping_method.charge_excl_tax)

    def test_charge_incl_tax_gives_correct_price(self):
        shipping_method = RoyalMailInternationalStandard()
        self.assertEqual(Decimal('3.85'), shipping_method.charge_incl_tax)
