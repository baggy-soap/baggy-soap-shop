from django.test import TestCase

from custom_apps.shipping.models import WeightBased, WeightBand


class WeightBasedTest(TestCase):

    def setUp(self):
        self.weight_based = WeightBased.objects.create(name='1st Class')
        self.low_band = WeightBand.objects.create(method=self.weight_based, upper_limit=0.25, charge=1.00)
        self.medium_band = WeightBand.objects.create(method=self.weight_based, upper_limit=0.50, charge=1.50)
        self.top_band = WeightBand.objects.create(method=self.weight_based, upper_limit=0.75, charge=2.00)

    def test_get_charge_returns_correct_band(self):
        self.assertEqual(self.weight_based.get_charge(0.1), 1.00)
        self.assertEqual(self.weight_based.get_charge(0.25), 1.00)
        self.assertEqual(self.weight_based.get_charge(0.251), 1.50)
        self.assertEqual(self.weight_based.get_charge(0.5), 1.50)
        self.assertEqual(self.weight_based.get_charge(0.51), 2.00)
        self.assertEqual(self.weight_based.get_charge(0.75), 2.00)

    def test_get_charge_returns_double_charge_if_send_multiples_is_true(self):
        self.weight_based.send_multiples = True
        self.assertEqual(self.weight_based.get_charge(0.8), 3.00)

    def test_get_charge_does_not_return_double_charge_if_send_multiples_is_false(self):
        self.weight_based.send_multiples = False
        self.assertEqual(self.weight_based.get_charge(0.8), 0.00)

    def test_package_count_returns_correct_value(self):
        self.weight_based.send_multiples = True
        self.weight_based.get_charge(0.1)
        self.assertEqual(self.weight_based.package_count, 1)
        self.weight_based.get_charge(0.8)
        self.assertEqual(self.weight_based.package_count, 2)
        self.weight_based.get_charge(1.55)
        self.assertEqual(self.weight_based.package_count, 3)
