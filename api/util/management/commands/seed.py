from django.conf import settings
from django.core.management.base import BaseCommand

from crime.factories import GVAIncidentCategoryFactory


DEV_MODE = "dev"
PRO_MODE = "pro"


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        self.mode = DEV_MODE if settings.DEBUG else PRO_MODE
        self._create("gva_incident_categories")

    # PRIVATE

    def _create(self, name, **kwargs):
        records = getattr(self, "_create_" + name)(**kwargs)
        print("created {0} {1}".format(len(records), name))
        return records

    def _create_gva_incident_categories(self):
        categories = ["mass_shooting", "officer_involved_shootings"]
        return [GVAIncidentCategoryFactory.create(name=c) for c in categories]

    def _dev_mode(self):
        return self.mode == DEV_MODE

    def _pro_mode(self):
        return self.mode == PRO_MODE
