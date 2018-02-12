import datetime

from django.core.management.base import BaseCommand

from localflavor.us.us_states import STATES_NORMALIZED

from crime.spiders import MassShootingSpider
from crime.models import GVAIncident
from taxonomy.models import Tag


# @todo create a report each time this is run?

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


class Command(BaseCommand):

    def __init__(self, *args, **kwargs):
        self.incidents = {}
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **kwargs):
        # if no DB records, get all
        # else get delta since last record
        self._create("mass_shootings")

    # PRIVATE

    def _create(self, name, **kwargs):
        records = getattr(self, "_create_" + name)(**kwargs)
        print("created {0} {1}".format(len(records), name))
        return records

    def _create_incident(self, attrs, tag):
        incident = GVAIncident.objects.create(**attrs)
        incident.tags.add(tag)
        return incident

    def _create_mass_shootings(self):
        tag = Tag.objects.get_or_create(name="mass_shooting")[0]
        incidents = []

        for year in range(2014, 2019):
            rows = self._get_mass_shootings(year)
            incidents += [self._create_incident(self._row_to_attrs(row), tag) for row in rows]

        return incidents

    def _get_mass_shootings(self, year):
        ms = MassShootingSpider(year=year)
        ms.crawl()
        return ms.row_data

    def _row_to_attrs(self, row):
        return {
            "city_county": row[2],
            "date": datetime.datetime.strptime(row[0], "%B %d, %Y").date(),
            "gva_id": int(row[6]),
            "injured": int(row[5]),
            "killed": int(row[4]),
            "state": STATES_NORMALIZED[row[1].lower()],
            "street": row[3]
        }
