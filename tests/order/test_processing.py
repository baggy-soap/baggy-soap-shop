from django.test import TestCase
from mock import Mock

from custom_apps.order.processing import EventHandler


class EventHandlerTest(TestCase):
    fixtures = ['shipping-event-types']

    def setUp(self):
        self.handler = EventHandler()

    def test_handle_shipping_event_consumes_stock_allocations_if_shipped(self):
        mock_line = Mock(stockrecord=Mock())
        mock_event_type = Mock(code='dispatched')
        self.handler.handle_shipping_event(Mock(), mock_event_type, [mock_line], [4])
        mock_line.stockrecord.consume_allocation.assert_called_once_with(4)
        mock_line.stockrecord.cancel_allocation.assert_not_called()

    def test_handle_shipping_event_cancels_stock_allocations_if_cancelled(self):
        mock_line = Mock(stockrecord=Mock())
        mock_event_type = Mock(code='cancelled')
        self.handler.handle_shipping_event(Mock(), mock_event_type, [mock_line], [2])
        mock_line.stockrecord.cancel_allocation.assert_called_once_with(2)
        mock_line.stockrecord.consume_allocation.assert_not_called()

    def test_handle_order_status_change_consumes_stock_allocations_if_status_dispatched(self):
        mock_order = Mock()
        mock_line = Mock(stockrecord=Mock(), quantity=3)
        mock_order.lines.all.return_value = [mock_line]
        self.handler.handle_order_status_change(mock_order, 'Dispatched')
        mock_line.stockrecord.consume_allocation.assert_called_once_with(3)
        mock_line.stockrecord.cancel_allocation.assert_not_called()

    def test_handle_order_status_change_cancels_stock_allocations_if_status_cancelled(self):
        mock_order = Mock()
        mock_line = Mock(stockrecord=Mock(), quantity=1)
        mock_order.lines.all.return_value = [mock_line]
        self.handler.handle_order_status_change(mock_order, 'Cancelled')
        mock_line.stockrecord.cancel_allocation.assert_called_once_with(1)
        mock_line.stockrecord.consume_allocation.assert_not_called()

    def test_handle_order_status_change_leaves_stock_allocations_as_is_if_status_packaged(self):
        mock_order = Mock()
        mock_line = Mock(stockrecord=Mock(), quantity=1)
        mock_order.lines.all.return_value = [mock_line]
        self.handler.handle_order_status_change(mock_order, 'Packaged')
        mock_line.stockrecord.cancel_allocation.assert_not_called()
        mock_line.stockrecord.consume_allocation.assert_not_called()
