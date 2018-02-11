from django.core.management.base import BaseCommand

from crime.spiders import MassShootingSpider


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
        self._get_mass_shootings()

    # PRIVATE

    def _get_mass_shootings(self):
        ms = MassShootingSpider(year=2018)
        ms.crawl()
        print(ms.column_names)
        print(ms.row_data)
