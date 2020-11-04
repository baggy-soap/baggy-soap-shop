from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from oscar.apps.address.models import Country

from custom_apps.shipping.admin import WeightBased
from custom_apps.shipping.postal_zones import ZONES


class Command(BaseCommand):
    help = 'Populates countries for all shipping methods, using postal zones defined in Shipping app'

    def handle(self, *args, **options):
        for method in WeightBased.objects.all():
            print('*' * 50)
            print('Checking shipping method ', method)
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
                    print(list(Country.objects.all()))
                    raise
            print('Updated countries: ', list(method.countries.all()))

        self.stdout.write(self.style.SUCCESS('Successfully updated shipping methods'))