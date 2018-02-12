import datetime

from django.core.management.base import BaseCommand

from localflavor.us.us_states import STATES_NORMALIZED

from crime.spiders import MassShootingSpider
from crime.models import GVAIncident


# @todo
# use `bulk_create` to reduce DB bottle-necking
# how to reconcile incidents appearing in multiple groups? can this be done with `bulk_create`?
# create a report each time this is run?

# REPORTS
# children killed
# children injured
# teens killed
# teens injured
# accidental deaths
# accidental injuries
# accidental deaths (children ages 0-11)
# accidental injuries (children ages 0-11)
# accidental deaths (teens ages 12-17)
# accidental injuries (teens ages 12-17)
# officer involved shootings
# mass shootings in 2014
# mass shootings in 2015
# mass shootings in 2016
# mass shootings in 2017
# mass shootings in 2018


class Command(BaseCommand):

    def __init__(self, *args, **kwargs):
        self.incidents = {}
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **kwargs):
        # if no DB records, get all
        # else get delta since last record
        (column_names, row_data) = self._get_mass_shootings()
        GVAIncident.objects.bulk_create([self._row_to_object(row) for row in row_data])

    # PRIVATE

    def _get_mass_shootings(self):
        ms = MassShootingSpider(year=2018)
        ms.crawl()
        return (ms.column_names, ms.row_data)

    def _row_to_object(self, raw):
        return GVAIncident(
            city_county=raw[2],
            date=datetime.datetime.strptime(raw[0], "%B %d, %Y").date(),
            gva_id=int(raw[6]),
            injured=int(raw[5]),
            killed=int(raw[4]),
            state=STATES_NORMALIZED[raw[1].lower()],
            street=raw[3])
