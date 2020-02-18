from django.test import TestCase
from oscar.apps.partner.models import StockRecord, Partner

from custom_apps.catalogue.models import Product, Category, ProductClass, ProductCategory


class ProductTest(TestCase):

    def setUp(self):
        self.product_class = ProductClass.objects.create(name='Toiletries')
        self.product = Product.objects.create(product_class=self.product_class)

    def test_is_soap_product_returns_true_for_soap_product(self):
        baggy_soap_category = Category.objects.create(name='Soap', depth=0)
        ProductCategory.objects.create(product=self.product, category=baggy_soap_category)
        self.assertTrue(self.product.is_soap_product)

    def test_is_soap_product_returns_true_for_soap_product_variant(self):
        soap_refills_category = Category.objects.create(name='Soap', depth=0)
        ProductCategory.objects.create(product=self.product, category=soap_refills_category)
        child = Product.objects.create(parent=self.product, structure=Product.CHILD)
        self.assertTrue(child.is_soap_product)

    def test_is_soap_product_returns_true_for_shampoo_product(self):
        baggy_shampoo_category = Category.objects.create(name='Shampoo', depth=0)
        ProductCategory.objects.create(product=self.product, category=baggy_shampoo_category)
        self.assertTrue(self.product.is_soap_product)

    def test_is_soap_product_returns_true_for_shampoo_product_variant(self):
        shampoo_refills_category = Category.objects.create(name='Shampoo', depth=0)
        ProductCategory.objects.create(product=self.product, category=shampoo_refills_category)
        child = Product.objects.create(parent=self.product, structure=Product.CHILD)
        self.assertTrue(child.is_soap_product)

    def test_is_soap_product_returns_false_for_hooks(self):
        hooks_category = Category.objects.create(name='Hooks', depth=0)
        ProductCategory.objects.create(product=self.product, category=hooks_category)
        self.assertFalse(self.product.is_soap_product)

    def test_has_stockrecords_available_for_product(self):
        partner = Partner.objects.create()
        StockRecord.objects.create(product=self.product, partner=partner, num_in_stock=2)
        self.assertTrue(self.product.has_stockrecords_available)

    def test_has_stockrecords_available_for_child_product(self):
        child = Product.objects.create(parent=self.product, structure=Product.CHILD)
        partner = Partner.objects.create()
        StockRecord.objects.create(product=child, partner=partner, num_in_stock=2)
        self.assertTrue(child.has_stockrecords_available)

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

    def test_total_stock_count_for_parent_and_child_products(self):
        self.product.structure = Product.PARENT
        child_1 = Product.objects.create(parent=self.product, structure=Product.CHILD)
        child_2 = Product.objects.create(parent=self.product, structure=Product.CHILD)
        partner_1 = Partner.objects.create()
        partner_2 = Partner.objects.create()
        StockRecord.objects.create(product=child_1, partner=partner_1, num_in_stock=2)
        StockRecord.objects.create(product=child_2, partner=partner_2, num_in_stock=5)
        self.assertEqual(2, child_1.total_stock_count)
        self.assertEqual(5, child_2.total_stock_count)
        self.assertEqual(7, self.product.total_stock_count)

    def test_total_allocated_for_single_record(self):
        partner = Partner.objects.create()
        StockRecord.objects.create(product=self.product, partner=partner, num_in_stock=2, num_allocated=1)
        self.assertEqual(1, self.product.total_allocated)

    def test_total_allocated_for_multiple_records(self):
        partner_1 = Partner.objects.create()
        partner_2 = Partner.objects.create()
        StockRecord.objects.create(product=self.product, partner=partner_1, num_in_stock=2, num_allocated=1)
        StockRecord.objects.create(product=self.product, partner=partner_2, num_in_stock=5, num_allocated=1)
        self.assertEqual(2, self.product.total_allocated)

    def test_total_allocated_for_when_num_allocated_is_none(self):
        partner = Partner.objects.create()
        StockRecord.objects.create(product=self.product, partner=partner, num_in_stock=2)
        self.assertEqual(0, self.product.total_allocated)

    def test_total_allocated_for_parent_and_child_products(self):
        self.product.structure = Product.PARENT
        child_1 = Product.objects.create(parent=self.product, structure=Product.CHILD)
        child_2 = Product.objects.create(parent=self.product, structure=Product.CHILD)
        partner_1 = Partner.objects.create()
        partner_2 = Partner.objects.create()
        StockRecord.objects.create(product=child_1, partner=partner_1, num_in_stock=2, num_allocated=1)
        StockRecord.objects.create(product=child_2, partner=partner_2, num_in_stock=5, num_allocated=1)
        self.assertEqual(1, child_1.total_allocated)
        self.assertEqual(1, child_2.total_allocated)
        self.assertEqual(2, self.product.total_allocated)

    def test_get_description_returns_description(self):
        product = Product.objects.create(product_class=self.product_class, structure=Product.PARENT, description="Foo")
        self.assertEqual(product.get_description(), product.description)

    def test_get_description_for_child_gets_parents_description(self):
        parent = Product.objects.create(product_class=self.product_class, structure=Product.PARENT, description="Foo")
        child = Product.objects.create(parent=parent, structure=Product.CHILD)
        self.assertEqual(child.get_description(), parent.description)

    def test_full_title_returns_product_title(self):
        product = Product.objects.create(product_class=self.product_class, title="Lavender")
        self.assertEqual(product.full_title, product.title)

    def test_full_title_returns_parent_and_product_title_for_child(self):
        parent = Product.objects.create(product_class=self.product_class, title="Lavender")
        child = Product.objects.create(parent=parent, structure=Product.CHILD, title="Ocean Blue")
        self.assertEqual(child.full_title, "Lavender (Ocean Blue)")

    def test_full_title_returns_parent_title_if_no_title(self):
        parent = Product.objects.create(product_class=self.product_class, title="Lavender")
        child = Product.objects.create(parent=parent, structure=Product.CHILD)
        self.assertEqual(child.full_title, "Lavender")

    def test_get_rating_for_product(self):
        self.product.rating = 5
        self.assertEqual(5, self.product.get_rating())

    def test_get_rating_for_child_product(self):
        self.product.rating = 5
        child = Product.objects.create(parent=self.product, structure=Product.CHILD)
        self.assertEqual(5, child.get_rating())

    def test_get_reviews_for_product(self):
        self.product.reviews.set = ["great product"]
        self.assertEqual(self.product.reviews, self.product.get_reviews())

    def test_get_reviews_for_child_product(self):
        self.product.reviews.set = ["great product"]
        child = Product.objects.create(parent=self.product, structure=Product.CHILD)
        self.assertEqual(self.product.reviews, child.get_reviews())

    def test_get_num_approved_reviews_for_product(self):
        self.product.num_approved_reviews = 5
        self.assertEqual(5, self.product.get_num_approved_reviews())

    def test_get_num_approved_reviews_for_child_product(self):
        self.product.num_approved_reviews = 5
        child = Product.objects.create(parent=self.product, structure=Product.CHILD)
        self.assertEqual(5, child.get_num_approved_reviews())
