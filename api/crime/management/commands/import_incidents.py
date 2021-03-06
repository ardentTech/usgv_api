import datetime

from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from crime.spiders import MassShootingSpider
from crime.models import GVAIncident
from geo.models import UsState
from taxonomy.models import Tag


class Command(BaseCommand):

    def __init__(self, *args, **kwargs):
        self.incidents = {}
        self.us_states = {o.name.lower(): o for o in UsState.objects.all()}
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **kwargs):
        self._import("mass_shootings")

    # PRIVATE

    def _import(self, name, **kwargs):
        records = getattr(self, "_import_" + name)(**kwargs)
        print("created {0} {1}".format(len(records), name))
        return records

    def _create_incident(self, attrs, tag):
        incident = GVAIncident.objects.create(**attrs)
        incident.tags.add(tag)
        return incident

    def _import_mass_shootings(self):
        incidents = []
        stop_year = datetime.date.today().year + 1
        tag = Tag.objects.get_or_create(name="mass_shooting")[0]

        try:
            start_year = GVAIncident.objects.all().order_by("-date")[0].date.year
            years = range(start_year, stop_year)
        except IndexError as e:
            years = range(2014, stop_year)

        for year in years:
            for row in self._get_mass_shootings(year):
                try:
                    incidents.append(self._create_incident(self._row_to_attrs(row), tag))
                except IntegrityError:
                    pass

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
            "state": self.us_states[row[1].lower()],
            "street": row[3]
        }
