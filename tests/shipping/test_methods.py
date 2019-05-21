from decimal import Decimal
from django.test import TestCase

from shipping.methods import RoyalMailInternationalStandard, RoyalMailFlatRateFirstClass


class RoyalMailFlatRateFirstClassTest(TestCase):

    def test_charge_excl_tax_gives_correct_price(self):
        shipping_method = RoyalMailFlatRateFirstClass()
        self.assertEqual(Decimal('2.99'), shipping_method.charge_excl_tax)

    def test_charge_incl_tax_gives_correct_price(self):
        shipping_method = RoyalMailFlatRateFirstClass()
        self.assertEqual(Decimal('2.99'), shipping_method.charge_incl_tax)


class RoyalMailInternationalStandardTest(TestCase):

    def test_charge_excl_tax_gives_correct_price(self):
        shipping_method = RoyalMailInternationalStandard()
        self.assertEqual(Decimal('4.99'), shipping_method.charge_excl_tax)

    def test_charge_incl_tax_gives_correct_price(self):
        shipping_method = RoyalMailInternationalStandard()
        self.assertEqual(Decimal('4.99'), shipping_method.charge_incl_tax)
