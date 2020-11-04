from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from oscar.apps.address.models import Country

from custom_apps.shipping.admin import WeightBased
from custom_apps.shipping.postal_zones import ZONES


class Command(BaseCommand):
    """This management command uses the postal zones defined in postal_zones.py, and adds them to the
    weight based shipping methods defined in the Oscar dashboard. It sets 'is_shipping_country' to True
    for all countries on all weight based shipping methods.

    Note: This command does not remove countries from a shipping method - this must be done manually through
    the dashboard, if necessary (or this command can be updated to do so)."""
    help = 'Populates countries for all shipping methods, using postal zones defined in Shipping app'

    def handle(self, *args, **options):
        shippable_countries = set()
        for method in WeightBased.objects.all():
            print('*' * 50)
            print('Checking shipping method: ', method)
            print('Existing countries: ', list(method.countries.all()))
            zones = ["Europe", "World Zone 1", "World Zone 2", "World Zone 3"]

            for zone in zones:
                if zone in method.name:
                    zone_name = zone
                    break
            else:
                zone_name = "United Kingdom"

            for country in ZONES[zone_name]:
                try:
                    WeightBased.countries.through.objects.update_or_create(
                        weightbased_id=method.id, country_id=Country.objects.get(printable_name=country).code
                    )
                except ObjectDoesNotExist:
                    print("Country '%s' not valid" % country)
                    raise
            print('Updated countries: ', list(method.countries.all()))
            shippable_countries.update(set(method.countries.all()))

        for country in shippable_countries:
            country.is_shipping_country = True
            country.save()
        print('*' * 50)
        print('Non-shippable countries: ', set(Country.objects.filter(is_shipping_country=False)))

        self.stdout.write(self.style.SUCCESS('Successfully updated shipping methods'))