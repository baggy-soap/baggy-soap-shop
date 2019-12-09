from decimal import Decimal
from django.test import TestCase

from shipping.methods import (
    RoyalMailInternationalStandardEurope, RoyalMailFlatRateFirstClass,
    RoyalMailInternationalStandardWorldZone1, RoyalMailInternationalStandardWorldZone2
)


class RoyalMailFlatRateFirstClassTest(TestCase):

    def test_charge_excl_tax_gives_correct_price(self):
        shipping_method = RoyalMailFlatRateFirstClass()
        self.assertEqual(Decimal('2.99'), shipping_method.charge_excl_tax)

    def test_charge_incl_tax_gives_correct_price(self):
        shipping_method = RoyalMailFlatRateFirstClass()
        self.assertEqual(Decimal('2.99'), shipping_method.charge_incl_tax)


class RoyalMailInternationalStandardEuropeTest(TestCase):

    def test_charge_excl_tax_gives_correct_price(self):
        shipping_method = RoyalMailInternationalStandardEurope()
        self.assertEqual(Decimal('4.99'), shipping_method.charge_excl_tax)

    def test_charge_incl_tax_gives_correct_price(self):
        shipping_method = RoyalMailInternationalStandardEurope()
        self.assertEqual(Decimal('4.99'), shipping_method.charge_incl_tax)


class RoyalMailInternationalStandardEuropeWorldZone1Test(TestCase):

    def test_charge_excl_tax_gives_correct_price(self):
        shipping_method = RoyalMailInternationalStandardWorldZone1()
        self.assertEqual(Decimal('6.99'), shipping_method.charge_excl_tax)

    def test_charge_incl_tax_gives_correct_price(self):
        shipping_method = RoyalMailInternationalStandardWorldZone1()
        self.assertEqual(Decimal('6.99'), shipping_method.charge_incl_tax)


class RoyalMailInternationalStandardEuropeWorldZone2Test(TestCase):

    def test_charge_excl_tax_gives_correct_price(self):
        shipping_method = RoyalMailInternationalStandardWorldZone2()
        self.assertEqual(Decimal('7.99'), shipping_method.charge_excl_tax)

    def test_charge_incl_tax_gives_correct_price(self):
        shipping_method = RoyalMailInternationalStandardWorldZone2()
        self.assertEqual(Decimal('7.99'), shipping_method.charge_incl_tax)