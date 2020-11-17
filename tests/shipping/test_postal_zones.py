from collections import Counter

from django.test import TestCase

from custom_apps.shipping.postal_zones import ZONES


class PostalZonesTest(TestCase):

    def test_countries_are_not_duplicated(self):
        country_counter = Counter(country for countries in ZONES.values() for country in countries)

        for country, count in country_counter.items():
            self.assertEqual(count, 1, "Country %s appears in postal zones %s times" % (country, count))
