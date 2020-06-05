from decimal import Decimal

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
        self.mock_basket = Mock()
        self.uk = Country.objects.create(name="UK", iso_3166_1_a2="GB")
        self.pt = Country.objects.create(name="Portugal", iso_3166_1_a2="PT")
        self.product_class = ProductClass.objects.create(name='Toiletries')
        self.product = Product.objects.create(product_class=self.product_class, title="Baggy Soap")

    def test_get_available_shipping_methods_returns_empty_list_if_no_shipping_address(self):
        shipping_methods = self.repository.get_available_shipping_methods(self.mock_basket)
        self.assertEqual([], shipping_methods)

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
        basket = Basket.objects.create()
        Line(basket=basket, product=self.product, quantity=1)
        shipping_methods = self.repository.get_available_shipping_methods(basket, shipping_addr=address)
        self.assertEqual([first_class_uk, second_class_uk], shipping_methods)

    def test_get_available_shipping_methods_returns_empty_list_if_no_method_for_shipping_address(self):
        first_class_uk = WeightBased.objects.create(name="1st Class UK")
        first_class_uk.countries.set([self.uk])
        address = Mock(country=self.pt)
        basket = Basket.objects.create()
        Line(basket=basket, product=self.product, quantity=1)
        shipping_methods = self.repository.get_available_shipping_methods(basket, shipping_addr=address)
        self.assertEqual([], shipping_methods)

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
        partner = Partner.objects.create(code="foo")
        stockrecord = StockRecord.objects.create(product=self.product, partner=partner, num_in_stock=20)
        basket = Basket.objects.create()
        Line.objects.create(basket=basket, product=self.product, quantity=10, stockrecord=stockrecord)
        shipping_methods = self.repository.get_available_shipping_methods(basket, shipping_addr=address)
        self.assertEqual([small_parcel_uk], shipping_methods)
