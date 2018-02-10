import datetime

import factory
from factory import Faker, fuzzy
from localflavor.us.us_states import US_STATES


class GVAIncidentFactory(factory.DjangoModelFactory):

    city_county = Faker("pystr", max_chars=128)
    date = fuzzy.FuzzyDate(datetime.date.today() - datetime.timedelta(days=7))
    gva_id = fuzzy.FuzzyInteger(1000)
    injured = fuzzy.FuzzyInteger(10)
    killed = fuzzy.FuzzyInteger(10)
    state = fuzzy.FuzzyChoice([s[0] for s in US_STATES])
    street = Faker("pystr", max_chars=128)

    class Meta:
        model = "crime.GVAIncident"

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for tag in extracted:
                self.tags.add(tag)
