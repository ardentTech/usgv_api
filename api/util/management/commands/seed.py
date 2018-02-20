from django.conf import settings
from django.core.management.base import BaseCommand

from geo.factories import UsStateFactory
from geo.fixtures import US_STATES


# @todo not a fan of how to these modes work


DEV_MODE = "dev"
PRO_MODE = "pro"


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        self.mode = DEV_MODE if settings.DEBUG else PRO_MODE
        self._create("us_states")

    # PRIVATE

    def _create(self, name, **kwargs):
        records = getattr(self, "_create_" + name)(**kwargs)
        print("created {0} {1}".format(len(records), name))
        return records

    def _create_us_states(self):
        return [UsStateFactory.create(
            fips_code=s[0], name=s[1], postal_code=s[2]) for s in US_STATES]

    def _dev_mode(self):
        return self.mode == DEV_MODE

    def _pro_mode(self):
        return self.mode == PRO_MODE
