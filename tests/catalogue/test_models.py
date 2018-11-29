from django.test import TestCase
from oscar.apps.partner.models import StockRecord, Partner

from catalogue.models import Product, ProductCategory, Category, ProductClass


class ProductTest(TestCase):

    def setUp(self):
        self.product_class = ProductClass.objects.create(name='Toiletries')
        self.product = Product.objects.create(product_class=self.product_class)

    def test_is_soap_product_returns_true_for_baggy_soap(self):
        baggy_soap_category = Category.objects.create(name='Soap with Bag', depth=0)
        ProductCategory.objects.create(product=self.product, category=baggy_soap_category)
        self.assertTrue(self.product.is_soap_product)

    def test_is_soap_product_returns_true_for_soap_refills(self):
        soap_refills_category = Category.objects.create(name='Soap Refills', depth=0)
        ProductCategory.objects.create(product=self.product, category=soap_refills_category)
        self.assertTrue(self.product.is_soap_product)

    def test_is_soap_product_returns_true_for_baggy_shampoo(self):
        baggy_shampoo_category = Category.objects.create(name='Shampoo with Bag', depth=0)
        ProductCategory.objects.create(product=self.product, category=baggy_shampoo_category)
        self.assertTrue(self.product.is_soap_product)

    def test_is_soap_product_returns_true_for_shampoo_refills(self):
        shampoo_refills_category = Category.objects.create(name='Shampoo Refills', depth=0)
        ProductCategory.objects.create(product=self.product, category=shampoo_refills_category)
        self.assertTrue(self.product.is_soap_product)

    def test_is_soap_product_returns_false_for_hooks(self):
        hooks_category = Category.objects.create(name='Hooks', depth=0)
        ProductCategory.objects.create(product=self.product, category=hooks_category)
        self.assertFalse(self.product.is_soap_product)

    def test_total_stock_count_for_single_record(self):
        partner = Partner.objects.create()
        StockRecord.objects.create(product=self.product, partner=partner, num_in_stock=2)
        self.assertEqual(2, self.product.total_stock_count)

    def test_total_stock_count_for_multiple_records(self):
        partner_1 = Partner.objects.create()
        partner_2 = Partner.objects.create()
        StockRecord.objects.create(product=self.product, partner=partner_1, num_in_stock=2)
        StockRecord.objects.create(product=self.product, partner=partner_2, num_in_stock=5)
        self.assertEqual(7, self.product.total_stock_count)
