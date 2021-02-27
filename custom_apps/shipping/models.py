from decimal import Decimal as D

from django.db import models
from django.utils.translation import gettext_lazy as _
from oscar.apps.shipping.abstract_models import AbstractWeightBased


class WeightBased(AbstractWeightBased):

    send_multiples = models.BooleanField(_("Send Multiples"), default=False,
                                         help_text="Send as multiple packages if the upper weight limit is exceeded")

    package_count = 1

    def get_charge(self, weight):
        """
        Calculates shipping charges for a given weight.

        If there is one or more matching weight band for a given weight, the
        charge of the closest matching weight band is returned.

        By default, we do not want to send multiples of a given shipping type
        (we'd prefer to send one package in the next band up). However, if the
        weight exceeds the top weight band and we want to send multiples, the
        top weight band charge is added until a matching weight band is found.
        This models the concept of "sending as many of the large boxes as needed".

        Please note that it is assumed that the closest matching weight band
        is the most cost-effective one, and that the top weight band is more
        cost effective than e.g. sending out two smaller parcels.
        Without that assumption, determining the cheapest shipping solution
        becomes an instance of the bin packing problem. The bin packing problem
        is NP-hard and solving it is left as an exercise to the reader.
        """
        weight = D(weight)  # weight really should be stored as a decimal
        if not self.bands.exists():
            return D('0.00')

        top_band = self.top_band
        if weight <= top_band.upper_limit:
            band = self.get_band_for_weight(weight)
            return band.charge

        if not self.send_multiples:
            return D('0.00')

        quotient, remaining_weight = divmod(weight, top_band.upper_limit)
        self.package_count = quotient + int(bool(remaining_weight))
        if remaining_weight:
            remainder_band = self.get_band_for_weight(remaining_weight)
            return quotient * top_band.charge + remainder_band.charge

        return quotient * top_band.charge


from oscar.apps.shipping.models import *  # noqa isort:skip pylint: disable=W0614, W0401, C0413
