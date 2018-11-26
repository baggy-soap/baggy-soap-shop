from oscar.apps.order import processing
from oscar.apps.order.models import ShippingEventType


class EventHandler(processing.EventHandler):

    def handle_shipping_event(self, order, event_type, lines, line_quantities, **kwargs):
        """
        Handle a shipping event for a given order.

        This is most common entry point to this class - most of your order
        processing should be modelled around shipping events.  Shipping events
        can be used to trigger payment and communication events.

        You will generally want to override this method to implement the
        specifics of you order processing pipeline.
        """
        self.validate_shipping_event(order, event_type, lines, line_quantities, **kwargs)

        if event_type.code == 'dispatched':
            self.consume_stock_allocations(order, lines, line_quantities)
        elif event_type.code == 'cancelled':
            self.cancel_stock_allocations(order, lines, line_quantities)

        return self.create_shipping_event(order, event_type, lines, line_quantities, **kwargs)

    def handle_order_status_change(self, order, new_status, note_msg=None):
        """
        Handle a requested order status change

        This method is not normally called directly by client code.  The main
        use-case is when an order is cancelled, which in some ways could be
        viewed as a shipping event affecting all lines.
        """
        order.set_status(new_status)

        if new_status in ['Dispatched', 'Cancelled']:
            event_type = ShippingEventType.objects.get(code=new_status.lower())
            lines = order.lines.all()
            line_quantities = [line.quantity for line in lines]
            self.handle_shipping_event(order, event_type=event_type, lines=lines, line_quantities=line_quantities)
        if note_msg:
            self.create_note(order, note_msg)
