from django.db import models
from django.utils.translation import gettext_lazy as _

from oscar.apps.order.abstract_models import AbstractOrder


class Order(AbstractOrder):

    package_count = models.PositiveSmallIntegerField(_("Package count"), default=1)


from oscar.apps.order.models import *  # noqa isort:skip pylint: disable=W0614, W0401
