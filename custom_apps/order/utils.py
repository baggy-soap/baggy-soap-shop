from decimal import Decimal as D

from django.conf import settings
from django.contrib.sites.models import Site
from django.db import transaction
from django.utils.translation import gettext_lazy as _

import oscar.apps.order.utils as utils
from oscar.apps.order.signals import order_placed


class OrderCreator(utils.OrderCreator):
    """
        Places the order by writing out the various models
        """

    def place_order(self, basket, total,  # noqa (too complex (12)) pylint: disable=R0913, R0914
                    shipping_method, shipping_charge, user=None,
                    shipping_address=None, billing_address=None,
                    order_number=None, status=None, request=None, **kwargs):
        """
        Placing an order involves creating all the relevant models based on the
        basket and session data.
        """
        if basket.is_empty:
            raise ValueError(_("Empty baskets cannot be submitted"))
        if not order_number:
            generator = utils.OrderNumberGenerator()
            order_number = generator.order_number(basket)
        if not status and hasattr(settings, 'OSCAR_INITIAL_ORDER_STATUS'):
            status = getattr(settings, 'OSCAR_INITIAL_ORDER_STATUS')

        if utils.Order._default_manager.filter(number=order_number).exists():   # pylint: disable=W0212
            raise ValueError(_("There is already an order with number %s")
                             % order_number)

        with transaction.atomic():
            # Ok - everything seems to be in order, let's place the order
            order = self.create_order_model(
                user, basket, shipping_address, shipping_method, shipping_charge,
                billing_address, total, order_number, status, request, **kwargs)
            for line in basket.all_lines():
                self.create_line_models(order, line)
                self.update_stock_records(line)

            # Record any discounts associated with this order
            for application in basket.offer_applications:
                # Trigger any deferred benefits from offers and capture the
                # resulting message
                application['message'] \
                    = application['offer'].apply_deferred_benefit(basket, order,
                                                                  application)
                # Record offer application results
                if application['result'].affects_shipping:
                    # Skip zero shipping discounts
                    shipping_discount = shipping_method.discount(basket)
                    if shipping_discount <= D('0.00'):
                        continue
                    # If a shipping offer, we need to grab the actual discount off
                    # the shipping method instance, which should be wrapped in an
                    # OfferDiscount instance.
                    application['discount'] = shipping_discount
                self.create_discount_model(order, application)
                self.record_discount(application)

            for voucher in basket.vouchers.all():
                self.record_voucher_usage(order, voucher, user)

        # Send signal for analytics to pick up
        order_placed.send(sender=self, order=order, user=user)

        return order

    def create_order_model(self, user, basket, shipping_address,    # pylint: disable=R0913
                           shipping_method, shipping_charge, billing_address,
                           total, order_number, status, request=None, **extra_order_fields):
        """Create an order model."""
        order_data = {'basket': basket,
                      'number': order_number,
                      'currency': total.currency,
                      'total_incl_tax': total.incl_tax,
                      'total_excl_tax': total.excl_tax,
                      'shipping_incl_tax': shipping_charge.incl_tax,
                      'shipping_excl_tax': shipping_charge.excl_tax,
                      'shipping_method': shipping_method.name,
                      'shipping_code': shipping_method.code,
                      'package_count': shipping_method.package_count}
        if shipping_address:
            order_data['shipping_address'] = shipping_address
        if billing_address:
            order_data['billing_address'] = billing_address
        if user and user.is_authenticated:
            order_data['user_id'] = user.id
        if status:
            order_data['status'] = status
        if extra_order_fields:
            order_data.update(extra_order_fields)
        if 'site' not in order_data:
            order_data['site'] = Site._default_manager.get_current(request)     # pylint: disable=W0212, E1101
        order = utils.Order(**order_data)
        order.save()
        return order

    def create_line_models(self, order, basket_line, extra_line_fields=None):
        """
        Create the batch line model.

        You can set extra fields by passing a dictionary as the
        extra_line_fields value
        """
        product = basket_line.product
        stockrecord = basket_line.stockrecord
        if not stockrecord:
            raise utils.exceptions.UnableToPlaceOrder(
                "Basket line #%d has no stockrecord" % basket_line.id)
        partner = stockrecord.partner
        line_data = {
            'order': order,
            # Partner details
            'partner': partner,
            'partner_name': partner.name,
            'partner_sku': stockrecord.partner_sku,
            'stockrecord': stockrecord,
            # Product details
            'product': product,
            'title': product.full_title,
            'upc': product.upc,
            'quantity': basket_line.quantity,
            # Price details
            'line_price_excl_tax':
            basket_line.line_price_excl_tax_incl_discounts,
            'line_price_incl_tax':
            basket_line.line_price_incl_tax_incl_discounts,
            'line_price_before_discounts_excl_tax':
            basket_line.line_price_excl_tax,
            'line_price_before_discounts_incl_tax':
            basket_line.line_price_incl_tax,
            # Reporting details
            'unit_cost_price': stockrecord.cost_price,
            'unit_price_incl_tax': basket_line.unit_price_incl_tax,
            'unit_price_excl_tax': basket_line.unit_price_excl_tax,
            'unit_retail_price': stockrecord.price_retail,
            # Shipping details
            'est_dispatch_date':
            basket_line.purchase_info.availability.dispatch_date
        }
        extra_line_fields = extra_line_fields or {}
        if hasattr(utils.settings, 'OSCAR_INITIAL_LINE_STATUS'):
            if not (extra_line_fields and 'status' in extra_line_fields):
                extra_line_fields['status'] = getattr(
                    utils.settings, 'OSCAR_INITIAL_LINE_STATUS')
        if extra_line_fields:
            line_data.update(extra_line_fields)

        order_line = utils.Line._default_manager.create(**line_data)    # pylint: disable=W0212
        self.create_line_price_models(order, order_line, basket_line)
        self.create_line_attributes(order, order_line, basket_line)
        self.create_additional_line_models(order, order_line, basket_line)

        return order_line
