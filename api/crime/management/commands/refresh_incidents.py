import datetime

from django.core.management.base import BaseCommand

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

    # @todo handle update-only
    def _create_mass_shootings(self):
        incidents = []
        stop_year = datetime.date.today().year + 1
        tag = Tag.objects.get_or_create(name="mass_shooting")[0]

        try:
            start_year = GVAIncident.objects.all().order_by("-date")[0].date.year
            years = range(start_year, stop_year)
        except IndexError as e:
            years = range(2014, stop_year)

        for year in years:
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
