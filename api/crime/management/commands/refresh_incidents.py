from django.core.management.base import BaseCommand


# @todo
# use `bulk_create` to reduce DB bottle-necking
# how to reconcile incidents appearing in multiple groups? can this be done with `bulk_create`?

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

    def handle(self, *args, **kwargs):
        # if no DB records, get all
        # else get delta since last record
        pass

    # PRIVATE

    # @todo abstract this away
    def _create(self, name, **kwargs):
        records = getattr(self, "_create_" + name)(**kwargs)
        print("created {0} {1}".format(len(records), name))
        return records

    def _get_incidents_since(self, timestamp=None):
        # determine which crawler to use for which... GVAIncidentCategory?
        # what about years?
        pass

    def _get_incidents(self):
        pass
