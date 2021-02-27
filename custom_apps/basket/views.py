from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from oscar.apps.basket import views
from oscar.apps.basket.signals import voucher_removal


class BasketView(views.BasketView):     # pylint: disable=R0901
    remove_signal = voucher_removal

    def get_basket_voucher_form(self):
        self._remove_stale_vouchers()
        return views.BasketVoucherForm()

    def _remove_stale_vouchers(self):
        for voucher in self.request.basket.vouchers.all():
            available_to_user = voucher.is_available_to_user(user=self.request.user)[0]
            if not voucher.is_active() or not available_to_user:
                self.request.basket.vouchers.remove(voucher)
                self.remove_signal.send(sender=self, basket=self.request.basket, voucher=voucher)
                messages.warning(self.request, _("Stale voucher '%s' removed from basket") % voucher.code)
