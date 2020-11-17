from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase
from mock import Mock
from oscar.apps.address.models import Country
from oscar.apps.basket.models import Line, Basket
from oscar.apps.catalogue.models import ProductAttribute
from oscar.apps.partner.models import StockRecord, Partner

from custom_apps.shipping.models import WeightBased, WeightBand
from custom_apps.shipping.repository import Repository
from custom_apps.catalogue.models import Product, ProductClass, ProductAttributeValue


class RepositoryTest(TestCase):

    def setUp(self):
        self.repository = Repository()
        self.uk = Country.objects.create(name="UK", iso_3166_1_a2="GB")
        self.pt = Country.objects.create(name="Portugal", iso_3166_1_a2="PT")
        self.product_class = ProductClass.objects.create(name='Toiletries', requires_shipping=True)
        self.product = Product.objects.create(product_class=self.product_class, title="Baggy Soap")
        partner = Partner.objects.create(code="foo")
        self.stockrecord = StockRecord.objects.create(product=self.product, partner=partner, num_in_stock=20)
        self.basket = Basket.objects.create()
        self.line = Line.objects.create(basket=self.basket, product=self.product, quantity=1, stockrecord=self.stockrecord)

    # This behaviour has been implemented because, otherwise, a guest user trying to view their basket would
    # see an error relating to no shipping methods being found. Ideally, we would ascertain the default shipping
    # method based on a guest user's location, but I don't really know how to get this information reliably.
    def test_get_available_shipping_methods_defaults_to_uk_if_no_shipping_address(self):
        first_class_uk = WeightBased.objects.create(name="1st Class UK")
        first_class_uk.countries.set([self.uk])
        first_class_pt = WeightBased.objects.create(name="1st Class PT")
        first_class_pt.countries.set([self.pt])
        WeightBand.objects.create(method=first_class_uk, upper_limit=0.75, charge=2.99)
        WeightBand.objects.create(method=first_class_pt, upper_limit=0.75, charge=3.99)
        shipping_methods = self.repository.get_available_shipping_methods(self.basket)
        self.assertListEqual([first_class_uk], shipping_methods)

    def test_get_available_shipping_methods_returns_all_for_given_shipping_country(self):
        first_class_uk = WeightBased.objects.create(name="1st Class UK")
        first_class_uk.countries.set([self.uk])
        second_class_uk = WeightBased.objects.create(name="2nd Class UK")
        second_class_uk.countries.set([self.uk])
        first_class_pt = WeightBased.objects.create(name="1st Class PT")
        first_class_pt.countries.set([self.pt])
        WeightBand.objects.create(method=first_class_uk, upper_limit=0.75, charge=2.99)
        WeightBand.objects.create(method=second_class_uk, upper_limit=0.75, charge=2.49)
        WeightBand.objects.create(method=first_class_pt, upper_limit=0.75, charge=3.99)
        address = Mock(country=self.uk)
        shipping_methods = self.repository.get_available_shipping_methods(self.basket, shipping_addr=address)
        # This is equivalent to assertItemsEqual in Python 2
        self.assertCountEqual([first_class_uk, second_class_uk], shipping_methods)

    def test_get_available_shipping_methods_returns_empty_list_if_no_method_for_shipping_address(self):
        first_class_uk = WeightBased.objects.create(name="1st Class UK")
        first_class_uk.countries.set([self.uk])
        address = Mock(country=self.pt)
        shipping_methods = self.repository.get_available_shipping_methods(self.basket, shipping_addr=address)
        self.assertListEqual([], shipping_methods)

    def test_get_available_shipping_methods_returns_only_chargeable_methods(self):
        first_class_uk = WeightBased.objects.create(name="1st Class UK")
        first_class_uk.countries.set([self.uk])
        small_parcel_uk = WeightBased.objects.create(name="Small Parcel UK")
        small_parcel_uk.countries.set([self.uk])
        WeightBand.objects.create(method=first_class_uk, upper_limit=0.75, charge=2.99)
        WeightBand.objects.create(method=small_parcel_uk, upper_limit=2.00, charge=4.99)
        address = Mock(country=self.uk)
        weight_attribute = ProductAttribute.objects.create(product_class=self.product_class, code="weight")
        ProductAttributeValue.objects.create(attribute=weight_attribute, product=self.product, value=0.1)
        self.line.quantity = 10
        self.line.save()
        shipping_methods = self.repository.get_available_shipping_methods(self.basket, shipping_addr=address)
        self.assertListEqual([small_parcel_uk], shipping_methods)

    def test_get_available_shipping_methods_returns_sorted_methods(self):
        first_class = WeightBased.objects.create(name="1st Class")
        first_class.countries.set([self.uk])
        second_class = WeightBased.objects.create(name="2nd Class")
        second_class.countries.set([self.uk])
        small_parcel = WeightBased.objects.create(name="Small Parcel")
        small_parcel.countries.set([self.uk])
        WeightBand.objects.create(method=first_class, upper_limit=0.75, charge=2.99)
        WeightBand.objects.create(method=second_class, upper_limit=0.75, charge=2.49)
        WeightBand.objects.create(method=small_parcel, upper_limit=2.00, charge=3.99)
        address = Mock(country=self.uk)
        shipping_methods = self.repository.get_available_shipping_methods(self.basket, shipping_addr=address)
        self.assertListEqual([second_class, first_class, small_parcel], shipping_methods)

    def test_get_default_shipping_method_does_not_error_when_no_shipping_address_provided(self):
        first_class_uk = WeightBased.objects.create(name="1st Class UK")
        first_class_uk.countries.set([self.uk])
        first_class_pt = WeightBased.objects.create(name="1st Class PT")
        first_class_pt.countries.set([self.pt])
        WeightBand.objects.create(method=first_class_uk, upper_limit=0.75, charge=2.99)
        WeightBand.objects.create(method=first_class_pt, upper_limit=0.75, charge=3.99)
        self.assertIsNotNone(self.repository.get_default_shipping_method(self.basket))

    def test_get_default_shipping_method_returns_cheapest_uk_method_when_no_shipping_address_provided(self):
        first_class_uk = WeightBased.objects.create(name="1st Class UK")
        first_class_uk.countries.set([self.uk])
        second_class_uk = WeightBased.objects.create(name="2nd Class UK")
        second_class_uk.countries.set([self.uk])
        first_class_pt = WeightBased.objects.create(name="1st Class PT")
        first_class_pt.countries.set([self.pt])
        WeightBand.objects.create(method=first_class_uk, upper_limit=0.75, charge=2.99)
        WeightBand.objects.create(method=second_class_uk, upper_limit=0.75, charge=2.49)
        WeightBand.objects.create(method=first_class_pt, upper_limit=0.75, charge=3.99)
        self.assertEqual(second_class_uk, self.repository.get_default_shipping_method(self.basket))

    def test_get_default_shipping_method_raises_error_when_no_shipping_methods_defined(self):
        address = Mock(country=self.uk)
        with self.assertRaises(ImproperlyConfigured):
            self.repository.get_default_shipping_method(self.basket, shipping_addr=address)
